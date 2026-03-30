import uuid
from .config import SessionLocal
from .models import User, Email, Response, BankingContext


# ---------------------------
# CREATE USER (AUTO SAFE)
# ---------------------------
def create_user(name, email):
    db = SessionLocal()
    try:
        user = User(name=name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user.user_id
    finally:
        db.close()


# ---------------------------
# STORE EMAIL
# ---------------------------
def store_email(user_id, subject, body, intent):
    db = SessionLocal()
    try:
        email = Email(
            user_id=user_id,
            subject=subject,
            body=body,
            intent=intent
        )
        db.add(email)
        db.commit()
        db.refresh(email)
        return email.email_id
    finally:
        db.close()


# ---------------------------
# GET USER CONTEXT
# ---------------------------
def get_user_context(user_id):
    db = SessionLocal()
    try:
        return db.query(BankingContext).filter_by(user_id=user_id).first()
    finally:
        db.close()


# ---------------------------
# STORE RESPONSE
# ---------------------------
def store_response(email_id, response_text, source, confidence=0.9):
    db = SessionLocal()
    try:
        response = Response(
            email_id=email_id,
            response_text=response_text,
            generated_by=source,
            confidence=confidence
        )
        db.add(response)
        db.commit()
        db.refresh(response)
        return response.response_id
    finally:
        db.close()


# ---------------------------
# ADD BANKING CONTEXT
# ---------------------------
def add_banking_context(user_id, account_type, balance, last_txn):
    db = SessionLocal()
    try:
        context = BankingContext(
            user_id=user_id,
            account_type=account_type,
            balance=balance,
            last_transaction=last_txn
        )
        db.add(context)
        db.commit()
    finally:
        db.close()
