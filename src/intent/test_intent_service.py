from src.intent.service import process_intent

event_id = "123"

# Test Case 1 (Rule-based)
clean_text = "Send my bank statement for last 3 months"

entities = {
    "duration": "last 3 months"
}

result = process_intent(event_id, clean_text, entities)

print("RESULT 1:", result)


# Test Case 2 (LLM fallback)
clean_text = "Can you give me my account summary?"

entities = {}

result = process_intent(event_id, clean_text, entities)

print("RESULT 2:", result)