from uuid import UUID

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from ..database.repository.events_aggregator import EventsAggregatorRepository
from ..services.events_aggregator import EventsAggregatorService
from ..services.events_provider import EventsProviderService
from ..shemas import Registration, Seats, Ticket

router = APIRouter(
    prefix="/api",
    tags=["events_provider"],
)


@router.get("/events/{event_id}/seats", name="get_seats", response_model=Seats)
@cache(expire=30)
async def get_seats(event_id: UUID) -> Seats:
    async with EventsProviderService(
        service=EventsAggregatorService(repository=EventsAggregatorRepository())
    ) as session:
        seats = await session.get_seats(event_id=event_id)
    return seats


@router.post("/tickets", name="register_ticket", response_model=Ticket)
async def register_ticket(registration: Registration) -> Seats:
    async with EventsProviderService(
        service=EventsAggregatorService(repository=EventsAggregatorRepository())
    ) as session:
        ticket = await session.register_ticket(registration=registration)
    return ticket


@router.delete("/tickets/{ticket_id}", name="cansel_ticket")
async def cansel_ticket(ticket_id: UUID):
    async with EventsProviderService(
        service=EventsAggregatorService(repository=EventsAggregatorRepository())
    ) as session:
        status = await session.cancel_ticket(ticket_id=ticket_id)
    return status
