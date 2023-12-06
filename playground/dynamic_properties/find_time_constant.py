import os
from argparse import ArgumentParser
import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import json


def is_valid_file(parser, arg):
    if not os.path.exists(arg.strip()):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg.strip()


def is_positive_float(parser, arg):
    try:
        float_value = float(arg)
        if float_value <= 0:
            raise parser.error("Value must be a positive floating-point number.")
        return float_value
    except ValueError:
        raise parser.error("Invalid floating-point number.")


def is_valid_pressure_sensor(parser, arg):
    VALID_SENSORS = [
        "PT0101[Bar]",
        "PT0102[Bar]",
        "PT0201[Bar]",
        "PT0202[Bar]",
        "PT0203[Bar]",
        "outlet_pressure[Bar]",
        "PT0106",
    ]
    if arg not in VALID_SENSORS:
        parser.error(f"The sensor {arg} is not valid for this script")
    return arg


def float_2_decimals(number: float):
    """Converts the float to a string with 2 decimals and then back to float"""
    return float(f"{number:0.2f}")


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
        "-s",
        dest="step_time",
        required=False,
        help="The step time in seconds",
        type=lambda x: is_positive_float(parser, x),
    )

    parser.add_argument(
        "-p",
        dest="pressure_sensor",
        default="PT0102[Bar]",
        help="The sensor data to use for step",
        type=lambda x: is_valid_pressure_sensor(parser, x),
    )

    args = parser.parse_args()

    path = Path(args.filepath)
    step_start_raw = args.step_time
    pressure_sensor = args.pressure_sensor

    data = pd.read_csv(f"{path}", delimiter=";")
    try:
        time = data.pop("YYYY-MM-DD-HH:MM:SS")
    except:
        print(f"Key error for file {path}. keys: {data.keys()}")
        exit(1)

    FILE = path.stem
    FILE_ENDING = path.suffix
    RESULTS_FOLDER = f"../results/dynamic_props/{FILE}"
    CALCULATIONS_FILE = "calc.json"
    CALC_FILE = f"{RESULTS_FOLDER}/{CALCULATIONS_FILE}"

    # Create if result folder not exists:
    Path(f"{RESULTS_FOLDER}").mkdir(parents=True, exist_ok=True)

    time = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S:%f") for t in time]
    t_start = time[0]
    time_d = [(t - t_start).total_seconds() for t in time]  # X-axis
    t_diff_max = [0, 0]
    for i in range(1, len(time_d)):
        diff = time_d[i] - time_d[i - 1]
        if diff > t_diff_max[0]:
            t_diff_max = [diff, i]

    SAMPLE_FREQ = 1 / time_d[1]

    pressure = data[pressure_sensor]
    pressure_unit_start = pressure_sensor.find("[")
    pressure_unit_end = pressure_sensor.find("]")
    pressure_unit = pressure_sensor[pressure_unit_start : pressure_unit_end + 1]

    unit_start = pressure_sensor.find("[")
    unit_end = pressure_sensor.find("]")
    unit = pressure_sensor[unit_start : unit_end + 1]
    title = f"{pressure_sensor[:unit_start]}_{t_start.strftime('%Y-%m-%d-%H-%M-%S')}"

    _, ax = plt.subplots(figsize=(13.66, 7.68))
    ax.set_title(title)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel(f"Pressure {unit}")
    ax.plot(time_d, pressure, label=pressure_sensor[:unit_start])
    plt.grid()
    plt.show(block=False)

    # Hack the figure to be zoomed around 20..23 to easier determine step time
    # plt.axis([20.1, 23, plt.axis()[2], plt.axis()[3]])

    if not step_start_raw:
        step_start_raw = input("Enter step start time[s]:")
    step_start_sample = round(float(step_start_raw) * SAMPLE_FREQ)
    step_start_time = float(step_start_raw)

    # Get the starting pressure: Take the average of a few samples before step start
    step_start_p = np.average(pressure[step_start_sample - 15 : step_start_sample - 5])
    # Time constant when decharging: 36.8 % of initial value
    time_constant_p = step_start_p * 0.368

    tau_sample_t, tau_sample_p = next(
        (t, p)
        for t, p in zip(time_d[step_start_sample:], pressure[step_start_sample:])
        if p < time_constant_p
    )

    ax.axvline(x=step_start_time, color="g", label="Step start")
    ax.axvline(x=tau_sample_t, color="r", label="Time constant")
    ax.legend(loc="center right")

    plt.text(
        tau_sample_t + 1,
        step_start_p / 2,
        f"tau = {tau_sample_t:0.2f} - {step_start_time:0.2f} = {(tau_sample_t - step_start_time):0.2f}",
        verticalalignment="center",
    )

    with open(CALC_FILE, "w") as outfile:
        json.dump(
            {
                "step_start": {
                    "time[s]": float_2_decimals(step_start_time),
                    "sample[ ]": step_start_sample,
                    "pressure[bar]": step_start_p,
                },
                "tau": {
                    "discharge_time[s]": float_2_decimals(
                        tau_sample_t - step_start_time
                    ),  # Actual tau value
                    "sample_time[s]": tau_sample_t,  # The time of the sample that was used
                    "sample_pressure[bar]": tau_sample_p,
                    "sample[ ]": round(float(tau_sample_t) * SAMPLE_FREQ),
                    "min_pressure[bar]": float_2_decimals(
                        time_constant_p
                    ),  # Sample must be less-than this pressure to be used for tau
                },
                "sample_diff[ ]": round(float(tau_sample_t) * SAMPLE_FREQ)
                - step_start_sample,
            },
            outfile,
            indent=4,
        )

    plt.axis("auto")  # Reset zoom
    plt.savefig(f"{RESULTS_FOLDER}/interval.png", dpi=400)
