# controller.py

from validator import validate_input
from router import route_action


# ---------------- DECISION LOGIC ---------------- #

def make_decision(is_valid, message, data):
    if not is_valid:
        return "REJECT", message

    intent_data = data["intents"][0]
    action_data = data["actions"][0]

    confidence = intent_data.get("confidence", 0)
    requires_action = action_data.get("blocking")

    if not requires_action:
        return "REJECT", "No action required"

    if confidence < 0.6:
        return "REJECT", "Low confidence"

    if 0.6 <= confidence < 0.75:
        return "NEED_CLARIFICATION", "Please confirm your request"

    return "PROCEED", "Valid to execute"


# ---------------- MAIN CONTROLLER ---------------- #

def process_request(data):
    # Step 1: Validate input
    is_valid, message = validate_input(data)

    # Step 2: Decision
    decision, decision_msg = make_decision(is_valid, message, data)

    # Step 3: Handle decision
    if decision != "PROCEED":
        return {
            "status": decision,
            "message": decision_msg
        }

    # Step 4: Route action
    result = route_action(data)

    return {
        "status": "SUCCESS",
        "data": result
    }