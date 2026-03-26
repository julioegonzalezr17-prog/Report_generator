import pandas as pd
import logging

logger = logging.getLogger(__name__)


def load_test_definition_xlsx(path_xlsx: str, sheet_name:str) -> dict:

    """
    Load an XLSX file defining the test variables for CSV analysis.
    Creates a dictionary indexed by Test Number (first column),
    where each key maps to another dictionary containing the attributes
    for that test. Supports heterogeneous attributes (different columns
    populated for each test).

    Returns:
        test_dict = {
            test_number: {
                "ATTRIBUTE_1": value,
                "ATTRIBUTE_2": value,
                ...
            },
            ...
        }
    """

    # Load raw XLSX (infer sheet if not provided)
    logger.info("Reading test configuration file: %s", path_xlsx)
    try:
        xl = pd.ExcelFile(path_xlsx, engine="openpyxl")

        # If user didn't specify sheet name, take the first one
        if sheet_name is None:
            sheet_name = xl.sheet_names[0]
        df = pd.read_excel(path_xlsx, sheet_name=sheet_name, engine="openpyxl")

        # Normalize headers
        df.columns = [
            " ".join(str(c).strip().upper().split())
            for c in df.columns
        ]

        # Test Number must be the first column
        first_col = df.columns[0]

        # Convert Test Number to integer (safe conversion)
        df[first_col] = pd.to_numeric(df[first_col], errors="coerce").astype("Int64")

        # Drop rows without a valid test number
        df = df.dropna(subset=[first_col])

        # Build dictionary
        test_dict = {}

        for _, row in df.iterrows():
            test_number = int(row[first_col])

            # Attributes = all columns except the first
            attributes = {}
            for col in df.columns[1:]:
                val = row[col]

                # Ignore completely empty values
                if pd.notna(val):
                    attributes[col] = val

            test_dict[test_number] = attributes
        logger.debug("Test configuration succesfully loaded, dictionary crated")
        return test_dict
    except Exception:
        logger.exception("ERROR analizing: %s", path_xlsx)
        raise
    