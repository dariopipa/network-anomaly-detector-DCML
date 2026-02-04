import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from fault_injector import FaultInjector
from server_config import MONITOR_IP, TCP_PORT, UDP_PORT, COMMUNICATION_PORT
import random
import time
from communicate_client import CommunicateClient
from colorama import Fore, Style


def main():
    print("\n" + "=" * 65)
    print(
        Fore.RED
        + Style.BRIGHT
        + "              FAULT INJECTOR - ATTACK SIMULATOR"
        + Style.RESET_ALL
    )
    print("=" * 65 + "\n")

    fault_injector = FaultInjector(host=MONITOR_IP, port=TCP_PORT)
    udp_injector = FaultInjector(host=MONITOR_IP, port=UDP_PORT)

    attacks = [
        fault_injector.tcp_connection_flood,
        fault_injector.tcp_bandwidth_exhaustion,
        fault_injector.port_scan_simulation,
        fault_injector.bulk_download,
        udp_injector.udp_flood,
    ]

    communicate_client = CommunicateClient(MONITOR_IP, COMMUNICATION_PORT)

    attack_deck = []

    while True:
        if not attack_deck:
            attack_deck = attacks.copy()
            random.shuffle(attack_deck)

        attack_func = attack_deck.pop(0)

        # todo: UPDATE THE RANDOMNESS BEFORE ATTACK ()
        wait_before_attack = random.randint(30, 120)

        print(Fore.CYAN + "Injection started" + Style.RESET_ALL)
        print(Fore.CYAN + f"Time before attack {wait_before_attack}" + Style.RESET_ALL)
        time.sleep(wait_before_attack)

        print(
            Fore.YELLOW
            + Style.BRIGHT
            + f"Attack: {attack_func.__name__}"
            + Style.RESET_ALL
        )

        print(Fore.RED + Style.BRIGHT + "Attack started" + Style.RESET_ALL)
        communicate_client.signal_start(attack_type=attack_func.__name__)

        attack_func()

        print(Fore.GREEN + Style.BRIGHT + "Attack finished" + Style.RESET_ALL)
        communicate_client.signal_stop()

        print("=" * 60)


if __name__ == "__main__":
    main()
