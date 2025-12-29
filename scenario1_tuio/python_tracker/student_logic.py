import pandas as pd
import socket
import csv
import os
import time
from datetime import datetime

# ===============================
# CONFIG
# ===============================
CTRL_PORT = 5007
MARKER_PORT = 5006
RESULTS_FILE = "../../database/results/session_results.csv"

# ===============================
# PREPARE RESULTS FILE
# ===============================
os.makedirs("../../database/results", exist_ok=True)

if not os.path.isfile(RESULTS_FILE):
    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            "timestamp",
            "age_group",
            "subject",
            "question",
            "selected_answer",
            "correct_answer",
            "is_correct",
            "time_taken_seconds"
        ])

# ===============================
# LOAD QUESTIONS
# ===============================
df = pd.read_excel("../../database/questions.xlsx")
df.columns = df.columns.str.strip().str.lower()

print("[STUDENT] Service running (multi-session safe)")

# ===============================
# CREATE SERVERS ONCE
# ===============================
ctrl_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ctrl_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ctrl_server.bind(("127.0.0.1", CTRL_PORT))
ctrl_server.listen(1)

marker_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
marker_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
marker_server.bind(("127.0.0.1", MARKER_PORT))
marker_server.listen(1)

# ===============================
# MAIN LOOP
# ===============================
while True:
    # ---------- Teacher ----------
    print("\n[STUDENT] Waiting for teacher...")
    ctrl_conn, _ = ctrl_server.accept()

    AGE_GROUP = None
    SUBJECT = None

    while True:
        msg = ctrl_conn.recv(1024).decode().strip()
        if msg.startswith("AGE:"):
            AGE_GROUP = msg.split(":")[1]
        elif msg.startswith("SUBJECT:"):
            SUBJECT = msg.split(":")[1]
        elif msg == "START":
            break

    ctrl_conn.close()
    print(f"[CONTEXT] {AGE_GROUP} | {SUBJECT}")

    # ---------- Load Questions ----------
    questions = df[
        (df["age_group"] == AGE_GROUP) &
        (df["subject"] == SUBJECT)
    ].head(3)

    if questions.empty:
        print("[WARNING] No questions for this context.")
        print("[STUDENT] Returning to teacher.\n")
        continue  # ← CRITICAL FIX

    # ---------- Marker ----------
    print("[STUDENT] Waiting for marker input...")
    marker_conn, _ = marker_server.accept()

    score = 0
    session_start = time.time()

    with open(RESULTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        for _, row in questions.iterrows():
            print(f"\nQ: {row['question']}")
            print(f"A) {row['a']}  B) {row['b']}  C) {row['c']}")

            q_start = time.time()
            current = None

            while True:
                try:
                    msg = marker_conn.recv(1024).decode().strip()
                except ConnectionResetError:
                    print("[MARKER] Disconnected. Ending session.")
                    break

                if not msg.startswith("MARKER:"):
                    continue

                mid = int(msg.split(":")[1])

                if mid == 0:
                    current = "A"
                    print("Selected A")
                elif mid == 1:
                    current = "B"
                    print("Selected B")
                elif mid == 2:
                    current = "C"
                    print("Selected C")
                elif mid == 3 and current:
                    duration = round(time.time() - q_start, 2)
                    correct = current == row["correct"]
                    score += correct

                    print(f"{'✔' if correct else '✖'} ({duration}s)")

                    writer.writerow([
                        datetime.now().isoformat(),
                        AGE_GROUP,
                        SUBJECT,
                        row["question"],
                        current,
                        row["correct"],
                        correct,
                        duration
                    ])
                    break

    marker_conn.close()

    total_time = round(time.time() - session_start, 2)
    accuracy = round((score / len(questions)) * 100, 2)

    print(f"\nFINAL SCORE: {score}/{len(questions)}")
    print(f"TIME: {total_time}s | ACCURACY: {accuracy}%")
    print("[STUDENT] Ready for next session")
