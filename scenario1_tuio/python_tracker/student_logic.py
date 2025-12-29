import socket
import pandas as pd
import time
from datetime import datetime
import os

# =========================
# PATH RESOLUTION (FIX)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

DATA_FILE = os.path.join(PROJECT_ROOT, "database", "questions.xlsx")
RESULTS_FILE = os.path.join(PROJECT_ROOT, "database", "results", "evaluation_log.csv")

HOST = "127.0.0.1"
PORT = 5007


def normalize(text):
    return str(text).strip().lower()


print("[STUDENT] Service running (multi-session safe)")
print(f"[DEBUG] Loading questions from: {DATA_FILE}")

while True:
    try:
        # =========================
        # Wait for teacher config
        # =========================
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((HOST, PORT))
            server.listen(1)

            print("[STUDENT] Waiting for teacher...")
            conn, _ = server.accept()

            with conn:
                data = conn.recv(1024).decode().strip().splitlines()

        age_group = ""
        subject = ""

        for line in data:
            if line.startswith("AGE:"):
                age_group = normalize(line.replace("AGE:", ""))
            elif line.startswith("SUBJECT:"):
                subject = normalize(line.replace("SUBJECT:", ""))
            elif line == "START":
                pass

        print(f"[CONTEXT] {age_group} | {subject}")

        # =========================
        # Load & filter questions
        # =========================
        if not os.path.exists(DATA_FILE):
            raise FileNotFoundError(DATA_FILE)

        df = pd.read_csv(DATA_FILE)

        df["age_group"] = df["age_group"].apply(normalize)
        df["subject"] = df["subject"].apply(normalize)

        questions = df[
            (df["age_group"] == age_group) &
            (df["subject"] == subject)
        ]

        if questions.empty:
            print("[WARNING] No questions for this context.")
            print("[STUDENT] Returning to teacher.\n")
            continue

        # =========================
        # Start test
        # =========================
        score = 0
        start_time = time.time()

        print("[STUDENT] Waiting for marker input...")

        for _, q in questions.iterrows():
            q_start = time.time()

            print(f"\nQ: {q['question']}")
            print(f"A) {q['a']}  B) {q['b']}  C) {q['c']}")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", 6000))
                s.listen(1)
                conn, _ = s.accept()

                with conn:
                    answer = conn.recv(1024).decode().strip()

            elapsed = round(time.time() - q_start, 2)

            if answer.upper() == q["correct"].upper():
                score += 1
                result = "Correct"
            else:
                result = "Wrong"

            print(f"? {result} ({elapsed}s)")

        # =========================
        # Evaluation
        # =========================
        total_time = round(time.time() - start_time, 2)
        accuracy = round((score / len(questions)) * 100, 2)

        print(f"\nFINAL SCORE: {score}/{len(questions)}")
        print(f"TIME: {total_time}s | ACCURACY: {accuracy}%")

        # =========================
        # Log results
        # =========================
        os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)

        log = {
            "timestamp": datetime.now(),
            "age_group": age_group,
            "subject": subject,
            "score": score,
            "total": len(questions),
            "accuracy": accuracy,
            "time_seconds": total_time
        }

        pd.DataFrame([log]).to_csv(
            RESULTS_FILE,
            mode="a",
            index=False,
            header=not os.path.exists(RESULTS_FILE)
        )

        print("[STUDENT] Ready for next session\n")

    except Exception as e:
        print(f"[ERROR] {e}")
        print("[STUDENT] Recovering...\n")
