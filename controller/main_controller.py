from db.operations import *
from services.response_generator import generate_response
from services.email_service import send_email


def process_user_request(user_name, user_email, user_query):
    
    print("Step 1: Creating / Fetching user")
    user_id = create_user(user_name, user_email)
    
    print("Step 2: Storing email")
    intent = "BALANCE_QUERY"   # temporary
    
    email_id = store_email(user_id, "User Query", user_query, intent)
    
    print("Step 3: Fetching data")
    # Step 3: Fetching data based on intent

    if intent == "BALANCE_QUERY":
        data = get_balance(user_id)

    elif intent == "LAST_TRANSACTION":
        data = get_last_transaction(user_id)


    else:
        data = None
    
    print("Step 4: Generating response")
    response = generate_response(intent, data)
    
    print("Step 5: Sending email")
    send_email(user_email, response)
    
    print("Step 6: Storing response")
    store_response(email_id, response, "RULE", 0.99)
    
    print("Process Completed Successfully")


# TEST
if __name__ == "__main__":
    
    process_user_request(
        "Ishika",
        "Ishika.jindal907@gmail.com",
        "What is my balance?"
    )