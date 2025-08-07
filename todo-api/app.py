from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime
import json
import os

# Create sessions folder if it doesn't exist
SESSION_DIR = "sessions"
if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)

SESSION_FILE = os.path.join(SESSION_DIR, "sessions.json")
session_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app = Flask(__name__)
CORS(app)

# Helper functions
def load_sessions():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"todos": []}
    return {"todos": []}

def save_sessions(data):
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sessions', methods=['GET'])
def list_sessions():
    sessions = load_sessions()
    return jsonify([list(s.keys())[0] for s in sessions["todos"]])

@app.route("/todos", methods=["GET"])
def get_all_todos():
    sessions = load_sessions()
    return jsonify(sessions), 200
    
@app.route("/todos/<session_time>/<int:todo_id>", methods=["PUT"])
def update_todo(session_time, todo_id):
    data = request.get_json()
    sessions = load_sessions()

    for session_group in sessions["todos"]:
        if session_time in session_group:
            for todo in session_group[session_time]:
                if todo["id"] == todo_id:
                    todo["task"] = data.get("task", todo["task"])
                    todo["completed"] = data.get("completed", todo["completed"])
                    save_sessions(sessions)
                    return jsonify(todo), 200

    return jsonify({"error": "Todo not found"}), 404

@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    sessions = load_sessions()

    new_todo = {
        "id": 1,
        "task": data["task"],
        "completed": False
    }

    session_exists = False
    for session_group in sessions["todos"]:
        if session_timestamp in session_group:
            new_todo["id"] = len(session_group[session_timestamp]) + 1
            session_group[session_timestamp].append(new_todo)
            session_exists = True
            break

    if not session_exists:
        sessions["todos"].append({session_timestamp: [new_todo]})

    save_sessions(sessions)
    return jsonify(new_todo), 201

@app.route("/todos/<session_time>", methods=["POST"])
def create_todo_in_session(session_time):
    data = request.get_json()
    sessions = load_sessions()

    new_todo = {
        "id": 1,
        "task": data["task"],
        "completed": False
    }

    for session_group in sessions["todos"]:
        if session_time in session_group:
            new_todo["id"] = len(session_group[session_time]) + 1
            session_group[session_time].append(new_todo)
            save_sessions(sessions)
            return jsonify(new_todo), 201

    # If session not found, create new session
    sessions["todos"].append({session_time: [new_todo]})
    save_sessions(sessions)
    return jsonify(new_todo), 201

if __name__ == "__main__":
    app.run(debug=True)

