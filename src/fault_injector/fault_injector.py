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

    # TCP Flood,hold connections open
    def tcp_connection_flood(self) -> None:
        duration = random.randint(60, 120)
        start_time = time.time()
        held_sockets = []

        def flood_worker():
            while time.time() - start_time < duration:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((self.host, self.port))
                    held_sockets.append(sock)
                    time.sleep(0.001)
                except Exception:
                    time.sleep(0.1)

        threads = [threading.Thread(target=flood_worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        for sock in held_sockets:
            try:
                sock.close()
            except Exception:
                pass

    # Bandwidth Exhaustion
    def tcp_bandwidth_exhaustion(self) -> None:
        duration = random.randint(60, 120)
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

    # UDP Flood — multi-threaded for higher throughput
    def udp_flood(self):
        duration = random.randint(60, 120)
        data = random.randbytes(65507)
        start_time = time.time()

        def flood_worker():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                while time.time() - start_time < duration:
                    try:
                        sock.sendto(data, (self.host, self.port))
                    except Exception:
                        time.sleep(0.1)

        threads = [threading.Thread(target=flood_worker) for _ in range(15)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    # Port Scanning Attack
    def port_scan_simulation(self):
        duration = random.randint(60, 120)
        start_time = time.time()
        scan_ports = random.sample(range(1, 65536), 10000)
        port_index = 0
        lock = threading.Lock()

        def scan_worker():
            nonlocal port_index
            while time.time() - start_time < duration:
                with lock:
                    if port_index >= len(scan_ports):
                        break
                    port = scan_ports[port_index]
                    port_index += 1
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(0.01)
                        sock.connect((self.host, port))
                except Exception:
                    pass

        threads = [threading.Thread(target=scan_worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    # Large file download
    def bulk_download(self):
        duration = random.randint(60, 120)
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
            except Exception:
                time.sleep(0.1)
