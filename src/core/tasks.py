from ..database.connection import async_session
from ..database.repository.events_aggregator import EventsAggregatorRepository
from ..database.repository.outbox_repository import OutboxRepository
from ..database.repository.sync_metadata_repository import SyncMetadataRepository
from ..services.events_aggregator import EventsAggregatorService
from ..services.events_paginator import EventsPaginatorService
from ..services.events_provider import EventsProviderService
from ..services.sync_metadata_service import SyncMetadataService


async def sync_metadata():
    service = SyncMetadataService(
        service=EventsPaginatorService(
            service=EventsProviderService(
                service=EventsAggregatorService(repository=EventsAggregatorRepository())
            ),
        ),
        repository=SyncMetadataRepository(),
    )
    await service.sync_events()


async def sync_notifications():
    async with async_session() as db:
        repository = OutboxRepository(db=db)
        await repository.get(status="ожидает отправки")
