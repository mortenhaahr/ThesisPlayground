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
import pressure_diffs_no_flow 


pressure_diffs_no_flow.run() #Generate intervals and find pressure difference in rooms

# Find the average of all the results
CALCULATIONS_FILE = "calc.json" 
OUTPUT_FILE_NAME = "average.json"

DATA_LOC = "../results/stable_no_flow"
OUTPUT_FILE = f"{DATA_LOC}/{OUTPUT_FILE_NAME}"

Of_interrest = [
    os.path.join(DATA_LOC, path) for path in os.listdir(Path(DATA_LOC)) if os.path.isdir(os.path.join(DATA_LOC, path))
]

def calc_average(paths, output_file):
    # Run from script dir
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    p_diff = {
        "kitchen"  : [],
        "bathroom" : [],
        "garden"   : []
    }

    missing = {
        "kitchen"  : 0,
        "bathroom" : 0,
        "garden"   : 0
    }

    for p in paths:
        file_path = Path(f"{p}/{CALCULATIONS_FILE}")
        with open(file_path, "r") as file:
            calc_data = json.load(file)
            for key, value in calc_data["room_pressure_diff"].items():
                room_pressure = calc_data["room_pressure"][key][0]
                if room_pressure < 1: #missing measurements
                    missing[key] = missing[key] + 1
                    continue
                p_diff[key].append(value[0])

    description = dict()
    for key in p_diff.keys():
        desc = pd.DataFrame.from_dict({key : p_diff[key]}).describe()
        description.update(desc.to_dict())

    calculations = {
        "static_room_pressure_loss" : {
            key : [value["mean"], "Pa"] for key, value in description.items()
        }
    }

    calculations["density"] = [998.204, "kg/m3"]
    calculations["gravity"] = [9.82, "m/s2"]

    calculations["room_height"] = {
        key : [value[0] / (calculations["density"][0] * calculations["gravity"][0]), "m"] for key, value in calculations["static_room_pressure_loss"].items()
    }

    with open(output_file, "w") as file:
        json.dump(calculations, file)


calc_average(Of_interrest, OUTPUT_FILE)
calc_average([path for path in Of_interrest if "20231101" in f"{path}"], f"{DATA_LOC}/20231101_{OUTPUT_FILE_NAME}")
calc_average([path for path in Of_interrest if "20231101" not in f"{path}"], f"{DATA_LOC}/not_20231101_{OUTPUT_FILE_NAME}")