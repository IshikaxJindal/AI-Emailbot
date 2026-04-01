# test_controller.py

from controller import process_request


# ✅ Test 1: Valid balance request
data1 = {
    'event_id': 't2',
    'intents': [{'type': 'GET_STATEMENT', 'confidence': 0.9}],
    'entities': {'duration': {'value': 4, 'unit': 'months'}},
    'actions': [{'action_type': 'FETCH_BANK_STATEMENT', 'priority': 'HIGH', 'blocking': True}],
    'meta': {'source': 'rule_based', 'processed_at': '2026-04-01T10:01:00'}
}


data2 = {
    'event_id': 't3',
    'intents': [{'type': 'GET_STATEMENT', 'confidence': 0.92}],
    'entities': {},
    'actions': [{'action_type': 'FETCH_BANK_STATEMENT', 'priority': 'HIGH', 'blocking': True}],
    'meta': {'source': 'rule_based', 'processed_at': '2026-04-01T10:02:00'}
}

data3 = {
    'event_id': 't4',
    'intents': [{'type': 'BALANCE_QUERY', 'confidence': 0.7}],
    'entities': {},
    'actions': [{'action_type': 'FETCH_BALANCE', 'priority': 'HIGH', 'blocking': True}],
    'meta': {}
}

# ⚠️ Test 4: Needs clarification
data4 = {
   'event_id': 't5',
   'intents': [{'type': 'GET_BALANCE', 'confidence': 0.4}],
   'entities': {},
   'actions': [{'action_type': 'FETCH_BALANCE', 'priority': 'HIGH', 'blocking': True}],
   'meta': {'source': 'rule_based', 'processed_at': '2026-04-01T10:04:00'}
}

# No action required
data5 = {
   'event_id': 't6',
   'intents': [{'type': 'GET_BALANCE', 'confidence': 0.7}],
   'entities': {},
   'actions': [{'action_type': 'FETCH_BALANCE', 'priority': 'HIGH', 'blocking': True}],
   'meta': {'source': 'rule_based', 'processed_at': '2026-04-01T10:05:00'}
}

print("Test 1:", process_request(data1))
print("Test 2:", process_request(data2))
print("Test 3:", process_request(data3))
print("Test 4:", process_request(data4))
print("Test 5:", process_request(data5))