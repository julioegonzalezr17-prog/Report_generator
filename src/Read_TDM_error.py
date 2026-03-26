import os
import pandas as pd
from typing import Dict, Any
import logging


# Cache to avoid reading the same file multiple times
# cache[path] = { fault_code: { "FAULT NAME": ..., "ERROR LIST NAME FOR MANUAL": ... } }
_tdm_cache: Dict[str, Dict[int, Dict[str, Any]]] = {}
logger = logging.getLogger(__name__)


def load_tdm_once(xlsx_path: str, header_row: int ) -> Dict[int, Dict[str, str]]:
    """
    Read the XLSX file only once, extract the 'TDM' sheet and build a dictionary
    keyed by FAULT CODE. If called again with the same path, cached data is reused.

    Parameters:
        xlsx_path: path to the Excel file
        header_row: 1-based row number where the header is located (default: 5)

    Returns a dictionary:
        {
            fault_code: {
                "FAULT NAME": str,
                "ERROR LIST NAME FOR MANUAL": str
            },
            ...
        }
    """
    logger.info("Reading TDM fault file: %s", xlsx_path)
    try:
        # Return from cache if available
        if xlsx_path in _tdm_cache:
            return _tdm_cache[xlsx_path]

        # Open the Excel file
        try:
            xl = pd.ExcelFile(xlsx_path, engine="openpyxl")
        except PermissionError as e:
            raise PermissionError(
                f"Cannot open file '{xlsx_path}'. Check permissions the file is locked by OneDrive or Excel. Original: {e}"
            )
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {xlsx_path}") from e

        # Normalization helper to find the TDM sheet
        def norm(s):
            return " ".join(str(s).strip().upper().split())

        # Find the TDM sheet (tolerant search)
        tdm_sheet = None
        for sheet in xl.sheet_names:
            if norm(sheet) == "TDM" or norm(sheet).startswith("TDM"):
                tdm_sheet = sheet
                break

        if tdm_sheet is None:
            logger.info("TDM sheet %s not found in ", tdm_sheet, xlsx_path)
            raise ValueError(f"TDM sheet not found in {xlsx_path}")

        # Determine the 0-based header index for pandas (user passes 1-based row)
        header_index = max(0, header_row - 1)

        # Read the TDM sheet using the specified header row
        df = pd.read_excel(xl, sheet_name=tdm_sheet, engine="openpyxl", header=header_index)

        # Normalize column names
        df.columns = [norm(c) for c in df.columns]

        # Required columns
        required_cols = ["FAULT CODE", "FAULT NAME", "ERROR LIST NAME FOR MANUAL"]
        for c in required_cols:
            if c not in df.columns:
                logger.info(f"Missing required column: {c}")
                raise ValueError(f"Missing required column: {c}")

        # Convert FAULT CODE to integer
        df["FAULT CODE"] = pd.to_numeric(df["FAULT CODE"], errors="coerce").astype("Int64")
        df = df.dropna(subset=["FAULT CODE"])

        # Handle duplicates:
        # - If a fault code has 2 or more rows, accept up to two distinct values
        #   and concatenate them (preserving original order) for both FAULT NAME
        #   and ERROR LIST NAME FOR MANUAL.
        # - If a fault code has 1 row, keep its values as-is.
        cleaned_records = []
        for code, sub in df.groupby("FAULT CODE"):
            # preserve the order of appearance
            names = []
            manuals = []
            for _, r in sub.iterrows():
                n = str(r["FAULT NAME"]).strip()
                m = str(r["ERROR LIST NAME FOR MANUAL"]).strip()
                if n not in names:
                    names.append(n)
                if m not in manuals:
                    manuals.append(m)

            # Take up to the first two distinct values
            combined_name = " | ".join(names[:2]) if names else ""
            combined_manual = " | ".join(manuals[:2]) if manuals else ""

            # Build a single representative row for this fault code
            cleaned_records.append({
                "FAULT CODE": int(code),
                "FAULT NAME": combined_name,
                "ERROR LIST NAME FOR MANUAL": combined_manual,
            })

        # Rebuild dataframe from cleaned records
        df = pd.DataFrame(cleaned_records)
        if not df.empty:
            df["FAULT CODE"] = pd.to_numeric(df["FAULT CODE"], errors="coerce").astype("Int64")
        else:
            df = pd.DataFrame(columns=["FAULT CODE", "FAULT NAME", "ERROR LIST NAME FOR MANUAL"]) 

        # Build final mapping
        mapping: Dict[int, Dict[str, str]] = {}
        for _, row in df.iterrows():
            code = int(row["FAULT CODE"])
            mapping[code] = {
                "FAULT NAME": str(row["FAULT NAME"]).strip(),
                "ERROR LIST NAME FOR MANUAL": str(row["ERROR LIST NAME FOR MANUAL"]).strip(),
            }

        # Save to cache
        _tdm_cache[xlsx_path] = mapping
        logger.debug("TDM fault list succesfully loaded, dictionary crated")
        return mapping
    except Exception:
        logger.exception("ERROR analizing: %s", xlsx_path)
        raise