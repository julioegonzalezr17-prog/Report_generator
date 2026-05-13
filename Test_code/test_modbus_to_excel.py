import os
import sys
from pathlib import Path

# Add workspace to path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from modbus_to_excel import csv_to_excel_with_fill


from lin_to_excel import lin_csv_to_excel


if __name__ == "__main__":
    lin_csv_to_excel(
        r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\data_test\03_Data\Test_1\Log_lin_Pump_1-2-3_RAW.csv",
        r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\data_test\03_Data\Test_1\resultado_lin.xlsx"
    )
