import pandas as pd
from typing import Tuple
import logging

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

def read_custom_csv(csv_path: str, separator: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Read a CSV file with a custom structure.

    Format expected:
        - Line 0: metadata/header line (raw, not used as data)
        - Line 1: metadata/header line (raw, not used as data)
        - Line 2: actual column names
        - Line 3: blank/separator (skipped)
        - Line 4+: data rows

    Parameters:
        csv_path: path to the CSV file
        separator: field delimiter (default: ";")

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]:
            - custom_header: first two rows as a DataFrame (for reference)
            - data_frame: the main data starting from line 4, with proper column names from line 2
    """
    logger.info("Reading data test: %s", csv_path)
    try:
        # Read the file line-by-line to handle the exact structure
        lines = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            for line in f:
                lines.append(line.rstrip('\n\r'))

        # Extract metadata rows (lines 0-1) as 2 rows, 1 column
        custom_header = pd.DataFrame({
            'Metadata': [lines[0], lines[1]]
        })

        # Extract column names from line 2
        column_names = lines[2].split(separator)

        # Extract data from line 4 onwards (skip blank line 3)
        data_rows = []
        for line in lines[4:]:
            if line.strip() and not line.strip().startswith("#ENDACQUISITION#"):  # Only process non-empty lines and exclude #ENDACQUISITION#
                row = line.split(separator)
                data_rows.append(row)

        # Create data frame
        data_frame = pd.DataFrame(data_rows)
        if not data_frame.empty:
            # Assign column names, handling extra columns if any
            if data_frame.shape[1] > len(column_names):
                column_names.extend([f"Column_{i}" for i in range(len(column_names), data_frame.shape[1])])
            data_frame.columns = column_names[:data_frame.shape[1]]
            
            # Keep first two columns as strings (for time data)
            # Convert remaining columns to numeric
            for i, col in enumerate(data_frame.columns):
                if i >= 2:  # Skip first two columns
                    try:
                        data_frame[col] = pd.to_numeric(data_frame[col], errors='coerce')
                    except Exception:
                        pass  # Keep as string if conversion fails
            
            data_frame.reset_index(drop=True, inplace=True)

        logger.debug("File read succesfully data extracted!!!!!")
        return custom_header, data_frame
    except Exception as e:
        logger.exception("ERROR aloading data: %s", csv_path)
        return None, None


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
            logger.debug("File saved succesfully !!!!!")
    except Exception:
        logger.exception("ERROR saving data: %s", excel_path)    
        raise