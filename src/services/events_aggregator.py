from datetime import date
from uuid import UUID

from ..database.repository.events_aggregator import EventsAggregatorRepository
from ..shemas import Registration


class EventsAggregatorService:
    def __init__(self, repository: EventsAggregatorRepository):
        self.repository = repository

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
