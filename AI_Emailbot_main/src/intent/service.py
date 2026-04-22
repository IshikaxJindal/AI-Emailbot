from src.intent.classifier import classify_rule_based
from src.intent.formatter import format_output
from src.intent.llm_classifier import classify_with_llm


def process_intent(event_id: str, clean_text: str, entities: dict):

    # ---------------------------
    # STEP 1: RULE-BASED INTENT
    # ---------------------------
    intents = classify_rule_based(clean_text)
    source = "rule_based"

    # 🔒 SAFETY: ensure valid structure
    if not intents or not isinstance(intents, list):
        intents = [{"type": "OTHER", "confidence": 0.0}]

    # ---------------------------
    # STEP 2: LLM FALLBACK
    # ---------------------------
    if intents[0].get("type") == "UNKNOWN":
        print("Using LLM fallback...")

        try:
            llm_data = classify_with_llm(clean_text)

            if isinstance(llm_data, dict):
                intents = llm_data.get("intents", [{"type": "OTHER", "confidence": 0.0}])
                entities = llm_data.get("entities", {})
            else:
                intents = [{"type": "OTHER", "confidence": 0.0}]
                entities = {}

            source = "llm"

        except Exception as e:
            print("LLM failed:", e)
            intents = [{"type": "OTHER", "confidence": 0.0}]
            entities = {}
            source = "rule_based"

    # ---------------------------
    # STEP 3: NORMALIZE INTENTS (🔥 IMPORTANT FIX)
    # ---------------------------
    normalized_intents = []

    for intent in intents:
        if isinstance(intent, dict):
            raw_type = intent.get("type")

            # 🔥 FIX: handle nested dict
            if isinstance(raw_type, dict):
                intent_type = raw_type.get("intent") or raw_type.get("type") or "OTHER"
            else:
                intent_type = raw_type or "OTHER"

            normalized_intents.append({
                "type": intent_type,
                "confidence": intent.get("confidence", 0.5)
            })

        elif isinstance(intent, str):
            normalized_intents.append({
                "type": intent,
                "confidence": 0.5
            })

    intents = normalized_intents

    # ---------------------------
    # STEP 4: FORMAT OUTPUT
    # ---------------------------
    result = format_output(event_id, intents, entities)

    # ---------------------------
    # STEP 5: ENSURE ACTION LIST EXISTS
    # ---------------------------
    if not result.get("actions"):
        result["actions"] = [{}]

    # ---------------------------
    # STEP 6: INTENT → ACTION MAPPING
    # ---------------------------
    intent_type = intents[0].get("type", "OTHER")

    intent_to_action = {
        "BALANCE_QUERY": "FETCH_BALANCE",
        "STATEMENT_QUERY": "FETCH_STATEMENT",
        "LAST_TRANSACTIONS": "FETCH_TRANSACTIONS",
        "BLOCK_CARD": "BLOCK_CARD"
    }

    # ---------------------------
    # STEP 7: APPLY ACTION LOGIC
    # ---------------------------
    if intent_type in intent_to_action:
        result["actions"][0]["action_type"] = intent_to_action[intent_type]
        result["actions"][0]["priority"] = "MEDIUM"
        result["actions"][0]["blocking"] = True
    else:
        result["actions"][0]["action_type"] = "FETCH_BALANCE"
        result["actions"][0]["priority"] = "LOW"
        result["actions"][0]["blocking"] = False

    # ---------------------------
    # STEP 8: ADD META
    # ---------------------------
    if "meta" not in result:
        result["meta"] = {}

    result["meta"]["source"] = source

    return result