# usefull data for UI_report
test_type = ["Standalone test","Integration test"]
            
inverter = {
            "Pacman 5": [
                            "RD4021",
                            "ID1PH_R290", 
                            "Ariston"
                        ],
            "1 UP": [
                        "RD4021", 
                        "RD4018"
                    ]
            } 
header_row_default = 5      # Default header row for TDM error-fault XLSX files (1-based index)
sw_version = "2.6.00"

header_default_table = { 
                        "Pacman 5": [
                                        "Test Number",
                                        "TEST EVENTS", 
                                        "TEST SCOPE", 
                                        "FAULTS EXPECTED",
                                        "TDM LOG FILE",
                                        "MODBUS LOG FILE",
                                        "TEST RESULT",
                                        "TEST SUMMARY"
                                    ],
                        "1 UP": [   
                                    "Test Number",
                                    "TEST EVENTS", 
                                    "TEST SCOPE", 
                                    "FAULTS EXPECTED",
                                    "TDM LOG FILE",
                                    "LIN LOG FILE",
                                    "MODBUS LOG FILE",
                                    "TEST RESULT",
                                    "TEST SUMMARY"
                                ]
                        }
time_data_set = ["Absolute time", "Relative Time"]

error_list_LIN = { 0:{
                        "Name": "NO error",
                        "error_type": "Status"
                        },                    
                    1:{
                        "Name": "Driver fault",
                        "error_type": "Final error"
                        },
                    2:{
                        "Name": "Over current",
                        "error_type": "Error"
                        },
                    3:{
                        "Name": "Blocked rotor",
                        "error_type": "Final error"
                        },  
                    5:{
                        "Name": "Overload motor",
                        "error_type": "Error"
                        },
                    6:{
                        "Name": "Overvoltage",
                        "error_type": "Error"
                        },
                    7:{
                        "Name": "Undervoltage fast drop",
                        "error_type": "Error"
                        },
                    8:{
                        "Name": "Over speed",
                        "error_type": "Error"
                        },  
                    9:{
                        "Name": "Turbine mode",
                        "error_type": "Error"
                        },
                    10:{
                        "Name": "Undervoltage slow drop",
                        "error_type": "Error"
                        },
                    12:{
                        "Name": "Over temperature motor",
                        "error_type": "Error"
                        },
                    14:{
                        "Name": "Over temperature module",
                        "error_type": "Error"
                        },  
                    15:{
                        "Name": "Over temperature power bridge",
                        "error_type": "Error"
                        },
                    16:{
                        "Name": "Generator operation",
                        "error_type": "Warning"
                        },
                    17:{
                        "Name": "Dry running",
                        "error_type": "Warning"
                        },
                    18:{
                        "Name": "Overload motor",
                        "error_type": "Warning"
                        },
                    19:{
                        "Name": "Over temperature module",
                        "error_type": "Warning"
                        },
                    20:{
                        "Name": "Blocked rotor",
                        "error_type": "Warning"
                        },
                    21:{
                        "Name": "Medium temperature sensor",
                        "error_type": "Warning"
                        }
                }

status_TDM = {
                1: "ODU is in Stand-by",
                11: "Waiting to start generator in heating",
                12: "EXV reset state heating",
                13: "EXV Init state heating",
                14: "startup heating",
                15: "Modulation heating",
                16: "Modulation Booster heating",
                17: "Rating heating",
                18: "Defrost",
                19: "Hard stop",
                21: "Waiting to start generator in cooling",
                22: "EXV reset state cooling",
                23: "EXV Init state cooling",
                24: "startup cooling",
                25: "Modulation cooling",
                26: "Modulation Booster cooling",
                27: "Rating cooling",
                28: "Pump Down (not implement in TDM4)",
                32: "Generator switching off procedure - heating",
                33: "Generator switching off procedure - cooling",
                40: "Defrost manual",
                51: "fault state",
                52: "hard fault state",
                101: "TDM4 is initializing the ODU",
                150: "the OTA is completed and the TDM4 is preparing the ODU before lunching the upgrading",
                253: "PC Control",
                254: "Setup Mode"
            }

DEFAULT_TEST_STEPS_PACMAN5 = {1: [{ 
                                    "action": "highlight_column",
                                    "column": ["DSP_MAIN_VERSION_EcoKing",
                                            "PB_DSP_FW2",
                                            "HW_VERSION_EcoKing",
                                            "EEPROM_VERSION_EK_RD",
                                            "HP CTRL BOX ID RD",
                                            "Fault_Code"                      
                                            ],
                                    "color": "FFFF00"
                                }, 
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "validate_version",
                                    "column": ["DSP_MAIN_VERSION_EcoKing",
                                            "PB_DSP_FW2",
                                            "HW_VERSION_EcoKing",
                                            "EEPROM_VERSION_EK_RD"                      
                                            ]
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            2 : [{  
                                    "action": "highlight_column",
                                    "column": ["FAN_MODEL_RD",
                                            "HP CTRL BOX ID WR",
                                            "HP CTRL BOX ID RD",
                                            "TDM_STATUS",
                                            "Generator External Request ",
                                            "FAN_CONFIG",
                                            "HP Compressor Model RD",
                                            "Fault_Code"                      
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            3: [{   
                                    "action": "highlight_column",
                                    "column": ["HP Compressor Freq",
                                            "FAN 1 Speed Real",
                                            "Compressor ON/OFF Status",
                                            "TDM_STATUS",
                                            "Generator External Request ",
                                            "Fault_Code",
                                            "Compressor Phase Current",
                                            "EXV1_REAL_RD",
                                            "EXV1_SP_WR",
                                            "EXV Valve value"
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            4: [{   
                                    "action": "highlight_column",
                                    "column": ["FAN 1 Speed Real",
                                            "Compressor Phase Current",
                                            "HP Compressor Freq",
                                            "EXV1_REAL_RD",
                                            "EXV1_SP_WR",
                                            "TDM_STATUS",
                                            "Fault_Code",
                                            "Generator External Request"              
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            5: [{   
                                    "action": "highlight_column",
                                    "column": ["LOAD_STATUS_REAL_RD",
                                            "LOAD_STATUS_SP_WR",
                                            "Compressor PRE Heating Status",
                                            "Compressor Phase Current",
                                            "TDM_STATUS",
                                            "Fault_Code",
                                            "Generator External Request",
                                            "CMP_HEATER_TD_TGT_K1_8_8",
                                            "CMP_HEATER_TD_TGT_K2_8_8",
                                            "CMP_HEATER_TD_TGT_K3_8_8"
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            6: [{   
                                    "action": "highlight_column",
                                    "column": ["Compressor Phase Current",
                                            "TDM_STATUS",
                                            "HP Compressor Freq",
                                            "Fault_Code",
                                            "Generator External Request "                    
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            7: [{   
                                    "action": "highlight_column",
                                    "column": ["Compressor Phase Current",
                                            "TDM_STATUS",
                                            "Generator External Request",
                                            "Fault_Code"                      
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            8: [{   
                                    "action": "highlight_column",
                                    "column": ["INVERTER_REG_RD_INPUTCURR_AVG",
                                            "Compressor Phase Current",
                                            "HP Compressor Freq",
                                            "TDM_STATUS",
                                            "Fault_Code"                      
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "insert_current_colmun",
                                    "column": "Compressor Phase Current"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                },
                                {
                                    "action": "plot_headers_from_excel",
                                    "column": ["Compressor Phase Current_[A]",
                                                "HP Compressor Freq"]
                                }
                            ],
                            9: [{   
                                    "action": "highlight_column",
                                    "column": ["HEATSINK_TEMPERATURE",
                                            "Compressor Phase Current",
                                            "HP Compressor Freq",
                                            "TDM_STATUS",
                                            "Fault_Code"                      
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "insert_temp_colmun",
                                    "column": "HEATSINK_TEMPERATURE"
                                },                                
                                {
                                    "action": "insert_current_colmun",
                                    "column": "Compressor Phase Current"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                },
                                {
                                    "action": "highlight_der_temp",
                                    "column": "HEATSINK_TEMPERATURE_T°C"
                                },
                                {
                                    "action": "plot_headers_from_excel",
                                    "column": ["HEATSINK_TEMPERATURE_T°C",
                                                "Compressor Phase Current_[A]",
                                                "HP Compressor Freq"]
                                }
                            ],
                            10: [{  
                                    "action": "highlight_column",
                                    "column": ["INVERTER_REG_RD_INPUTVOLT_AVG",
                                            "Compressor Phase Current",
                                            "HP Compressor Freq",
                                            "TDM_STATUS",
                                            "Fault_Code"                      
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                },
                                {
                                    "action": "highlight_over_voltage",
                                    "column": "INVERTER_REG_RD_INPUTVOLT_AVG",
                                    "color": "00FF00"
                                }
                            ],
                            11: [{  
                                    "action": "highlight_column",
                                    "column": ["INVERTER_REG_RD_INPUTVOLT_AVG",
                                            "Compressor Phase Current",
                                            "HP Compressor Freq",
                                            "TDM_STATUS",
                                            "Fault_Code"                      
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                },
                                {
                                    "action": "highlight_under_voltage",
                                    "column": "INVERTER_REG_RD_INPUTVOLT_AVG",
                                    "color": "00FF00"
                                }
                            ],
                            12: [{  
                                    "action": "highlight_column",
                                    "column": ["TDM_STATUS",
                                            "Generator External Request",
                                            "Compressor Phase Current",
                                            "HP Compressor Freq",
                                            "Fault_Code"                      
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            13: [{  
                                    "action": "highlight_column",
                                    "column": ["TDM_STATUS",
                                            "Generator External Request",
                                            "Compressor Phase Current",
                                            "HP Compressor Freq",
                                            "Fault_Code"                      
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            14: [{  
                                    "action": "highlight_column",
                                    "column": ["INVERTER_COMM_ERROR_TOT_COUNTER",
                                            "INVERTER_COMM_ERROR_SEQ_COUNTER_RD",
                                            "INVERTER_COMM_ERROR_SEQ_COUNTER_WR",
                                            "INVERTER_CTRL_BOX_ID_WRONG_VALUE_COUNTER",
                                            "CTRL_BOARD_COMM_ERROR_SEQ_COUNTER_RD",
                                            "CTRL_BOARD_COMM_ERROR_SEQ_COUNTER_WR",
                                            "TDM_STATUS",
                                            "Generator External Request",
                                            "Fault_Code"                      
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            15: [{  
                                    "action": "highlight_column",
                                    "column": ["CONTROL_BOARD_REG_WR_SENS_ENABLE",
                                            "PDISCH_SOURCE",
                                            "PSUCT_SOURCE",
                                            "Pressure Discharge Virtual",
                                            "Pressure Discharge",
                                            "Pressure Suction Virtual",
                                            "Pressure Suction",
                                            "Fault_Code",
                                            "TDM_STATUS"                      
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            16: [{  
                                    "action": "highlight_column",
                                    "column": ["Compressor PRE Heating Status",
                                            "Compressor Phase Current",
                                            "TDM_STATUS",
                                            "Generator External Request",
                                            "CMP_HEATER_TD_TGT_K1_8_8",
                                            "CMP_HEATER_TD_TGT_K2_8_8",
                                            "CMP_HEATER_TD_TGT_K3_8_8",
                                            "Fault_Code"                      
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            17: [{  
                                    "action": "highlight_column",
                                    "column": ["TDM_STATUS",
                                            "Fault_Code",
                                            "Generator External Request",
                                            "FACTORY_CODE_1",
                                            "FACTORY_CODE_2",
                                            "FACTORY_CODE_3",
                                            "FACTORY_CODE_4",
                                            "FACTORY_CODE_5",
                                            "FACTORY_CODE_6",
                                            "FACTORY_CODE_7",
                                            "FACTORY_CODE_1_WR",
                                            "FACTORY_CODE_2_WR",
                                            "FACTORY_CODE_3_WR",
                                            "FACTORY_CODE_4_WR",
                                            "FACTORY_CODE_5_WR",
                                            "FACTORY_CODE_6_WR",
                                            "FACTORY_CODE_7_WR",
                                            "Factory Code Mode"                   
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ],
                            18: [{  
                                    "action": "highlight_column",
                                    "column": ["Compressor Phase Current",
                                            "HP Compressor Freq",
                                            "TDM_STATUS",
                                            "Generator External Request",
                                            "Fault_Code"                      
                                            ],
                                    "color": "FFFF00"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "Fault_Code",
                                    "value": "Fault_name"
                                },
                                {   
                                    "action": "populate_column_fault",
                                    "column": "Fault_name"
                                },
                                {   
                                    "action": "insert_column",
                                    "column": "TDM_STATUS",
                                    "value": "TDM_STATUS_name"
                                },
                                {   
                                    "action": "populate_tdm_status",
                                    "column": "TDM_STATUS_name"
                                },
                                {
                                    "action": "highlight_event",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "00FF00"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "NO fault",
                                    "color": "FFD966"
                                },
                                {
                                    "action": "find_and_highlight",
                                    "column": "Fault_Code",
                                    "value": "Faults Expected",
                                    "color": "00FF00"
                                },        
                                {
                                    "action": "highlight_not_in_list",
                                    "column": "Fault_Code",
                                    "value": ["NO fault",
                                            "Faults Expected"
                                            ],
                                    "color": "FF0000"
                                }
                            ]
                        }
DEFAULT_TEST_STEPS_1UP = {1: [{ 
                                "action": "highlight_column",
                                "column": ["DSP_MAIN_VERSION_EcoKing",
                                        "PB_DSP_FW2",
                                        "HW_VERSION_EcoKing",
                                        "EEPROM_VERSION_EK_RD",
                                        "HP CTRL BOX ID RD",
                                        "Fault_Code",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            }, 
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },                            
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "validate_version",
                                "column": ["DSP_MAIN_VERSION_EcoKing",
                                        "PB_DSP_FW2",
                                        "HW_VERSION_EcoKing",
                                        "EEPROM_VERSION_EK_RD"                      
                                        ]
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        2 : [{  
                                "action": "highlight_column",
                                "column": ["FAN_MODEL_RD",
                                        "HP CTRL BOX ID WR",
                                        "HP CTRL BOX ID RD",
                                        "TDM_STATUS",
                                        "Generator External Request ",
                                        "FAN_CONFIG",
                                        "HP Compressor Model RD",
                                        "Fault_Code",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        3: [{   
                                "action": "highlight_column",
                                "column": ["HP Compressor Freq",
                                        "FAN 1 Speed Real",
                                        "Compressor ON/OFF Status",
                                        "TDM_STATUS",
                                        "Generator External Request ",
                                        "Fault_Code",
                                        "Compressor Phase Current",
                                        "EXV1_REAL_RD",
                                        "EXV1_SP_WR",
                                        "EXV Valve value",
                                        "LIN_PUMP_ERROR_CODE_ID"
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        4: [{   
                                "action": "highlight_column",
                                "column": ["FAN 1 Speed Real",
                                        "Compressor Phase Current",
                                        "HP Compressor Freq",
                                        "EXV1_REAL_RD",
                                        "EXV1_SP_WR",
                                        "TDM_STATUS",
                                        "Fault_Code",
                                        "Generator External Request",
                                        "LIN_PUMP_ERROR_CODE_ID"              
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        5: [{   
                                "action": "highlight_column",
                                "column": ["LOAD_STATUS_REAL_RD",
                                        "LOAD_STATUS_SP_WR",
                                        "Compressor PRE Heating Status",
                                        "Compressor Phase Current",
                                        "TDM_STATUS",
                                        "Fault_Code",
                                        "Generator External Request",
                                        "CMP_HEATER_TD_TGT_K1_8_8",
                                        "CMP_HEATER_TD_TGT_K2_8_8",
                                        "CMP_HEATER_TD_TGT_K3_8_8",
                                        "LIN_PUMP_ERROR_CODE_ID"
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        6: [{   
                                "action": "highlight_column",
                                "column": ["Compressor Phase Current",
                                        "TDM_STATUS",
                                        "HP Compressor Freq",
                                        "Fault_Code",
                                        "Generator External Request",
                                        "LIN_PUMP_ERROR_CODE_ID"                    
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        7: [{
                                "action": "highlight_column",
                                "column": ["Compressor Phase Current",
                                        "TDM_STATUS",
                                        "Generator External Request",
                                        "Fault_Code",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        8: [{
                                "action": "highlight_column",
                                "column": ["INVERTER_REG_RD_INPUTCURR_AVG",
                                        "Compressor Phase Current",
                                        "HP Compressor Freq",
                                        "TDM_STATUS",
                                        "Fault_Code",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "insert_current_colmun",
                                "column": "Compressor Phase Current"
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            },
                            {
                                "action": "plot_headers_from_excel",
                                "column": ["Compressor Phase Current_[A]",
                                            "HP Compressor Freq"]
                            }
                        ],
                        9: [{
                                "action": "highlight_column",
                                "column": ["HEATSINK_TEMPERATURE",
                                        "Compressor Phase Current",
                                        "HP Compressor Freq",
                                        "TDM_STATUS",
                                        "Fault_Code",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "insert_temp_colmun",
                                "column": "HEATSINK_TEMPERATURE"
                            },                            
                            {
                                "action": "insert_current_colmun",
                                "column": "Compressor Phase Current"
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            },
                            {
                                "action": "highlight_der_temp",
                                "column": "HEATSINK_TEMPERATURE_T°C"
                            },
                            {
                                "action": "plot_headers_from_excel",
                                "column": ["HEATSINK_TEMPERATURE_T°C",
                                            "Compressor Phase Current_[A]",
                                            "HP Compressor Freq"]
                            }
                        ],
                        10: [{
                                "action": "highlight_column",
                                "column": ["INVERTER_REG_RD_INPUTVOLT_AVG",
                                        "Compressor Phase Current",
                                        "HP Compressor Freq",
                                        "TDM_STATUS",
                                        "Fault_Code",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            },
                            {
                                "action": "highlight_over_voltage",
                                "column": "INVERTER_REG_RD_INPUTVOLT_AVG",
                                "color": "00FF00"
                            }
                        ],
                        11: [{
                                "action": "highlight_column",
                                "column": ["INVERTER_REG_RD_INPUTVOLT_AVG",
                                        "Compressor Phase Current",
                                        "HP Compressor Freq",
                                        "TDM_STATUS",
                                        "Fault_Code",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            },
                            {
                                "action": "highlight_under_voltage",
                                "column": "INVERTER_REG_RD_INPUTVOLT_AVG",
                                "color": "00FF00"
                            }
                        ],
                        12: [{
                                "action": "highlight_column",
                                "column": ["TDM_STATUS",
                                        "Generator External Request",
                                        "Compressor Phase Current",
                                        "HP Compressor Freq",
                                        "Fault_Code",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        13: [{
                                "action": "highlight_column",
                                "column": ["TDM_STATUS",
                                        "Generator External Request",
                                        "Compressor Phase Current",
                                        "HP Compressor Freq",
                                        "Fault_Code",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        14: [{
                                "action": "highlight_column",
                                "column": ["INVERTER_COMM_ERROR_TOT_COUNTER",
                                        "INVERTER_COMM_ERROR_SEQ_COUNTER_RD",
                                        "INVERTER_COMM_ERROR_SEQ_COUNTER_WR",
                                        "INVERTER_CTRL_BOX_ID_WRONG_VALUE_COUNTER",
                                        "CTRL_BOARD_COMM_ERROR_SEQ_COUNTER_RD",
                                        "CTRL_BOARD_COMM_ERROR_SEQ_COUNTER_WR",
                                        "TDM_STATUS",
                                        "Generator External Request",
                                        "Fault_Code",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        15: [{
                                "action": "highlight_column",
                                "column": ["CONTROL_BOARD_REG_WR_SENS_ENABLE",
                                        "PDISCH_SOURCE",
                                        "PSUCT_SOURCE",
                                        "Pressure Discharge Virtual",
                                        "Pressure Discharge",
                                        "Pressure Suction Virtual",
                                        "Pressure Suction",
                                        "Fault_Code",
                                        "TDM_STATUS",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        16: [{
                                "action": "highlight_column",
                                "column": ["Compressor PRE Heating Status",
                                        "Compressor Phase Current",
                                        "TDM_STATUS",
                                        "Generator External Request",
                                        "CMP_HEATER_TD_TGT_K1_8_8",
                                        "CMP_HEATER_TD_TGT_K2_8_8",
                                        "CMP_HEATER_TD_TGT_K3_8_8",
                                        "Fault_Code",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        17: [{
                                "action": "highlight_column",
                                "column": ["TDM_STATUS",
                                        "Fault_Code",
                                        "Generator External Request",
                                        "FACTORY_CODE_1",
                                        "FACTORY_CODE_2",
                                        "FACTORY_CODE_3",
                                        "FACTORY_CODE_4",
                                        "FACTORY_CODE_5",
                                        "FACTORY_CODE_6",
                                        "FACTORY_CODE_7",
                                        "FACTORY_CODE_1_WR",
                                        "FACTORY_CODE_2_WR",
                                        "FACTORY_CODE_3_WR",
                                        "FACTORY_CODE_4_WR",
                                        "FACTORY_CODE_5_WR",
                                        "FACTORY_CODE_6_WR",
                                        "FACTORY_CODE_7_WR",
                                        "Factory Code Mode",
                                        "LIN_PUMP_ERROR_CODE_ID"                   
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        18: [{
                                "action": "highlight_column",
                                "column": ["Compressor Phase Current",
                                        "HP Compressor Freq",
                                        "TDM_STATUS",
                                        "Generator External Request",
                                        "Fault_Code",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        19: [{
                                "action": "highlight_column",
                                "column": ["FAN 1 Speed Real",
                                        "HP FAN Model RD",
                                        "FAN_CONFIG",
                                        "Fault_Code",
                                        "EM Fixed FAN 1 Speed (rpm)",
                                        "TDM_STATUS",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        20: [{
                                "action": "highlight_column",
                                "column": ["FAN 1 Speed Real",
                                        "FAN_CONFIG",
                                        "Fault_Code",
                                        "EBM_FAN_REG_MINIMUM_SPEED",
                                        "EBM_FAN_REG_MAXIMUM_SPEED",
                                        "EBM_FAN_REG_MAXIMUM_POWER",
                                        "EBM_FAN_REG_DC_LINK_CURRENT_REFERENCE",
                                        "EBM_FAN_REG_SET_POINT",
                                        "EBM_FAN_REG_ENABLE_DISABLE",    
                                        "EBM_FAN_REG_CURRENT_DIRECTION_OF_ROTATION",
                                        "EBM_FAN_REG_ENABLE_DISABLE_INPUT_STATE",
                                        "EBM_FAN_REG_CURRENT_POWER_ABSOLUTE_CODING",
                                        "EBM_FAN_REG_MOTOR_TEMPERATURE",
                                        "EBM_FAN_REG_MODULE_TEMPERTURE",
                                        "EBM_FAN_REG_INSIDE_ELECTRONIC_TEMPERATURE",
                                        "TDM_STATUS",
                                        "LIN_PUMP_ERROR_CODE_ID"
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        21: [{
                                "action": "highlight_column",
                                "column": ["FAN 1 Speed Real",
                                        "HP FAN1 Status",
                                        "Fault_Code",
                                        "EBM_FAN_REG_SET_POINT",
                                        "TDM_STATUS",
                                        "LIN_PUMP_ERROR_CODE_ID"                     
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        22: [{
                                "action": "highlight_column",
                                "column": ["FAN 1 Speed Real",
                                        "HP Compressor Freq",
                                        "EBM_FAN_REG_MINIMUM_SPEED",
                                        "EBM_FAN_REG_MAXIMUM_SPEED",
                                        "Fault_Code",
                                        "EBM_FAN_REG_MAXIMUM_POWER",
                                        "EBM_FAN_REG_DC_LINK_CURRENT_REFERENCE",
                                        "EBM_FAN_REG_SET_POINT",
                                        "EBM_FAN_REG_ENABLE_DISABLE",
                                        "EBM_FAN_REG_CURRENT_DIRECTION_OF_ROTATION",
                                        "EBM_FAN_REG_ENABLE_DISABLE_INPUT_STATE",
                                        "EBM_FAN_REG_CURRENT_POWER_ABSOLUTE_CODING",
                                        "EBM_FAN_REG_MOTOR_TEMPERATURE",
                                        "EBM_FAN_REG_MODULE_TEMPERTURE",
                                        "EBM_FAN_REG_INSIDE_ELECTRONIC_TEMPERATURE",
                                        "TDM_STATUS",
                                        "LIN_PUMP_ERROR_CODE_ID"
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        23: [{
                                "action": "highlight_column",
                                "column": ["INVERTER_REG_RD_INPUTVOLT_AVG",
                                        "Fault_Code",
                                        "TDM_STATUS"                     
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            },
                            {
                                "action": "highlight_under_voltage",
                                "column": "INVERTER_REG_RD_INPUTVOLT_AVG",
                                "color": "00FF00"
                            }
                        ],
                        24: [{
                                "action": "highlight_column",
                                "column": ["FAN 1 Speed Real",
                                        "Fault_Code",
                                        "TDM_STATUS",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        25: [{
                                "action": "highlight_column",
                                "column": ["FAN 1 Speed Real",
                                        "HP FAN1 Status",
                                        "Fault_Code",
                                        "TDM_STATUS",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        26: [{
                                "action": "highlight_column",
                                "column": ["INVERTER_REG_RD_INPUTVOLT_AVG",
                                        "Fault_Code",
                                        "TDM_STATUS",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            },
                            {
                                "action": "highlight_under_voltage",
                                "column": "INVERTER_REG_RD_INPUTVOLT_AVG",
                                "color": "00FF00"
                            }
                        ],
                        27: [{
                                "action": "highlight_column",
                                "column": ["Compressor Phase Current",
                                        "FAN 1 Speed Real",
                                        "INVERTER_REG_RD_INPUTVOLT_AVG",
                                        "Fault_Code",
                                        "TDM_STATUS",
                                        "LIN_PUMP_ERROR_CODE_ID"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            },
                            {
                                "action": "highlight_over_voltage",
                                "column": "INVERTER_REG_RD_INPUTVOLT_AVG",
                                "color": "00FF00"
                            }
                        ],
                        28: [{
                                "action": "highlight_column",
                                "column": ["INVERTER_REG_RD_INPUTVOLT_AVG",
                                        "Fault_Code",
                                        "TDM_STATUS",
                                        "LIN_PUMP_ERROR_CODE_ID"                     
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            },
                            {
                                "action": "highlight_under_voltage",
                                "column": "INVERTER_REG_RD_INPUTVOLT_AVG",
                                "color": "00FF00"
                            }
                        ],
                        29: [{
                                "action": "highlight_column",
                                "column": ["LIN_PUMP_ESTIMATED_HEAD",
                                        "Fault_Code",
                                        "LIN_PUMP_OPERATIONAL_STATUS",
                                        "LIN_PUMP_READY_FOR_OPERATION",
                                        "LIN_PUMP_ROTATION_DIRECTION_SET_WR",
                                        "LIN_PUMP_ROTATION_DIRECTION_SET_RD",
                                        "LIN_PUMP_WARNING_PRESENT",
                                        "LIN_PUMP_ERROR_PRESENT",
                                        "LIN_PUMP_FINAL_ERROR_PRESENT",
                                        "LIN_PUMP_OPERATION_LIMIT_REACHED",
                                        "LIN_PUMP_RESPONSE_ERROR",
                                        "LIN_PUMP_TEST_BENCH",
                                        "LIN_PUMP_VDMA_PROFILE_REVISION",
                                        "LIN_PUMP_PROD_YEAR"    
                                        "LIN_PUMP_ESTIMATED_MAINSVOLTAGE",
                                        "LIN_PUMP_ESTIMATED_RPM", 
                                        "LIN_PUMP_ERROR_CODE_ID",
                                        "TDM_STATUS"                 
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        30: [{
                                "action": "highlight_column",
                                "column": ["INVERTER_REG_RD_INPUTVOLT_AVG",
                                        "Fault_Code",
                                        "LIN_PUMP_ESTIMATED_MAINSVOLTAGE",
                                        "LIN_PUMP_ERROR_CODE_ID",
                                        "TDM_STATUS"                     
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            },
                            {
                                "action": "highlight_under_voltage",
                                "column": ["INVERTER_REG_RD_INPUTVOLT_AVG",
                                            "LIN_PUMP_ESTIMATED_MAINSVOLTAGE"],
                                "color": "00FF00"
                            }
                        ],
                        31: [{
                                "action": "highlight_column",
                                "column": ["Compressor Phase Current",
                                        "INVERTER_REG_RD_INPUTVOLT_AVG",
                                        "LIN_PUMP_ESTIMATED_HEAD",
                                        "HP Compressor Freq",
                                        "Fault_Code",
                                        "LIN_PUMP_ESTIMATED_MAINSVOLTAGE",
                                        "LIN_PUMP_ERROR_CODE_ID",
                                        "TDM_STATUS"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            },
                            {
                                "action": "highlight_over_voltage",
                                "column": ["INVERTER_REG_RD_INPUTVOLT_AVG",
                                            "LIN_PUMP_ESTIMATED_MAINSVOLTAGE"],
                                "color": "00FF00"
                            }
                        ],
                        32: [{
                                "action": "highlight_column",
                                "column": ["LIN_PUMP_ESTIMATED_HEAD",
                                        "LIN_PUMP_WARNING_PRESENT",
                                        "LIN_PUMP_ERROR_CODE_ID",
                                        "Fault_Code",
                                        "TDM_STATUS"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ],
                        33: [{
                                "action": "highlight_column",
                                "column": ["LIN_PUMP_ESTIMATED_HEAD",
                                        "LIN_PUMP_WARNING_PRESENT",
                                        "LIN_PUMP_ERROR_CODE_ID",
                                        "Fault_Code",
                                        "TDM_STATUS"                      
                                        ],
                                "color": "FFFF00"
                            },
                            {   
                                "action": "insert_column",
                                "column": "Fault_Code",
                                "value": "Fault_name"
                            },
                            {   
                                "action": "populate_column_fault",
                                "column": "Fault_name"
                            },
                            {   
                                "action": "insert_column",
                                "column": "TDM_STATUS",
                                "value": "TDM_STATUS_name"
                            },
                            {   
                                "action": "populate_tdm_status",
                                "column": "TDM_STATUS_name"
                            },
                            {   
                                "action": "append_column",
                                "column": "Lin_fault_name",
                            },
                            {   
                                "action": "populate_lin_fault",
                                "column": "Lin_fault_name",
                            },
                            {
                                "action": "highlight_event",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "00FF00"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "NO fault",
                                "color": "FFD966"
                            },
                            {
                                "action": "find_and_highlight",
                                "column": "Fault_Code",
                                "value": "Faults Expected",
                                "color": "00FF00"
                            },        
                            {
                                "action": "highlight_not_in_list",
                                "column": "Fault_Code",
                                "value": ["NO fault",
                                        "Faults Expected"
                                        ],
                                "color": "FF0000"
                            }
                        ]
                    }

