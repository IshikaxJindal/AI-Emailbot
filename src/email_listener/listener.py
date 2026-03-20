"""
EMAIL LISTENER SERVICE

Purpose
-------
This service listens for new incoming emails using Microsoft Graph Webhooks.

When a new email arrives in the Outlook inbox, Microsoft Graph sends a
notification to this webhook endpoint.

Flow
----
Customer Email
      ↓
Outlook Inbox
      ↓
Microsoft Graph
      ↓
Webhook Notification
      ↓
Email Listener (this service)
      ↓
Email Preprocessing Layer


Installation Steps
------------------
1. Clone the repository

   git clone <repo-url>
   cd AI-Emailbot

2. Create virtual environment

   python -m venv venv

3. Activate environment

   Windows:
   venv\Scripts\activate

4. Install dependencies

   pip install fastapi uvicorn


Running the Service
-------------------

Start the FastAPI server:

uvicorn src.email_listener.listener:app --reload

Server will run at:

http://127.0.0.1:8000

You can test if the service is running by opening the above URL in a browser.


Webhook Endpoint
----------------

POST /webhook

Microsoft Graph sends notifications to this endpoint whenever a new
email arrives in the monitored inbox.


Local Development (Webhook Testing)
-----------------------------------

Microsoft Graph cannot send webhooks to localhost directly.

So during development we expose our local server using ngrok.

Steps:

1. Run the FastAPI server

2. Start ngrok

   ngrok http 8000

3. ngrok will provide a public URL like:

   https://random-domain.ngrok-free.dev

4. Webhook endpoint becomes:

   https://random-domain.ngrok-free.dev/webhook
"""

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse


# Create FastAPI application
app = FastAPI()


# ---------------------------------------------------------
# HEALTH CHECK ENDPOINT
# ---------------------------------------------------------
# This endpoint simply confirms the Email Listener service
# is running correctly.
#
# Test:
# http://127.0.0.1:8000
#
@app.get("/")
def home():
    return {"message": "Email Listener Running"}


# ---------------------------------------------------------
# WEBHOOK ENDPOINT
# ---------------------------------------------------------
# Microsoft Graph calls this endpoint for two purposes:
#
# 1. Webhook Validation
#    During subscription creation Microsoft sends:
#
#    /webhook?validationToken=xyz
#
#    Our server must return the token exactly as plain text.
#
# 2. Email Notification
#    When a new email arrives, Microsoft sends a POST request
#    containing notification metadata.
#
@app.api_route("/webhook", methods=["GET", "POST"])
async def webhook(request: Request):

    # Step 1 — Webhook validation
    token = request.query_params.get("validationToken")

    if token:
        return PlainTextResponse(content=token)

    # Step 2 — Receive email notification
    # The payload contains details such as subscription ID,
    # message resource, etc.
    try:
        data = await request.json()

        # Currently we only print the notification.
        # In the next stage this data will be used to
        # fetch the full email content via Microsoft Graph API.
        print("Webhook received:", data)

    except:
        pass

    return {"status": "ok"}