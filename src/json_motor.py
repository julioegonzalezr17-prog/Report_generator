import pandas as pd
import json
from dictDataIntegration import (DEFAULT_TEST_STEPS_PACMAN5, DEFAULT_TEST_STEPS_1UP)
import logging

logger = logging.getLogger(__name__)

def _normalize_header(name):
    """Convierte un nombre de columna al formato estándar: MAYÚSCULAS sin caracteres especiales"""
    import re
    # Convertir a string, quitar caracteres no alfanuméricos, convertir a mayúsculas
    return re.sub(r'[^a-zA-Z0-9]', '', str(name).strip()).upper()

def _normalize_step(step):
    """Normaliza todos los nombres de columna dentro de un paso"""
    normalized = {}
    for key, value in step.items():
        if key == "column":
            # Si es una lista de columnas, normalizar cada una
            if isinstance(value, list):
                normalized[key] = [_normalize_header(col) for col in value]
            else:
                normalized[key] = _normalize_header(value)
        else:
            # El resto de campos (color, value, action, etc) se dejan igual
            normalized[key] = value
    return normalized


def create_test_config_json(xlsx_path: str, 
                            json_path: str, 
                            sheet_name: str, 
                            machine_type: str, 
                            inverter_type: str)-> dict:

    logger.info("Creating test configuration file: %s", json_path)
    try:
        if machine_type == "":
            machine_type = "Pacman 5"
        if inverter_type == "":
            inverter_type = "RD4021"

        xl = pd.ExcelFile(xlsx_path, engine="openpyxl")
        if sheet_name is None:
            sheet_name = xl.sheet_names[0]

        df = pd.read_excel(xlsx_path, sheet_name=sheet_name, engine="openpyxl")

        df.columns = [
            " ".join(str(c).strip().upper().split())
            for c in df.columns
        ]

        test_col = df.columns[0]
        df[test_col] = pd.to_numeric(df[test_col], errors="coerce").astype("Int64")
        df = df.dropna(subset=[test_col])

        config = {"tests": {}}

        for _, row in df.iterrows():
            test_number = int(row[test_col])
            key = str(test_number)

            attributes = {}
            for col in df.columns[1:]:
                val = row[col]
                if pd.isna(val):
                    continue
                if isinstance(val, str) and ";" in val:
                    attributes[col] = [v.strip() for v in val.split(";") if v.strip()]
                else:
                    attributes[col] = val

            # ⭐ Agregar atributos al JSON
            config["tests"][key] = attributes

            # ⭐ IMPORTANTE: normalizar los pasos antes de agregarlos
            if machine_type == "Pacman 5":
                if test_number in DEFAULT_TEST_STEPS_PACMAN5:
                    raw_steps = DEFAULT_TEST_STEPS_PACMAN5[test_number]
                    config["tests"][key]["steps"] = [_normalize_step(step) for step in raw_steps]
                else:
                    # Si quieres que todos tengan steps aunque sea vacío
                    config["tests"][key]["steps"] = []
            else:
                if test_number in DEFAULT_TEST_STEPS_1UP:
                    raw_steps = DEFAULT_TEST_STEPS_1UP[test_number]
                    config["tests"][key]["steps"] = [_normalize_step(step) for step in raw_steps]
                else:
                    # Si quieres que todos tengan steps aunque sea vacío
                    config["tests"][key]["steps"] = []

        # Guardar archivo JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        logger.debug("JSON succesfully saved, STEP dictionary crated")
        return config
    except Exception:
        logger.exception("ERROR analizing: %s", json_path)
        raise