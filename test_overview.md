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
- After meeting with Jorge on 21.09, it might seem as if the testdata generated from before this date was generated with tool little pressure in the tank.
- When we came out on the 25.10 to perform more tests, the pump was behaving very oddly. Initially, it didn't work at all so we power cycled.
    - Sometimes it would perform work when no appliance was turned on.
    - Other times it would not perform work when we turned on an appliance
    - Finally, it would sometimes work as expected.
    - We made some tests with this malfunctioning pump. They have been prepended "ano".

### Errors
- The bathroom (CV0202) leakage flow does not change despite changing the setting in PLC
    - TODO: Fixed on tests from: TBD
- The bathroom (CV0202) leakage percentage opening is not logged due to error in PLC code
    - TODO: Fixed on tests from: TBD
- The garden hose (PT0203) sensor data is incorrect in due to error in PLC code
    - TODO: Fixed on tests from: TBD
- The program says we are sampling at a rate of 10Hz but the log files are sampled at 8.33 Hz


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


### 20231025_0750_ano_KC1_full
- Setpoint of pump is at 4 bars but pressure is not reached (see start of data)
- No flow for 20 seconds
- KC1 running full for 80 seconds - doesn't look like it
    - Pump was not doing any work
- No flow for 20 seconds
- Following the test the pump would:
    - About 2 minutes after the pump started increasing the pressure again
    - Have the setpoint LED blinking at 2 bars
    - Indicate unable to reach setpoint pressure (error LED 5 (p. 15 in manual))

### 20231025_0805_ano_toilet_big
- Note that pump had been reset around 2 minutes prior to the test but it was not really doing anything.
- No flow for 20 seconds
- Big toilet flush. Filling for 75 seconds.
- Pump trying to reach setpoint until around 4min20sec.
- Pump stops doing work. Pressure indicator blinking at 2,5 bars

### 20231025_0815_ano_shower_full
- Setpoint changed to 3.5 bars but eventually pump reaches 4 bars...
- No flow for 20 seconds - setpoint not reached
- Shower running full:
    - Until 97 seconds there was very low flow and pump not performing a lot of work
    - The pump then decided to work. Shower running full at intended setpoint pressure until 151 seconds where I turned off.
    - No flow until 201 seconds. Pump doing work for quite a while after. 

### 20231025_0826_ano_garden_full
- Setpoint set back to 4.0 bars. Everything actually seems to be working as intended.
- No flow for 20 seconds
- Garden full for 60 seconds.
- No flow for 60 seconds. Pump eventually turns off. Everything seems good.


### 20231025_0836_ano_sanity_garden_full
- Setpoint still on 4.0 bars
- Turned on garden hose to provide flow of around 10 l/min for 15min20s.
  - (I went away during most of the test)
- No flow for 2min.
- When done with the test pressure indicator blinking at 3,5 bars
- Conclusion: It looks better than some of the earlier tests but still not desired behaviour

### 20231025_0916_ano_trans_toilet_big
- Note: Test pressure indicator blinking at 3,5 bars
- BV0103 valve turned at 30 seconds
- Toilet big flush at 60 seconds
- BV0103 turned again at 90 seconds
- Pump done filling cisterne at around 2min20
    - Behaving as expected
- Measurement stopped at 2min50

### 20231025_0934_ano_trans_KC1_full
- Note: Test pressure indicator blinking at 3,5 bars
- BV0103 valve turned at 30 seconds
- KC1 turned to full at 60 seconds
- BV0103 valve turned again at 90 seconds
- KC1 turned off at 150 seconds
- No flow until 210 seconds
    - Pump was doing work until 3min10.

### 20231025_1216_ano_KC1_LF_mode
- No flow 30 seconds
- 16 seconds to adjust sink
- Until around 10min it is behaving normally but not going into LF mode
- After 10min It takes a big dip in pressure and then slowly increases pressure.
- After 16min the pressure plummets again only to increase slowly first then steadily.

### XXXX_stable_appliance
- No flow for xx seconds
- At xx seconds turn the appliance to full
- xx seconds steady flow
- At xx seconds shut off appliance
- xx in steady 0 flow (pump wierdness)

### XXXX_stable_shower_xL
- No flow for xx seconds
- xx seconds to adjust shower to about xL
- xx seconds steady flow at about xL
- At xx seconds shut off shower
- xx in steady 0 flow (pump wierdness)

### xxxx_stable_wsm_gd_hose_full
- No flow for xx seconds
- At xx open the washing mashine
  - The first 2 mins are basically crap due to pump error...
- After pump stabilised xx seconds of steady washing mashine
- Open Garden hose full
- Steady with both for xx seconds
- Close washing mashine
- Pump error for xx seconds
- Stable garden hose full for xx seconds
- Close garden hose
- Steady 0 flow for xx seconds

### xxxx_stable_br_shower_gd_hose_full
- No flow for xx seconds
- Open shower at full capacity
- Pump settling due to error for xx seconds
- Steady shower only flow for xx seconds
- Open garden hose at full capacity (xx seconds)
- Pump settling due to error for xx seconds
- Steady both for xx seconds
- Close shower 
- Pump settling due to error for xx seconds
- Steady garden hose ony for xx seconds
- Close garden hose
- Steady 0 flow for xx seconds