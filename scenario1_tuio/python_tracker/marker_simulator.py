import socket
import time

HOST = "127.0.0.1"
PORT = 5006

print("[SIMULATOR] Marker simulator started")

while True:
    # -------------------------------
    # Connect for ONE session
    # -------------------------------
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print("[SIMULATOR] Waiting for student...")
        sock.connect((HOST, PORT))
        print("[SIMULATOR] Connected")
    except ConnectionRefusedError:
        print("[SIMULATOR] Student not ready, retrying...")
        time.sleep(1)
        continue

    print("""
Marker Simulator
----------------
0 → Answer A
1 → Answer B
2 → Answer C
3 → Confirm
q → Quit simulator
""")

    # -------------------------------
    # Session loop
    # -------------------------------
    while True:
        try:
            key = input("Enter marker ID: ").strip()
        except KeyboardInterrupt:
            print("\n[SIMULATOR] Exiting")
            sock.close()
            exit()

        if key.lower() == "q":
            print("[SIMULATOR] Quit requested")
            sock.close()
            exit()

        if key not in ["0", "1", "2", "3"]:
            print("[SIMULATOR] Invalid marker")
            continue

        try:
            sock.sendall(f"MARKER:{key}".encode())
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            print("[SIMULATOR] Session ended by student")
            sock.close()
            break   # ← EXIT SESSION, RECONNECT FOR NEXT ONE

    # Small delay before reconnect
    time.sleep(0.5)
