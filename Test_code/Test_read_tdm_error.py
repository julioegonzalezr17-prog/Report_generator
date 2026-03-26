import os
from Read_TDM_error import load_tdm_once


# Ensure the current folder is on sys.path so local imports resolve in the editor
HERE = os.path.dirname(__file__)
if HERE not in os.sys.path:
    os.sys.path.insert(0, HERE)

# Path to the TDM Excel file (adjust as needed)
path = os.path.join(HERE, "Tabella diagnostica TDM4 v19.xlsx")
# Read using header row 5 (top of file is empty)
tdm_map = load_tdm_once(path, header_row=5)

code = 2222
info = tdm_map.get(code)
if info:
    print("FAULT NAME:", info["FAULT NAME"])
    print("MANUAL:", info["ERROR LIST NAME FOR MANUAL"])
else:
    print("Code not found")