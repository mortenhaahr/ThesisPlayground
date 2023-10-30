
from find_avg_of_sample import process_measurement


DATA_LOC = "../testdata"
Of_interrest = [
    "20230918_1129_steady_half_show_steady",
    "20230918_1136_steady_wash_steady",
    "20230918_1333_steady_washing_KC_stdy",
    "20230921_1200_steady_bt_sink_full_steady",
    "20230921_1232_toilet_test_big_10",
    "20230921_1235_toilet_test_big_20",
    "20230921_1243_toilet_test_big_30",
]

CMD = "find_avg_of_sample.py"

for f in Of_interrest:
    process_measurement(f"{DATA_LOC}/{f}.csv", False)