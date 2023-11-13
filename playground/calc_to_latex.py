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


CALCULATION_FOLDER = "results/data_stats"
SUB_FOLDERS = [ f"{CALCULATION_FOLDER}/{path}" for path in os.listdir(Path(CALCULATION_FOLDER)) if os.path.isdir(Path(f"{CALCULATION_FOLDER}/{path}"))]

CALCULATION_FILE = "calc.json"
OUTPUT_FILE = "calc.tex"

for folder in SUB_FOLDERS:
    with open(Path(f"{folder}/{CALCULATION_FILE}"), "r") as file:
        data = json.load(file)

    pressure_unit = 10**(-9) #Giga

    flow = "{:2.8f}".format(data['flow'][0] * (10**5))
    pressure = "{:.3f}".format(data["pressure"][0])
    r_pipe = [
        value[0]*pressure_unit for _, value in data["R_pipe"].items()
    ]
    r_app = [
        value[0]*pressure_unit for _, value in data["R_appliance"].items()
    ]
    r_total = [
        value[0]*pressure_unit for _, value in data["R_total"].items()
    ]

    with open(Path(f"{folder}/{OUTPUT_FILE}"), "w") as out_file:
        for i in range(3):
            to_print = [
                flow,
                pressure,
                f"{r_total[i]:6f}",
                f"{r_app[i]:6f}",
                f"{r_pipe[i]:6f}"
            ]

            line = " & ".join(to_print)
            out_file.write(line + "\\\\ \hline\n")            

