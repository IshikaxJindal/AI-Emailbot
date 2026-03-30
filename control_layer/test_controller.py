# test_controller.py

from controller import process_request


# ✅ Test 1: Valid balance request
data1 = {
    "event_id": "1",
    "intents": [{"type": "BALANCE_QUERY", "confidence": 0.95}],
    "entities": {},
    "actions": [{"action_type": "FETCH_BALANCE", "priority": "HIGH", "blocking": True}],
    "meta": {}
}


data2 = {
    'event_id': '2',
    'intents': [{'type': 'BALANCE_QUERY', 'confidence': 0.4}],
    'entities': {},
    'actions': [{'action_type': 'FETCH_BALANCE', 'priority': 'HIGH', 'blocking': True}],
    'meta': {'source': 'rule_based', 'processed_at': '2026-03-26T12:21:15'}
}

data3 = {
    "event_id": "3",
    "intents": [{"type": "BALANCE_QUERY", "confidence": 0.7}],
    "entities": {},
    "actions": [{"action_type": "FETCH_BALANCE", "priority": "HIGH", "blocking": True}],
    "meta": {}
}

# ⚠️ Test 4: Needs clarification
data4 = {
    "event_id": "4",
    "intents": [{"type": "BALANCE_QUERY", "confidence": 0.9}],
    "entities": {},
    "actions": [{"action_type": "FETCH_BALANCE", "priority": "HIGH", "blocking": False}],
    "meta": {}
}

# No action required
data5 = {
    "event_id": "5",
    "intents": [{"type": "UNKNOWN_INTENT", "confidence": 0.9}],
    "entities": {},
    "actions": [{"action_type": "FETCH_BALANCE", "priority": "HIGH", "blocking": True}],
    "meta": {}
}

print("Test 1:", process_request(data1))
print("Test 2:", process_request(data2))
print("Test 3:", process_request(data3))
print("Test 4:", process_request(data4))
print("Test 5:", process_request(data5))