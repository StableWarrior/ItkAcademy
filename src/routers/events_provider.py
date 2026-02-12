from uuid import UUID
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from ..services.events_provider import EventsProviderService
from ..services.events_aggregator import EventsAggregatorService
from ..database.repository.events_aggregator import EventsAggregatorRepository
from ..shemas import Seats

router = APIRouter(
    prefix="/api",
    tags=["events_provider"],
)


@router.get("/events/{event_id}/seats", name="get_seats", response_model=Seats)
@cache(expire=30)
async def get_seats(event_id: UUID) -> Seats:
    async with EventsProviderService(
        service=EventsAggregatorService(
            repository=EventsAggregatorRepository()
        )
    ) as session:
        seats = await session.get_seats(event_id=event_id)
    return seats
