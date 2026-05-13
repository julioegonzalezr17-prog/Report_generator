import pandas as pd

def csv_to_excel_with_fill(input_csv)-> str:
    """
    Convert a CSV log file into an Excel file (.xlsx),
    cleaning empty columns and filling missing values.

    Features:
    - Removes fully empty columns
    - Forward fills previous values (ffill)
    - Fills remaining empty cells with 0
    - Converts Timestamp column to datetime
    - Sorts data by Timestamp
    """

    # -------- READ CSV --------
    df = pd.read_csv(input_csv)

    # -------- CLEAN DATA --------

    # Drop columns that are completely empty
    df = df.dropna(axis=1, how='all')

    # Clean column names (remove backslashes if any)
    df.columns = [col.replace("\\", "") for col in df.columns]

    # Convert Timestamp column to datetime format
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

    # -------- FILL MISSING VALUES --------

    # Forward fill: propagate last valid value forward
    df = df.ffill()

    # Fill remaining NaN values with 0
    df = df.fillna(0)

    # -------- SORT DATA --------

    if 'Timestamp' in df.columns:
        df = df.sort_values(by='Timestamp')

    # -------- EXPORT TO EXCEL --------

    output_excel = input_csv.replace(".csv", ".xlsx")
    df.to_excel(output_excel, index=False, engine='openpyxl', freeze_panes=(1, 0))
    return output_excel
