from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Outbox


class OutboxRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(
        self, event_type: str, payload: dict[str, Any], status: str, ticket_id: UUID
    ):

        outbox = Outbox(
            event_type=event_type,
            payload=payload,
            status=status,
            ticket_id=ticket_id,
        )
        self.db.add(outbox)

        return outbox

    async def get(self, status: str):
        result = await self.db.execute(select(Outbox).where(Outbox.status == status))

        outbox = result.scalars().all()

        return outbox
