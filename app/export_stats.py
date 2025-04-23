import os
import statistics
import pandas as pd
from collections import defaultdict
from scapy.all import *

PCAP_DIRECTORY = "./captures"
OUTPUT_DIRECTORY = "./stats.csv"

def traffic_intervals(timestamps):
    timestamps = sorted(timestamps)
    deltas = [t2 - t1 for t1, t2 in zip(timestamps, timestamps[1:])]

    if not deltas:
        return 0.0, 0.0, 0.0

    return statistics.mean(deltas), statistics.median(deltas), statistics.pstdev(deltas)
def analyze(filepath):
    packets = rdpcap(filepath)

    # Guess the local IP
    ip_counter = defaultdict(int)
    for pkt in packets:
        if IP in pkt:
            ip_counter[pkt[IP].src] += 1
            ip_counter[pkt[IP].dst] += 1

    local_ip = max(ip_counter.items(), key=lambda x: x[1])[0]

    # Traffic analysis
    out_times, in_times = [], []
    out_sizes, in_sizes = [], []

    for pkt in packets:
        if IP not in pkt:
            continue

        ts = pkt.time
        src = pkt[IP].src
        dst = pkt[IP].dst
        size = len(pkt)

        if src == local_ip:
            out_times.append(ts)
            out_sizes.append(size)
        elif dst == local_ip:
            in_times.append(ts)
            in_sizes.append(size)

    # Timestampes analysis for traffic
    in_mean, in_median, in_std = traffic_intervals(in_times)
    out_mean, out_median, out_std = traffic_intervals(out_times)

    return {
        "site_name": filepath.split('_')[0].split('/')[-1],
        "packets_in": len(in_times),
        "bytes_in": sum(in_sizes),
        "packets_out": len(out_times),
        "bytes_out": sum(out_sizes),
        "in_times_mean": in_mean,
        "in_times_median": in_median,
        "in_times_std": in_std,
        "out_times_mean": out_mean,
        "out_times_median": out_median,
        "out_times_std": out_std
    }

if __name__ == "__main__":
    results = []
    for fname in os.listdir(PCAP_DIRECTORY):
        if fname.endswith(".pcapng"):
            path = os.path.join(PCAP_DIRECTORY, fname)
            print(f"Processing {fname}...")
            try:
                stats = analyze(path)
                results.append(stats)
            except Exception as e:
                print(f"Error processing {fname}: {e}")

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_DIRECTORY, index=False)
    print(f"Statistics saved to {OUTPUT_DIRECTORY}")
