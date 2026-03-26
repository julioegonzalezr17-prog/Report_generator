
from json_motor import create_test_config_json


config = create_test_config_json(
    xlsx_path="C:\\Users\\gonzpidr\\OneDrive - Ariston Group\\Documenti\\Python\\Report_generator\\data_base\\Report_config_Pacman5.xlsx",
    json_path="C:\\Users\\gonzpidr\\OneDrive - Ariston Group\\Documenti\\Python\\Report_generator\\data_base\\test_config.json",
    sheet_name="RD4021",
    machine_type = "1 UP",
    inverter_type = "RD4021"
)

