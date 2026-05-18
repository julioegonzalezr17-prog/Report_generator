import sys
from PySide6.QtWidgets import QApplication
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from pprint import pprint
# IMPORTA TU VENTANA
from UI_buglist import BugSelectionWindow
from UI_BugReport import BugReportWindow
# ↑ ajusta el nombre del archivo si es distinto


def main():
    # -----------------------------
    # Fake test data (mock)
    # -----------------------------
    bug_results = {'Test': {'1': {'BUG': '',
                'Notes Technology': '',
                'data_print_report': {'Analysis': 'DGTO_validation: PASS DGTO list: []\n'
                                                    'FAULT_validation: FAIL Fault list: 2234 → INVERTER ERROR NOT VISIBLE\n'
                                                    '1992 → FLOW_WITH_P1_OFF _HARD_STOP\n'
                                                    'VERSION_validation: PASS',
                                        'Modbus Log': 'C:/Users/gonzpidr/Ariston Group/Alignement - '
                                                    'General/01_INVERTERS/05_Ariston Inverter/03_Testing/02_SW Qualification - '
                                                    'Integration Inverter-TDM/2026_04_27 TDM 100.35.00-Ariston '
                                                    '15.15.01/03_Data/Test_1/log_2026-04-23_14-29-54.xlsx',
                                        'Supporting Data': '',
                                        'TDM log': 'C:\\Users\\gonzpidr\\Ariston Group\\Alignement - '
                                                    'General\\01_INVERTERS\\05_Ariston Inverter\\03_Testing\\02_SW Qualification - '
                                                    'Integration Inverter-TDM\\2026_04_27 TDM 100.35.00-Ariston '
                                                    '15.15.01\\03_Data\\Test_1\\Log_test_1_20260423_1430.xlsx'},
                'test_scope': 'Read boards FW versions via TDM DGTO\nRead CTRL_BOX_ID'},
                '2': {'BUG': '',
                'Notes Technology': '',
                'data_print_report': {'Analysis': 'DGTO_validation: PASS DGTO list: []\n'
                                                    'FAULT_validation: FAIL Fault list: 2234 → INVERTER ERROR NOT VISIBLE\n'
                                                    '1992 → FLOW_WITH_P1_OFF _HARD_STOP\n'
                                                    'VERSION_validation: PASS',
                                        'Modbus Log': 'C:/Users/gonzpidr/Ariston Group/Alignement - '
                                                    'General/01_INVERTERS/05_Ariston Inverter/03_Testing/02_SW Qualification - '
                                                    'Integration Inverter-TDM/2026_04_27 TDM 100.35.00-Ariston '
                                                    '15.15.01/03_Data/Test_1/log_2026-04-23_14-29-54.xlsx',
                                        'Supporting Data': '',
                                        'TDM log': 'C:\\Users\\gonzpidr\\Ariston Group\\Alignement - '
                                                    'General\\01_INVERTERS\\05_Ariston Inverter\\03_Testing\\02_SW Qualification - '
                                                    'Integration Inverter-TDM\\2026_04_27 TDM 100.35.00-Ariston '
                                                    '15.15.01\\03_Data\\Test_1\\Log_test_1_20260423_1430.xlsx'},
                'test_scope': 'Read boards FW versions via TDM DGTO\nRead CTRL_BOX_ID'},
                '3': {'BUG': '',
                'Notes Technology': '',
                'data_print_report': {'Analysis': 'DGTO_validation: PASS DGTO list: []\n'
                                                    'FAULT_validation: PASS Fault list: []\n'
                                                    'VERSION_validation: PASS',
                                        'Modbus Log': 'C:/Users/gonzpidr/Ariston Group/Alignement - '
                                                    'General/01_INVERTERS/05_Ariston Inverter/03_Testing/02_SW Qualification - '
                                                    'Integration Inverter-TDM/2026_04_27 TDM 100.35.00-Ariston '
                                                    '15.15.01/03_Data/Test_1/log_2026-04-23_14-29-54.xlsx',
                                        'Supporting Data': '',
                                        'TDM log': 'C:\\Users\\gonzpidr\\Ariston Group\\Alignement - '
                                                    'General\\01_INVERTERS\\05_Ariston Inverter\\03_Testing\\02_SW Qualification - '
                                                    'Integration Inverter-TDM\\2026_04_27 TDM 100.35.00-Ariston '
                                                    '15.15.01\\03_Data\\Test_1\\Log_test_1_20260423_1430.xlsx'},
                'test_scope': 'Read boards FW versions via TDM DGTO\nRead CTRL_BOX_ID'},
                '4': {'BUG': '',
                'Notes Technology': '',
                'data_print_report': {'Analysis': 'DGTO_validation: FAIL DGTO list: Unknown 0x1063-Unknown 0x00C2-Unknown '
                                                    '0xF0D5\n'
                                                    'FAULT_validation: FAIL Fault list: 2234 → INVERTER ERROR NOT VISIBLE\n'
                                                    '1992 → FLOW_WITH_P1_OFF _HARD_STOP\n'
                                                    'VERSION_validation: PASS',
                                        'Modbus Log': 'C:/Users/gonzpidr/Ariston Group/Alignement - '
                                                    'General/01_INVERTERS/05_Ariston Inverter/03_Testing/02_SW Qualification - '
                                                    'Integration Inverter-TDM/2026_04_27 TDM 100.35.00-Ariston '
                                                    '15.15.01/03_Data/Test_1/log_2026-04-23_14-29-54.xlsx',
                                        'Supporting Data': '',
                                        'TDM log': 'C:\\Users\\gonzpidr\\Ariston Group\\Alignement - '
                                                    'General\\01_INVERTERS\\05_Ariston Inverter\\03_Testing\\02_SW Qualification - '
                                                    'Integration Inverter-TDM\\2026_04_27 TDM 100.35.00-Ariston '
                                                    '15.15.01\\03_Data\\Test_1\\Log_test_1_20260423_1430.xlsx'},
                'test_scope': 'Read boards FW versions via TDM DGTO\nRead CTRL_BOX_ID'}},
            'report_data': {'control_board': ['3', '5', '0'],
                            'inverter_arm': ['', ''],
                            'inverter_dsp': ['15', '15', '01'],
                            'inverter_eeprom': ['', ''],
                            'inverter_model': 'Ariston',
                            'inverter_pfc': ['', ''],
                            'machine_model': 'Pacman 5',
                            'notes': '',
                            'rdp_number': 'RDP 0258-26',
                            'report_config': 'C:/Users/gonzpidr/OneDrive - Ariston '
                                            'Group/Documenti/Python/Report_generator/data_base/Report_config_Pacman5.xlsx',
                            'report_file': 'C:/Users/gonzpidr/Ariston Group/Alignement - General/01_INVERTERS/05_Ariston '
                                            'Inverter/03_Testing/02_SW Qualification - Integration Inverter-TDM/2026_04_27 TDM '
                                            '100.35.00-Ariston 15.15.01/02_Report/Report_Integration_ATG_15.15.01 - '
                                            'TDM_100.35.00.xlsx',
                            'requester_name': 'Giorgio',
                            'tdm_config': 'C:/Users/gonzpidr/OneDrive - Ariston '
                                        'Group/Documenti/TDM/TDM4_RX130_ATG485_100_35_00/TDM4_WEBA_ATG485_RELEASE_100_35_00.csv',
                            'tdm_error': 'C:/Users/gonzpidr/OneDrive - Ariston '
                                        'Group/Documenti/Python/Report_generator/data_base/Tabella diagnostica TDM4 v20.xlsx',
                            'tdm_version': ['100', '35', '00'],
                            'tester_name': 'Julio'},
            'RDP_path': 'C:\\Users\\gonzpidr\\OneDrive - Ariston Group\\Documenti\\data_test'

    }

    # -----------------------------
    # Qt Application
    # -----------------------------
    app = QApplication(sys.argv)
    dlg = BugSelectionWindow(bug_results)


    if dlg.exec():
        if dlg.get_updated_data() is not None:
            updated_data = dlg.get_updated_data()
            pprint(updated_data)

    else:
        print("\n❌ Bug review canceled")

    if 'updated_data' not in locals():
        print("\nNo data to show in bug report window. Exiting.")
        sys.exit(0)
    dlg2 = BugReportWindow(updated_data)


    if dlg2.exec():
        print("\n✅ Bug report generated successfully")

    else:
        print("\n❌ Bug review canceled")

    sys.exit(0)

    


if __name__ == "__main__":
    main()