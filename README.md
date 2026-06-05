# Story History Logger Microservice

Saves and retrieves generated story entries paired with their source palettes, persisting data across sessions.

---

## Setup

1. Install dependencies:
```
python -m pip install flask
```

2. Start the microservice:
```
python app.py
```

The service runs on **http://localhost:5301**

---

## Communication Contract

### Endpoint: `POST /history`

Save a story entry with its palette.

**Request format:**

```json
{
  "story": "A mysterious figure wandered the gothic halls...",
  "palette": ["#1A1A2E", "#E94560", "#0F3460"]
}
```

**Example request (Python):**

```python
import requests

response = requests.post(
    "http://localhost:5301/history",
    json={
        "story": "A mysterious figure wandered the gothic halls...",
        "palette": ["#1A1A2E", "#E94560", "#0F3460"]
    }
)
data = response.json()
print(data["id"])        # unique entry ID
print(data["timestamp"]) # UTC timestamp
```

**Success response (HTTP 201):**

```json
{
  "id": "a1b2c3d4-...",
  "timestamp": "2026-05-18T12:00:00Z"
}
```

**Error responses:**

| Scenario | Status | Response |
|---|---|---|
| Missing or empty `story` | 400 | `{"error": "Missing or empty 'story' field"}` |
| Missing `palette` | 400 | `{"error": "Missing 'palette' field"}` |
| `palette` not an array | 400 | `{"error": "'palette' must be an array of hex codes"}` |

---

### Endpoint: `GET /history`

Retrieve all saved story entries.

**Example request (Python):**

```python
import requests

response = requests.get("http://localhost:5301/history")
entries = response.json()
for entry in entries:
    print(entry["id"], entry["story"], entry["palette"], entry["timestamp"])
```

**Success response (HTTP 200):**

```json
[
  {
    "id": "a1b2c3d4-...",
    "story": "A mysterious figure wandered the gothic halls...",
    "palette": ["#1A1A2E", "#E94560", "#0F3460"],
    "timestamp": "2026-05-18T12:00:00Z"
  }
]
```

Returns an empty array `[]` if no entries have been saved.

---

### Endpoint: `GET /health`

Returns `{"status": "ok"}` with HTTP 200 to confirm the service is running.

---

## Notes

- Story entries are persisted in `history.json` in the same directory
- Data survives microservice restarts
- Each entry receives a unique UUID and UTC timestamp automatically
- The microservice runs in its own process and is called via HTTP — no direct function imports