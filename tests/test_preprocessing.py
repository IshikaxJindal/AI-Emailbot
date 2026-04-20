from src.preprocessing.email_preprocessor import preprocess_email

sample_email = """
test@outlook.com

Hi team,

Please send my bank statement for the last 3 months.
I'll be highly obliged.

Regards,
xws
"""

result = preprocess_email(sample_email)

print(result)