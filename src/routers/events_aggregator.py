from typing import Optional
from datetime import date
from fastapi import APIRouter, Query
from ..services.events_aggregator import EventsAggregatorService
from ..database.repository.events_aggregator import EventsAggregatorRepository
from ..shemas import Page

router = APIRouter(
    prefix="/api",
    tags=["events_aggregator"],
)


@router.get("/events", name="get_events", response_model=Page)
async def get_events(
        date_from: Optional[date] = Query(date(2000, 1, 1), description="Формат: YYYY-MM-DD"),
        page: Optional[int] = Query(1, ge=1),
        page_size: Optional[int] = Query(10, ge=1)
) -> Page:

    service = EventsAggregatorService(
        repository=EventsAggregatorRepository(),
    )
    page = await service.get_page(
        date_from=date_from,
        page=page,
        page_size=page_size
    )
    return page
