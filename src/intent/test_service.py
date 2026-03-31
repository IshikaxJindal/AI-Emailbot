from src.intent.service import process_intent

event_id = "123"

clean_text = "Please send my bank statement for last 3 months"

entities = {
    "duration": "last 3 months"
}

result = process_intent(event_id, clean_text, entities)

print(result)