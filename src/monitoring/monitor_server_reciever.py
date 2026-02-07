import socketserver
from colorama import Fore, Style
from src.server_config import COMMUNICATION_PORT

label = 0
attack_type = "normal"


# ControlHandler is the listener that will write global variables like label and attack type so the monitoring script labels the data correctly.
class ControlHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global label
        global attack_type

        while True:
            data = self.request.recv(1024).decode().strip()
            if not data:
                break

            if data.startswith("START:"):
                label = 1
                attack_type = data.split(":", 1)[1]

                print(
                    Fore.RED
                    + Style.BRIGHT
                    + f"[LABEL] START → label={label}, attack={attack_type}"
                    + Style.RESET_ALL
                )

            elif data == "STOP":
                label = 0
                attack_type = "normal"
                print(
                    Fore.GREEN
                    + Style.BRIGHT
                    + f"[LABEL] Received STOP → label = {label} , attack={attack_type}"
                    + Style.RESET_ALL
                )


def start_control_server():
    with socketserver.ThreadingTCPServer(
        ("0.0.0.0", COMMUNICATION_PORT), ControlHandler
    ) as server:
        server.allow_reuse_address = True
        print(f"Control Server listening on 0.0.0.0:{COMMUNICATION_PORT}")
        server.serve_forever()
