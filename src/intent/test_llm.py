from src.intent.llm_classifier import classify_with_llm

text = "Can you provide my account summary?"

result = classify_with_llm(text)

print(result)