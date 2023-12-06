# import required module
import os
import json

# assign directory
directory = "../../testdata/dyn_tmp"

RERUN_EXISTING = False

# Map of files that requires other sensors
REQUIRES_OTHER_SENSORS_MAP = {
    (
        "20231127_0735_dyn_KSink_no_main.csv",
        "20231127_1200_dyn_KSink_no_main.csv",
    ): "PT0201[Bar]",
    (
        "20231127_1202_dyn_BSink_no_main.csv",
        "20231127_0739_dyn_BSink_no_main.csv",
    ): "PT0202[Bar]",
    (
        "20231127_0753_dyn_GHose_no_main.csv",
        "20231127_0749_dyn_GHose_no_main_high_flow.csv",
        "20231127_1204_dyn_GHose_no_main.csv",
    ): "PT0203[Bar]",
}


def find_step_time_from_results(results_folder):
    with open(f"{results_folder}/calc.json", "r") as f:
        data = json.load(f)
        return data["step_start"]["time[s]"]


def find_alternative_sensor(filename):
    for key, value in REQUIRES_OTHER_SENSORS_MAP.items():
        if filename in key:
            return value
    return None  # Return None if the filename is not found included


if __name__ == "__main__":
    # Run from script dir
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    files = os.listdir(directory)
    for f in files:
        sensor = "PT0102[Bar]"
        if "no_main" in f and (sensor := find_alternative_sensor(f)) == None:
            print(
                f"Skipping {f} since we can't use PT0102 and alternative wasn't found in REQUIRES_OTHER_SENSORS_MAP"
            )
            continue
        # Otherwise we use alternative sensor

        file = os.path.join(directory, f)
        results_folder = f"../results/dynamic_props/{f[:-4]}"
        results_exists = os.path.exists(results_folder)
        if RERUN_EXISTING and results_exists:
            step_time = find_step_time_from_results(results_folder)
            os.system(
                f"python find_time_constant.py -f {file} -s {step_time} -p {sensor}"
            )
        elif (not RERUN_EXISTING) and results_exists:
            print(f"Skipping {file}, the result folder already exists.")
            continue
        else:  # not results_exists
            print(f"Running interactive on file: {file}")
            os.system(f"python find_time_constant.py -f {file} -p {sensor}")
