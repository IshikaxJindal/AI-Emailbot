# --------------------------
# IMPORT INTENT SYSTEM
# --------------------------
import sys
import os

sys.path.insert(0, os.path.abspath("AI_Emailbot_main"))

from dblayer.db.operations import get_balance, get_last_transaction
from dblayer.services.email_service import send_email   # 👈 added
from AI_Emailbot_main.src.intent.service import process_intent


# --------------------------
# HANDLE ACTION
# --------------------------
def handle_action(user_id, intent_data):
    action = intent_data["actions"][0]["action_type"]

    if action == "FETCH_BALANCE":
        balance = get_balance(user_id)
        response = f"Your balance is Rs {balance}"

    elif action == "FETCH_TRANSACTIONS":
        txn = get_last_transaction(user_id)
        response = f"Your last transaction was: {txn}"

    elif action == "FETCH_STATEMENT":
        response = "Your statement will be sent to your email."

    elif action == "BLOCK_CARD":
        response = "Your card has been blocked successfully."

    else:
        response = "Sorry, I could not process your request."

    # --------------------------
    # SEND EMAIL
    # --------------------------
    send_email(
        "ishika.jindal907@gmail.com",
        
        response
    )

    return response


# --------------------------
# TEST FLOW
# --------------------------
if __name__ == "__main__":

    user_id = "dc4c0771-8ee2-4088-ae17-231678cde4c1"

    query = "What is my account balance?"

    # Step 1: Get intent
    intent_result = process_intent(
        event_id="123",
        clean_text=query,
        entities={}
    )

    print("\nIntent Output:\n", intent_result)

    # Step 2: Get response + send email
    response = handle_action(user_id, intent_result)

    print("\nFinal Response:\n", response)