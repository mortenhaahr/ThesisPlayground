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

        flow = "{:2.8f}".format(data['flow'][0] * (10**5))
        pressure = "{:.3f}".format(data["pressure"][0])
        r_total = "{:.6f}".format(data["R_total"][0] * 10**(-6))
        r_pipe = [
            "{:.6f}".format(data["R_pipe"]["kitchen"][0]*10**(-6)),
            "{:.6f}".format(data["R_pipe"]["bathroom"][0]*10**(-6)),
            "{:.6f}".format(data["R_pipe"]["garden"][0]*10**(-6))
        ]
        r_app = [
            "{:.6f}".format(data["R_appliance"]["kitchen"][0]*10**(-6)),
            "{:.6f}".format(data["R_appliance"]["bathroom"][0]*10**(-6)),
            "{:.6f}".format(data["R_appliance"]["garden"][0]*10**(-6))
        ]

        with open(Path(f"{folder}/{OUTPUT_FILE}"), "w") as out_file:
            for i in range(3):
                to_print = [
                    flow,
                    pressure,
                    r_total,
                    r_app[i],
                    r_pipe[i]
                ]

                line = " & ".join(to_print)
                out_file.write(line + "\\\\ \hline\n")            

