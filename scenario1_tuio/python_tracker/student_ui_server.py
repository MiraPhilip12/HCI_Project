# student_ui_server.py
import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 51000

clients = []
lock = threading.Lock()

def broadcast(message: dict):
    data = (json.dumps(message) + "\n").encode()
    with lock:
        for c in clients[:]:
            try:
                c.sendall(data)
            except:
                clients.remove(c)

def handle_client(conn):
    with lock:
        clients.append(conn)
    try:
        while True:
            if not conn.recv(1):
                break
    finally:
        with lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[UI SERVER] Listening on {HOST}:{PORT}")

    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    start_server()
