import socket


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
