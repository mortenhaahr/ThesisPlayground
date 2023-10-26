
from find_avg_of_sample import stats_of_sample


DATA_LOC = "../testdata"
Of_interrest = [
    "20230921_1232_toilet_test_big_10",
    "20230921_1235_toilet_test_big_20",
    "20230921_1243_toilet_test_big_30"
]

CMD = "find_avg_of_sample.py"

for f in Of_interrest:
    stats_of_sample(f"{DATA_LOC}/{f}.csv")