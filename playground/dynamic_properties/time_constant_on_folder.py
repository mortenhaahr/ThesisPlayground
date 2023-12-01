# import required module
import os
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
 
if __name__ == "__main__":
    # Run from script dir
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    files = os.listdir(directory)
    for f in files:
        file = os.path.join(directory, f)
        if os.path.exists(f"../results/dynamic_props/{f[:-4]}"):
            print(f'Skipping {file}, the result folder already exists.')
            continue
        print(f"File: {file}")
        os.system(f"python find_time_constant.py -f {file}")
    