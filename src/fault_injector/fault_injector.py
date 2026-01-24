import socket
import time
import random

"""
Fault Injector class will be used to create different types of injection 
in the network for both TCP and UDP connections.
"""


class FaultInjector:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    # TCP Flood
    def tcp_connection_flood(self) -> None:
        for _ in range(random.randint(200, 800)):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))
                time.sleep(random.uniform(0.01, 0.05))

    # Bandwidth Exhaustion
    def tcp_bandwidth_exhaustion(self) -> None:
        data = random.randbytes(10485760)  # 10 mb of data
        for _ in range(100):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))
                for _ in range(random.randint(2, 5)):
                    # this will send 10 mb of data and then sleep and do it again.
                    sock.sendall(data)
                    time.sleep(random.uniform(0.01, 0.05))

    # UDP Flood
    def udp_flood(self):
        data = random.randbytes(512)
        for _ in range(random.randint(1000, 5000)):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.sendto(data, (self.host, self.port))
                time.sleep(random.uniform(0.01, 0.05))

    # Port Scanning Attack
    def port_scan_simulation(self):
        scan_ports = range(1, 1025)  # common predefined ports
        for port in scan_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((self.host, port))
                    time.sleep(random.uniform(0.01, 0.05))
            except:
                pass

            time.sleep(random.uniform(0.01, 0.05))

    # Large file download
    def bulk_download(self):
        data = random.randbytes(104857600)  # 100 mb of data
        for _ in range(1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # connect to server
                sock.connect((self.host, self.port))
                # send 100 mb of data * the random number generated from 5 to 15,meaning it will be min 500mb and maximum 1.5 gb of data being sent.
                for _ in range(random.randint(5, 15)):
                    sock.sendall(data)
