import sys
from PySide6.QtWidgets import QApplication
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from pprint import pprint
# IMPORTA TU VENTANA
from Read_json_standalone import build_modbus_dict

def main():

    json_path = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Modbus_SW\Inverter config\Ariston Extended.json"
    modbus_dict = build_modbus_dict(json_path)
    pprint(modbus_dict)

    sys.exit(0)

    


if __name__ == "__main__":
    main()