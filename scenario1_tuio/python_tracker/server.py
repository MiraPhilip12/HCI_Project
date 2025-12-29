import socket
import threading

HOST = "127.0.0.1"
PORT = 5005

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"[RECEIVED] {data.decode()}")
        conn.sendall(b"ACK\n")

    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr)
        )
        thread.start()

if __name__ == "__main__":
    start_server()
