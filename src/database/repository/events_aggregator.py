from datetime import date
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from src.config import EVENTS_AGGREGATOR_URL

from ..connection import async_session
from ..models import Event


class EventsAggregatorRepository:
    @classmethod
    async def get_events(
        cls,
        date_from: date = date(2000, 1, 1),
        page: int = 1,
        page_size: int = 10,
    ):
        async with async_session() as db:
            offset = (page - 1) * page_size

            query = (
                select(Event)
                .where(Event.event_time >= date_from)
                .options(joinedload(Event.place))
                .order_by(Event.event_time)
            )
            count_query = (
                select(func.count())
                .select_from(Event)
                .where(Event.event_time >= date_from)
            )

            result = await db.execute(query.limit(page_size).offset(offset))

            events = result.unique().scalars().all()
            total_count = (await db.execute(count_query)).scalar_one()

            next_url = None
            if offset + page_size < total_count:
                next_url = f"{EVENTS_AGGREGATOR_URL}/api/events/?page={page + 1}"

            previous_url = None
            if page > 1:
                previous_url = f"{EVENTS_AGGREGATOR_URL}/api/events/?page={page - 1}"

            response = {
                "count": total_count,
                "next": next_url,
                "previous": previous_url,
                "results": events,
            }

        return response

    @classmethod
    async def get_event(cls, event_id: UUID):
        async with async_session() as db:
            result = await db.execute(
                select(Event)
                .options(joinedload(Event.place))
                .where(Event.id == event_id)
            )
            event = result.scalar_one_or_none()

            if event is None:
                raise HTTPException(status_code=404, detail="Event not found")

        return event
