from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Body, Depends
from sqlalchemy.orm import Session
import uuid
from core.dependencies import get_db
from model.models import EmailEvent, ProcessingLog
from src.pipeline.email_pipeline import process_email

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Email Listener Running"}

@app.post("/webhook")
async def webhook(body: dict = Body(...), db: Session = Depends(get_db)):

    try:

        # FIX: ensure message_id exists
        message_id = body.get("message_id") or str(uuid.uuid4())
        email_body = body.get("body", "")

        # 1. IDEMPOTENCY CHECK
        existing = db.query(EmailEvent).filter_by(message_id=message_id).first()
        if existing:
            return {"message": "Duplicate ignored"}

        # 2. STORE RAW EVENT
        event = EmailEvent(
            message_id=message_id,
            payload=body,
            status="RECEIVED"
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        # 3. LOG RECEIVED
        db.add(ProcessingLog(event_id=event.id, status="RECEIVED"))
        db.commit()

        # 4. PREPARE DATA
        email_data = {
            "email_id": str(event.id),
            "sender": "test@example.com",
            "subject": "Test Subject",
            "body": email_body,
            "received_at": "2026-03-20"
        }


        # 5. PIPELINE
        result = process_email(email_data, db, event.id)

        print("Pipeline result:", result)

        return {
            "status": "processed",
            "data": result
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "status": "ERROR",
            "message": str(e)
        }