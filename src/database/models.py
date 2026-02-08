import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .connection import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name = Column(String(255), nullable=False)

    place_id = Column(
        UUID(as_uuid=True), ForeignKey("places.id", ondelete="CASCADE"), nullable=False
    )
    place = relationship("Place", back_populates="events")

    event_time = Column(DateTime(timezone=True), nullable=False)
    registration_deadline = Column(DateTime(timezone=True), nullable=False)

    status = Column(String(50), nullable=False)
    number_of_visitors = Column(Integer, default=0)


class Place(Base):
    __tablename__ = "places"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    seats_pattern = Column(String(255), nullable=False)

    events = relationship("Event", back_populates="place", cascade="all, delete-orphan")


class SyncMetadata(Base):
    __tablename__ = "sync_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    last_sync_time = Column(DateTime(timezone=True), nullable=True)
    last_changed_at = Column(DateTime(timezone=True), nullable=True)
    sync_status = Column(String(50), nullable=False)
