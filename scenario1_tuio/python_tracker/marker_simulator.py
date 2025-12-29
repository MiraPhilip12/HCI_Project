import socket
import time

HOST = "127.0.0.1"
PORT = 5006

print("[SIMULATOR] Ready")

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        print("[SIMULATOR] Connected to student")
    except ConnectionRefusedError:
        print("[SIMULATOR] Student not ready, retrying...")
        time.sleep(1)
        continue

    while True:
        key = input("Enter marker ID (q to quit): ")

        if key.lower() == "q":
            sock.close()
            break

        if key in ["0", "1", "2", "3"]:
            try:
                sock.sendall(f"MARKER:{key}".encode())
            except (BrokenPipeError, ConnectionResetError):
                print("[SIMULATOR] Session ended")
                sock.close()
                break
