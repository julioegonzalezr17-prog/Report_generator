import sys
from PySide6.QtWidgets import QApplication
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from pprint import pprint
# IMPORTA TU VENTANA
from Read_standalone_report import load_excel_tests

def main():

    path = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\data_base\report_test\standalone\FWTestList_RD4021A2.xlsx"
    data = load_excel_tests(path)
    pprint(data)

    sys.exit(0)

    


if __name__ == "__main__":
    main()