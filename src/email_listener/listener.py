# from fastapi import FastAPI, Body
# from fastapi.responses import PlainTextResponse
# import uuid
#
# from src.pipeline.email_pipeline import process_email
#
# app = FastAPI()
#
#
# @app.get("/")
# def home():
#     return {"message": "Email Listener Running"}
#
#
# @app.post("/webhook")
# async def webhook(body: dict = Body(...)):
#
#     try:
#         print("Webhook received:", body)
#
#         # TAKE BODY FROM USER INPUT
#         email_body = body.get("body", "")
#
#         email_data = {
#             "email_id": str(uuid.uuid4()),
#             "sender": "test@example.com",
#             "subject": "Test Subject",
#             "body": email_body,
#             "received_at": "2026-03-20"
#         }
#
#         process_email(email_data)
#
#     except Exception as e:
#         print("Error:", str(e))
#
#     return {"status": "ok"}
#
# # from fastapi import APIRouter, Depends
# # from sqlalchemy.orm import Session
# # from models import EmailEvent, ProcessingLog
# # from dependencies import get_db
# # from pipeline import process_email
# #
# # router = APIRouter()
# #
# #
# # @router.post("/webhook")
# # def receive_email(data: dict, db: Session = Depends(get_db)):
# #
# #     print("Webhook received:", data)
# #
# #     message_id = data.get("message_id")
# #
# #     # 1. Idempotency check
# #     existing = db.query(EmailEvent).filter_by(message_id=message_id).first()
# #     if existing:
# #         return {"message": "Duplicate ignored"}
# #
# #     # 2. Store event
# #     event = EmailEvent(
# #         message_id=message_id,
# #         payload=data,
# #         status="RECEIVED"
# #     )
# #     db.add(event)
# #     db.commit()
# #     db.refresh(event)
# #
# #     #  3. Log RECEIVED
# #     db.add(ProcessingLog(event_id=event.id, status="RECEIVED"))
# #     db.commit()
# #
# #     #  4. CALL PIPELINE (IMPORTANT)
# #     process_email(event, db)
# #
# #     return {"message": "Processing done"}

from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Body, Depends
from sqlalchemy.orm import Session
import uuid

from dependencies import get_db
from models import EmailEvent, ProcessingLog
from src.pipeline.email_pipeline import process_email

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Email Listener Running"}


@app.post("/webhook")
async def webhook(body: dict = Body(...), db: Session = Depends(get_db)):

    try:
        print("Webhook received:", body)

        message_id = body.get("message_id")
        email_body = body.get("body", "")

        #  1. IDEMPOTENCY CHECK
        existing = db.query(EmailEvent).filter_by(message_id=message_id).first()
        if existing:
            return {"message": "Duplicate ignored"}

        #  2. STORE RAW EVENT
        event = EmailEvent(
            message_id=message_id,
            payload=body,
            status="RECEIVED"
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        #  3. LOG RECEIVED
        db.add(ProcessingLog(event_id=event.id, status="RECEIVED"))
        db.commit()

        #  4. PREPARE DATA FOR PIPELINE
        email_data = {
            "email_id": str(event.id),
            "sender": "test@example.com",
            "subject": "Test Subject",
            "body": email_body,
            "received_at": "2026-03-20"
        }

        #  5. CALL PIPELINE WITH DB
        result = process_email(email_data, db, event.id)

    except Exception as e:
        print("Error:", str(e))

    return {
        "status": "processed",
        "data": result
    }