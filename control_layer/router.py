# router.py

def route_action(data):
    intent = data["intents"][0]["type"]
    action_type = data["actions"][0]["action_type"]

    if action_type == "FETCH_BALANCE":
        return handle_read("GET_BALANCE", data)

    elif action_type == "FETCH_BANK_STATEMENT":
        return handle_read("GET_STATEMENT", data)

    elif action_type == "FETCH_TRANSACTIONS":
        return handle_read("LAST_TRANSACTIONS", data)

    else:
        return {"status": "error", "message": "Unknown READ action"}


def handle_read(intent, data):
    if intent == "GET_BALANCE":
        return {
            "operation": "GET_BALANCE",
            "message": "Fetching account balance"
        }

    elif intent == "GET_STATEMENT":
        duration = data.get("entities", {}).get("duration")

        return {
            "operation": "GET_STATEMENT",
            "message": f"Fetching statement for {duration['value']} {duration['unit']}" if duration else "Fetching statement"
        }

    elif intent == "LAST_TRANSACTIONS":
        return {
            "operation": "LAST_TRANSACTIONS",
            "message": "Fetching last transactions"
        }

    return {"status": "error", "message": "Invalid READ intent"}