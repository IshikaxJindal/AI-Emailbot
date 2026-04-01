# validator.py

ALLOWED_INTENTS = {
    "GET_BALANCE",
    "GET_STATEMENT",
    "LAST_TRANSACTIONS"
}

ALLOWED_ACTIONS = {
    "FETCH_BALANCE",
    "FETCH_BANK_STATEMENT",
    "FETCH_TRANSACTIONS"
}

ALLOWED_PRIORITY = {"LOW", "MEDIUM", "HIGH"}



INTENT_MAP = {
    "BALANCE_QUERY": "GET_BALANCE",
    "STATEMENT_QUERY": "GET_STATEMENT",
    "BANK_STATEMENT_REQUEST": "GET_STATEMENT"
}


def validate_input(data):
    try:
        intent_data = data["intents"][0]
        action_data = data["actions"][0]
    except (KeyError, IndexError):
        return False, "Invalid structure: missing intents/actions"

    intent = intent_data.get("type")
    confidence = intent_data.get("confidence", 0)
    action_type = action_data.get("action_type")
    priority = action_data.get("priority")
    requires_action = action_data.get("blocking")

  
    intent = INTENT_MAP.get(intent, intent)
    intent_data["type"] = intent  # update in-place

    # requires_action
    if not requires_action:
        return False, "No action required"

    # confidence
    if confidence < 0.6:
        return False, "Low confidence"

    # intent
    if intent not in ALLOWED_INTENTS:
        return False, "Invalid intent"

    # action
    if action_type not in ALLOWED_ACTIONS:
        return False, "Invalid action type"

    # priority
    if priority not in ALLOWED_PRIORITY:
        return False, "Invalid priority"

    # entities
    entities = data.get("entities", {})

    if intent == "GET_STATEMENT":
        # optional duration OR date range
        if not entities.get("duration") and not (
            entities.get("start_date") and entities.get("end_date")
        ):
            return False, "Missing duration or date range"

    return True, "Valid input"