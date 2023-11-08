
from find_avg_of_sample import process_measurement
import os
from pathlib import Path

DATA_LOC = "../testdata/stable_measurements"
Of_interrest = [
    path for path in os.listdir(Path(DATA_LOC)) if os.path.isfile(os.path.join(DATA_LOC, path))
]

CMD = "find_avg_of_sample.py"

for f in Of_interrest:
    process_measurement(Path(f"{DATA_LOC}/{f}"), False)