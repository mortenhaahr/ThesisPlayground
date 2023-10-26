import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from argparse import ArgumentParser, BooleanOptionalAction
import sys
import re
import numpy as np
from enum import Enum, auto
import operator


def is_valid_file(parser, arg):
    if not os.path.exists(arg.strip()):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg.strip()


FEATURES = [
    "PT0102",
    "PT0106",
    "PT020",
    "outlet",
    "FT0101",
]

def stats_of_sample(filepath): 
    # Run from script dir
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    path = Path(filepath)

    FILE = path.stem    

    data = pd.read_csv(f"{path}", delimiter=";")
    try:
        time = data.pop("YYYY-MM-DD-HH:MM:SS")
    except:
        raise(f"Key error for file {path}. keys: {data.keys()}")

    time = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S:%f") for t in time]
    t_start = time[0]
    time_d = [(t - t_start).total_seconds() for t in time]

    SAMPLE_FREQ = 1/time_d[1]

    # Remove elements that match regex
    regex_str = "\.*|".join(FEATURES)
    regex = re.compile(regex_str)
    data = data.filter([item for item in data.keys() if regex.match(item)])

    RESULTS_FOLDER = f"results/data_stats/{FILE}"
     # Create if result folder not exists:
    Path(f"{RESULTS_FOLDER}").mkdir(parents=True, exist_ok=True)

    FLOW_KEY = "FT0101[l/m]"
    flow = data[FLOW_KEY]

    unit_start = FLOW_KEY.find("[")
    unit_end = FLOW_KEY.find("]")
    unit = FLOW_KEY[unit_start : unit_end + 1]

    title = f"Flow"

    _, ax = plt.subplots(figsize=(13.66, 7.68))
    ax.plot(time_d, flow)
    ax.set_title(title)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel(unit)
    ax.grid()
    plt.show(block=False)
    interval_low_raw = input("Enter lower interval[s]:")
    interval_low = round(int(interval_low_raw) * SAMPLE_FREQ)
    ax.axvline(x=time_d[interval_low])        
    interval_high_raw = input("Enter high interval[s]:")
    interval_high = round(int(interval_high_raw) * SAMPLE_FREQ)
    ax.axvline(x=time_d[interval_high])
    plt.savefig(f"{RESULTS_FOLDER}/{title}.png", dpi=400)
    plt.close()

    for d in data:
        data[d] = data[d][interval_low:interval_high+1]
    with open(f"{RESULTS_FOLDER}/interval", "w") as f:
        f.write(f"({interval_low_raw}:{interval_high_raw})")

    with open(f"{RESULTS_FOLDER}/stats.csv", "w") as f:
        f.write(data.describe().to_string())


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        dest="filepath",
        required=True,
        help="input file with data from PLC",
        metavar="FILE",
        type=lambda x: is_valid_file(parser, x),
    )

    args = parser.parse_args()
    stats_of_sample(args.filepath)
    
