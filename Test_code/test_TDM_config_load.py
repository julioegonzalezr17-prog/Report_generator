"""Simple quick test for TDM_config_load.load_tdm_config.

This script generates a tiny CSV in the workspace, invokes the loader, and
prints the resulting dictionary.  It also contains a basic assertion to make
sure the structure is what we expect.
"""

import os
import json
import pandas as pd
# En tu script de la subcarpeta:
try:
    from TDM_config_load import find_positions, load_tdm_config  # Nombre del archivo sin .py
    print("¡Éxito! La función fue importada.")
except ModuleNotFoundError:
    print("Error: VS Code aún no encuentra la carpeta principal.")



# load it
csv_path = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\data_base\TDM4_RX130_ATG485_70_11_00.csv"
tdm_config = load_tdm_config(csv_path)
print("Loaded dictionary:")
# sanity check
base = os.path.splitext(os.path.basename(csv_path))[0]
assert base in tdm_config, "Base filename key missing"
assert set(tdm_config[base].keys()) == {"DGTO", "reg_DGTO", "name_DGTO", "info_DGTO"}

print("\nQuick test passed. Structure is correct.")
print("Base key:", base)  # print the base key
print("Sample DGTO values:", tdm_config[base]["DGTO"][:5])  # print first 5 DGTO values

list_DGTO = ['0-1-0-9', '0-3-0-6', '0-3-0-7', '0-3-0-8', '1-6-0-3']
serch_DGTO = find_positions(tdm_config, "DGTO", list_DGTO, mode="exact")
print("\nPositions of DGTO values:", serch_DGTO)
print("\nnames DGTO:", [tdm_config[base]["name_DGTO"][i] for i in serch_DGTO])
new_DGTO = find_positions(tdm_config, "name_DGTO", list_DGTO, mode="exact")
print("\nPositions of name_DGTO values:", new_DGTO)
name_list = ["Factory Code Mode","FAN_MAX_NOISE_OVR", "hola mundo"]
serch_DGTO = find_positions(tdm_config, "name_DGTO", name_list, mode="exact")
print("\nPositions of name_DGTO values:", serch_DGTO)
print("\nDGTO CODE:", [tdm_config[base]["DGTO"][i] for i in serch_DGTO])
print("\nDGTO REG CODE:", [tdm_config[base]["reg_DGTO"][i] for i in serch_DGTO])

