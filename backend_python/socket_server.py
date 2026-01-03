import socket
import time

HOST = "127.0.0.1"
PORT = 5005

questions = [
    ("QUESTION: 2 + 3 = ? | A:4 B:5 C:6", "CORRECT"),
    ("QUESTION: 5 - 2 = ? | A:1 B:3 C:4", "CORRECT"),
    ("QUESTION: 3 * 2 = ? | A:5 B:6 C:7", "INCORRECT")
]

def run_student_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print("Student Server listening on port", PORT)

    while True:
        conn, addr = server.accept()
        print("Student connected:", addr)

        # WAIT state (session controlled externally)
        conn.sendall("SESSION_START\n".encode())

        score = 0
        for q, result in questions:
            conn.sendall((q + "\n").encode())
            time.sleep(0.5)
            conn.sendall(("RESULT: " + result + "\n").encode())

            if result == "CORRECT":
                score += 1

            time.sleep(1.5)

        conn.sendall(f"FINAL_SCORE: {score} / {len(questions)}\n".encode())
        conn.close()

if __name__ == "__main__":
    run_student_server()
