import requests

BASE_URL = "http://localhost:5301"

def run_test(name, method, endpoint, payload=None, expected_status=None):
    print(f"\n--- {name} ---")
    try:
        if method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
        else:
            response = requests.get(f"{BASE_URL}{endpoint}")

        print(f"Status:   {response.status_code}")
        print(f"Response: {response.json()}")

        if expected_status and response.status_code == expected_status:
            print("PASS")
        elif expected_status:
            print(f"FAIL (expected {expected_status})")
    except Exception as e:
        print(f"ERROR: {e}")


# Test 1: Save a valid story entry
run_test(
    name="Test 1: Save valid story entry",
    method="POST",
    endpoint="/history",
    payload={
        "story": "A mysterious figure wandered the gothic halls...",
        "palette": ["#1A1A2E", "#E94560", "#0F3460"]
    },
    expected_status=201
)

# Test 2: Save another valid entry
run_test(
    name="Test 2: Save second story entry",
    method="POST",
    endpoint="/history",
    payload={
        "story": "The whimsical forest glowed with pastel light...",
        "palette": ["#FFB3C6", "#CDB4DB", "#A2D2FF"]
    },
    expected_status=201
)

# Test 3: Retrieve all history
run_test(
    name="Test 3: Retrieve all history",
    method="GET",
    endpoint="/history",
    expected_status=200
)

# Test 4: Missing story field
run_test(
    name="Test 4: Missing 'story' field",
    method="POST",
    endpoint="/history",
    payload={"palette": ["#FF0000"]},
    expected_status=400
)

# Test 5: Missing palette field
run_test(
    name="Test 5: Missing 'palette' field",
    method="POST",
    endpoint="/history",
    payload={"story": "A story with no palette"},
    expected_status=400
)

# Test 6: Health check
run_test(
    name="Test 6: Health check",
    method="GET",
    endpoint="/health",
    expected_status=200
)
