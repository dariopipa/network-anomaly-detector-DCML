from dataclasses import dataclass


@dataclass
class CPUMemoryInfo:
    cpu_usage: float
    memory_usage: float


@dataclass
class DataIOCounter:
    bytes_sent: int = 0
    bytes_recv: int = 0
    packets_sent: int = 0
    packets_recv: int = 0


@dataclass
class NetworkConnectionData:
    tcp_connections_total: int
    udp_sockets_total: int
    tcp_established: int
    tcp_listen: int
    tcp_time_wait: int
    tcp_close_wait: int
    unique_remote_ips: int
    unique_remote_ports: int
