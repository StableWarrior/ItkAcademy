from datetime import datetime
from typing import List, Optional
from uuid import UUID

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


class Page(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[Event]


class SyncMetadata(BaseModel):
    last_sync_time: datetime
    last_changed_at: datetime
    sync_status: str
