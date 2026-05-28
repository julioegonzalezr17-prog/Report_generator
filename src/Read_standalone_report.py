import pandas as pd

def normalize(text):
    return str(text).upper().replace("°", "").replace("_", " ").strip()

def find_header_row(df):
    """
    Encuentra la fila que probablemente contiene los headers
    """
    for i in range(min(20, len(df))):  # escanea primeras 20 filas
        row = df.iloc[i].astype(str).apply(normalize)

        hits = 0
        for cell in row:
            if "REFERENCE" in cell:
                hits += 1
            if "TEST N" in cell:
                hits += 1
            if "SCOPO DEL TEST" in cell:
                hits += 1

        # si encuentra suficientes coincidencias → header
        if hits >= 2:
            return i

    return 0  # fallback

def load_excel_tests(file_path: str):
    # Leer sin header
    raw_df = pd.read_excel(file_path, header=None, engine="openpyxl")

    # Detectar fila header
    header_row = find_header_row(raw_df)
    print(header_row)

    # Leer otra vez con header correcto
    df = pd.read_excel(file_path, header=header_row, engine="openpyxl")

    # Normalizar nombres de columnas
    columns_map = {col: normalize(col) for col in df.columns}

    col_test = None
    col_scope = None
    col_log = None

    for original, norm in columns_map.items():
        if "TEST N" in norm:
            col_test = original
        elif "SCOPO DEL TEST" in norm:
            col_scope = original
        elif "REFERENCE" in norm:
            col_log = original

    data = []
    for _, row in df.iterrows():
        test_num = row.get(col_test)
        scope = row.get(col_scope)

        if pd.isna(test_num):
            continue

        data.append({
            "test": str(test_num),
            "scope": str(scope),
            "log": ""
        })

    return data