# import required module
import os
import multiprocessing
import subprocess
# assign directory
directory = '../testdata'

def do_work(f):
    file = os.path.join(directory, f)
    if os.path.isfile(file) and file.endswith(".csv"):

        #subprocess.call(["python", "playground.py", "-f", file], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        os.system(f"python playground.py -f {file}")
 
if __name__ == "__main__":
    # iterate over files in
    # that directory
    with multiprocessing.Pool() as pool:
        pool.map(do_work,  os.listdir(directory))
    