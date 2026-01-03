import socket
import threading

HOST = "127.0.0.1"
PORT = 6000

current_context = {
    "age": None,
    "subject": None
}

def handle_client(conn):
    global current_context

    data = conn.recv(1024).decode().strip()
    print("TEACHER COMMAND:", data)

    if data.startswith("START_TEST"):
        _, age, subject = data.split()
        current_context["age"] = age
        current_context["subject"] = subject
        print(f"TEST STARTED → Age: {age}, Subject: {subject}")

    elif data == "RESET_TEST":
        current_context["age"] = None
        current_context["subject"] = None
        print("TEST RESET")

    conn.close()


def start_controller():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print("Test Controller listening on port", PORT)

    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
