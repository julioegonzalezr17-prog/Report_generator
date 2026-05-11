import os
from pathlib import Path
import win32com.client as win32
import pywintypes
import logging

logger = logging.getLogger(__name__)

# ---------------------------
# Utilities
# ---------------------------
def normalize_header(value):
    """Case-insensitive, trimmed text normalization."""
    if value is None:
        return ""
    return str(value).strip().lower()

def get_effective_cell_value(ws, row, col):
    """In Excel COM, merged cells already return the visible value."""
    return ws.Cells(row, col).Value

def find_header_rows(ws, expected_headers=("Test Env", "Test N°", "Test scope"),
                    start_row=1, end_row=None):
    """Find all rows where first 3 columns match the expected headers."""
    if end_row is None:
        end_row = ws.UsedRange.Rows.Count

    expected = [normalize_header(h) for h in expected_headers]
    found = []
    for r in range(start_row, end_row + 1):
        c1 = normalize_header(get_effective_cell_value(ws, r, 1))
        c2 = normalize_header(get_effective_cell_value(ws, r, 2))
        c3 = normalize_header(get_effective_cell_value(ws, r, 3))
        if [c1, c2, c3] == expected:
            found.append(r)
    return found

def segment_tables_by_headers(ws, header_rows):
    """Build (header_row, last_row_of_this_table) segments."""
    if not header_rows:
        return []
    last_row = ws.UsedRange.Rows.Count
    segments = []
    for i, h in enumerate(header_rows):
        if i < len(header_rows) - 1:
            segments.append((h, header_rows[i+1] - 1))
        else:
            segments.append((h, last_row))
    return segments

def equal_test_number(value, test_num):
    """
    Robust comparison between Excel COM values and your string test number.
    Handles 1 vs "1" vs "01" vs 1.0.
    """
    if value is None:
        return False
    try:
        return float(value) == float(test_num)
    except Exception:
        return str(value).strip().lower() == str(test_num).strip().lower()

def _norm_win_path(p: str) -> str:
    """
    Normalize a Windows path for Excel:
    - absolute path
    - backslashes
    - no URL-encoding
    """
    p = str(Path(p).resolve())
    p = os.path.normpath(p)
    return p

def _ensure_xlsx(p: str) -> str:
    """Ensure the file name ends with .xlsx."""
    if not p.lower().endswith(".xlsx"):
        p = p + ".xlsx"
    return p

def _looks_like_file(payload: str) -> bool:
    """
    Decide if payload is a local file path (for hyperlink).
    Extend as needed (add more extensions).
    """
    if not isinstance(payload, str):
        return False
    lower = payload.lower()
    return lower.endswith(".xlsx") or lower.endswith(".csv") or lower.endswith(".txt") or lower.endswith(".log")


# ---------------------------
# MAIN FUNCTION (pywin32)
# ---------------------------
def modify_excel_with_headers(
        excel_path: str,
        search_header: dict,      # {"TDM log": link, "Lin Log": link, "Modbus Log": link, "Analysis": text, Supporting Data: image path}
        test_num: str,            # locate row where "Test N°" == test_num
        output_path: str = None,
        table_header_structure=("Test Env", "Test N°", "Test scope")
    )->str:
    """
    Edits the workbook via Excel COM (pywin32) so that images, charts, shapes,
    formatting and everything else are preserved.

    - Finds table header rows by structure.
    - Locates the row where column "Test N°" matches test_num.
    - For each header in search_header:
        * if value looks like a file ⇒ adds a hyperlink
        * else writes plain text
    - Saves:
        * Save() if output_path is None (in-place),
        * SaveAs(FileFormat=51) if output_path is different (xlsx).
    """
    info_text = ""
    excel = win32.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    excel_path = _norm_win_path(excel_path)
    
    def safe_open_excel(path)->str:
        logger.info("Oppening report...: %s", path) 
        try:
            wb = excel.Workbooks.Open(path)
            logger.info("Report loaded...: %s", path)
            return wb   
        except pywintypes.com_error as e:
            logger.error("Report loaded Fail: %s", e)
            return None

    wb = safe_open_excel(excel_path)
    if wb is None:
        info_text = "ERROR"
        return info_text

    ws = wb.ActiveSheet

    # 1) Find header rows + segments
    header_rows = find_header_rows(ws, expected_headers=table_header_structure)
    if not header_rows:
        wb.Close(SaveChanges=False)
        excel.Quit()
        raise print("No table header rows found based on the provided structure.")

    segments = segment_tables_by_headers(ws, header_rows)

    # 2) Find the row inside the matching table where Test N° == test_num
    target_row = None
    header_for_this_table = None

    for header_row, last_row in segments:
        for r in range(header_row + 1, last_row + 1):
            value = get_effective_cell_value(ws, r, 2)  # Column 2 = "Test N°"
            if equal_test_number(value, test_num):
                target_row = r
                header_for_this_table = header_row
                break
        if target_row:
            break

    if not target_row:
        wb.Close(SaveChanges=False)
        excel.Quit()
        raise print(f"Test N° '{test_num}' not found in any table.")

    # 3) For each header in search_header, find its column and write
    last_col = ws.UsedRange.Columns.Count
    for header_name, payload in search_header.items():
        found_col = None

        for col in range(1, last_col + 1):
            header_val = get_effective_cell_value(ws, header_for_this_table, col)
            if normalize_header(header_val) == normalize_header(header_name):
                found_col = col
                break
        logger.info("Writting column ...: %s", found_col)    
        if not found_col:
            # Header not present in this table; skip
            continue

        cell = ws.Cells(target_row, found_col)

        
        is_supporting_data = normalize_header(header_name) == normalize_header("Supporting Data")
        is_image_path = isinstance(payload, str) and payload.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff"))        
        if is_supporting_data and is_image_path:
            try:
                img_path = _norm_win_path(payload)

                # 0) Desactivar compresión de imágenes a nivel de workbook (clave)
                try:
                    # ws.Parent es el Workbook
                    ws.Parent.DoNotCompressPictures = True
                except Exception:
                    pass

                # 1) Borrar imágenes previas ancladas exactamente a esta celda
                try:
                    to_delete = []
                    for i in range(1, ws.Shapes.Count + 1):
                        shp = ws.Shapes.Item(i)
                        try:
                            tl = shp.TopLeftCell
                            br = shp.BottomRightCell
                            if (tl.Row == target_row and tl.Column == found_col and
                                br.Row == target_row and br.Column == found_col):
                                to_delete.append(shp.Name)
                        except Exception:
                            pass
                    for name in to_delete:
                        try:
                            ws.Shapes.Item(name).Delete()
                        except Exception:
                            pass
                except Exception:
                    pass
                cell = ws.Cells(target_row, found_col)        
                # 2) Insertar con resolución ORIGINAL (sin forzar tamaño)
                #    Preferir AddPicture2 (Office 2010+) para evitar compresión interna.
                try:

                    pic = ws.Shapes.AddPicture2(
                        img_path, False, True,
                        cell.Left,
                        cell.Top,
                        -1, -1, 0                         
                    )
                    # Si AddPicture2 no soporta el arg 'Compress' en tu build, el código anterior igual inserta nativo.
                except Exception:
                    # Fallback: AddPicture clásico (tamaño nativo = Width/Height -1)
                    pic = ws.Shapes.AddPicture(
                        Filename=img_path,
                        LinkToFile=False,
                        SaveWithDocument=True,
                        Left=cell.Left,
                        Top=cell.Top,
                        Width=-1,  # tamaño original
                        Height=-1  # tamaño original
                    )

                # 3) No reducir calidad: solo ESCALAR SI SOBRA respecto a la celda (nunca ampliar)

                pic.LockAspectRatio = True
                pic.Placement = 2

                
                # 4) Ajustar la fila para que la imagen quepa (sin tocar la imagen)
                try:
                    # Añadimos un pequeño margen visual
                    desired_row_h = pic.Height + 4
                    if cell.RowHeight < desired_row_h:
                        cell.RowHeight = desired_row_h
                except Exception:
                    pass

                # 5) (Opcional) Ajustar la columna para que quepa el ancho de la imagen
                #    ColumnWidth está en "caracteres", no en puntos. Convertimos proporcionalmente.
                try:
                    current_cell_w_pts = cell.Width  # puntos
                    if current_cell_w_pts > 0 and pic.Width + 4 > current_cell_w_pts:
                        factor = (pic.Width + 4) / current_cell_w_pts
                        new_col_width = cell.ColumnWidth * factor
                        # Afecta a toda la columna; si no quieres cambiar el layout, comenta estas dos líneas.
                        ws.Columns(found_col).ColumnWidth = new_col_width
                except Exception:
                    pass

                # 6) Centrar visualmente dentro de la celda actual (si queda algo de margen)
                try:
                    pic.Left = cell.Left + max((cell.Width - pic.Width) / 2, 0)
                    pic.Top  = cell.Top  + max((cell.Height - pic.Height) / 2, 0)
                except Exception:
                    pass

                # Refuerzo: evitar compresión otra vez
                try:
                    ws.Parent.DoNotCompressPictures = True
                except Exception:
                    pass

            except Exception:
                # Fallback: si algo falla, al menos escribir la ruta como texto
                cell.Value = str(payload)   
            continue

        if _looks_like_file(payload):
            addr = _norm_win_path(payload)  # absolute, backslashes, no %20
            # Clear cell before adding hyperlink to ensure TextToDisplay is shown
            cell.Value = None
            cell.Hyperlinks.Delete()
            # If another workbook with the same name is open, Excel can complain.
            # Optional: ensure unique save names or close duplicates beforehand.
            ws.Hyperlinks.Add(
                Anchor=cell,
                Address=addr,
                TextToDisplay=f"{header_name}_test_{test_num}"
            )
        else:
            cell.Value = str(payload)
        logger.info("File updated header: %s", header_name)     # addd the name of the file to check format
    # 4) Save safely
    try:
        if output_path is None or _norm_win_path(output_path) == excel_path:
            # Same file ⇒ Save (not SaveAs)
            wb.Save()
        else:
            out = _ensure_xlsx(_norm_win_path(output_path))

            # WARNING about duplicate names:
            # Excel cannot keep two workbooks with the same Name open in the same instance.
            # If a workbook with the same file name is open (even in another folder),
            # SaveAs may throw. Ensure uniqueness or close duplicates.

            # 51 = xlOpenXMLWorkbook (.xlsx)
            wb.SaveAs(Filename=out, FileFormat=51)
            logger.info("Saved file %s", out) 
    except Exception as e:
        # Helpful diagnostics
        try:
            name_now = wb.Name
        except Exception:
            name_now = "<unknown>"
        wb.Close(SaveChanges=False)
        excel.Quit()
        raise logger.error("ERROR saving %s", e) from e

    wb.Close(SaveChanges=True)
    excel.Quit()
    return output_path or excel_path