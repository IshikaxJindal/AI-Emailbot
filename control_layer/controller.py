from validator import validate_input
from router import route_action


def make_decision(is_valid, message, data):
    if not is_valid:
        return "REJECT", message

    intent_data = data["intents"][0]
    action_data = data["actions"][0]

    intent = intent_data.get("type")
    confidence = intent_data.get("confidence", 0)

    action_type = action_data.get("action_type")
    priority = action_data.get("priority")
    requires_action = action_data.get("blocking")

    if not requires_action:
        return "REJECT", "No action required"

    if confidence < 0.6:
        return "REJECT", "Low confidence"

    if 0.6 <= confidence < 0.75:
        return "NEED_CLARIFICATION", "Please confirm your request"

    if intent == "BLOCK_CARD":
        if priority != "HIGH":
            return "NEED_CLARIFICATION", "Blocking requires high priority"

        if action_type != "BLOCK_CARD":
            return "REJECT", "Invalid action mapping"

    return "PROCEED", "Valid to execute"


def process_request(data):
    is_valid, message = validate_input(data)

    decision, decision_msg = make_decision(is_valid, message, data)

    if decision != "PROCEED":
        return {
            "status": decision,
            "message": decision_msg
        }

    result = route_action(data)

    return {
        "status": "SUCCESS",
        "data": result
    }