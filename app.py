from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os
import uuid

app = Flask(__name__)
CORS(app)

HISTORY_FILE = "history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


@app.route('/history', methods=['POST'])
def add_entry():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    story = data.get("story", "").strip()
    palette = data.get("palette", None)

    if not story:
        return jsonify({"error": "Missing or empty 'story' field"}), 400

    if palette is None:
        return jsonify({"error": "Missing 'palette' field"}), 400

    if not isinstance(palette, list):
        return jsonify({"error": "'palette' must be an array of hex codes"}), 400

    entry = {
        "id": str(uuid.uuid4()),
        "story": story,
        "palette": palette,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    history = load_history()
    history.append(entry)
    save_history(history)

    return jsonify({"id": entry["id"], "timestamp": entry["timestamp"]}), 201


@app.route('/history', methods=['GET'])
def get_history():
    history = load_history()
    return jsonify(history), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(port=5301, debug=True)
