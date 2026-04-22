from src.intent.actions import INTENT_TO_ACTION
from datetime import datetime


def parse_duration(entity_list):
    if not entity_list:
        return {}

    text = entity_list[0].lower()
    words = text.split()

    for i, word in enumerate(words):
        if word.isdigit():
            value = int(word)
            unit = words[i + 1] if i + 1 < len(words) else None
            return {"duration": {"value": value, "unit": unit}}

    if "year" in text:
        return {"duration": {"value": 1, "unit": "year"}}
    if "month" in text:
        return {"duration": {"value": 1, "unit": "month"}}
    if "week" in text:
        return {"duration": {"value": 1, "unit": "week"}}

    return {}


def format_output(event_id, intents, entities):

    structured_entities = parse_duration(entities)

    # ✅ KEEP FULL INTENT STRUCTURE (FIX)
    formatted_intents = []
    for intent in intents:
        if isinstance(intent, dict):
            formatted_intents.append({
                "type": intent.get("type", "OTHER"),
                "confidence": intent.get("confidence", 0.5)
            })
        else:
            formatted_intents.append({
                "type": intent,
                "confidence": 0.5
            })

    # ✅ CREATE PROPER ACTION OBJECTS (FIX)
    actions = []
    for intent in formatted_intents:
        intent_type = intent["type"]
        action_type = INTENT_TO_ACTION.get(intent_type)

        if action_type:
            actions.append({
                "action_type": action_type,
                "priority": "MEDIUM",
                "blocking": True
            })

    return {
        "event_id": str(event_id),
        "intents": formatted_intents,   # ✅ FIXED
        "entities": structured_entities,
        "actions": actions,             # ✅ FIXED
        "meta": {
            "source": "rule_based",
            "processed_at": datetime.utcnow().isoformat()
        }
    }