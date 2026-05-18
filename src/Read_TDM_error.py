import os
import pandas as pd
from typing import Dict, Any
import logging

_tdm_cache: Dict[str, Dict[int, Dict[str, Any]]] = {}

logger = logging.getLogger(__name__)


# ============================================
# 🔧 CLEAN FAULT NAME
# ============================================
def clean_fault_name(value: str) -> str:
    if not isinstance(value, str):
        return ""

    value = value.strip()

    # Remove CELL-based path strings
    if "]" in value:
        value = value.split("]")[-1]

    return value.strip()


# ============================================
# ✅ MAIN FUNCTION (FULL COMPATIBLE)
# ============================================
def load_tdm_once(xlsx_path: str, header_row: int) -> Dict[int, Dict[str, str]]:

    logger.info("Reading TDM fault file: %s", xlsx_path)

    # ✅ CACHE
    if xlsx_path in _tdm_cache:
        return _tdm_cache[xlsx_path]

    try:
        xl = pd.ExcelFile(xlsx_path, engine="openpyxl")

        # =========================
        # FIND TDM SHEET
        # =========================
        def norm(s):
            return " ".join(str(s).strip().upper().split())

        tdm_sheet = None
        for sheet in xl.sheet_names:
            if norm(sheet).startswith("TDM"):
                tdm_sheet = sheet
                break

        if not tdm_sheet:
            raise ValueError(f"TDM sheet not found in {xlsx_path}")

        header_index = max(0, header_row - 1)

        df = pd.read_excel(
            xl,
            sheet_name=tdm_sheet,
            engine="openpyxl",
            header=header_index
        )

        # ✅ NORMALIZE COLUMNS
        df.columns = [norm(c) for c in df.columns]
        logger.info("Columns detected: %s", list(df.columns))

        # =========================
        # ✅ DETECT FAULT CODE
        # =========================
        if "FAULT CODE" not in df.columns:
            raise ValueError("Missing FAULT CODE column")

        # =========================
        # ✅ DETECT FAULT NAME (KEY LOGIC)
        # =========================
        fault_name_col = None

        # ✅ PRIORITY 1 → exact old format
        if "FAULT NAME" in df.columns:
            fault_name_col = "FAULT NAME"

        # ✅ PRIORITY 2 → detect dynamic column (new Excel)
        if fault_name_col is None:
            for col in df.columns:

                if col == "FAULT CODE":
                    continue

                # detect path-like headers
                if ("\\" in col or "/" in col or "[" in col):
                    fault_name_col = col
                    break

        # ✅ PRIORITY 3 → fallback: first non FAULT CODE column
        if fault_name_col is None:
            for col in df.columns:
                if col != "FAULT CODE":
                    fault_name_col = col
                    break

        if fault_name_col is None:
            raise ValueError("Could not detect FAULT NAME column")

        logger.info("Using FAULT NAME column: %s", fault_name_col)

        # =========================
        # ✅ MANUAL COLUMN (OPTIONAL)
        # =========================
        if "ERROR LIST NAME FOR MANUAL" not in df.columns:
            logger.warning("Missing manual column → using empty")
            df["ERROR LIST NAME FOR MANUAL"] = ""

        # =========================
        # ✅ CLEAN DATA
        # =========================
        df[fault_name_col] = df[fault_name_col].apply(clean_fault_name)

        # =========================
        # ✅ FAULT CODE CLEAN
        # =========================
        df["FAULT CODE"] = pd.to_numeric(df["FAULT CODE"], errors="coerce")
        df = df.dropna(subset=["FAULT CODE"])

        # =========================
        # ✅ GROUP LOGIC
        # =========================
        cleaned_records = []

        for code, sub in df.groupby("FAULT CODE"):

            names = []
            manuals = []

            for _, r in sub.iterrows():

                n = str(r[fault_name_col]).strip()
                m = str(r["ERROR LIST NAME FOR MANUAL"]).strip()

                if n and n not in names:
                    names.append(n)

                if m and m not in manuals:
                    manuals.append(m)

            cleaned_records.append({
                "FAULT CODE": int(code),
                "FAULT NAME": " | ".join(names[:2]) if names else "",
                "ERROR LIST NAME FOR MANUAL": " | ".join(manuals[:2]) if manuals else "",
            })

        # =========================
        # ✅ BUILD FINAL DICT
        # =========================
        mapping: Dict[int, Dict[str, str]] = {}

        for row in cleaned_records:
            mapping[row["FAULT CODE"]] = {
                "FAULT NAME": row["FAULT NAME"],
                "ERROR LIST NAME FOR MANUAL": row["ERROR LIST NAME FOR MANUAL"],
            }

        _tdm_cache[xlsx_path] = mapping

        logger.info("TDM mapping loaded ✅")

        return mapping

    except Exception:
        logger.exception("ERROR analyzing TDM file: %s", xlsx_path)
        raise