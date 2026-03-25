from src.fault_injector.fault_injector import FaultInjector
from src.server_config import MONITOR_IP, TCP_PORT, UDP_PORT, COMMUNICATION_PORT
from src.fault_injector.communicate_client import CommunicateClient
import random
import time
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

    try:
        communicate_client = CommunicateClient(MONITOR_IP, COMMUNICATION_PORT)
        print(Fore.GREEN + "[Info] Connected to monitoring script" + Style.RESET_ALL)
    except ConnectionRefusedError:
        communicate_client = None
        print(
            Fore.YELLOW
            + "[Warning] Monitoring script not online — running without labelling"
            + Style.RESET_ALL
        )

    attack_deck = []

    try:
        while True:
            # This will randomly shuffle the attacks and then will choose, this will also make sure that all attacks are run before re running.
            if not attack_deck:
                attack_deck = attacks.copy()
                random.shuffle(attack_deck)

            attack_func = attack_deck.pop(0)

            wait_before_attack = random.randint(180, 300)

            print(Fore.CYAN + "Injection started" + Style.RESET_ALL)
            print(
                Fore.CYAN + f"Time before attack {wait_before_attack}" + Style.RESET_ALL
            )
            time.sleep(wait_before_attack)

            print(
                Fore.YELLOW
                + Style.BRIGHT
                + f"Attack: {attack_func.__name__}"
                + Style.RESET_ALL
            )

            print(Fore.RED + Style.BRIGHT + "Attack started" + Style.RESET_ALL)

            # this will communicate to the monitoring machine , if an attack is ongoing or not to be able to label the data.
            if communicate_client:
                communicate_client.signal_start(attack_type=attack_func.__name__)

            attack_func()

            print(Fore.GREEN + Style.BRIGHT + "Attack finished" + Style.RESET_ALL)
            if communicate_client:
                communicate_client.signal_stop()

            print("=" * 60)

    except KeyboardInterrupt:
        print("fault injector script stopped")
        exit(0)


if __name__ == "__main__":
    main()
