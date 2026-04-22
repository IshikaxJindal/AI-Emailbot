from google import genai
import json
import os

# Initialize client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def classify_with_llm(text: str):
    prompt = f"""
You are a banking assistant.

Return ONLY valid JSON.

Use STRICT values:

INTENTS:
BALANCE_QUERY
STATEMENT_QUERY
LAST_TRANSACTIONS
BLOCK_CARD
OTHER

ACTIONS:
FETCH_BALANCE
FETCH_STATEMENT
FETCH_TRANSACTIONS
BLOCK_CARD

Rules:
- BALANCE_QUERY → FETCH_BALANCE
- STATEMENT_QUERY → FETCH_STATEMENT
- LAST_TRANSACTIONS → FETCH_TRANSACTIONS
- BLOCK_CARD → BLOCK_CARD
- OTHER → blocking=false

Format:
{{
  "intents": [{{"type": "...", "confidence": 0.9}}],
  "actions": [{{"action_type": "...", "priority": "MEDIUM", "blocking": true}}],
  "entities": {{}}
}}


Email:
{text}
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    content = response.text
    print("LLM RAW OUTPUT:", content)

    # Clean markdown
    if "```" in content:
        content = content.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(content)
        print("FINAL PARSED DATA:", parsed)
        
        return {
        "intents": parsed.get("intents", [{"type": "OTHER", "confidence": 0.0}]),
        "actions": parsed.get("actions", [{
        "action_type": "FETCH_BALANCE",
        "priority": "LOW",
        "blocking": False
    }]),
    "entities": parsed.get("entities", {})
}

    except Exception as e:
        print("Parsing Error:", e)
    return {
    "intents": [{"type": "OTHER", "confidence": 0.0}],
    "actions": [{
        "action_type": "FETCH_BALANCE",
        "priority": "LOW",
        "blocking": False
    }],
    "entities": {}
}