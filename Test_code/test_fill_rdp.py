
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))


from fill_RDP_report import update_excel_template



header_data = {
    "Request by:": "Giorgio Baglivo",
    "Performed by:": "Julio Gonzalez",
    "TDM": "100.32.00",
    "Control Board": "03.05.00",
    "Inverter fw": "15.15.01",
    "Test start Date:": "2026-04-20",
    "Test end Date:": "2026-04-27",
    "machine": "PCM5"
}

tests = [
    {
        "num": 1,
        "desc": "Communication startup",
        "TDM_Logs": "tdm_log_1.txt",
        "Modbus_Logs": "modbus_log_1.txt",
        "notes": "test superado sin problemas",
        "result": "PASS"
    },
    {
        "num": 2,
        "desc": "Inverter stress test",
        "TDM_Logs": "tdm_log_2.txt",
        "Modbus_Logs": "modbus_log_2.txt",
        "notes": "Timeout detected",
        "result": "FAIL"
    }
]

update_excel_template(
    template_path=r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\data_test\Report RdP 0258-26 - PACMAN 5 WEBA - Ariston inverter R290 Integration Testing TDM 100.32.00.xlsx",
    output_path=None,
    data_path = r"C:\Users\gonzpidr\Ariston Group\Alignement - General\01_INVERTERS\05_Ariston Inverter\03_Testing\02_SW Qualification - Integration Inverter-TDM\2026_04_20 TDM 100.32.00-Ariston 15.15.01",
    header_data=header_data,
    tests=tests
)