from datetime import datetime

from sqlalchemy import desc, select

from src.shemas import Event as EventSchema

from ..connection import async_session
from ..models import Event, Place, SyncMetadata


class SyncMetadataRepository:
    @classmethod
    async def sync_event(cls, event: EventSchema):
        async with async_session() as db:
            async with db.begin():
                place_data = event.place.model_dump()
                result = await db.execute(
                    select(Place).where(Place.id == place_data["id"])
                )
                place = result.scalar_one_or_none()

                if not place:
                    place = Place(**place_data)
                    db.add(place)
                    await db.flush()
                    await db.refresh(place)

                event_data = event.model_dump()
                event_data["place_id"] = place.id
                event_data.pop("place")
                event_db = Event(**event_data)
                db.add(event_db)

    @classmethod
    async def save(
        cls, last_sync_time: datetime, last_changed_at: datetime, sync_status: str
    ):
        async with async_session() as db:
            async with db.begin():
                metadata = SyncMetadata(
                    last_sync_time=last_sync_time,
                    last_changed_at=last_changed_at,
                    sync_status=sync_status,
                )
                db.add(metadata)

        return metadata

    @classmethod
    async def get_last_changed_at(cls):
        async with async_session() as db:
            result = await db.execute(
                select(SyncMetadata.last_changed_at)
                .order_by(desc(SyncMetadata.last_changed_at))
                .limit(1)
            )
            last_changed_at = result.scalar_one_or_none()
        return last_changed_at
