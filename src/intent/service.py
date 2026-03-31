from src.intent.classifier import classify_rule_based
from src.intent.formatter import format_output
from src.intent.llm_classifier import classify_with_llm


def process_intent(event_id: str, clean_text: str, entities: dict):

    intents = classify_rule_based(clean_text)
    source = "rule_based"

    if intents[0]["type"] == "UNKNOWN":
        print("Using LLM fallback...")
        intents = classify_with_llm(clean_text)
        source = "llm"

    result = format_output(event_id, intents, entities)

    # 👇 override meta source
    result["meta"]["source"] = source

    return result