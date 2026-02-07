import csv
import os
import sys
from time import sleep
import time
from colorama import Fore, Style
import pandas as pd
import psutil
from src.monitoring.models import DataIOCounter
from src.monitoring.monitor import (
    calculate_network_io_byte_difference,
    get_cpu_and_memory_information,
    get_network_connection_data,
    get_network_io_data,
)


# Based on the documentation, the CPU usage detector
# should be run once beforehand,
# since on the first run it will output 0, and that is incorrect.
def run_baseline_cpu_usage_detector() -> None:
    psutil.cpu_percent(interval=None)
    sleep(0.1)
    return


def cli_script() -> None:
    print("\n" + "=" * 65)
    print(
        Fore.CYAN
        + Style.BRIGHT
        + "         NETWORK MONTIROING & COLLECTION SCRIPT"
        + Style.RESET_ALL
    )
    print("=" * 65 + "\n")

    print(Fore.WHITE + Style.BRIGHT + "OVERVIEW:" + Style.RESET_ALL)
    print("  Continuously monitors host network activity and system\n  resources.\n")

    print("=" * 65)

    detected_os = sys.platform
    print(
        Fore.WHITE
        + Style.BRIGHT
        + "Detected OS: "
        + Style.RESET_ALL
        + Fore.GREEN
        + f"{detected_os}"
        + Style.RESET_ALL
    )

    os_confirm = input(
        Fore.CYAN
        + "Is this correct? Type "
        + Fore.GREEN
        + "YES"
        + Fore.CYAN
        + " to continue: "
        + Style.RESET_ALL
    ).strip()

    if os_confirm.lower() not in {"yes", "y"}:
        print(Fore.RED + "\nScript cancelled.\n" + Style.RESET_ALL)
        exit(1)

    print(Fore.GREEN + "\nStarting collecting...\n" + Style.RESET_ALL)


def write_to_csv(filename: str, data: dict):
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)


def collect_monitored_data(
    previous_network_io: DataIOCounter, label: int = 0, attack_type: str = "normal"
) -> tuple[dict, DataIOCounter]:

    current_network_io_data = get_network_io_data()
    cpu_memory_usage = get_cpu_and_memory_information()
    network_data_diff = calculate_network_io_byte_difference(
        previous_network_io, current_network_io_data
    )
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
        "label": label,
        "attack_type": attack_type,
    }

    return data, current_network_io_data


def aggregate_dataframe_into_20_seconds_interval(data):
    """
    This function will take the data in 1s intervals and aggregate it into 20-second intervals, while also doing some aggregation on the data, like finding the min, max, mean, and std, which will create the necessary features for the model to be trained on. This is in the monitoring helper because notebooks cannot import from each other.
    """

    data["datetime"] = pd.to_datetime(data["time"])
    data = data.set_index("datetime")

    # Define column groups for different aggregation strategies
    state_cols = [
        "cpu_usage",
        "memory_usage",
        "tcp_connections_total",
        "udp_sockets_total",
        "tcp_established",
        "tcp_listen",
        "tcp_time_wait",
        "tcp_close_wait",
        "unique_remote_ips",
        "unique_remote_ports",
    ]

    traffic_cols = ["bytes_recv", "bytes_sent", "packets_recv", "packets_sent"]

    agg_rules = {}
    for col in state_cols:
        agg_rules[col] = ["mean", "max", "min", "std"]
    for col in traffic_cols:
        agg_rules[col] = ["sum", "mean", "max", "std"]

    resampled_data = data[state_cols + traffic_cols].resample("20s").agg(agg_rules)

    resampled_data.columns = [
        "_".join(col).strip() for col in resampled_data.columns.values
    ]

    resampled_data.dropna()
    return resampled_data
