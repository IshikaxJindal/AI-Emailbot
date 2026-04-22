INTENT_MAPPING = {
    "BANK_STATEMENT_REQUEST": "STATEMENT_QUERY",
    "BALANCE_REQUEST": "BALANCE_QUERY",
    "ACCOUNT_INFO": "BALANCE_QUERY"
}

ACTION_MAPPING = {
    "FETCH_BANK_STATEMENT": "FETCH_STATEMENT",
    "FETCH_BALANCE": "FETCH_BALANCE",
    "FETCH_TRANSACTIONS": "FETCH_TRANSACTIONS",
    "BLOCK_CARD": "BLOCK_CARD"
}


def format_for_decision(intent_result):

    # ---------------------------
    # 🔥 FIX 1: HANDLE INTENT DICT
    # ---------------------------
    raw_intent = intent_result.get("intents", [{}])[0]

    if isinstance(raw_intent, dict):
        intent_type = raw_intent.get("type", "UNKNOWN")
    else:
        intent_type = raw_intent

    mapped_intent = INTENT_MAPPING.get(intent_type, intent_type)

    # ---------------------------
    # 🔥 FIX 2: HANDLE ACTION DICT
    # ---------------------------
    raw_action = intent_result.get("actions", [{}])
    raw_action = raw_action[0] if raw_action else {}

    if isinstance(raw_action, dict):
        action_type = raw_action.get("action_type", "NONE")
    else:
        action_type = raw_action

    mapped_action = ACTION_MAPPING.get(action_type, action_type)

    # ---------------------------
    # ENTITIES
    # ---------------------------
    entities = intent_result.get("entities", {})
    formatted_entities = {}

    if mapped_intent == "STATEMENT_QUERY":
        duration = entities.get("duration", {})
        if duration:
            formatted_entities["start_date"] = "2026-01-01"
            formatted_entities["end_date"] = "2026-04-01"

    # ---------------------------
    # FINAL STRUCTURE
    # ---------------------------
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