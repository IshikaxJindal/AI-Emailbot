# db/models.py

import uuid
from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .config import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Email(Base):
    __tablename__ = "emails"

    email_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    subject = Column(Text)
    body = Column(Text)
    intent = Column(String)
    received_at = Column(TIMESTAMP, server_default=func.now())


class Response(Base):
    __tablename__ = "responses"

    response_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(UUID(as_uuid=True), ForeignKey("emails.email_id"))
    response_text = Column(Text)
    generated_by = Column(String)  # AI / RULE
    confidence = Column(Numeric)
    created_at = Column(TIMESTAMP, server_default=func.now())


class BankingContext(Base):
    __tablename__ = "banking_context"

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    account_type = Column(String)
    last_transaction = Column(Text)
    balance = Column(Numeric)
