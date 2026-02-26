from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import OutboxIdempotency, TicketIdempotency


class IdempotencyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_ticket(self, idempotency_key: str | None):

        result = await self.db.execute(
            select(TicketIdempotency).where(TicketIdempotency.key == idempotency_key)
        )

        idempotency = result.scalar_one_or_none()

        if idempotency:
            return idempotency.ticket

        return idempotency

    async def get_outbox(self, idempotency_key: str | None):

        result = await self.db.execute(
            select(OutboxIdempotency).where(OutboxIdempotency.key == idempotency_key)
        )

        idempotency = result.scalar_one_or_none()

        if idempotency:
            return idempotency.outbox

        return idempotency

    async def save_ticket(self, ticket_id: UUID, idempotency_key: str):

        idempotency = TicketIdempotency(ticket_id=ticket_id, key=idempotency_key)

        self.db.add(idempotency)

        return idempotency

    async def save_outbox(self, outbox_id: UUID, idempotency_key: str):

        idempotency = OutboxIdempotency(outbox_id=outbox_id, key=idempotency_key)

        self.db.add(idempotency)

        return idempotency
