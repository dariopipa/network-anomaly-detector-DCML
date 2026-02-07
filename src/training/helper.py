import pandas as pd

RESAMPLE_TIME_INTERVAL = "20s"


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

    resampled_data = (
        data[state_cols + traffic_cols + ["label"]]
        .resample(RESAMPLE_TIME_INTERVAL)
        .agg(agg_rules)
    )

    resampled_data.columns = [
        "_".join(col).strip() for col in resampled_data.columns.values
    ]

    attack_seconds = data["label"].resample(RESAMPLE_TIME_INTERVAL).sum()
    resampled_data["label"] = (attack_seconds >= 8).astype(int)

    # When using resample, the function creates 20-second windows from the first timestamp to the last, even if no data was collected during some of those intervals. We then drop the windows that contain only null values.
    resampled_data = resampled_data.dropna()

    return resampled_data
