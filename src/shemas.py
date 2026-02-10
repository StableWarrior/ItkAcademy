from datetime import datetime
from uuid import UUID
from typing import Literal
from pydantic import BaseModel


class Place(BaseModel):
    id: UUID
    name: str
    city: str
    address: str
    seats_pattern: str

class Event(BaseModel):
    id: UUID
    name: str
    place: Place
    event_time: datetime
    registration_deadline: datetime
    status: str
    number_of_visitors: int


class SyncMetadata(BaseModel):
    last_sync_time: datetime
    last_changed_at: datetime
    sync_status: str