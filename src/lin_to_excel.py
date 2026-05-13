import pandas as pd
from openpyxl import load_workbook

def lin_csv_to_excel(input_csv)-> str:
    """
    Process LIN communication CSV into a single Excel sheet.

    - Correct forward fill (fixed)
    - No NaN → all zeros or propagated values
    - Single sheet
    - Header frozen
    """

    # -------- READ CSV --------
    df = pd.read_csv(input_csv, sep=';', low_memory=False)

    # -------- CLEAN --------

    df = df.dropna(axis=1, how='all')
    df = df.dropna(how='all')

    df.columns = [col.replace("\\", "").strip() for col in df.columns]

    # IMPORTANT: do NOT convert to string here ❗

    # Replace empty strings with NaN
    df = df.replace(r'^\s*$', pd.NA, regex=True)

    # -------- FORWARD FILL --------

    non_fill_columns = ['Timestamp', 'Comand Type', 'Data Frame']
    non_fill_columns = [col for col in non_fill_columns if col in df.columns]

    data_columns = [col for col in df.columns if col not in non_fill_columns]

    # Forward fill works correctly NOW
    df[data_columns] = df[data_columns].ffill()

    # Replace remaining NaN with 0
    df[data_columns] = df[data_columns].fillna(0)

    # Final safety (everything)
    df = df.fillna(0)

    # -------- SORT --------
    if "Timestamp" in df.columns:
        df = df.sort_values(by="Timestamp")

    # -------- EXPORT --------
    output_excel = input_csv.replace(".csv", ".xlsx")
    df.to_excel(
        output_excel,
        sheet_name="LIN_Data",
        index=False,
        engine='openpyxl',
        freeze_panes=(1, 0)
    )

    # -------- AUTO WIDTH --------
    wb = load_workbook(output_excel)
    ws = wb.active

    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter

        for cell in col:
            if cell.value is not None:
                max_length = max(max_length, len(str(cell.value)))

        ws.column_dimensions[col_letter].width = max_length + 2

    wb.save(output_excel)
    
    return output_excel
