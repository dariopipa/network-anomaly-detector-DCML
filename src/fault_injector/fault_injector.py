import socket
import threading
import time
import random


class FaultInjector:
    """
    Fault Injector class will be used to create different types of injection
    in the network for both TCP and UDP connections.
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    # TCP Flood
    def tcp_connection_flood(self) -> None:
        duration = random.randint(30, 90)  # 30-90 seconds
        start_time = time.time()
        connections = 0

        while time.time() - start_time < duration:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(2)
                    sock.connect((self.host, self.port))
                    time.sleep(random.uniform(0.01, 0.05))
                    connections += 1
            except Exception as e:
                time.sleep(0.1)

    # Bandwidth Exhaustion
    def tcp_bandwidth_exhaustion(self) -> None:
        duration = random.randint(30, 90)
        start_time = time.time()
        data = random.randbytes(10485760)  # 10MB

        def send_data():
            while time.time() - start_time < duration:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.connect((self.host, self.port))
                        sock.sendall(data)
                except Exception:
                    time.sleep(0.1)

        threads = [threading.Thread(target=send_data) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    # UDP Flood
    def udp_flood(self):
        duration = random.randint(30, 90)
        data = random.randbytes(65507)
        start_time = time.time()

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            while time.time() - start_time < duration:
                try:
                    sock.sendto(data, (self.host, self.port))
                except Exception as e:
                    time.sleep(0.1)

    # Port Scanning Attack
    def port_scan_simulation(self):
        duration = random.randint(30, 90)
        start_time = time.time()
        scan_ports = random.sample(range(1, 65536), 2000)

        for port in scan_ports:
            if time.time() - start_time >= duration:
                break

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.05)
                    sock.connect((self.host, port))
            except Exception as e:
                pass

    # Large file download
    def bulk_download(self):
        duration = random.randint(30, 90)
        data = random.randbytes(10485760)
        start_time = time.time()

        while time.time() - start_time < duration:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(5)
                    sock.connect((self.host, self.port))

                    while time.time() - start_time < duration:
                        sock.sendall(data)
                        time.sleep(random.uniform(0.01, 0.05))
            except Exception as e:
                time.sleep(0.1)
