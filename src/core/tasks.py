from ..config import LOGGER
from ..database.connection import async_session
from ..database.repository.events_aggregator import EventsAggregatorRepository
from ..database.repository.idempotency_repository import IdempotencyRepository
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
        async with db.begin():
            service = EventsProviderService(
                service=EventsAggregatorService(
                    repository=EventsAggregatorRepository(),
                    idempotency=IdempotencyRepository(db=db),
                )
            )
            repository = OutboxRepository(db=db)
            outboxes = await repository.get(status="ожидает отправки")

            for outbox in outboxes:
                try:
                    idempotency_key = f"notification-{outbox.id}"
                    async with service as session:
                        status, result = await session.send_to_capashino(
                            message=f"Вы успешно зарегистрированы на мероприятие - '{outbox.event_type}'",
                            reference_id=outbox.ticket_id,
                            idempotency_key=idempotency_key,
                        )

                    if status == 201:
                        await repository.update(outbox=outbox)
                        await session.service.save_outbox_idempotency(
                            outbox_id=outbox.id, idempotency_key=idempotency_key
                        )

                except Exception as exc:
                    error = {
                        "result": False,
                        "error_type": exc.__class__.__name__,
                        "error_message": exc.__str__(),
                    }
                    LOGGER.error("Failed to sync outbox message", error=error)
