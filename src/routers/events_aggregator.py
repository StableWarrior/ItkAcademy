from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query

from ..database.repository.events_aggregator import EventsAggregatorRepository
from ..services.events_aggregator import EventsAggregatorService
from ..shemas import Event, Page

router = APIRouter(
    prefix="/api",
    tags=["events_aggregator"],
)


@router.get("/events", name="get_events", response_model=Page)
async def get_events(
    date_from: Optional[date] = Query(
        date(2000, 1, 1), description="Формат: YYYY-MM-DD"
    ),
    page: Optional[int] = Query(1, ge=1),
    page_size: Optional[int] = Query(10, ge=1),
) -> Page:

    service = EventsAggregatorService(
        repository=EventsAggregatorRepository(),
    )
    page = await service.get_page(date_from=date_from, page=page, page_size=page_size)
    return page


@router.get("/events/{event_id}", name="get_event", response_model=Event)
async def get_event(event_id: UUID) -> Event:
    service = EventsAggregatorService(
        repository=EventsAggregatorRepository(),
    )
    event = await service.get_event(event_id=event_id)
    return event
