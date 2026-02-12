from datetime import datetime
from zoneinfo import ZoneInfo

from src.shemas import Event

from ..config import LOGGER
from ..database.repository.sync_metadata_repository import SyncMetadataRepository
from .events_paginator import EventsPaginatorService


class SyncMetadataService:
    def __init__(
        self, service: EventsPaginatorService, repository: SyncMetadataRepository
    ):
        self.service = service
        self.repository = repository

    async def sync_events(self):

        last_changed_at = await self.repository.get_last_changed_at()
        await self.service.set_changed_at(last_changed_at or "2000-01-01")

        try:
            async for page in self.service:
                for event in page:
                    dt = datetime.fromisoformat(event["changed_at"])
                    if last_changed_at is None or last_changed_at < dt:
                        last_changed_at = dt
                    model = Event.model_validate(event)
                    await self.repository.sync_event(model)
        except Exception as exc:
            error = {
                "result": False,
                "error_type": exc.__class__.__name__,
                "error_message": str(exc),
            }
            LOGGER.error("Handle event", error=error)

        metadata = await self.repository.save(
            last_sync_time=datetime.now(ZoneInfo("Asia/Vladivostok")),
            last_changed_at=last_changed_at,
            sync_status="Error" if last_changed_at is None else "Ok",
        )

        return metadata
