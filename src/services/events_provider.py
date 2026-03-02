from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

import aiohttp
from fastapi import HTTPException

from ..config import EVENTS_API_URL, EVENTS_CAPASHINO_URL, LOGGER, X_API_KEY
from ..shemas import Registration
from .events_aggregator import EventsAggregatorService


class EventsProviderService:
    def __init__(self, service: EventsAggregatorService):
        self.service = service

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "x-api-key": X_API_KEY,
                "Content-Type": "application/json",
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_first_page(self, changed_at: str):
        async with self.session.get(
            f"{EVENTS_API_URL}/api/events/?changed_at={changed_at}"
        ) as response:
            page = await response.json()
        return page

    async def get_page(self, url: str):
        async with self.session.get(url) as response:
            page = await response.json()
        return page

    async def get_seats(self, event_id: UUID):
        event = await self.service.get_event(event_id=event_id)
        if event.status != "published":
            raise HTTPException(status_code=400, detail="Event is not published")

        async with self.session.get(
            f"{EVENTS_API_URL}/api/events/{event_id}/seats/"
        ) as response:
            seats = await response.json()
            seats["event_id"] = event_id

        return seats

    async def register_ticket(self, registration: Registration):
        ticket_id = await self.service.get_ticket_idempotency(
            registration=registration, idempotency_key=registration.idempotency_key
        )
        ticket = {"ticket_id": ticket_id}

        if ticket_id is None:
            seats = await self.get_seats(event_id=registration.event_id)
            event = await self.service.get_event(event_id=registration.event_id)

            LOGGER.info("seats", seats=seats)

            if registration.seat not in seats["seats"]:
                raise HTTPException(status_code=404, detail="Seat is not found")
            if event.registration_deadline <= datetime.now(
                ZoneInfo("Asia/Vladivostok")
            ):
                raise HTTPException(
                    status_code=400, detail="Registration deadline has passed"
                )

            registration_data = registration.model_dump()
            registration_data.pop("event_id")

            async with self.session.post(
                f"{EVENTS_API_URL}/api/events/{registration.event_id}/register/",
                json=registration_data,
            ) as response:
                ticket = await response.json()

            await self.service.register_ticket(
                ticket_id=ticket["ticket_id"], registration=registration
            )

        return ticket

    async def cancel_ticket(self, ticket_id: UUID):
        ticket = await self.service.get_ticket(ticket_id=ticket_id)

        if ticket.event.event_time < datetime.now(ZoneInfo("Asia/Vladivostok")):
            raise HTTPException(status_code=400, detail="Event already started")

        async with self.session.delete(
            f"{EVENTS_API_URL}/api/events/{ticket.event_id}/unregister/",
            json={"ticket_id": str(ticket_id)},
        ) as response:
            status = await response.json()

        await self.service.cansel_ticket(ticket_id=ticket_id)

        return status

    async def send_to_capashino(
        self,
        message: str,
        reference_id: UUID,
        idempotency_key: str = None,
    ):
        data = {"message": message, "reference_id": str(reference_id)}
        if idempotency_key:
            data["idempotency_key"] = idempotency_key

        async with self.session.post(
            f"{EVENTS_CAPASHINO_URL}/api/notifications", json=data
        ) as response:
            LOGGER.info("response", response=response.text)
            LOGGER.info("ticket", outbox=reference_id)
            status = response.status
            result = await response.json()

        return status, result
