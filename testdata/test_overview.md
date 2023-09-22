### TMP:
- Missing tests:
    - Make tests determining how long the toilets should be pressed until we start seeing different behaviour
    - A lot with leakages

### Ways of control
- Shower: Mechanical valve
- Washing machine: Binary valve
- Garden hose: Mechanical valve
- Faucets: Mechanical valve
- Toilet: Press buttons with two settings. Big flush will empty cisterne of around 7,5 liters or keep flushing until let go. Small flush will empty cisterne of around 4,5 liters or or keep flushing until let go.
- Bathroom leakage:
    - Controllable electronic valve.
    - Manual mechanical valve.
        - Blue and red valve. Blue is quick on/off, red can turn for a while.
- Kitchen leakage: Mechanical valves.
    - Blue and red valve. Blue is quick on/off, red can turn for a while.
- Garden leakage: Mechanical valves.
    - Blue and red valve. Blue is quick on/off, red can turn for a while.
- Pump leakage: Controllable electronic valve.

### Max values
- Kitchen sink: $\approx 2.6$ l/min
- Washing machine: $\approx 19$ l/min
- Bathroom sink: ? l/min
- Shower: $\approx 10$ l/min
- Toilet: $\approx 7,5$ l/min (but we have seen it be around 7 l/min depending on day)
- Garden hose: $\approx 26.7$ l/min

### Other
- Unless otherwise indicated: LOWFLOW_MODE is on.
- Toilet: A small flush will empty the cisterne for around 37 seconds (?). A big flush will empty is for around 60 seconds.

### Errors
- The bathroom (CV0202) leakage flow does not change despite changing the setting in PLC
    - TODO: Fixed on tests from: TBD
- The bathroom (CV0202) leakage percentage opening is not logged due to error in PLC code
    - TODO: Fixed on tests from: TBD
- The garden hose (PT0203) sensor data is incorrect in due to error in PLC code
    - TODO: Fixed on tests from: TBD


### 20230918_1129_steady_half_show_steady:
- No flow for 60 seconds
- Shower on 5 L for 240 seconds
- No flow for 60 seconds

### 20230918_1136_steady_wash_steady
- No flow for 30 seconds
- Washing machine on for 60 seconds
- No flow for 30 seconds

### 20230918_1141_steady_full_shower_steady
- No flow for 30 seconds
- Shower on 100 % for 60 seconds
- No flow for 30 seconds

### 20230918_1143_steady_0.75_garden_steady
- No flow for 30 seconds
- Garden hose on 75 % for 60 seconds
- No flow for 30 seconds

### 20230918_1203_steady_garden_full_stdy
- No flow for 30 seconds
- Garden hose on 100 % for 60 seconds
- No flow for 30 seconds

### 20230918_1207_steady_LF_KC_15_stdy
- No flow for 60 seconds
- Kitchen sink on ~25 % for 15 minutes
    - Note that LOWFLOW_MODE does not appear to turn on despite the option being on
- No flow for 60 seconds

### 20230918_1225_steady_LF_OFF_KC_15_stdy
- LOWFLOW_MODE is turned off
- No flow for 60 seconds
- Kitchen sink on ~6 % for 15 minutes
- No flow for ~7 minutes

### 20230918_1207_steady_LF_KC_15_stdy
- No flow for 60 seconds
- Adjusting sink level for around 20 seconds
- Kitchen sink on ~21 % for 15 minutes
    - Note outlet pressure is very interesting on this one. 
    - We have some weird dives for the first ~10 minutes (TODO: clarification from Jorge needed)
    - The pump then goes into LOWFLOW_MODE
- No flow for 60 seconds

### 20230918_1318_steady_WC_big_stdy
- No flow for 30 seconds
- Toilet big flush filling for around 60 seconds
- No flow for 60 seconds

### 20230918_1322_steady_C1_shower_half_stdy
- No flow for 30 seconds
- Kitchen sink 100 % for 30 seconds
- Kitchen sink 100 % and shower on 50 % for 90 seconds
- No flow for 60 seconds

### 20230918_1326_steady_both_C1s_stdy
- No flow for 30 seconds
- Kitchen sink and bathroom sink 100 % for 60 seconds
- No flow for 60 seconds

### 20230918_1329_steady_KC_run_2_HWash_stdy
- No flow for 30 seconds
- Kitchen sink 100 % for 30 seconds
- Kitchen sink and bathroom sink 100 % for 30 seconds
- Kitchen sink 100 % for 30 seconds
- Kitchen sink and bathroom sink 100 % for 30 seconds
- No flow for 30 seconds

### 20230918_1333_steady_washing_KC_stdy
- No flow for 30 seconds
- Washing machine on for 30 seconds
- Washing machine on and kitchen sink 100 % for 60 seconds
- Small transition period where sink is off but we walk to PCL and turn off washing machine
- No flow for 30 seconds

### 20230918_1336_steady_KC_WC_small_stdy
- No flow for 30 seconds
- Kitchen sink 100 % for 30 seconds
- Kitchen sink 100 % and toilet small flush for 45 seconds
- No flow for 30 seconds

### 20230918_1339_steady_WC_small_KC_stdy
- No flow for 30 seconds
- Small transition between turning kitchen sink on and flushing toilet
- Kitchen sink 100 % and toilet small flush for $\approx 10$ seconds
- Toilet small flush for $\approx 35$ seconds
- No flow for 30 seconds

### 20230920_0912_steady_WC_small_steady
- No flow for 30 seconds
- Small flush for around 37 seconds
- No flow for 60 seconds

### 20230920_1013_steady_50leak_Bath_steady
- No flow for 40 seconds
- Bathroom leakage 50 % for around 80 seconds
- No flow for 50 seconds

### 20230921_1200_steady_bt_sink_full_steady
- No flow for 30 seconds
- Bathroom sink full for 60 seconds
- No flow for 30 seconds

### 20230921_1219_kc_leakage_full
- Red kitchen leakage valve turned to max. Blue turned off.
- No flow for 20 seconds
- Blue kitchen leakage valve turned on for 12 seconds
    - Container on weight started emptying
- No flow for 30 seconds

### 20230921_1223_garden_leakage_full
- Red garden leakage valve turned to max. Blue turned off.
- No flow for 20 seconds
- Blue garden leakage valve turned on for 13 seconds
    - Container on weight started emptying
- No flow for 30 seconds

### 20230921_1228_bt_manual_leakage_full
- Red bathroom leakage valve turned to max. Blue turned off.
- No flow for 20 seconds
- Blue bathroom leakage valve turned on for 13 seconds
    - Container on weight started emptying
- No flow for 30 seconds

### 20230921_1232_toilet_test_big_10
- No flow for 20 seconds
- Toilet big flush held for 10 seconds
- Filling cisterne for 60 seconds (?)
    - This started happening while holding big flush
- No flow for around 30 seconds

### 20230921_1235_toilet_test_big_20
- No flow for 20 seconds
- Toilet big flush held for 20 seconds
- Filling cisterne for 77 seconds
    - This started happening while holding big flush
- No flow for around 30 seconds

### 20230921_1243_toilet_test_big_30
- No flow for 20 seconds
- Toilet big flush held for 30 seconds
- Filling cisterne until around 123 seconds
    - This started happening while holding big flush
- No flow for around 30 seconds