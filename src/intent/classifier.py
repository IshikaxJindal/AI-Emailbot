from src.intent.intents import INTENTS

def classify_rule_based(text: str):
    text = text.lower()

    detected_intents = []

    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            if keyword in text:
                detected_intents.append({
                    "type": intent,
                    "confidence": 0.8
                })
                break  # avoid duplicate matches

    # If nothing matched
    if not detected_intents:
        detected_intents.append({
            "type": "UNKNOWN",
            "confidence": 0.0
        })

    return detected_intents