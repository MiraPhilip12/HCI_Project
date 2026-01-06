from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

def dump(address, *args):
    print(address, args)

dispatcher = Dispatcher()
dispatcher.set_default_handler(dump)

server = BlockingOSCUDPServer(("0.0.0.0", 3334), dispatcher)

print("Listening for ANY OSC messages on port 3334...")
server.serve_forever()
