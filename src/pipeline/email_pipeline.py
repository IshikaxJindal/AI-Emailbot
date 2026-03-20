from src.preprocessing.email_preprocessor import preprocess_email

def process_email(email_data):
    email_id = email_data["email_id"]

    print(f"[{email_id}] Email received")

    # YOUR preprocessing pipeline
    result = preprocess_email(email_data["body"])

    print(f"[{email_id}] Clean text:", result["clean_text"])
    print(f"[{email_id}] Time entities:", result["time_entities"])

    print(f"[{email_id}] Pipeline working")