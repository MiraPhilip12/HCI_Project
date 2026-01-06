# tuio_handler.py
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
import threading

print(">>> tuio_handler.py LOADED <<<")

def start_tuio_listener(socketio):
    dispatcher = Dispatcher()

    # Catch EVERYTHING (including bundles)
    dispatcher.set_default_handler(handle_any, socketio)

    server = ThreadingOSCUDPServer(
        ("0.0.0.0", 3334),
        dispatcher
    )

    print("TUIO OSC listener active on UDP port 3334")

    threading.Thread(
        target=server.serve_forever,
        daemon=True
    ).start()


def handle_any(address, *args):
    socketio = args[-1]
    data = args[:-1]

    # Only care about TUIO object updates
    if address != "/tuio/2Dobj":
        return

    if not data or data[0] != "set":
        return

    # Official TUIO 2Dobj format
    _, session_id, symbol_id, x, y, angle, *_ = data

    print(
        f"Marker {symbol_id} "
        f"(session {session_id}) "
        f"at ({x:.3f}, {y:.3f})"
    )

    socketio.emit(
        "tuio_marker",
        {
            "marker_id": int(symbol_id),
            "session_id": int(session_id),
            "x": float(x),
            "y": float(y),
            "angle": float(angle)
        },
        broadcast=True
    )
