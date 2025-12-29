import socket

# ===============================
# Socket Setup (send context)
# ===============================
HOST = "127.0.0.1"
PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

age_groups = ["5-9", "10-14", "15-20"]
subjects = ["Math", "Science", "English"]

age_index = 0
subject_index = 0

print("""
Teacher Controller
------------------
a / d : rotate age group
j / l : rotate subject
c     : confirm
q     : quit
""")

while True:
    print(f"\nCurrent Age Group: {age_groups[age_index]}")
    print(f"Current Subject  : {subjects[subject_index]}")

    key = input("Command: ").lower()

    if key == "a":
        age_index = (age_index - 1) % len(age_groups)

    elif key == "d":
        age_index = (age_index + 1) % len(age_groups)

    elif key == "j":
        subject_index = (subject_index - 1) % len(subjects)

    elif key == "l":
        subject_index = (subject_index + 1) % len(subjects)

    elif key == "c":
        sock.sendall(f"AGE:{age_groups[age_index]}\n".encode())
        sock.sendall(f"SUBJECT:{subjects[subject_index]}\n".encode())
        sock.sendall(b"START\n")
        print("\n[TEACHER] Test started")
        break

    elif key == "q":
        break

sock.close()
