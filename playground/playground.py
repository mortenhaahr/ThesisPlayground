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


IGNORED_FEATURES = (
    r"act_mode\d|DBB_ANTI\.*|M2\.*|M3\.*|equal_period_count\.*|PT03\.*|FT010[3|4|6]\.*"
)


def _detect_interval_indices_old(
    data, DELTA_DIFF=1.0, MEAN_WINDOW=4, EVENT_SEPERATION_SAMPLES=2
):
    """
    Finds periods where the data is of similar values.
    Ignores noise by averaging the differences over a window controlled by MEAN_WINDOW.
    Isolates transition periods by removing sequences where deltas occured contigously
    (in reference to indices).

    Args:
        data:                       Data to find changes in
        DELTA_DIFF:                 Minimum value to consider a significant difference
        MEAN_WINDOW:                Window length used to filter out noise
        EVENT_SEPERATION_SAMPLES:   Controls transition period filtering

    Returns:
        List of pairs indicating the intervals that belong together in data

    Raises:
        RuntimeError: Intervals are for some reason of different lengths
    """
    diffs_detected = []
    for i in range(1, len(data) - MEAN_WINDOW):
        diffs = [data[k + i] - data[k + i - 1] for k in range(MEAN_WINDOW)]
        avg_diff = np.mean(diffs)
        if abs(avg_diff) > DELTA_DIFF:
            diffs_detected.append(i)

    # Filter diffs to not include e.g.:
    transition_start = [0]
    transition_end = []
    for i in range(len(diffs_detected)):
        if (i < len(diffs_detected) - 1) and (
            abs(diffs_detected[i] - diffs_detected[i + 1]) > EVENT_SEPERATION_SAMPLES
        ):
            transition_end.append(diffs_detected[i])
        elif (i > 0) and (
            abs(diffs_detected[i] - diffs_detected[i - 1]) > EVENT_SEPERATION_SAMPLES
        ):
            transition_start.append(diffs_detected[i])

    transition_end.append(diffs_detected[i])
    if len(transition_start) != len(transition_end):
        raise RuntimeError("Intervals appear to be of different lengths")

    return zip(transition_start, transition_end)



def detect_interval_indices(data, DELTA_THRESHOLD = 0.5, MEAN_WINDOW=10):
    class FSMState(Enum):
        LookingForChange = auto()
        LookingForSteady = auto()

    # TODO: MHK try variance

    start = 0
    intervals = []
    FSM_state = FSMState.LookingForChange

    # This implementation uses windows before and after the given datapoint.
    # Therefore the range will have to start and stop for the loop will have to be changed by MEAN_WINDOW size.
    for i in range(MEAN_WINDOW, len(data) - MEAN_WINDOW):

        window_before = data[i-MEAN_WINDOW:i]
        mean_before = np.mean(window_before)
        current_sample = data[i]
        window_after = data[i+1:i+MEAN_WINDOW]
        mean_after = np.mean(window_after)

        """
            If the system is currently in a steady state, the gt operator is used to detect big chagnges.
            If the system flow is changing rapidly, then the lt operator is used to detect steady state.
        """
        comp = operator.gt if FSM_state == FSMState.LookingForChange else operator.lt

        # If a the difference between the mean values of the before and after window is below the threshold, then an event was detected.
        if comp(abs(mean_before - mean_after), DELTA_THRESHOLD):
            # Append the start and end to intervals and update the starting point for the next entry
            end = i
            intervals.append(((start, end), FSM_state.name))
            start = end

            # Update the state of the method
            FSM_state = FSMState.LookingForChange if FSM_state == FSMState.LookingForSteady else FSMState.LookingForSteady
    
    intervals.append(((start, len(data) -1), FSM_state.name)) # Add last point
    return intervals


if __name__ == "__main__":
    # Run from script dir
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        dest="filepath",
        required=True,
        help="input file with data from PLC",
        metavar="FILE",
        type=lambda x: is_valid_file(parser, x),
    )
    parser.add_argument(
        "--show",
        action=BooleanOptionalAction,
        default=False,
        help="Enable to show diagrams",
    )

    args = parser.parse_args()

    path = Path(args.filepath)

    FILE = path.stem
    FILE_ENDING = path.suffix
    RESULTS_FOLDER = f"results/{FILE}"

    data = pd.read_csv(f"{path}", delimiter=";")
    try:
        time = data.pop("YYYY-MM-DD-HH:MM:SS")
    except:
        print(f"Key error for file {path}. keys: {data.keys()}")
        exit(1)

    time = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S:%f") for t in time]
    t_start = time[0]
    time_d = [(t - t_start).total_seconds() for t in time]

    # Remove elements that match regex
    regex = re.compile(IGNORED_FEATURES)
    data = data.filter([item for item in data.keys() if not regex.match(item)])

    # Create if result folder not exists:
    Path(f"{RESULTS_FOLDER}").mkdir(parents=True, exist_ok=True)

    for d in data:
        if d != "FT0101[l/m]":
            continue
        unit_start = d.find("[")
        if unit_start != -1:
            unit_end = d.find("]")
            unit = d[unit_start : unit_end + 1]
        else:
            unit_start = len(d)
            unit = "[]"
        title = f"{d[:unit_start]}_{t_start.strftime('%Y-%m-%d-%H-%M-%S')}"
        fig, ax = plt.subplots(figsize=(19.20, 10.80))
        ax.plot(time_d, data[d])
        ax.set_title(title)
        ax.set_xlabel("Time [s]")
        ax.set_ylabel(unit)
        ax.grid()
        if d == "FT0101[l/m]":
            intervals = tuple(detect_interval_indices(data[d]))
            print(intervals)
            colors = iter(plt.cm.rainbow(np.linspace(0, 1, len(intervals))))
            for interval,_ in intervals:
                c = next(colors)
                ax.axvline(x=time_d[interval[0]], color=c)
                ax.axvline(x=time_d[interval[1]], color=c)
        plt.savefig(f"{RESULTS_FOLDER}/{title}.png", dpi=400)
        if args.show:
            plt.show()
        plt.close(fig)

    with open(f"{RESULTS_FOLDER}/info.csv", "w") as f:
        tmp = sys.stdout
        sys.stdout = f  # Redirect stdout to the file
        data.info()  # Print the info to the file
        sys.stdout = tmp
    with open(f"{RESULTS_FOLDER}/stats.csv", "w") as f:
        f.write(data.describe().to_string())
