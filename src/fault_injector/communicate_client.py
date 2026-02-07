import socket


# The class will be used to be able to communicate between the host machine and the fault injecting machine, when an attack is ongoing or not, to be able to LABEL the data that is being collected.
class CommunicateClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def signal_start(self, attack_type: str) -> None:
        message = f"START:{attack_type}"
        self.sock.sendall(message.encode())

    def signal_stop(self) -> None:
        self.sock.sendall(b"STOP")

    def close(self):
        self.sock.close()
