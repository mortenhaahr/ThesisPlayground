
# Header description of CSV files

This document lists and describes the different header values in the CSV files generated on the Grundfos setup.

TO FIX:
    CV0202 (leak bathroom) is missing <br>
        Talk to Jorge about opening the project in visual studio
        Found the logging inP_FastLog.TcPOU and found some issues:
            PT0301[Bar] is set twice, once correctly and once to P_Valves.CV0201.M_GetPosition().

            PT0203[Bar] is set to P_Valves.CV0201.M_GetPosition() instead of P_Sensors.PT0203.rValue.

    Figure out if FT0401 is really in m3/h and if that makes sense..




| Header name          	| Unit  	| Description                                                                           	| Keep (y/n) 	|
|----------------------	|-------	|---------------------------------------------------------------------------------------	|------	|
| YYYY-MM-DD-HH:MM:SS  	| time  	| The time of the measurement                                                           	| y    	|
| FT0101[l/m]          	| l/m   	| The flow out of the pump external                                                     	| y    	|
| FT0401[m3/h]         	| m3/h  	| The total flow from leakages                                                          	| y    	|
| PT0101[Bar]          	| Bar   	| The pressure at the reservoir. Always 0.                                              	| n    	|
| PT0102[Bar]          	| Bar   	| The pressure after the pump external                                                  	| y    	|
| PT0201[Bar]          	| Bar   	| The pressure at the kitchen                                                           	| y    	|
| PT0202[Bar]          	| Bar   	| The pressure at the bathroom                                                          	| y    	|
| PT0301[Bar]          	| Bar   	| Something with hot water                                                              	| n    	|
| PT0302[Bar]          	| Bar   	| Something with hot water                                                              	| n    	|
| PT0303[Bar]          	| Bar   	| Something with hot water                                                              	| n    	|
| CV0201[%]            	| %     	| Probably control amount on pre manifold leak                                          	| y    	|
| CV0202[%]            	| %     	| Probably control amount on bathroom leak                                                	| y    	|
| PT0203[Bar]          	| Bar   	| The pressure at the garden                                                            	| y    	|
| PT0301[Bar]          	| Bar   	| Something with hot water                                                              	| n    	|
| act_mode3            	| ?     	| ?                                                                                     	| n    	|
| act_mode1            	| ?     	| ?                                                                                     	| n    	|
| act_mode4            	| ?     	| ?                                                                                     	| n    	|
| p                    	| W     	| The power draw of the pump                                                            	| y    	|
| t_w[K]               	| K     	| The water temperature at the pump                                                     	| y    	|
| speed[RPM]           	| RPM   	| The rotational speed of either the impeller or the moter                              	| y    	|
| outlet_pressure[Bar] 	| Bar   	| The pressure at the pump outlet from internal pump sensor                             	| y    	|
| p_lo_min[W]          	| W     	| The minimum power draw of the pump. Always 0.                                         	| n    	|
| p_lo_max[W]          	| W     	| The maximum power draw of the pump. Always 573.                                       	| n    	|
| DBB_ANTI_CYCLING_TRI 	| ?     	| ?                                                                                     	| n    	|
| DBB_ANTI_CYCLING_TIM 	| ?     	| ?                                                                                     	| n    	|
| equal_period_count   	| ?     	| ?                                                                                     	| n    	|
| time_in_stop         	| ?     	| Probably a counter which keeps track of cycles between wakeup periods                 	| n    	|
| last_time_in_stop    	| ?     	| ?                                                                                     	| n    	|
| speed_avedev         	| Num   	| Probably the derivative of the average speed of the motor                             	| n    	|
| M2_warning_out       	| ?     	| ?                                                                                     	| n    	|
| M2_alarm_out         	| ?     	| ?                                                                                     	| n    	|
| M2_reset_out         	| ?     	| ?                                                                                     	| n    	|
| M2_cntCycles         	| ?     	| ?                                                                                     	| n    	|
| M2_pumpToff          	| ?     	| ?                                                                                     	| n    	|
| M2_pumpToffAvg       	| ?     	| ?                                                                                     	| n    	|
| M2_pumpToffVar       	| ?     	| ?                                                                                     	| n    	|
| M2_algState          	| ?     	| ?                                                                                     	| n    	|
| M3_warning_out       	| ?     	| ?                                                                                     	| n    	|
| M3_alarm_out         	| ?     	| ?                                                                                     	| n    	|
| M3_reset_out         	| ?     	| ?                                                                                     	| n    	|
| M3_cumVol            	| ?     	| ?                                                                                     	| n    	|
| M3_edgeType          	| ?     	| ?                                                                                     	| n    	|
| M3_edgeDetectionStat 	| ?     	| ?                                                                                     	| n    	|
| M3_maxVol_warning    	| ?     	| ?                                                                                     	| n    	|
| M3_maxVol_alarm      	| ?     	| ?                                                                                     	| n    	|
| M3_Tevent            	| ?     	| ?                                                                                     	| n    	|
| M2_cumVol            	| ?     	| ?                                                                                     	| n    	|
| M3_qAvg              	| ?     	| ?                                                                                     	| n    	|
| pump_output_control_ 	| ?     	| Probably an internal variable in the PLC                                              	| n    	|
| M2_plumbingCheck_cnt 	| ?     	| ?                                                                                     	| n    	|
| M2_plumbingCheck_cnt 	| ?     	| ?                                                                                     	| n    	|
| M2_plumbingCheck_cnt 	| ?     	| ?                                                                                     	| n    	|
| M2_plumbingCheck_dpd 	| ?     	| ?                                                                                     	| n    	|
| M2_PlumbingCheck_fla 	| ?     	| ?                                                                                     	| n    	|
| M2_PlumbingWarning   	| ?     	| ?                                                                                     	| n    	|
| FT0106               	| ?     	| Flow at one of the alternate flow sensors in the setup. Probably the encased one      	| n    	|
| PT0106               	| Bar   	| Pressure after the initial flow measurement                                           	| n    	|
| FT0103               	| ?     	| Flow at one of the alternate flow sensors in the setup. Probably the constricting one 	| n    	|
| FT0104               	| ?     	| ?                                                                                     	| n    	|
| FT0105               	| l/m   	| Flow at the triple split flow sensor. This is the 'vanilla' one.                      	| y    	|
| PV0106               	| ?     	| ?                                                                                     	| n    	|
| SC0401               	| ? (g) 	| The scale that is used to detect small leakages.                                      	| y    	|
| M2_stp_alg           	| ?     	| ?                                                                                     	| n    	| 
