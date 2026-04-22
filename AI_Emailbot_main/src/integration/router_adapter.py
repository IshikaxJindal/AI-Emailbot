ACTION_MAPPING = {
    "FETCH_BANK_STATEMENT": "READ",
    "FETCH_BALANCE": "READ",
    "FETCH_ACCOUNT_INFO": "READ"
}
INTENT_MAPPING_ROUTER = {
    "STATEMENT_QUERY": "GET_STATEMENT",
    "BALANCE_QUERY": "GET_BALANCE"
}

def format_for_router(decision_input):
    intent = decision_input["intents"][0]["type"]
    action = decision_input["actions"][0]["action_type"]

    mapped_intent = INTENT_MAPPING_ROUTER.get(intent, intent)

    return {
        "intent": mapped_intent,
        "action_type": "READ"
    }