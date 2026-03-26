import os
import csv
import pandas as pd
from typing import List, Tuple, Optional, Dict, Callable, Union
import logging
logger = logging.getLogger(__name__)


def _detect_separator(sample: str, candidates: Tuple[str, ...] = (',', ';', '\t', '|')) -> Optional[str]:
    """Intenta detectar el separador con csv.Sniffer; si falla, None."""
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=''.join(candidates))
        return dialect.delimiter
    except Exception:
        return None

def _robust_read_lines(csv_path: str, encodings=('utf-8', 'cp1252', 'latin1')) -> Tuple[List[str], str]:
    """
    Lee el archivo como líneas con una lista de encodings de fallback.
    Retorna (lines, encoding_usado). Reemplaza caracteres inválidos.
    """
    last_err = None
    for enc in encodings:
        try:
            with open(csv_path, 'r', encoding=enc, errors='replace') as f:
                return f.readlines(), enc
        except Exception as e:
            last_err = e
    # Si nada funcionó (muy raro), relanza el último error
    raise last_err if last_err else RuntimeError("No se pudo leer el archivo por ninguna codificación.")

def _normalize_to_four_fields(rows: List[List[str]], sep: str, expected_cols: int = 4) -> List[List[str]]:
    """
    Asegura que cada fila tenga exactamente expected_cols columnas.
    - Si tiene más, concatena extras en la última columna (unidas por el separador).
    - Si tiene menos, rellena con ''.
    """
    norm = []
    for r in rows:
        if len(r) < expected_cols:
            r = r + [''] * (expected_cols - len(r))
        elif len(r) > expected_cols:
            head = r[:expected_cols - 1]
            tail_join = sep.join(r[expected_cols - 1:])
            r = head + [tail_join]
        norm.append(r)
    return norm

def load_tdm_config(csv_path: str) -> dict:
    """Load a DGTO configuration CSV and return a nested dictionary.

    Expected: no header, exactly four columns (DGTO, reg_DGTO, name_DGTO, info_DGTO).
    Returns: {<basename>: {"DGTO": [...], "reg_DGTO": [...], "name_DGTO": [...], "info_DGTO": [...]}}

    Raises:
        FileNotFoundError: si el archivo no existe.
        ValueError: si no se pueden obtener 4 columnas tras normalización.
    """
    logger.info("Reading TDM configuration file: %s", csv_path)
    try:
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        lines, used_encoding = _robust_read_lines(csv_path, encodings=('utf-8', 'cp1252', 'latin1'))

        raw_lines = [ln.rstrip('\n') for ln in lines if ln.strip() != '']

        if not raw_lines:
            raise ValueError("El archivo CSV está vacío o sólo contiene líneas en blanco.")

        sample = '\n'.join(raw_lines[:100])  # muestra limitada
        sep = _detect_separator(sample, candidates=(',', ';', '\t', '|')) or ';'  # preferencia por ';'

        try:
            df = pd.read_csv(
                csv_path,
                header=None,
                dtype=str,
                sep=sep,
                encoding=used_encoding,
                engine='python',
                on_bad_lines='skip',
                quoting=csv.QUOTE_MINIMAL,
                keep_default_na=False
            )
            # Si pandas leyó 0 filas, caemos a manual
            if df.shape[0] == 0 or df.shape[1] == 0:
                raise ValueError("Lectura con pandas produjo DataFrame vacío; se intentará modo manual.")
            rows = df.astype(str).values.tolist()
        except Exception:
            # 4) Modo manual: split por separador detectado y normalización
            rows = [ln.split(sep) for ln in raw_lines]

        # 5) Normalizar a exactamente 4 columnas
        normalized = _normalize_to_four_fields(rows, sep=sep, expected_cols=4)

        # 6) Validación: si tras normalizar aún hay irregularidades (no debería)
        bad_lengths = [len(r) for r in normalized if len(r) != 4]
        if bad_lengths:
            # Preparar diagnóstico mínimo
            sample_bad = [r for r in normalized if len(r) != 4][:3]
            raise ValueError(
                f"No se pudo obtener un dataset consistente de 4 columnas. "
                f"Líneas problemáticas: {len(bad_lengths)}. Ejemplos: {sample_bad[:3]}"
            )

        # 7) Construir DataFrame final con columnas requeridas
        df_final = pd.DataFrame(normalized, columns=["DGTO", "reg_DGTO", "name_DGTO", "info_DGTO"])

        # 8) Armar el dict de salida
        base = os.path.splitext(os.path.basename(csv_path))[0]
        result = {base: {col: df_final[col].tolist() for col in df_final.columns}}
        logger.debug("TDM configuration succesfully loaded, dictionary crated")
        return result
    except Exception:
        logger.exception("ERROR analizing: %s", csv_path)
        raise




def get_internal_dataset(data: dict) -> dict:
    """
    Extracts the internal dictionary from the structure:
        {basename: {DGTO: [...], reg_DGTO: [...], ...}}
    """
    if not isinstance(data, dict) or len(data) != 1:
        raise ValueError("Expected a dictionary with exactly one top-level key.")

    inner = next(iter(data.values()))

    if not isinstance(inner, dict):
        raise ValueError("Invalid internal structure in dataset.")

    return inner


def default_normalizer(x: Optional[str], case_insensitive: bool) -> str:
    """
    Normalize string for comparison: strip and optional lowercase.
    """
    if x is None:
        return ""
    x = str(x).strip()
    return x.lower() if case_insensitive else x


def find_positions( data: dict,
                    key: str,
                    values: Union[str, List[str]],
                    *,
                    mode: str = "exact",           # "exact" or "contains"
                    case_insensitive: bool = True
                ) -> Dict[str, List[int]]:
    """
    Searches for positions (indices) in the list associated with `key` inside
    the dictionary produced by load_tdm_config().

    Parameters
    ----------
    data : dict
        The dictionary returned by load_tdm_config().
    key : str
        Column name to search ("DGTO", "reg_DGTO", "name_DGTO", "info_DGTO").
    values : str or list of str
        Value(s) to search for.
    mode : str, optional
        "exact" for exact match, "contains" for substring match.
    case_insensitive : bool, optional
        If True, search ignores capitalization.

    Returns
    -------
    Dict[str, List[int]]
        Mapping of each searched value to a list of positions where it appears.
    """

    inner = get_internal_dataset(data)

    if key not in inner:
        raise KeyError(f"Column '{key}' not found. Available: {list(inner.keys())}")

    vec = inner[key]

    # Ensure values is a list
    query_values = values if isinstance(values, list) else [values]

    # Normalize full vector once
    norm_vec = [
        default_normalizer(x, case_insensitive=case_insensitive)
        for x in vec
    ]


    # Validate mode
    if mode not in ("exact", "contains"):
        raise ValueError("mode must be 'exact' or 'contains'.")

    all_positions = []

    # Perform search
    for q in query_values:
        nq = default_normalizer(q, case_insensitive=case_insensitive)

        if mode == "exact":
            positions = [i for i, nv in enumerate(norm_vec) if nv == nq]
        else:  # mode == "contains"
            if nq == "":
                positions = []
            else:
                positions = [i for i, nv in enumerate(norm_vec) if nq in nv]

        all_positions.extend(positions)

    # Remove duplicates and keep order
    unique_positions = sorted(set(all_positions))

    return unique_positions


