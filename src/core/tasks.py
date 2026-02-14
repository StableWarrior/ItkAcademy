from ..database.repository.sync_metadata_repository import SyncMetadataRepository
from ..services.events_paginator import EventsPaginatorService
from ..services.events_provider import EventsProviderService
from ..services.sync_metadata_service import SyncMetadataService


async def sync_metadata():
    service = SyncMetadataService(
        service=EventsPaginatorService(
            service=EventsProviderService(),
        ),
        repository=SyncMetadataRepository(),
    )
    await service.sync_events()
