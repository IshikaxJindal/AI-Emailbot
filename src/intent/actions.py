"""
This file maps detected intents → system actions (action hints)

NOTE:
- These are NOT executed here
- These are passed to the control/action router layer
"""

INTENT_TO_ACTION = {
    "BANK_STATEMENT_REQUEST": "FETCH_BANK_STATEMENT",
    "BALANCE_QUERY": "FETCH_BALANCE",
    "UNKNOWN": None
}