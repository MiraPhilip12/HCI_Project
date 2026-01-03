import time

ANSWER_MARKERS = {
    1: "A",
    2: "B",
    3: "C"
}

CONFIRM_MARKER_ID = 99

# STATE
current_answer = None
confirmed = False
locked = False
final_answer_sent = False
start_time = None
alive_markers = set()


def reset():
    global current_answer, confirmed, locked, final_answer_sent, start_time
    current_answer = None
    confirmed = False
    locked = False
    final_answer_sent = False
    start_time = None
    print("System reset. Ready for next question.")


def update_alive(marker_ids):
    global alive_markers

    # Reset ONLY when confirm marker is removed
    if CONFIRM_MARKER_ID in alive_markers and CONFIRM_MARKER_ID not in marker_ids:
        reset()

    alive_markers = set(marker_ids)


def process_marker(marker_id):
    global current_answer, confirmed, locked, start_time

    # Ignore everything if locked
    if locked:
        return current_answer, confirmed

    # Answer selection
    if marker_id in ANSWER_MARKERS and not confirmed:
        if start_time is None:
            start_time = time.time()

        if current_answer != ANSWER_MARKERS[marker_id]:
            current_answer = ANSWER_MARKERS[marker_id]
            print(f"Answer selected: {current_answer}")

    # Confirmation (ONE TIME)
    elif (
        marker_id == CONFIRM_MARKER_ID
        and current_answer is not None
        and not confirmed
    ):
        confirmed = True
        locked = True
        print("Answer confirmed!")

    return current_answer, confirmed


def get_time_taken():
    if start_time is None:
        return 0.0
    return round(time.time() - start_time, 2)
