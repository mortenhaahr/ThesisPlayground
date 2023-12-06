# import required module
import os
import json

# assign directory
directory = '../../testdata/dyn_tmp'

"""
NOTE: The following have not been generated, as they can't be determined by PT0102:
../../testdata/dyn_tmp/20231127_1202_dyn_BSink_no_main.csv
../../testdata/dyn_tmp/20231127_0753_dyn_GHose_no_main.csv
../../testdata/dyn_tmp/20231127_0739_dyn_BSink_no_main.csv
../../testdata/dyn_tmp/20231127_1200_dyn_KSink_no_main.csv
../../testdata/dyn_tmp/20231127_0749_dyn_GHose_no_main_high_flow.csv
"""
 
RERUN_EXISTING = False

def find_step_time_from_results(results_folder):
    with open(f"{results_folder}/calc.json", "r") as f:
        data = json.load(f)
        return data["step_start"]["time[s]"]

if __name__ == "__main__":
    # Run from script dir
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    files = os.listdir(directory)
    for f in files:
        file = os.path.join(directory, f)
        results_folder = f"../results/dynamic_props/{f[:-4]}"
        results_exists = os.path.exists(results_folder)
        if RERUN_EXISTING and results_exists:
            step_time = find_step_time_from_results(results_folder)
            os.system(f"python find_time_constant.py -f {file} -s {step_time}")
        elif (not RERUN_EXISTING) and results_exists:
            print(f'Skipping {file}, the result folder already exists.')
            continue
        else: # not results_exists
            print(f"Running interactive on file: {file}")
            os.system(f"python find_time_constant.py -f {file}")
    