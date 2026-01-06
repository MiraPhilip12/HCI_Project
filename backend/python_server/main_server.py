# ==============================
# main_server.py (THREADING MODE)
# ==============================

import os
import sys
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import pandas as pd
from flask import send_from_directory
from tuio_handler import start_tuio_listener


# ------------------------------
# Flask Setup (NO EVENTLET)
# ------------------------------
app = Flask(__name__)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

# ------------------------------
# Excel Path
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "database", "questions.xlsx")
)

print("Loading Excel from:", DB_PATH)

# ------------------------------
# Load Excel
# ------------------------------
try:
    df = pd.read_excel(DB_PATH)
    print("Database loaded successfully")
except Exception as e:
    print("Failed to load Excel:", e)
    sys.exit(1)

REQUIRED_COLUMNS = {
    "Age_Group",
    "Subject",
    "Question",
    "Correct_Answer",
    "Options"
}

if not REQUIRED_COLUMNS.issubset(df.columns):
    print("Excel schema invalid.")
    print("Required:", REQUIRED_COLUMNS)
    print("Found:", set(df.columns))
    sys.exit(1)

df["Age_Group"] = df["Age_Group"].astype(int)
df["Subject"] = df["Subject"].astype(int)

# ------------------------------
# REST API
# ------------------------------
@app.route("/api/age_groups")
def get_age_groups():
    return jsonify(sorted(df["Age_Group"].unique().tolist()))

@app.route("/api/subjects")
def get_subjects():
    return jsonify(sorted(df["Subject"].unique().tolist()))

@app.route("/api/question_count")
def get_question_count():
    age = request.args.get("age", type=int)
    subject = request.args.get("subject", type=int)

    count = len(df[
        (df["Age_Group"] == age) &
        (df["Subject"] == subject)
    ])

    return jsonify({"count": count})

# ------------------------------
# SOCKET EVENTS
# ------------------------------
@socketio.on("teacher_start_session")
def start_session(data):
    age = int(data["age"])
    subject = int(data["subject"])

    print(f"[TEACHER] Start session → Age={age}, Subject={subject}")

    filtered = df[
        (df["Age_Group"] == age) &
        (df["Subject"] == subject)
    ]

    if filtered.empty:
        emit("error", {"message": "No questions found"})
        return

    questions = [
        {
            "question": row["Question"],
            "options": str(row["Options"]).split("|"),
            "correct_answer": row["Correct_Answer"]
        }
        for _, row in filtered.iterrows()
    ]

    emit(
        "test_started",
        {
            "questions": questions,
            "current_index": 0,
            "first_question": questions[0]
        },
        broadcast=True
    )

    print("[SERVER] test_started broadcast sent")

FRONTEND_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..", "frontend")
)

@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "js"), filename)

@app.route("/")
def teacher_ui():
    return send_from_directory(FRONTEND_DIR, "teacher.html")

@app.route("/student")
def student_ui():
    return send_from_directory(FRONTEND_DIR, "student.html")

# ------------------------------
# Server Start
# ------------------------------
if __name__ == "__main__":
    print(">>> Starting TUIO listener NOW")
    start_tuio_listener(socketio)
    print("Server running at http://127.0.0.1:5000")
    socketio.run(app, host="0.0.0.0", port=5000)
