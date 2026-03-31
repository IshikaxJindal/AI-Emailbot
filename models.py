import uuid
from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey, Integer, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from database import Base


class EmailEvent(Base):
    __tablename__ = "email_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(String, unique=True, index=True)
    payload = Column(JSONB)
    status = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Email(Base):
    __tablename__ = "emails"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("email_events.id"))
    clean_text = Column(Text)
    entities = Column(JSONB)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class ProcessingLog(Base):
    __tablename__ = "processing_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("email_events.id"))
    status = Column(String)
    error_message = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class IntentResult(Base):
    __tablename__ = "intent_results"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(UUID(as_uuid=True), ForeignKey("email_events.id"), nullable=False)

    intents = Column(JSON)
    entities = Column(JSON)
    actions = Column(JSON)

    source = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

