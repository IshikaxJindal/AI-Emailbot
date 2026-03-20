"""
Email Preprocessing Module

Responsible for cleaning and structuring raw email input before
passing it to the intent validation layer.

Pipeline:
1. Remove HTML
2. Remove reply chains
3. Remove email addresses
4. Remove signatures
5. Remove greetings
6. Remove polite phrases
7. Remove punctuation
8. Normalize text
9. Extract time expressions
"""

import re
import spacy
from bs4 import BeautifulSoup

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def remove_html(text):
    """Remove HTML tags."""
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def remove_reply_chain(text):
    """Remove previous email threads."""
    parts = re.split(r'On .* wrote:', text)
    return parts[0]


def remove_email_addresses(text):
    """Remove email addresses."""
    return re.sub(r'\S+@\S+', '', text)


def remove_signature(text):
    """Remove signatures appearing at the end."""
    return re.sub(
        r'(thanks|regards|best|sincerely)[\s\S]*$',
        '',
        text,
        flags=re.IGNORECASE
    )


def remove_greeting(text):
    """Remove greetings at the beginning."""
    return re.sub(
        r'^(hi|hello|dear|hi team|dear team|dear sir|dear madam)\s+',
        '',
        text,
        flags=re.IGNORECASE
    )


def remove_polite_phrases(text):
    """Remove unnecessary polite phrases."""
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
    """Remove punctuation marks."""
    return re.sub(r'[^\w\s]', '', text)


def normalize_text(text):
    """Normalize whitespace and lowercase."""
    text = text.lower()
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_time_expressions(text):
    """Extract time expressions using spaCy."""
    doc = nlp(text)

    times = []

    for ent in doc.ents:
        if ent.label_ in ["DATE", "TIME"]:
            times.append(ent.text)

    return times


def preprocess_email(text):
    """Main preprocessing pipeline."""

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
        "clean_text": text,
        "time_entities": time_entities
    }