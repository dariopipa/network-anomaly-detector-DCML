import threading
from pathlib import Path
from src.monitoring.monitor import get_network_io_data
import logging
from src.monitoring import helper
import time
from src.monitoring import monitor_server_reciever

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
            data, previous_network_io = helper.collect_monitored_data(
                previous_network_io,
                label=monitor_server_reciever.label,
                attack_type=monitor_server_reciever.attack_type,
            )

            helper.write_to_csv(filename=str(DATASET_PATH), data=data)

            time.sleep(1)
        except KeyboardInterrupt:
            print("Data collection stopped.")
            exit(0)


if __name__ == "__main__":
    main()
