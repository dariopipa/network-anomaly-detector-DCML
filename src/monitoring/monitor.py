import logging
import socket
import psutil
from helper import CPUMemoryInfo, DataIOCounter, NetworkConnectionData

TCP_STATES = {
    "ESTABLISHED",
    "LISTEN",
    "SYN_SENT",
    "SYN_RECV",
    "TIME_WAIT",
    "CLOSE_WAIT",
}


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_cpu_and_memory_information() -> CPUMemoryInfo:
    cpu_usage = psutil.cpu_percent(interval=None)
    memory_usage = psutil.virtual_memory()

    return CPUMemoryInfo(cpu_usage=cpu_usage, memory_usage=memory_usage.percent)


def get_network_connection_data() -> NetworkConnectionData:
    total_tcp_conn = 0
    total_udp_conn = 0
    state_counts = {s: 0 for s in TCP_STATES}

    remote_ips = set()
    remote_ports = set()

    try:
        for connection in psutil.net_connections(kind="inet"):
            if connection.type == socket.SOCK_STREAM:
                total_tcp_conn += 1
                status = (connection.status or "").upper()
                if status in state_counts:
                    state_counts[status] += 1

            elif connection.type == socket.SOCK_DGRAM:
                total_udp_conn += 1

            if connection.raddr:
                remote_ips.add(connection.raddr.ip)
                remote_ports.add(connection.raddr.port)

        return NetworkConnectionData(
            tcp_connections_total=total_tcp_conn,
            udp_sockets_total=total_udp_conn,
            tcp_established=state_counts["ESTABLISHED"],
            tcp_listen=state_counts["LISTEN"],
            tcp_time_wait=state_counts["TIME_WAIT"],
            tcp_close_wait=state_counts["CLOSE_WAIT"],
            unique_remote_ips=len(remote_ips),
            unique_remote_ports=len(remote_ports),
        )

    except PermissionError:
        logging.error("Permission missing to get network information,script exiting.")
        exit(1)


def get_network_io_data() -> DataIOCounter:
    data_io = psutil.net_io_counters()

    return DataIOCounter(
        bytes_recv=data_io.bytes_recv,
        bytes_sent=data_io.bytes_sent,
        packets_recv=data_io.packets_recv,
        packets_sent=data_io.packets_sent,
    )


def calculate_network_io_byte_difference(
    previous_data: DataIOCounter, current_data: DataIOCounter
) -> DataIOCounter:
    if previous_data is None:
        return DataIOCounter()

    return DataIOCounter(
        bytes_sent=current_data.bytes_sent - previous_data.bytes_sent,
        bytes_recv=current_data.bytes_recv - previous_data.bytes_recv,
        packets_sent=current_data.packets_sent - previous_data.packets_sent,
        packets_recv=current_data.packets_recv - previous_data.packets_recv,
    )
