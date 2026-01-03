from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

from backend_python.main import save_result
from . import marker_logic
from .marker_logic import (
    process_marker,
    update_alive,
    get_time_taken
)


def on_object(addr, *args):
    if not args:
        return

    msg_type = args[0]

    # ---- SET MESSAGE ----
    if msg_type == "set":
        # TUIO set format:
        # set session_id class_id x y angle ...
        if len(args) < 3:
            return

        marker_id = args[2]

        answer, confirmed = process_marker(marker_id)

        # FINAL ANSWER → ONLY ONCE
        if confirmed and answer and not marker_logic.final_answer_sent:
            time_taken = get_time_taken()

            # TEMP values (UI will replace later)
            student_id = 1
            question_id = 1
            correct_option = "A"

            is_correct = save_result(
                student_id=student_id,
                question_id=question_id,
                selected_option=answer,
                correct_option=correct_option,
                time_taken=time_taken
            )

            print(f"FINAL ANSWER: {answer}")
            print(f"Time taken: {time_taken} seconds")
            print(f"Correct: {is_correct}")

            marker_logic.final_answer_sent = True

    # ---- ALIVE MESSAGE ----
    elif msg_type == "alive":
        alive_ids = args[1:]
        update_alive(alive_ids)


dispatcher = Dispatcher()
dispatcher.map("/tuio/2Dobj", on_object)

server = BlockingOSCUDPServer(("127.0.0.1", 3333), dispatcher)
print("Listening for TUIO markers...")
server.serve_forever()
