import threading
from pathlib import Path
from monitor import (
    get_network_connection_data,
    get_network_io_data,
    get_cpu_and_memory_information,
    calculate_network_io_byte_difference,
    get_processes_names_and_id,
)
import logging
import helper
import time
import monitor_server_reciever

SRC_DIR = Path(__file__).parent.parent

# TODO: UPDATE NAME AFTER CREATING THE DATASET TO NOT ACTUALLY APPEND INFO BY MISTAKE
DATASET_PATH = SRC_DIR / "dataset.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    server_thread = threading.Thread(
        target=monitor_server_reciever.start_control_server, daemon=True
    )
    server_thread.start()

    helper.cli_script()
    helper.run_baseline_cpu_usage_detector()

    previous_network_io = get_network_io_data()

    print("Data Collection started. Press Ctrl+C to stop.")
    while True:
        try:
            current_network_io_data = get_network_io_data()
            cpu_memory_usage = get_cpu_and_memory_information()
            network_data_diff = calculate_network_io_byte_difference(
                previous_network_io, get_network_io_data()
            )
            previous_network_io = current_network_io_data
            network_connection_info = get_network_connection_data()

            data = {
                "cpu_usage": cpu_memory_usage.cpu_usage,
                "memory_usage": cpu_memory_usage.memory_usage,
                "tcp_connections_total": network_connection_info.tcp_connections_total,
                "udp_sockets_total": network_connection_info.udp_sockets_total,
                "tcp_established": network_connection_info.tcp_established,
                "tcp_listen": network_connection_info.tcp_listen,
                "tcp_time_wait": network_connection_info.tcp_time_wait,
                "tcp_close_wait": network_connection_info.tcp_close_wait,
                "unique_remote_ips": network_connection_info.unique_remote_ips,
                "unique_remote_ports": network_connection_info.unique_remote_ports,
                "bytes_recv": network_data_diff.bytes_recv,
                "bytes_sent": network_data_diff.bytes_sent,
                "packets_recv": network_data_diff.packets_recv,
                "packets_sent": network_data_diff.packets_sent,
                "timestamp": time.monotonic(),
                "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "label": monitor_server_reciever.label,
                "attack_type": monitor_server_reciever.attack_type,
            }

            helper.write_to_csv(filename=str(DATASET_PATH), data=data)

            time.sleep(1)
        except KeyboardInterrupt:
            print("Data collection stopped.")
            exit(1)


if __name__ == "__main__":
    main()
