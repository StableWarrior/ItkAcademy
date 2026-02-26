from datetime import date
from uuid import UUID

from fastapi import HTTPException

from ..database.repository.events_aggregator import EventsAggregatorRepository
from ..database.repository.idempotency_repository import IdempotencyRepository
from ..shemas import Registration


class EventsAggregatorService:
    def __init__(
        self,
        repository: EventsAggregatorRepository,
        idempotency: IdempotencyRepository = None,
    ):
        self.repository = repository
        self.idempotency = idempotency

    async def get_page(
        self,
        date_from: date = date(2000, 1, 1),
        page: int = 1,
        page_size: int = 10,
    ):
        page = await self.repository.get_events(
            date_from=date_from, page=page, page_size=page_size
        )
        return page

    async def get_event(self, event_id: UUID):
        event = await self.repository.get_event(event_id=event_id)
        return event

    async def get_ticket(self, ticket_id: UUID):
        ticket = await self.repository.get_ticket(ticket_id=ticket_id)
        return ticket

    async def register_ticket(self, ticket_id: UUID, registration: Registration):
        ticket = await self.repository.register_ticket(
            ticket_id=ticket_id, registration=registration
        )
        return ticket

    async def cansel_ticket(self, ticket_id: UUID):
        ticket = await self.repository.cansel_ticket(ticket_id=ticket_id)
        return ticket

    async def get_ticket_idempotency(
        self, registration: Registration, idempotency_key: str | None
    ):
        ticket = await self.idempotency.get_ticket(idempotency_key=idempotency_key)
        if ticket:
            orm_dict = {
                "event_id": ticket.event_id,
                "first_name": ticket.user.first_name,
                "last_name": ticket.user.last_name,
                "email": ticket.user.email,
                "seat": ticket.seat,
            }
            pydantic_dict = registration.model_dump(exclude={"idempotency_key"})
            if orm_dict == pydantic_dict:
                return ticket.id
            else:
                raise HTTPException(status_code=409, detail="Conflict")

        return ticket

    async def get_outbox_idempotency(self, idempotency_key: str | None):
        outbox = await self.idempotency.get_outbox(idempotency_key=idempotency_key)
        return outbox

    async def save_ticket_idempotency(self, ticket_id: UUID, idempotency_key: str):
        result = await self.idempotency.save_ticket(
            ticket_id=ticket_id, idempotency_key=idempotency_key
        )
        return result

    async def save_outbox_idempotency(self, outbox_id: UUID, idempotency_key: str):
        result = await self.idempotency.save_outbox(
            outbox_id=outbox_id, idempotency_key=idempotency_key
        )
        return result
