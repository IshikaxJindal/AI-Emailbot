def generate_response(intent, data):
    
    if intent == "BALANCE_QUERY":
        return f"Dear Customer,\n\nYour current balance is {data}.\n\nThank you."
    
    elif intent == "LAST_TRANSACTION":
        return f"Dear Customer,\n\nYour last transaction was: {data}.\n\nThank you."
    
    elif intent == "STATEMENT_QUERY":
        return f"Dear Customer,\n\nHere is your account statement:\n{data}\n\nThank you."
    
    return "Dear Customer,\n\nWe could not understand your request.\n\nThank you."


if __name__ == "__main__":
    print(generate_response("BALANCE_QUERY", 50000))