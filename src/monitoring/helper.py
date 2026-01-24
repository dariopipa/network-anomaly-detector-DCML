import csv
from dataclasses import dataclass
import os
import sys
from time import sleep
from colorama import Fore, Style
import psutil


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


# Based on the documentation the cpu usage detector
# should be run once before, since the first run it will output 0 and that is incorrect.
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
