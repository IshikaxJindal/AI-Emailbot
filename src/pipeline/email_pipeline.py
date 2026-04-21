from model.models import ProcessingLog
from src.preprocessing.email_preprocessor import preprocess_email
from src.intent.service import process_intent
from src.integration.adapter import format_for_decision
from src.integration.router_adapter import format_for_router
from control_layer.controller import process_request
from control_layer.router import route_action


def process_email(email_data, db, event_id):
    try:
        print(f"[{event_id}] Processing started")

        db.add(ProcessingLog(event_id=event_id, status="PROCESSING"))
        db.commit()

        # STEP 1: PREPROCESS
        result = preprocess_email(email_data["body"])
        clean_text = result["clean_text"]

        print(f"[{event_id}] Clean text:", clean_text)

        # STEP 2: INTENT
        intent_result = process_intent(
            event_id=event_id,
            clean_text=clean_text,
            entities=result["time_entities"]
        )

        print(f"[{event_id}] Intent Result:", intent_result)

        # STEP 3: → DECISION FORMAT
        decision_input = format_for_decision(intent_result)
        print(f"[{event_id}] Decision Input:", decision_input)

        # STEP 4: DECISION
        decision_output = process_request(decision_input)
        print(f"[{event_id}] Decision Output:", decision_output)

        if decision_output.get("status") != "SUCCESS":
            return decision_output

        # STEP 5: → ROUTER FORMAT
        router_input = format_for_router(decision_input)
        print(f"[{event_id}] Router Input:", router_input)

        # STEP 6: ROUTER
        final_result = route_action(router_input)
        print(f"[{event_id}] Final Result:", final_result)

        db.add(ProcessingLog(event_id=event_id, status="SUCCESS"))
        db.commit()

        return {
            "status": "SUCCESS",
            "data": final_result
        }

    except Exception as e:
        print(f"[{event_id}] Error:", str(e))

        db.add(ProcessingLog(
            event_id=event_id,
            status="FAILED",
            error_message=str(e)
        ))
        db.commit()

        return {"error": str(e)}