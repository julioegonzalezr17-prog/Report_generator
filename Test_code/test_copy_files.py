
import shutil

origen = r"C:\Users\gonzpidr\Ariston Group\Alignement - General\01_INVERTERS\05_Ariston Inverter\03_Testing\02_SW Qualification - Integration Inverter-TDM\2026_04_20 TDM 100.32.00-Ariston 15.15.01"
destino = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\data_test"

shutil.copytree(origen, destino, dirs_exist_ok=True)
