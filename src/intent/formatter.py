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
    intent_types = [intent["type"] for intent in intents]

    actions = []
    for intent_type in intent_types:
        action_type = INTENT_TO_ACTION.get(intent_type)
        if action_type:
            actions.append(action_type)

    return {
        "event_id": str(event_id),
        "intents": intent_types,
        "entities": structured_entities,
        "actions": actions,
        "meta": {
            "source": "rule_based",
            "processed_at": datetime.utcnow().isoformat()
        }
    }