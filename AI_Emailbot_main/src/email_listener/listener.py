from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Body, Depends
from sqlalchemy.orm import Session
import uuid

from src.core.dependencies import get_db
from src.model.models import EmailEvent, ProcessingLog
from src.pipeline.email_pipeline import process_email

import sys
import os

# 👇 add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

# from dblayer.db.operations import get_balance, get_last_transaction
# from dblayer.services.email_service import send_email

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Email Listener Running"}


# --------------------------
# ACTION HANDLER (ADDED)
# --------------------------
def handle_action(user_id, intent_data):

    from dblayer.db.operations import get_balance, get_last_transaction

    # ---------------------------
    # 🔥 CASE 1: CONTROL LAYER OUTPUT
    # ---------------------------
    if "operation" in intent_data:

        operation = intent_data.get("operation")

        if operation == "GET_BALANCE":
            balance = get_balance(user_id)
            return f"Your balance is Rs {balance}"

        elif operation in ["GET_TRANSACTIONS", "LAST_TRANSACTIONS"]:
            txn = get_last_transaction(user_id)
            return f"Your last transaction was: {txn}"

        elif operation == "GET_STATEMENT":
            return "Your statement will be sent to your email."

        elif operation == "BLOCK_CARD":
            return "Your card has been blocked successfully."

        return "Sorry, I could not process your request."

    # ---------------------------
    # 🔥 CASE 2: OLD FORMAT (fallback)
    # ---------------------------
    actions = intent_data.get("actions", [])

    if not actions:
        return "Sorry, I could not understand your request."

    action = actions[0].get("action_type")

    if action == "FETCH_BALANCE":
        balance = get_balance(user_id)
        return f"Your balance is Rs {balance}"

    elif action == "FETCH_TRANSACTIONS":
        txn = get_last_transaction(user_id)
        return f"Your last transaction was: {txn}"

    elif action == "FETCH_STATEMENT":
        return "Your statement will be sent to your email."

    elif action == "BLOCK_CARD":
        return "Your card has been blocked successfully."

    return "Sorry, I could not process your request."

@app.post("/webhook")
async def webhook(body: dict = Body(...), db: Session = Depends(get_db)):

    print("ENDPOINT HIT")  

    try:
        from dblayer.services.email_service import send_email

        print("STEP 1: Request received")

        # INPUT
        message_id = body.get("message_id") or str(uuid.uuid4())
        email_body = body.get("body", "")
        user_id = body.get("user_id")
        email = body.get("email")

        print("STEP 2: Data extracted")

        # IDEMPOTENCY
        existing = db.query(EmailEvent).filter_by(message_id=message_id).first()
        if existing:
            return {"message": "Duplicate ignored"}

        # STORE EVENT
        event = EmailEvent(
            message_id=message_id,
            payload=body,
            status="RECEIVED"
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        print("STEP 3: Event stored")

        # LOG
        db.add(ProcessingLog(event_id=event.id, status="RECEIVED"))
        db.commit()

        # PIPELINE INPUT
        email_data = {
            "email_id": str(event.id),
            "sender": "test@example.com",
            "subject": "Test Subject",
            "body": email_body,
            "received_at": "2026-03-20"
        }

        print("STEP 4: Calling pipeline")

        # PIPELINE
        result = process_email(email_data, db, event.id)

        print("STEP 5: Pipeline result", result)

        # HANDLE ACTION
        intent_data = result.get("data", result)

        response_text = handle_action(user_id, intent_data)

        print("STEP 6: Response generated", response_text)

        # EMAIL
        send_email(email, response_text)

        print("STEP 7: Email sent")

        return {
            "status": "processed",
            "intent": result,
            "response": response_text,
            "email_sent_to": email
        }

    except Exception as e:
        print("ERROR OCCURRED:", str(e))
        return {
            "status": "ERROR",
            "message": str(e)
        }