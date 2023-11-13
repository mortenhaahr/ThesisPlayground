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
import json
import math


def is_valid_file(parser, arg):
    if not os.path.exists(arg.strip()):
        if parser:
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

INTERVAL_FILE = "interval"
CSV_FILE = "stats.csv"
CALCULATIONS_FILE = "calc.json"

def stats_of_sample(path, results): 
    data = pd.read_csv(f"{path}", delimiter=";")
    try:
        time = data.pop("YYYY-MM-DD-HH:MM:SS")
    except:
        raise(f"Key error for file {path}. keys: {data.keys()}")

    time = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S:%f") for t in time]
    t_start = time[0]
    time_d = [(t - t_start).total_seconds() for t in time]
    t_diff_max = [0, 0]
    for i in range(1, len(time_d)):
        diff = time_d[i] - time_d[i - 1]
        if diff > t_diff_max[0]:
            t_diff_max = [diff, i]
        
    SAMPLE_FREQ = 1/time_d[1]

    # Remove elements that match regex
    regex_str = "\.*|".join(FEATURES)
    regex = re.compile(regex_str)
    data = data.filter([item for item in data.keys() if regex.match(item)])

    
     # Create if result folder not exists:
    Path(f"{results}").mkdir(parents=True, exist_ok=True)

    FLOW_KEY = "FT0101[l/m]"
    flow = data[FLOW_KEY]
    flow_unit_start = FLOW_KEY.find("[")
    flow_unit_end = FLOW_KEY.find("]")
    flow_unit = FLOW_KEY[flow_unit_start : flow_unit_end + 1]
    if flow_unit == "[l/m]":
        flow_unit = "[l/min]"

    PRESURE_KEY = "PT0102[Bar]"
    pressure = data[PRESURE_KEY]
    pressure_unit_start = PRESURE_KEY.find("[")
    pressure_unit_end = PRESURE_KEY.find("]")
    pressure_unit = PRESURE_KEY[pressure_unit_start : pressure_unit_end + 1]

    _, ax = plt.subplots(figsize=(13.66, 7.68))
    ax.set_title(f"{path.stem}")
    ax.set_xlabel("Time [s]")
    color = "tab:red"
    ax.plot(time_d, flow, color=color)
    ax.set_ylabel(flow_unit, color=color)
    ax.tick_params(axis='y', color=color)
    
    color = "tab:blue"
    ax2 = ax.twinx()
    ax2.plot(time_d, pressure, color=color)
    ax2.set_ylabel(pressure_unit, color=color)
    ax2.tick_params(axis='y', color=color)

    plt.show(block=False)
    interval_low_raw = input("Enter lower interval[s]:")
    interval_low = round(int(interval_low_raw) * SAMPLE_FREQ)
    ax.axvline(x=time_d[interval_low], color="g")        
    interval_high_raw = input("Enter high interval[s]:")
    interval_high = round(int(interval_high_raw) * SAMPLE_FREQ)
    ax.axvline(x=time_d[interval_high], color="g")
    plt.savefig(f"{results}/interval.png", dpi=400)
    plt.close()
    with open(f"{results}/{INTERVAL_FILE}", "w") as f:
        f.write(f"({interval_low_raw}:{interval_high_raw})")

    for d in data:
        data[d] = data[d][interval_low:interval_high+1]

    data.describe().to_csv(f"{results}/{CSV_FILE}")


STATS_INDEX = {
    "count" : 0,
    "mean" : 1,
    "std" : 2
}

L_PR_S_IN_M3_PR_S = 0.001
L_PR_MIN_IN_L_PR_S = 1/60
L_PR_MIN_IN_M3_PR_S = L_PR_MIN_IN_L_PR_S*L_PR_S_IN_M3_PR_S

def main_flow(stats):
    flow_l_pr_min =  stats["FT0101[l/m]"][STATS_INDEX["mean"]]
    flow_l_pr_s = flow_l_pr_min * L_PR_MIN_IN_L_PR_S
    flow_m3_pr_s = flow_l_pr_s * L_PR_S_IN_M3_PR_S
    return [flow_m3_pr_s, "m3/s"]

BAR_TO_PA = 100000

def main_pressure(stats):
    p_bar = stats["PT0102[Bar]"][STATS_INDEX["mean"]]
    p_pa = p_bar * BAR_TO_PA
    return [p_pa, "Pa"]

def outlet_pressure(stats):
    p_bar = stats["outlet_pressure"][STATS_INDEX["mean"]]
    p_pa = p_bar * BAR_TO_PA
    return [p_pa, "Pa"]

def kitchen_pressure(stats):
    p_bar = stats["PT0201[Bar]"][STATS_INDEX["mean"]]
    p_pa = p_bar * BAR_TO_PA
    return [p_pa, "Pa"]

def bathroom_pressure(stats):
    p_bar = stats["PT0202[Bar]"][STATS_INDEX["mean"]]
    p_pa = p_bar * BAR_TO_PA
    return [p_pa, "Pa"]

def garden_pressure(stats):
    p_bar = stats["PT0203[Bar]"][STATS_INDEX["mean"]]
    p_pa = p_bar * BAR_TO_PA
    return [p_pa, "Pa"]




def process_measurement(filepath, new_interval=False):
    # Run from script dir
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    path = Path(filepath)

    FILE = path.stem    
    RESULTS_FOLDER = f"results/data_stats/{FILE}"
    STATS_FILE = f"{RESULTS_FOLDER}/{CSV_FILE}"
    CALC_FILE = f"{RESULTS_FOLDER}/{CALCULATIONS_FILE}"

    if new_interval or (not is_valid_file(None, STATS_FILE)):
        stats_of_sample(path, RESULTS_FOLDER)

    stats = pd.read_csv(STATS_FILE)
    STATIC_PRESSURE_FILE = "results/stable_no_flow/average.json"
    with open(STATIC_PRESSURE_FILE, "r") as file:
        calculations = json.load(file)
    

    pipe_diameters = {
        "main"   : 1.38 * 10**-3, # 1.1/4" inner diameter in meters
        "kc"     : 0.82 * 10**-3, #   3/4" inner diameter in meters
        "br_1"   : 1.05 * 10**-3, #     1" inner diameter in meters
        "br_2"   : 0.82 * 10**-3, #   3/4" inner diameter in meters
        "gd_1"   : 1.05 * 10**-3, #     1" inner diameter in meters
        "gd_2"   : 0.82 * 10**-3, #   3/4" inner diameter in meters

    }
    pipe_area = {
        key : value**2 * (math.pi / 2) for key, value in pipe_diameters.items()
    }

    calculations["pipe"] = {
        key : {
            "diameter" : [pipe_diameters[key], "m"],
            "area" : [pipe_area[key], "m2"]
        } for key in pipe_diameters.keys()
    }

    calculations["flow"] = main_flow(stats)
    calculations["pressure"] = main_pressure(stats)
    calculations["room_pressure"] = {
        "kitchen" : kitchen_pressure(stats),
        "bathroom" : bathroom_pressure(stats),
        "garden" : garden_pressure(stats),
    }

    calculations["temp"] = [273.15 + 20, "K"]
    calculations["density"] = [998.204, "kg/m3"]
    calculations["dyn_viscosity"] = [1.002 * 10**(-3), "N*s/m2"]
    calculations["kin_viscosity"] = [calculations["dyn_viscosity"][0] / calculations["density"][0], "m2/s"]
        
    calculations["Re"] = {
        key : (calculations["flow"][0] / value["area"][0]) * value["diameter"][0] / calculations["kin_viscosity"][0] for key, value in calculations["pipe"].items()
    }

    HYDRAULIC_OHM = "hOhm"
    calculations[HYDRAULIC_OHM] = "kg/(m^4 * s)"
    
    # From: P_total - P_room = P_pipe
    calculations["pipe_pressure"] = {key : [calculations["pressure"][0] - value[0], value[1]] for key, value in calculations["room_pressure"].items()}

    p_height = calculations["static_room_pressure_loss"]

    # From: (P_main - P_room) - P_height = R*Q²
    #       P_pipe - P_height = R*Q²
    #       R = (P_pipe - P_height)/Q²
    # The -P_height is here because there is a height difference between the 
    # pump and the room wich gives rise to a pressure difference.
    calculations["R_pipe"] = {key : [(value[0] - p_height[key][0]) / (calculations["flow"][0]**2), HYDRAULIC_OHM] for key, value in calculations["pipe_pressure"].items()}

    # From: (P_room - P_reservoir) - (P_height_appliance - P_height_room) = R*Q² 
    #       P_room - 0 = R*Q²
    #       R_room = R*Q²
    #       R = P_room/Q²
    # The two P_height's are assumed to be identical, which means that the room and appliance is at the same height, and thus cancels out.
    # The hight difference between the appliance and the reservoir also gives rise to a pressure difference, but this is applied after the water exits the appliance and is thus not a part of this formula.
    calculations["R_appliance"] = {key : [value[0] / (calculations["flow"][0]**2), HYDRAULIC_OHM] for key, value in calculations["room_pressure"].items()}

    calculations["R_total"] = {
        key : [value[0] + calculations["R_appliance"][key][0], value[1]] for key, value in calculations["R_pipe"].items()
    }

    with open(CALC_FILE, "w") as outfile: 
        json.dump(calculations, outfile, indent = 4)


    
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

    parser.add_argument(
        "--new_interval",
        action=BooleanOptionalAction,
        default=False,
        help="Specify new interval for sample",
    )

    args = parser.parse_args()
    process_measurement(args.filepath, args.new_interval)