ALLOWED_INTENTS = {
    "BALANCE_QUERY",
    "STATEMENT_QUERY",
    "LAST_TRANSACTIONS",
    "BLOCK_CARD",
    "OTHER"
}

ALLOWED_ACTIONS = {
    "FETCH_BALANCE",
    "FETCH_STATEMENT",
    "FETCH_TRANSACTIONS",
    "BLOCK_CARD"
}

ALLOWED_PRIORITY = {"LOW", "MEDIUM", "HIGH"}


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

    if intent == "STATEMENT_QUERY":
        if not entities.get("start_date") or not entities.get("end_date"):
            return False, "Missing date range"

    if intent == "BLOCK_CARD":
        if not entities.get("card_id"):
            return False, "Missing card_id"

    return True, "Valid input"