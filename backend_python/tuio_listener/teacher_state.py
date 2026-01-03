import time
import math
import socket


# -------------------------
# MENUS
# -------------------------
MENU_AGE = ["5-9", "10-14", "15-20"]
MENU_SUBJECT = ["Math", "Science", "English"]
MENU_ACTION = ["Start Test", "Back", "Reset"]

MENU_MARKER_ID = 50
CONFIRM_MARKER_ID = 99

# -------------------------
# STATE
# -------------------------
current_menu = "AGE"
current_index = 0

selected_age = None
selected_subject = None

# -------------------------
# GLOBAL DEBOUNCE CONFIG
# -------------------------
ROTATION_DEBOUNCE = 0.5      # seconds
CONFIRM_DEBOUNCE = 1.0       # seconds

last_rotation_time = 0
last_confirm_time = 0
last_index = None


# -------------------------
# HELPERS
# -------------------------
def angle_to_index(angle, menu_length):
    sector = (2 * math.pi) / menu_length
    return int(angle // sector) % menu_length


def get_menu():
    if current_menu == "AGE":
        return MENU_AGE
    elif current_menu == "SUBJECT":
        return MENU_SUBJECT
    return MENU_ACTION


# -------------------------
# MENU ROTATION (DEBOUNCED)
# -------------------------
def handle_menu(marker_id, angle):
    global current_index, last_index, last_rotation_time

    if marker_id != MENU_MARKER_ID:
        return

    now = time.time()
    menu = get_menu()
    index = angle_to_index(angle, len(menu))

    # --- DEBOUNCE ---
    if index == last_index:
        return
    if now - last_rotation_time < ROTATION_DEBOUNCE:
        return

    last_index = index
    last_rotation_time = now
    current_index = index

    print(f"{current_menu} OPTION:", menu[current_index])


# -------------------------
# CONFIRM ACTION (DEBOUNCED)
# -------------------------
def confirm_selection():
    global current_menu, selected_age, selected_subject
    global last_confirm_time, last_index

    now = time.time()

    # --- DEBOUNCE ---
    if now - last_confirm_time < CONFIRM_DEBOUNCE:
        return

    last_confirm_time = now
    last_index = None  # reset rotation debounce

    if current_menu == "AGE":
        selected_age = MENU_AGE[current_index]
        print("AGE CONFIRMED:", selected_age)
        current_menu = "SUBJECT"

    elif current_menu == "SUBJECT":
        selected_subject = MENU_SUBJECT[current_index]
        print("SUBJECT CONFIRMED:", selected_subject)
        current_menu = "ACTION"

    elif current_menu == "ACTION":
        action = MENU_ACTION[current_index]
        print("ACTION CONFIRMED:", action)

        if action == "Start Test":
            print(f"START TEST → Age: {selected_age}, Subject: {selected_subject}")
            send_teacher_command(f"START_TEST {selected_age} {selected_subject}")


        elif action == "Reset":
            send_teacher_command("RESET_TEST")
            reset_teacher_state()


        elif action == "Back":
            current_menu = "AGE"
            print("BACK TO AGE MENU")



def send_teacher_command(command):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 6000))
        s.sendall(command.encode())
        s.close()
    except Exception as e:
        print("Controller connection error:", e)


# -------------------------
# RESET (SAFE)
# -------------------------
def reset_teacher_state():
    global current_menu, selected_age, selected_subject
    global last_index, last_confirm_time

    current_menu = "AGE"
    selected_age = None
    selected_subject = None
    last_index = None
    last_confirm_time = 0

    print("TEACHER STATE RESET")
