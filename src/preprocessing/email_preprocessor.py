"""
Email Preprocessing Module (UPDATED WITH UUID SUPPORT)
"""

import re
import spacy
from bs4 import BeautifulSoup

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def remove_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def remove_reply_chain(text):
    parts = re.split(r'On .* wrote:', text)
    return parts[0]


def remove_email_addresses(text):
    return re.sub(r'\S+@\S+', '', text)


def remove_signature(text):
    return re.sub(
        r'(thanks|regards|best|sincerely)[\s\S]*$',
        '',
        text,
        flags=re.IGNORECASE
    )


def remove_greeting(text):
    return re.sub(
        r'^(hi|hello|dear|hi team|dear team|dear sir|dear madam)\s+',
        '',
        text,
        flags=re.IGNORECASE
    )


def remove_polite_phrases(text):
    phrases = [
        r"ill be highly obliged",
        r"i'll be highly obliged",
        r"i will be highly obliged",
        r"i would be grateful",
        r"kindly"
    ]

    for phrase in phrases:
        text = re.sub(phrase, '', text, flags=re.IGNORECASE)

    return text


def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_time_expressions(text):
    doc = nlp(text)
    times = []

    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            times.append(ent.text)

    return times


#  UPDATED FUNCTION SIGNATURE
def preprocess_email(text, correlation_id=None):
    """
    Main preprocessing pipeline with optional correlation ID
    """

    # (Optional debug visibility — can remove later)
    if correlation_id:
        print(f"[Preprocessing] correlationId: {correlation_id}")

    text = remove_html(text)
    text = remove_reply_chain(text)
    text = remove_email_addresses(text)
    text = remove_signature(text)
    text = remove_punctuation(text)
    text = normalize_text(text)

    # Remove greeting AFTER normalization
    text = remove_greeting(text)

    # Remove polite phrases
    text = remove_polite_phrases(text)

    time_entities = extract_time_expressions(text)

    return {
        "correlationId": correlation_id,  # 🔥 attach for downstream
        "clean_text": text,
        "time_entities": time_entities
    }
