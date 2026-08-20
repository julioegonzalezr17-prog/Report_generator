import pandas as pd
from typing import Tuple
import logging
import re

logger = logging.getLogger(__name__)


def detect_csv_delimiter(csv_path: str) -> str:
    """
    Detects whether the CSV file is delimited with ';' or ','.
    Reads only the first non-empty line.
    """
    logger.info("Finding delimiter: %s", csv_path)
    try:
        with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()

                if not line:    # skip empty lines
                    continue

                semicolons = line.count(";")
                commas = line.count(",")

                if semicolons == 0 and commas == 0:
                # No delimiter detected, return default
                    continue
                # Return whichever delimiter occurs more
                logger.debug("Delimiter detected")
                return ";" if semicolons >= commas else ","

        # File empty → default delimiter
        logger.debug("Delimiter by default: ;")
        return ";"
    except Exception:
        logger.exception("ERROR analizing: %s", csv_path)
        raise

def read_custom_csv(csv_path: str, separator: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Read a CSV file with a custom structure and generate both original
    and normalized headers.

    Returns:
        custom_header
        data_frame              -> original column names
        normalized_data_frame   -> headers without trailing "(...)"
    """

    logger.info("Reading data test: %s", csv_path)

    try:
        def normalize_header(header: str) -> str:
            """
            Examples:
            HP Compressor Model RD
                -> HP Compressor Model RD

            HP Compressor Model RD (4-15-3-29)
                -> HP Compressor Model RD
            """
            header = str(header).strip()

            # Remove trailing parenthesized content
            header = re.sub(r'\s*\([^)]*\)\s*$', '', header)

            return header.strip()

        # Read file
        lines = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            for line in f:
                lines.append(line.rstrip('\n\r'))

        # Metadata
        custom_header = pd.DataFrame({
            'Metadata': [lines[0], lines[1]]
        })

        # Original column names
        column_names = lines[2].split(separator)

        # Data rows
        data_rows = []
        for line in lines[4:]:
            if line.strip() and not line.strip().startswith("#ENDACQUISITION#"):
                data_rows.append(line.split(separator))

        # Original dataframe
        data_frame = pd.DataFrame(data_rows)

        if not data_frame.empty:

            if data_frame.shape[1] > len(column_names):
                column_names.extend(
                    [f"Column_{i}" for i in range(len(column_names), data_frame.shape[1])]
                )

            data_frame.columns = column_names[:data_frame.shape[1]]

            # Numeric conversion
            for i, col in enumerate(data_frame.columns):
                if i >= 2:
                    try:
                        data_frame[col] = pd.to_numeric(data_frame[col], errors='coerce')
                    except Exception:
                        pass

            data_frame.reset_index(drop=True, inplace=True)

        # Create dataframe with normalized headers
        normalized_data_frame = data_frame.copy()

        if not normalized_data_frame.empty:
            normalized_data_frame.columns = [
                normalize_header(col)
                for col in normalized_data_frame.columns
            ]

        logger.debug("File read successfully")

        return custom_header, data_frame, normalized_data_frame

    except Exception:
        logger.exception("ERROR loading data: %s", csv_path)
        return None, None, None


def save_to_excel(excel_path: str, custom_header: pd.DataFrame, data_frame: pd.DataFrame) -> None:
    """
    Write the custom header and data frame to an Excel file.

    Layout:
        - Rows 1-2: custom header data
        - Rows 3+: data frame with column names

    Parameters:
        excel_path: path to the output Excel file
        custom_header: DataFrame with the first two metadata rows
        data_frame: DataFrame with the main data
    """
    logger.info("Saving data test: %s", excel_path)
    try:
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            # Write custom header rows (rows 1-2)
            custom_header.to_excel(
                writer, index=False, header=False, sheet_name="DATA"
            )

            # Write data frame starting from row 3 (startrow=2 means row 3 in 1-based indexing)
            data_frame.to_excel(
                writer, index=False, sheet_name="DATA", startrow=2
            )
            
            # FREEZE PANES (Row 3)
            ws = writer.book["DATA"]
            ws.freeze_panes = "A4"

            logger.debug("File saved succesfully !!!!!")
    except Exception:
        logger.exception("ERROR saving data: %s", excel_path)    
        raise