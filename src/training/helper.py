import pandas as pd
import math


def aggregate_dataframe_into_seconds_interval(data, window_size):
    """
    This function will take the data in 1s intervals and aggregate it into windows as intervals, while also doing some aggregation on the data, like finding the min, max, mean, and std, which will create the necessary features for the model to be trained on. This is in the monitoring helper because notebooks cannot import from each other.
    """

    data["datetime"] = pd.to_datetime(data["time"])
    data = data.set_index("datetime")
    window_size_seconds = f"{window_size}s"

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
        "unique_local_ports",
    ]

    traffic_cols = ["bytes_recv", "bytes_sent", "packets_recv", "packets_sent"]

    agg_rules = {}
    for col in state_cols:
        agg_rules[col] = ["mean", "max", "min", "std"]
    for col in traffic_cols:
        agg_rules[col] = ["sum", "mean", "max", "std"]

    resampled_data = (
        data[state_cols + traffic_cols + ["label"]]
        .resample(window_size_seconds)
        .agg(agg_rules)
    )

    resampled_data.columns = [
        "_".join(col).strip() for col in resampled_data.columns.values
    ]

    attack_seconds = data["label"].resample(window_size_seconds).sum()

    # if 40% of a window is labeled as "attacked" the whole new window will be labeled "attacked"
    min_attack_seconds = math.ceil(0.4 * window_size)
    resampled_data["label"] = (attack_seconds >= min_attack_seconds).astype(int)

    # Drop windows where ALL mean columns are NaN - these are empty windows that get created by running the resample, and they do not contain any information.
    mean_cols = [c for c in resampled_data.columns if c.endswith("_mean")]
    resampled_data = resampled_data.dropna(subset=mean_cols, how="all")

    # Fill any remaining NaNs with 0 - these are windows where only 1 data point was recorded, which makes the std NaN since you need at least 2 points to calculate it.
    resampled_data = resampled_data.fillna(0)

    return resampled_data
