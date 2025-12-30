import socket
import pandas as pd
import time
from datetime import datetime
import os
import sys
import unicodedata
import socket, json

UI_HOST = "127.0.0.1"
UI_PORT = 51000

ui_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def ui_send(payload: dict):
    ui_sock.sendall((json.dumps(payload) + "\n").encode())


# =========================
# GLOBAL STATE
# =========================
RUNNING = True

def normalize(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("–", "-").replace("—", "-")
    text = text.replace("\u00a0", " ")
    return text.strip().lower()

def shutdown():
    global RUNNING
    RUNNING = False
    print("\n[STUDENT] Shutting down cleanly...")
    sys.exit(0)

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

DATA_FILE = os.path.join(PROJECT_ROOT, "database", "questions.xlsx")
RESULTS_FILE = os.path.join(PROJECT_ROOT, "database", "results", "evaluation_log.csv")

HOST = "127.0.0.1"
PORT = 5007

print("[STUDENT] Service running (multi-session safe)")
print(f"[DEBUG] Loading questions from: {DATA_FILE}")

while RUNNING:
    try:
        # =========================
        # Receive teacher config
        # =========================
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        server.settimeout(1.0)

        print("[STUDENT] Waiting for teacher...")

        while RUNNING:
            try:
                conn, _ = server.accept()
                break
            except socket.timeout:
                continue

        if not RUNNING:
            shutdown()

        with conn:
            raw = conn.recv(1024).decode(errors="ignore")

        server.close()

        print("[DEBUG] Raw teacher message:", raw)

        # =========================
        # ROBUST parsing
        # =========================
        age_group = ""
        subject = ""

        for part in raw.replace("\n", " ").split():
            if part.startswith("AGE:"):
                age_group = normalize(part.replace("AGE:", ""))
            elif part.startswith("SUBJECT:"):
                subject = normalize(part.replace("SUBJECT:", ""))

        print(f"[CONTEXT] {age_group} | {subject}")

        # =========================
        # Load Excel
        # =========================
        df = pd.read_excel(DATA_FILE, engine="openpyxl")

        df["age_group"] = df["age_group"].apply(normalize)
        df["subject"] = df["subject"].apply(normalize)

        print("[DEBUG] Available age groups:", df["age_group"].unique())
        print("[DEBUG] Available subjects:", df["subject"].unique())

        questions = df[
            (df["age_group"] == age_group) &
            (df["subject"] == subject)
        ]

        if questions.empty:
            print("[WARNING] No questions for this context.")
            print("[STUDENT] Returning to teacher.\n")
            continue

        # =========================
        # Run test
        # =========================
        score = 0
        start_time = time.time()

        print("[STUDENT] Waiting for marker input...")

        for _, q in questions.iterrows():
            q_start = time.time()

            print(f"\nQ: {q['question']}")
            print(f"A) {q['A']}  B) {q['B']}  C) {q['C']}")

            marker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            marker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            marker.bind(("127.0.0.1", 6000))
            marker.listen(1)
            marker.settimeout(1.0)

            while RUNNING:
                try:
                    conn, _ = marker.accept()
                    break
                except socket.timeout:
                    continue

            with conn:
                answer = conn.recv(1024).decode(errors="ignore").strip()

            marker.close()

            elapsed = round(time.time() - q_start, 2)

            if answer.upper() == str(q["correct"]).upper():
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

    except KeyboardInterrupt:
        shutdown()

    except Exception as e:
        print(f"[ERROR] {e}")
        print("[STUDENT] Recovering...\n")
