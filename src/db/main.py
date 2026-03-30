from db.operations import *

# Step 1: Create user
user_id = create_user("Aaradhya", "test@gmail.com")

# Step 2: Add banking context
add_banking_context(user_id, "Savings", 50000, "Paid Netflix ₹499")

# Step 3: Store email
email_id = store_email(
    user_id,
    "Balance Check",
    "What is my current balance?",
    "balance_query"
)

# Step 4: Store response
store_response(
    email_id,
    "Your balance is ₹50,000.",
    "RULE",
    0.99
)

print(" Full pipeline working")
