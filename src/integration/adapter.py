INTENT_MAPPING = {
    "BANK_STATEMENT_REQUEST": "STATEMENT_QUERY",
    "BALANCE_REQUEST": "BALANCE_QUERY",
    "ACCOUNT_INFO": "BALANCE_QUERY"
}

ACTION_MAPPING = {
    "FETCH_BANK_STATEMENT": "FETCH_STATEMENT",
    "FETCH_BALANCE": "FETCH_BALANCE"
}


def format_for_decision(intent_result):
    intent_type = intent_result.get("intents", ["UNKNOWN"])[0]
    actions = intent_result.get("actions", [])

    mapped_intent = INTENT_MAPPING.get(intent_type, intent_type)

    raw_action = actions[0] if actions else "NONE"
    mapped_action = ACTION_MAPPING.get(raw_action, raw_action)

    entities = intent_result.get("entities", {})
    formatted_entities = {}

    if mapped_intent == "STATEMENT_QUERY":
        duration = entities.get("duration", {})
        if duration:
            formatted_entities["start_date"] = "2026-01-01"
            formatted_entities["end_date"] = "2026-04-01"

    return {
        "intents": [
            {
                "type": mapped_intent,
                "confidence": 0.9
            }
        ],
        "actions": [
            {
                "action_type": mapped_action,
                "priority": "HIGH",
                "blocking": True
            }
        ],
        "entities": formatted_entities
    }