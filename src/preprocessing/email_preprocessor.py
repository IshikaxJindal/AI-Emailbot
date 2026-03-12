"""
Email Preprocessing Module

Responsible for cleaning and structuring raw email input before
passing it to the intent validation layer.

Steps:
1. Remove HTML
2. Remove reply chains
3. Remove signatures
4. Normalize text
5. Extract account numbers
6. Extract time expressions
"""
print("Script started")
import re
import spacy
from bs4 import BeautifulSoup

# Load NLP model
nlp = spacy.load("en_core_web_sm")


# Remove HTML tags
def remove_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


# Remove reply chain from previous emails
def remove_reply_chain(text):
    parts = re.split(r'On .* wrote:', text)
    return parts[0]


# Remove email signatures
def remove_signature(text):

    patterns = ["thanks", "regards", "best", "sincerely"]

    for pattern in patterns:
        text = re.split(pattern, text, flags=re.IGNORECASE)[0]

    return text


# Normalize text
def normalize_text(text):

    text = text.lower()
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# Extract account number
def extract_account_number(text):

    match = re.search(r'\b\d{6,12}\b', text)

    if match:
        return match.group()

    return None


# Extract date expressions using spaCy
def extract_dates(text):

    doc = nlp(text)

    dates = []

    for ent in doc.ents:
        if ent.label_ == "DATE":
            dates.append(ent.text)

    return dates


# Main preprocessing pipeline
def preprocess_email(sender, subject, body):

    body = remove_html(body)
    body = remove_reply_chain(body)
    body = remove_signature(body)
    body = normalize_text(body)

    account_number = extract_account_number(body)
    dates = extract_dates(body)

    return {
        "sender": sender,
        "subject": subject,
        "clean_body": body,
        "account_number": account_number,
        "dates": dates
    }


# Test block
if __name__ == "__main__":

    email_body = """
    Hi,

    Please send my bank statement for the last 3 months.
    Account number 12345678

    Thanks
    Rahul
    """

    result = preprocess_email(
        sender="rahul@gmail.com",
        subject="Bank Statement Request",
        body=email_body
    )

    print(result)
