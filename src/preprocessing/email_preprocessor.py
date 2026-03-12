"""Email Preprocessing Module

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

nlp = spacy.load("en_core_web_sm")
import re
import spacy
from bs4 import BeautifulSoup
def remove_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()
    
  def remove_reply_chain(text):
    parts = re.split(r'On .* wrote:', text)
    return parts[0]
    def remove_signature(text):

    patterns = ["thanks", "regards", "best", "sincerely"]

    for pattern in patterns:
        text = re.split(pattern, text, flags=re.IGNORECASE)[0]

    return text
      
    def normalize_text(text):

    text = text.lower()

    text = re.sub(r'\n+', ' ', text)

    text = re.sub(r'\s+', ' ', text)

    return text.strip()
    
   
