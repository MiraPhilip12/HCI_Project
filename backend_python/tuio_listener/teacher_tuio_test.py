from pythonosc import dispatcher, osc_server
from tuio_to_selection import SelectionState
import socket

state = SelectionState(options_count=3)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 6001))  # Java Teacher UI

def on_object(addr, *args):
    angle = args[4]     # rotation from TUIO
    idx = state.update_angle(angle)
    if idx is not None:
        sock.sendall(f"HIGHLIGHT:{idx}\n".encode())

def on_confirm(addr, *args):
    confirmed = state.confirm()
    if confirmed is not None:
        sock.sendall(f"CONFIRM:{confirmed}\n".encode())

disp = dispatcher.Dispatcher()
disp.map("/tuio/2Dobj", on_object)

server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 3334), disp)
server.serve_forever()
