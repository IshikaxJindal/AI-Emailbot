
from google import genai
import json

# 👉 Initialize client
client = genai.Client(api_key="AIzaSyBU-gZkzsQ9TNB5ea67ITKnTYkVrL1nlWM")


def classify_with_llm(text: str):
    prompt = f"""
You are an intent classifier for banking emails.

Classify into:
- BANK_STATEMENT_REQUEST
- BALANCE_QUERY
- OTHER

Return ONLY JSON:
{{"intent": "...", "confidence": 0.9}}

Email:
{text}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    content = response.text
    print("LLM RAW OUTPUT:", content)

    # Handle ```json formatting
    if "```" in content:
        content = content.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(content)

        return [{
            "type": parsed.get("intent", "UNKNOWN"),
            "confidence": parsed.get("confidence", 0.5)
        }]

    except Exception as e:
        print("Parsing Error:", e)

        return [{
            "type": "UNKNOWN",
            "confidence": 0.0
        }]