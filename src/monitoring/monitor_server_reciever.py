import socketserver
import sys
from pathlib import Path
from colorama import Fore, Style

sys.path.append(str(Path(__file__).parent.parent))
from server_config import COMMUNICATION_PORT

label = 0
attack_type = ""


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
                print(
                    Fore.GREEN
                    + Style.BRIGHT
                    + f"[LABEL] Received STOP → label = {label}"
                    + Style.RESET_ALL
                )


def start_control_server():
    with socketserver.ThreadingTCPServer(
        ("0.0.0.0", COMMUNICATION_PORT), ControlHandler
    ) as server:
        server.allow_reuse_address = True
        print(f"Control Server listening on 0.0.0.0:{COMMUNICATION_PORT}")
        server.serve_forever()
