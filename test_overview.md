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

### 20231101_0919_stable_shower
- No flow for 44 seconds
- Turn the shower to full
- Pump settling due to error 
- At 117 seconds steady flow begins
- At 228 seconds the pump determines flow
- Flow determined and back to steady at 280 seconds
- At 395 seconds pump determines flow
- At 472 seconds the flow is steady again
- At 535 seconds the shower is shut off
- The sysem is in 0 flow state for the remainder of the sample

### 20231101_1108_stable_kc_sink
- No flow for 2 seconds
- Turn the kitchen sink to full
- Steady flow for 126 seconds
- Pump measures flow rate for the remainder of the sample

### 20231101_1111_stable_wsm
- No flow for 26 seconds
- The washing mashine in the kitchen is turned on
- After stabilizing, the flow is steady untill 152 seconds
- Pump error untill 263 seconds
- The flow is steady untill 330 seconds
- The washing mashine is turned off
- The flow is steady at 0 for the remainder of the sample

### 20231101_1117_stable_br_sink
- No flow for 17 seconds
- The sink in the bathroom is turned to max
- The flow is steady but falling untill 144 seconds
- The pump tries to determine flow untill 197 seconds
- The flow is steady untill 317 seconds
- The pump tries to determine flow untill 349 seconds
- The bathroom sink is turned off
- Steady 0 flow untill end of sample

### 20231101_1124_stable_br_toilet_big
- No flow for 25 seconds
- A big flush is made in the toilet for 2 seconds
- The cisterne is being filled untill 81 seconds
- The rest of the sample is without action
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1127_stable_br_show_full
- No flow for 19 seconds
- The shower is opened all the way 
    - Takes about 3 seconds
- Steady flow untill 113 seconds
- The shower is turned off
    - Takes about 3 seconds
- No flow for the rest of the sample

### 20231101_1130_stable_br_toilet_small
- No flow for 30 seconds
- A small flush is made in the toilet (2 seconds)
- Cisterne is filled untill 66 seconds
- The cisterne is filled
- No flow for the rest of the sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1133_stable_gd_hose_full
- No flow for 26 seconds
- The garden hose is opened all the way 
    - Takes 7 seconds
- Steady flow untill 147 seconds
- The garden hose is shut off
    - Takes 7 seconds
- No flow for the rest of the sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1137_stable_wsm_shower_full
- No flow for 33 seconds
- The washing mashine is opened 
- Steady flow untill 90 seconds
- The shower is opened all the way
- Steady flow untill 159 seconds
- Pump has an error untill 192 seconds
- Steady flow of both appliances untill 255 seconds
- The washing mashine is shut off
- The pump is behaving wierdly untill 334 seconds
- Steady flow of the shower untill 402 seconds
- The shower is turned off
- I don't know what i did at 514 secs...
    - Probably a small shower flow to see what the pump was doing
    - Check this later

### 20231101_1149_stable_shower_2L
- No flow for 13 seconds
- The shower is tuned to about 2L of flow
    - Done at 100 seconds
- Steady flow of shower at about 2L untill 168 seconds
- Pump does flow measurement untill 209 seconds
- Steady flow of shower at about 2L untill 287 seconds
- The shower is turned off
- Steady 0 flow untill end of sample

### 20231101_1155_stable_shower_3L
- No flow for 4 seconds
- Shower is tuned to about 3L of flow
    - untill 30 seconds
- Steady flow at about 3L untill 116 seconds
- Shower is turned off 
    - Takes about 4 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1159_stable_shower_4L
This sample was cought in a logging error, so the sample starts a bit different from other samples.
- The shower is tuned to about 4L of flow
    - Takes untill 21 seconds
- Steady flow at about 4L untill 110 seconds
- Shower is turned off
    - takes 6 seconds
- Steady 0 flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure


### 20231101_1202_stable_shower_5L
- No flow for 8 seconds
- Shower is tuned to about 5L of flow
    - Takes 24 seconds
- Steady flow at about 5L untill 133 seconds
- Shower is turned off
    - Takes 5 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1206_stable_shower_6L
- No flow for 5 seconds
- Shower is opened and tuned to about 6L of flow
    - Done at 23 seconds
- Steady flow at about 6L of flow untill 132 seconds
- Pump does something wierd untill 174 seconds
    - The pump is behaving wierdly and takes a while to rebuild the pressure
- Steady flow at about 6L of flow untill 248 seconds
- Shower is turned off 
    - Takes 5 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1211_stable_shower_7L
- No flow for 6 seconds
- The shower is opened and tuned to about 7L of flow
    - Done at 29 seconds
- Steady flow at about 7L of flow untill 117 seconds
- Shower is turned off 
    - Done at 123 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1215_stable_shower_full
This sample was subject to a logging error and therefore starts a bit differently from most other samples.
- Shower is turned all the way up 
    - Steady at 6 seconds
- Steady flow untill 114 seconds
- Shower is turned off
    - Takes 5 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure
### 20231101_1218_stable_kc_sink
- No flow for 9 seconds
- The sink in the kitchen is opened all the way
    - Stable at 20 seconds
- Stable flow untill 100 seconds
- Sink is closed
    - Takes 4 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1222_stable_wsm
- No flow for 19 seconds
- The washing mashine is started
    - Fully open at 35 seconds
- Steady flow untill 127 seconds
- The washing mashine is turned off
    - Takes 5 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1224_stable_br_sink
- No flow for 12 seconds
- The bathroom sink is opened all the way
    - Takes 3 seconds
- The pump is in oscilation (low flow) mode untill 131 seconds
- The sink is turned off
    - Takes 5 seconds
- No flow untill 174 seconds
- The bathroom sink is opened all the way
    - Takes 4 seconds
- Steady flow with pump in normal operation untill 277 seconds
- Bathroom sink is turned off
    - Takes 6 seconds
- No flow for rest of sample

### 20231101_1239_stable_gd_hose_full
- No flow for 10 seconds
- The garden hose is opened fully
    - Takes 7 seconds
- Stable flow through fully open garden hose
    - Steady untill 123 seconds
- Garden hose is closed fully
    - Takes 7 seconds
- No flow for rest of sample


### 20231101_1242_stable_main_leak_full
- No flow for 28 seconds
- Main leak is fully opened 
    - Takes 7 seconds
- Steady flow out of main leak untill 135 seconds
- The main leak is fully closed
    - Takes 7 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1246_stable_br_leak_full
- No flow for 22 seconds
- The bathroom leak is opened to 100%
    - Takes 5 seconds
- Steady flow out of fully opened bathroom leak untill 131 seconds
- The bathroom leak is fully closed
    - Takes 8 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1250_stable_br_leak_full
This sample was subject to a logging error. No noticable difference in the data though.
- No flow for 4 seconds
- The bathroom leak is opened to 100%
    - Takes 9 seconds
- Steady flow out of fully opened bathroom leak untill 120 seconds
- The bathroom leak is fully closed
    - Takes 8 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1254_stable_main_leak_full
This sample was subject to a logging error. No noticable difference in the data though.
- No flow for 2 seconds
- The main pipe leakage is opened to 100%
    - Takes 7 seconds
- Steady flow out of main leakge untill 120 seconds
- The main pipe leakage is fully closed
    - Takes 8 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1258_stable_wsm_gd_hose_full
- No flow for 20 seconds
- Open the washing mashine
    - Takes 5 seconds
- Steady flow untill 42 seconds
- Pump error untill 134 seconds
    - No idea why this happened.
- After pump stabilised, steady washing mashine flow untill 230 seconds
- Garden hose was opened fully
    - Takes 5 seconds
- Steady flow of both garden hose and washing mashine untill 345 seconds
- The washing mashine is turned off
    - Takes 6 seconds
- The pump shuts itself off and is very slow to reestablish itself
    - Takes untill 425 seconds
- Stable garden hose full untill 526 seconds
- Close garden hose
    - Takes 6 seconds
- Steady 0 flow for rest of sample
    - One power and pressure sample is a total outlier in this steady 0 flow. The pressure rose to over 20 bar and the power consumption was above 6000 Watts.

### 20231101_1308_stable_br_shw_gd_hose_full
- No flow for 17 seconds
- Open shower at full capacity
    - Takes 4 seconds
- Steady shower flow untill 26 seconds
- Pump settling due to error untill 79 seconds
- Steady shower only flow untill 164 seconds
- Open garden hose at full capacity
    - Takes 8 seconds
- Steady flow of both shower and garden hose untill 194 seconds
- Pump settling due to error untill 267 seconds
- Steady both untill 362 seconds
- Close shower 
    - Takes 5 seconds
- Pump settling due to error untill 386 seconds
- Steady garden hose only untill 483 seconds
- Close garden hose
    - Takes 7 seconds
- No action for rest of sample
    - One power and pressure sample is a total outlier in this steady 0 flow. The pressure rose to over 20 bar and the power consumption was above 6000 Watts.

### 20231101_1319_stable_shower_1L
- No flow for 34 seconds
- Shower is tuned to about 1L
    - Takes untill 182 seconds
- Flow at about 1L untill 479 seconds
    - The pump is in hysteresis mode where it charges the hyrdophore, stops and then recharges the hydrophor after some time.
- The shower is turned off
    - Takes 3 seconds
- No flow for rest of sample

### 20231101_1328_stable_shower_2L
- No flow for 14 seconds
- The output of the shower is tuned to about 2L
    - Tuning done at 123 seconds
- The flow of the shower is steady at about 2L untill 226 seconds
- The shower is turned off  
    - Takes 6 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1333_stable_shower_3L
This sample was subject to a logging error. No noticable difference in the data though.
- No flow for 3 seconds
- The output of the shower is tuned to about 3L
    - Tuning done at 25 seconds
- The flow of the shower is steady at about 3L untill 115 seconds
- The pump tests the flow rate and does not go back into the same mode 
    - Lasts untill 223 seconds
- The shower is turned off  
    - Takes 5 seconds
- No flow for rest of sample

### 20231101_1338_stable_shower_4L
This sample was subject to a logging error. No noticable difference in the data though.
- No flow for 10 seconds
- The output of the shower is tuned to about 4L
    - Tuning done at 33 seconds
- The flow of the shower is steady at about 4L untill 145 seconds
- The shower is turned off  
    - Takes 8 seconds
- No flow for rest of sample
    - The pump is behaving wierdly and takes a while to rebuild the pressure

### 20231101_1342_stable_shower_5L
This sample was subject to a logging error. No noticable difference in the data though.
- No flow for 5 seconds
- The output of the shower is tuned to about 5L
    - Tuning done at 25 seconds
- The flow of the shower is steady at about 5L untill 113 seconds
- The shower is turned off  
    - Takes 5 seconds
- No flow for rest of sample

### 20231101_1345_stable_shower_full
This sample was subject to a logging error. No noticable difference in the data though.
- No flow for 10 seconds
- The output of the shower is turned all the way up
    - Takes 9 seconds
- The flow of the shower is lower than expected (due to pressure) so the shower dial is turned up and down to investigate and ultimately closed.
    - Done at 37 seconds
- No flow untill 45 seconds
- The shower is opened all the way
    - Takes 8 seconds
- Steady flow out of shower untill 148 seconds
- The shower is turned off  
    - Takes 5 seconds
- No flow for rest of sample

