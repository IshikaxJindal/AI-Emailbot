"""
EMAIL LISTENER SERVICE (UPDATED WITH UUID + PREPROCESSING INTEGRATION)
"""

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from uuid import uuid4

#  Import your preprocessing function
from src.preprocessing.email_preprocessor import preprocess_email


# Create FastAPI application
app = FastAPI()


# ---------------------------------------------------------
# HEALTH CHECK ENDPOINT
# ---------------------------------------------------------
@app.get("/")
def home():
    return {"message": "Email Listener Running"}


# ---------------------------------------------------------
# WEBHOOK ENDPOINT
# ---------------------------------------------------------
@app.api_route("/webhook", methods=["GET", "POST"])
async def webhook(request: Request):

    # Step 1 — Webhook validation
    token = request.query_params.get("validationToken")

    if token:
        return PlainTextResponse(content=token)

    # Step 2 — Receive email notification
    try:
        data = await request.json()

        # 🔥 STEP 1: Generate UUID at ENTRY POINT
        correlation_id = str(uuid4())

        print("Correlation ID:", correlation_id)
        print("Webhook received:", data)

        # 🔥 STEP 2: Pass UUID forward
        await process_email_notification(data, correlation_id)

    except Exception as e:
        print("Error:", str(e))

    return {"status": "ok"}


# ---------------------------------------------------------
# PIPELINE ENTRY FUNCTION
# ---------------------------------------------------------
async def process_email_notification(data, correlation_id):

    print("Processing with ID:", correlation_id)

    # Placeholder (replace later with Microsoft Graph fetch)
    email = {
        "subject": "Dummy subject",
        "body": "This is a test email",
        "from": "user@example.com"
    }

    # 🔥 CORRECT: pass ONLY body + correlationId
    processed = preprocess_email(email["body"], correlation_id)

    print("Processed Output:", processed)

    return processed
