# router.py

def route_action(data):
    intent = data.get("intent")
    action_type = data.get("action_type")

    # READ actions
    if action_type == "READ":
        return handle_read(intent, data)

    # BLOCK actions
    elif action_type == "BLOCK":
        return handle_block(intent, data)

    # UPDATE actions (future use)
    elif action_type == "UPDATE":
        return handle_update(intent, data)

    else:
        return {"status": "error", "message": "Unknown action type"}


# -------- HANDLERS -------- #

def handle_read(intent, data):
    if intent == "GET_BALANCE":
        return {"operation": "GET_BALANCE", "message": "Fetching account balance"}

    elif intent == "GET_STATEMENT":
        return {"operation": "GET_STATEMENT", "message": "Fetching account statement"}

    elif intent == "LAST_TRANSACTIONS":
        return {"operation": "LAST_TRANSACTIONS", "message": "Fetching last transactions"}

    return {"status": "error", "message": "Invalid READ intent"}


def handle_block(intent, data):
    if intent == "BLOCK_CARD":
        return {"operation": "BLOCK_CARD", "message": "Blocking card"}

    return {"status": "error", "message": "Invalid BLOCK intent"}


def handle_update(intent, data):
    return {"operation": "UPDATE", "message": "Update operation"}