import os
import sys
from pathlib import Path

# Add workspace to path
workspace_path = str(Path(__file__).parent)
if workspace_path not in sys.path:
    sys.path.insert(0, workspace_path)

from Read_TDM_error import load_tdm_once
from ExcelStyler import ExcelStyler
from step_engine import StepEngine
from json_motor import DEFAULT_TEST_STEPS_PACMAN5
from json_motor import create_test_config_json
import json 
from Read_TDM_report import read_custom_csv, save_to_excel, detect_csv_delimiter
import json_motor
from pathlib import Path

#csvpath = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\Test_files\log_TDM_test_1_2_3.csv"
csvpath = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\Test_files\2026_01_28 Integrazione TDM 70.35.00 - 4021 V1_T1\Test_21\Log_test_21_prueba.csv"

delimiter = detect_csv_delimiter(csvpath)
header_cust, report_data = read_custom_csv(csvpath.strip(),delimiter)

test_excel = str(Path(csvpath.strip()).with_suffix(".xlsx"))
save_to_excel(test_excel, header_cust, report_data)
config_xlsx = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\data_base\Report_config_Pacman5.xlsx"
config = create_test_config_json(
    xlsx_path="C:\\Users\\gonzpidr\\OneDrive - Ariston Group\\Documenti\\Python\\Report_generator\\data_base\\Report_config_Pacman5.xlsx",
    json_path="C:\\Users\\gonzpidr\\OneDrive - Ariston Group\\Documenti\\Python\\Report_generator\\data_base\\test_config.json",
    sheet_name="RD4021",
    machine_type = "Pacman 5",
    inverter_type = "RD4021"
)
tdm_path = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\data_base\Tabella diagnostica TDM4 v19.xlsx"
tdm_dict = load_tdm_once(tdm_path, header_row=5)
styler = ExcelStyler(test_excel, sheet_name="DATA", tdm_dict=tdm_dict)
engine = StepEngine(styler, config,"1")
result = engine.execute()
print(styler.plot_headers_from_excel(["HEATSINK_TEMPERATURE", "Compressor Phase Current", "HP Compressor Freq"]))

for clave, valor in result.items():
    print(clave, "→", valor)


styler.save(test_excel)

