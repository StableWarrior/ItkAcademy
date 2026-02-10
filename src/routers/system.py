from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..services.sync_metadata_service import SyncMetadataService
from ..services.events_provider import EventsProviderService
from ..services.events_paginator import EventsPaginatorService
from ..database.repository.sync_metadata_repository import SyncMetadataRepository
from ..shemas import SyncMetadata

router = APIRouter(
    prefix="/api/v1",
    tags=["system"],
)

@router.get(
    "/health",
    name="health_check"
)
async def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)


@router.post(
    '/sync/trigger',
    name='sync_metadata',
    response_model=SyncMetadata
)
async def sync_metadata() -> SyncMetadata:

    service = SyncMetadataService(
        service=EventsPaginatorService(
            service=EventsProviderService(),
        ),
        repository=SyncMetadataRepository()
    )
    metadata = await service.sync_events()
    return metadata
