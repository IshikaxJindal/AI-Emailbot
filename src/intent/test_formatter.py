from src.intent.classifier import classify_rule_based
from src.intent.formatter import format_output

event_id = "123"

text = "Please send my bank statement for last 3 months"

entities = {
    "duration": "last 3 months"
}

intents = classify_rule_based(text)

result = format_output(event_id, intents, entities)

print(result)