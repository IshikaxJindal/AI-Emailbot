from src.intent.classifier import classify_rule_based

text = "Check my remaining account balance"

result = classify_rule_based(text)

print(result)