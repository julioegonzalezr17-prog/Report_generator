import code

from pathlib import Path
from typing import List, Optional, Tuple
import math

import matplotlib.pyplot as plt
from unittest import result

from openpyxl import load_workbook
from openpyxl.styles import Border, PatternFill, Font, Alignment, Side
from openpyxl.formatting.rule import CellIsRule
import pandas as pd
from Read_report_file import normalize_header
from dictDataIntegration import error_list_LIN, status_TDM
import logging
import re

logger = logging.getLogger(__name__)


class ExcelStyler:
    """
    Utility class to customize Excel files created by pandas.
    Provides functionality for:
        - styling rows and columns
        - highlighting
        - adding columns at specific positions
        - conditional formatting
        - autosizing
        - saving changes safely
    """

    def __init__(self, initial_data: dict, 
                file_path: str, 
                tdm_dict: dict,
                sheet_name: str = "DATA"
                ):
        self.file_path = file_path
        logger.info("Reading Data file: %s", file_path)
        self.wb = load_workbook(file_path)
        logger.debug("Data file uploaded successfully: %s", file_path)
        self.ws = self.wb[sheet_name]
        self.start_row = 3  # Assuming headers are on row 3, data starts from row 4
        self.tdm_dict = tdm_dict or {}
        self.initial_data = initial_data

    def find_header_from_column(self, col)->list:
        logger.info("find_header_from_column INPUT: %s", col)
        if not isinstance(col, list):
            col = [col]
        headers = []    
        for num in col:                
            value = self.ws.cell(row=self.start_row, column=col).value
            if value is None:
                continue
            headers.append(self.ws.cell(row=self.start_row, column=num).value)
        logger.info("find_header_from_column OUTPUT: %s", headers)
        return headers

    # --------------------------------------------------------------
    # Highlight a full row
    # --------------------------------------------------------------
    def highlight_row(self, row, color: str = "FFFF00"):
        """
        Highlight one or multiple rows using a background color (hex).
        Accepts either a single row index (`int`) or an iterable of row indices (list/tuple).
        Example color: 'FFFF00' = yellow
        """
        logger.info("highlight_row INPUT: %s", row)
        fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        # Normalize to an iterable of row indices
        if isinstance(row, int):
            rows = (row,)
        else:
            # Accept strings that represent integers as well as iterables
            try:
                # If single string like "5"
                if isinstance(row, str):
                    rows = (int(row),)
                else:
                    # Iterable: convert items that are numeric strings to ints
                    rows = tuple(int(r) if isinstance(r, str) and r.isdigit() else r for r in row)
            except Exception:
                # Fallback: try to cast single value to int
                try:
                    rows = (int(row),)
                except Exception:
                    raise ValueError("`row` must be an int, a string integer, or an iterable of ints/string-integers")

        for r in rows:
            for col in range(1, self.ws.max_column + 1):
                self.ws.cell(row=r, column=col).fill = fill
        logger.info("highlight_row OUTPUT: OK")

    # --------------------------------------------------------------
    # Highlight a full column
    # --------------------------------------------------------------
    def highlight_column(self, col, color: str):
        """
        Highlight one or multiple columns using a background color.
        Accepts either a single column index (`int`) or an iterable of column indices (list/tuple).
        Column indices are 1-based (1 = A, 2 = B, etc.).
        color es OBLIGATORIO: hexadecimal sin '#' (ejemplo: 'FFFF00' para amarillo)
        """

        logger.info("highlight_column INPUT: %s", col)
        if color is None:
            raise ValueError("highlight_column needs color from JSON")
        fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        # Normalize to an iterable of column indices or header names
        def resolve_item(item):
            # int -> return as-is
            if isinstance(item, int):
                return item
            # column letter like 'A' -> number
            if isinstance(item, str):
                # First try header name lookup (headers are on row 3)
                col_letter = self.find_header_column(item)
                if col_letter:
                    return self.cell_letter_to_number(col_letter)
                # If the string is an Excel column letter (A, B, AA)
                if item.isalpha():
                    return self.cell_letter_to_number(item)
                # If string looks like a digit, convert
                if item.isdigit():
                    return int(item)
            raise ValueError(f"Cannot resolve column specifier: {item}")

        # If user passed an explicit list/tuple of headers (strings), resolve them first
        if isinstance(col, (list, tuple)) and all(isinstance(x, str) for x in col):
            resolved = []
            missing = []
            for header in col:
                col_letter = self.find_header_column(header)
                if col_letter:
                    resolved.append(self.cell_letter_to_number(col_letter))
                else:
                    missing.append(header)
            if missing:
                print(f"Header(s) not found: {missing}")                
            cols = tuple(resolved)
        else:
            if isinstance(col, (int, str)):
                cols = (resolve_item(col),)
            else:
                # Assume iterable of mixed types
                cols = tuple(resolve_item(c) for c in col)

        # Start highlighting from header row (row 3) down to last data row
        
        for c in cols:
            for row in range(self.start_row, self.ws.max_row + 1):
                self.ws.cell(row=row, column=c).fill = fill
        logger.info("highlight_column OUTPUT: OK")

    # --------------------------------------------------------------
    # Add a new column at a specific position
    # --------------------------------------------------------------
    def insert_column(self, existing_header, header, default_value=None):
        """
        Insert a new column at the given position (1-indexed).
        Shifts existing columns to the right.
        """
        logger.info("insert_column INPUT: %s", header)
        if not isinstance(existing_header,list):
            existing_header = [existing_header]
        if not isinstance(header,list):
            header = [header]
        for col_ex_name, new_col in zip(existing_header,header):
            position = self.cell_letter_to_number(self.find_header_column(col_ex_name))
            if position is None:
                raise ValueError(f"Header '{col_ex_name}' not found")
            self.ws.insert_cols(position)

            # Write header
            cell = self.ws.cell(row=self.start_row, column=position, value=new_col)
            cell.font = Font(bold=True)
            
            thin_border = Border(
                left=Side(style="thin", color="000000"),
                right=Side(style="thin", color="000000"),
                top=Side(style="thin", color="000000"),
                bottom=Side(style="thin", color="000000")
            )
            cell.border = thin_border

            # Write default values
            for r in range(self.start_row + 1, self.ws.max_row + 1):
                self.ws.cell(row=r, column=position, value=default_value)
        logger.info("insert_column OUTPUT: %s", header)

    # --------------------------------------------------------------
    # Populate fault name column based on a list of fault codes and the TDM dictionary
    # --------------------------------------------------------------  
    def populate_fault_names(self)->list:
        """
        Populate a new column with given values. 
        This is a custom method that looks up fault codes in the TDM dictionary and fills the corresponding fault names.
        """
        logger.info("populate_fault_names working...")
        header = "Fault_Code"
        col = self.cell_letter_to_number(self.find_header_column(header))
        
        fault_names = []
        for r in range(self.start_row + 1, self.ws.max_row + 1):
            fault_codes = self.ws.cell(row=r, column=col).value
            if fault_codes is None:
                fault_names.append(None)
                continue
            if fault_codes in self.tdm_dict.keys():
                fault_names.append(self.tdm_dict[fault_codes]["FAULT NAME"])
            elif fault_codes == 65535:
                fault_names.append("No fault")
            else:
                fault_names.append("Code Fault not found in TDM")
        # print(f"Fault names populated: {fault_names}")  
        logger.info("populate_fault_names OUTPUT: OK")      
        return fault_names
    
    def populate_lin_fault(self)->list:
        """
        Populate a new column with given values. 
        This is a custom method that looks up fault codes in the TDM dictionary and fills the corresponding fault names.
        """
        logger.info("populate_lin_fault working...")
        header = "LIN_PUMP_ERROR_CODE_ID"
        col = self.cell_letter_to_number(self.find_header_column(header))
        
        fault_names = []
        for r in range(self.start_row + 1, self.ws.max_row + 1):
            raw_value = self.ws.cell(row=r, column=col).value
            if raw_value is None:
                fault_names.append(None)
                continue
            try:
                fault_codes = int(raw_value)                
            except (TypeError, ValueError):
                fault_names.append("Invalid fault code format")
                continue

            if fault_codes in error_list_LIN:
                fault_names.append(error_list_LIN[fault_codes]["Name"] + "->" + error_list_LIN[fault_codes]["error_type"])
            else:
                fault_names.append("Code Fault not found in Pump datasheet")   
        logger.info("populate_lin_fault OUTPUT: OK")     
        return fault_names

    def populate_tdm_status(self)->list:
        """
        Populate a new column with given values. 
        This is a custom method that looks up status codes in the status_TDM dictionary and fills the corresponding status names.
        """
        logger.info("populate_tdm_status working...")
        header = "TDM_STATUS"
        col = self.cell_letter_to_number(self.find_header_column(header))
        
        status_names = []
        for r in range(self.start_row + 1, self.ws.max_row + 1):
            raw_value = self.ws.cell(row=r, column=col).value
            if raw_value is None:
                status_names.append(None)
                continue
            try:
                status_codes = int(raw_value)                
            except (TypeError, ValueError):
                status_names.append("Invalid status code format")
                continue

            if status_codes in status_TDM:
                status_names.append(status_TDM[status_codes])
            else:
                status_names.append("Status code not found in TDM")   
        logger.info("populate_tdm_status OUTPUT: OK")     
        return status_names

    # --------------------------------------------------------------
    # Populate a new column 
    # --------------------------------------------------------------  
    def populate_column(self, header: str, values: list):
        """
        Populate a new column with given values.
        """
        logger.info("populate_column: %s",header)
        col = self.cell_letter_to_number(self.find_header_column(header))

        for r, val in enumerate(start=self.start_row + 1, iterable=values):
            self.ws.cell(row=r, column=col, value=val)
        logger.info("populate_column: OK")
    
    # --------------------------------------------------------------
    # Populate not in Fault_code list
    # --------------------------------------------------------------  
    def populate_error_codes(self, values: list)-> dict:
        """
        Populate a dictionary with error codes and names.
        """
        logger.info("populate_error_codes working ....")
        error_dict = {}
        col_code = self.cell_letter_to_number(self.find_header_column("Fault_Code"))
        col_name = self.cell_letter_to_number(self.find_header_column("Fault_Name"))
        for r in values:
            fault_code = self.ws.cell(row=r, column=col_code).value
            fault_name = self.ws.cell(row=r, column=col_name).value                
            if fault_code not in error_dict:
                error_dict[fault_code] = {"Name": [], "Row": []}

            error_dict[fault_code]["Name"].append(fault_name)
            error_dict[fault_code]["Row"].append(r)
        logger.info("populate_error_codes OK")
        return error_dict
    # --------------------------------------------------------------
    # Append a new column at the end
    # --------------------------------------------------------------
    def append_column(self, header: str, default_value=None):
        """
        Appends a new column at the far right of the sheet.
        """
        logger.info("append_column INPUT: %s", header)
        col = self.ws.max_column + 1

        self.insert_column_by_num(col, header, default_value)
        logger.info("append_column OK")


    # -------------------------------------------------------------
    # Innsert column by number
    # ------------------------------------------------------------
    def insert_column_by_num(self, col, header, default_value=None):
        """
        Insert a new column at the given position (1-indexed).
        Shifts existing columns to the right.
        """
        logger.info("insert_column_by_num INPUT: %s", header)
        if not isinstance(col,list):
            col = [col]
        if not isinstance(header,list):
            header = [header]
        for col_ex_name, new_col in zip(col,header):
            if col_ex_name is None:
                raise ValueError(f"Header '{col_ex_name}' not found")
            self.ws.insert_cols(col_ex_name)

            # Write header
            cell = self.ws.cell(row=self.start_row, column=col_ex_name, value=new_col)
            cell.font = Font(bold=True)
            
            thin_border = Border(
                left=Side(style="thin", color="000000"),
                right=Side(style="thin", color="000000"),
                top=Side(style="thin", color="000000"),
                bottom=Side(style="thin", color="000000")
            )
            cell.border = thin_border

            # Write default values
            for r in range(self.start_row + 1, self.ws.max_row + 1):
                self.ws.cell(row=r, column=col_ex_name, value=default_value)
        logger.info("insert_column_by_num OK")

    # --------------------------------------------------------------
    # Apply conditional formatting to a column range
    # --------------------------------------------------------------
    def apply_conditional_formatting(self, col_letter: str, operator: str, formula: str,
                                    color: str = "FF9999"):
        """
        Add conditional formatting to a column.
        Example:
            operator = 'greaterThan'
            formula = '100'
            col_letter = 'D'
        """
        logger.info("apply_conditional_formatting working ...")
        fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        rule = CellIsRule(
            operator=operator,
            formula=[formula],
            stopIfTrue=True,
            fill=fill
        )

        range_ref = f"{col_letter}4:{col_letter}{self.ws.max_row}"
        self.ws.conditional_formatting.add(range_ref, rule)
        logger.info("apply_conditional_formatting OK")

    # --------------------------------------------------------------
    # Apply Equal to a column range
    # --------------------------------------------------------------
    
    def find_and_highlight(self, col_letter: str, search_value, color: str):
        """
        Search and highlight cells in a column that match the search value(s).
        
        Parameters:
            col_letter (str): Excel column letter, e.g. 'D'
            search_value: value(s) to search for - can be:
                - single value (string or number)
                - list/tuple of values to match against
            color (str): hex color code (obligatorio, formato AARRGGBB)
        
        Returns:
            List of cell addresses (e.g. ["D5", "D20", ...])
        """
        logger.info("find_and_highlight INPUT: %s", search_value)
        if color is None:
            raise ValueError("find_and_highlight requiere un color desde el JSON")
        
        fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        matches = []
        
        # Normalize search_value to a list of values and flatten nested iterables
        if isinstance(search_value, (list, tuple)):
            # shallow copy
            search_values = list(search_value)
        else:
            search_values = [search_value]

        # flatten any nested lists/tuples to avoid stringification issues
        flattened = []
        for sv in search_values:
            if isinstance(sv, (list, tuple)):
                flattened.extend(sv)
            else:
                flattened.append(sv)
        search_values = flattened
        
        # Loop through all data rows (row 4 onward)
        for row in range(4, self.ws.max_row + 1):
            cell = self.ws[f"{col_letter}{row}"]
            cell_value = cell.value
            
            if cell_value is None:
                continue
            
            matched = False
            
            # Exact match: handle strings and numbers
            for search_text in search_values:
                if isinstance(search_text, str):
                    # Normalizar ambos lados para comparación consistente
                    search_normalized = search_text.strip().upper()
                    cell_normalized = str(cell_value).strip().upper()
                    if cell_normalized == search_normalized:
                        matched = True
                        break
                else:
                    # Numeric comparison
                    try:
                        if float(cell_value) == float(search_text):
                            matched = True
                            break
                    except:
                        pass
            
            if matched:
                cell.fill = fill
                matches.append(cell.coordinate)

        logger.info("find_and_highlight OUTPUT: %s", matches)        
        return matches

    # --------------------------------------------------------------
    # Highlight event rows based on sequential value changes
    # --------------------------------------------------------------
    def highlight_event(self, cols, search_values, color: str = "00FF00"):
        """
        Scan columns for specific values and highlight rows based on value transitions.

        Parameters:
            cols: single column specifier (int, letter, header) or iterable of
                such specifiers. These columns are where the engine will look
                for the search values.
            search_values: a value or list of values to look for. The function
                processes them in order; for each value it identifies rows where
                that value appears. When the next row contains a DIFFERENT value,
                the function highlights:
                    - the current row (last occurrence of the current value)
                    - the next row (first occurrence of the new value)
            color: hex background colour used for highlighting (no '#' char).

        Returns:
            List[int]: the row numbers that were coloured.
        """
        logger.info("highlight_event INPUT: %s", search_values)
        if color is None:
            raise ValueError("highlight_event requires a color from the JSON")

        # helper to resolve a single column spec to a letter
        def resolve_col(item):
            if isinstance(item, int):
                from openpyxl.utils import get_column_letter
                return get_column_letter(item)
            if isinstance(item, str):
                # try as header name
                col_letter = self.find_header_column(item)
                if col_letter:
                    return col_letter
                # letter form
                if item.isalpha():
                    return item
                # numeric string
                if item.isdigit():
                    from openpyxl.utils import get_column_letter
                    return get_column_letter(int(item))
            raise ValueError(f"Cannot resolve column specifier: {item}")

        # build list of column letters to process
        if isinstance(cols, (list, tuple)):
            col_letters = [resolve_col(c) for c in cols]
        else:
            col_letters = [resolve_col(cols)]

        # prepare search value sequence (flatten nested iterables)
        if isinstance(search_values, (list, tuple)):
            seq = list(search_values)
        else:
            seq = [search_values]
        flat = []
        for v in seq:
            if isinstance(v, (list, tuple)):
                flat.extend(v)
            else:
                flat.append(v)
        # Normalize to strings for comparison, but keep originals too
        normalized_seq = [str(x).strip().upper() for x in flat]

        highlighted_rows = []
        maxrow = self.ws.max_row
        for col_letter in col_letters:
            for target_norm in normalized_seq:
                # print("data: ", target_norm)
                for row in range(4, maxrow):  # Go up to maxrow-1 to check next row
                    cell = self.ws[f"{col_letter}{row}"]
                    val = cell.value
                    curr = str(val).strip().upper() if val is not None else None

                    # If current row matches the target value
                    if curr == target_norm:
                        # Check the next row (+1 position)
                        nxt = self.ws[f"{col_letter}{row+1}"].value
                        nxt_norm = str(nxt).strip().upper() if nxt is not None else None

                        # If next row is DIFFERENT from current row
                        if nxt_norm != curr:
                            # Highlight current row
                            if row not in highlighted_rows:
                                self.highlight_row(row, color)
                                highlighted_rows.append(row)
                            # Highlight next row (+1 position)
                            if (row + 1) not in highlighted_rows:
                                self.highlight_row(row + 1, color)
                                highlighted_rows.append(row + 1)
        
        logger.info("highlight_event OUTPUT: %s", sorted(highlighted_rows))
        return sorted(highlighted_rows)

    # --------------------------------------------------------------
    # Highlight values IN an allowed list (opposite of highlight_not_in_list)
    # --------------------------------------------------------------
    def find_and_highlight_in_list(self, allowed_values, col, color: str):
        """
        Scan a single column and highlight cells cuyo valor SÍ está en allowed_values.
        (opuesto a highlight_not_in_list)

        Parameters:
            allowed_values (iterable): list/iterable of allowed values (numbers or strings)
            col: column identifier (int, column letter like 'A', or header name)
            color (str): hex color code para highlighting (format AARRGGBB)

        Returns:
            List[int]: row numbers where the column value IS in `allowed_values`.
        """
        logger.info("find_and_highlight_in_list INPUT: %s", allowed_values)
        if color is None:
            raise ValueError("find_and_highlight_in_list requiere un color desde el JSON")
        
        # Normalizar lista de valores permitidos
        if not isinstance(allowed_values, (list, tuple, set)):
            allowed_values = [allowed_values]
        
        # Resolve column to letter
        def resolve_col(item):
            if isinstance(item, int):
                from openpyxl.utils import get_column_letter
                return get_column_letter(item)
            if isinstance(item, str):
                # header name
                col_letter = self.find_header_column(item)
                if col_letter:
                    return col_letter
                # column letter
                if item.isalpha():
                    return item
                # numeric string
                if item.isdigit():
                    from openpyxl.utils import get_column_letter
                    return get_column_letter(int(item))
            raise ValueError(f"Cannot resolve column specifier: {item}")

        col_letter = resolve_col(col) if not isinstance(col, (list, tuple)) else resolve_col(col[0])
        
        fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        matches = []
        
        # Loop through all data rows (row 4 onward)
        for row in range(4, self.ws.max_row + 1):
            cell = self.ws[f"{col_letter}{row}"]
            cell_value = cell.value
            
            if cell_value is None:
                continue
            
            matched = False
            
            # Check if cell value is in the allowed list
            for allowed_val in allowed_values:
                if isinstance(allowed_val, str):
                    # Normalizar ambos lados para comparación consistente
                    allowed_normalized = allowed_val.strip().upper()
                    cell_normalized = str(cell_value).strip().upper()
                    if cell_normalized == allowed_normalized:
                        matched = True
                        break
                else:
                    # Numeric comparison
                    try:
                        if float(cell_value) == float(allowed_val):
                            matched = True
                            break
                    except:
                        pass
            
            if matched:  # Solo resaltar si SÍ está en la lista permitida
                cell.fill = fill
                matches.append(row)
        logger.info("find_and_highlight_in_list OUTPUT: %s", matches)
        return matches

    # --------------------------------------------------------------
    # Highlight values not in an allowed list
    # --------------------------------------------------------------
    def highlight_not_in_list(self, allowed_values, col, color: str):
        """
        Scan a single column and highlight cells cuyo valor NO está en allowed_values.

        Parameters:
            allowed_values (iterable): list/iterable of allowed values (numbers or strings)
            col: column identifier (int, column letter like 'A', or header name)
            color (str): hex color code para highlighting (format AARRGGBB)

        Returns:
            List[int]: row numbers where the column value is not in `allowed_values`.
        """
        logger.info("highlight_not_in_list INPUT: %s", allowed_values)
        if color is None:
            raise ValueError("highlight_not_in_list requiere un color desde el JSON")
        
        # Normalizar lista de valores permitidos
        if not isinstance(allowed_values, (list, tuple, set)):
            allowed_values = [allowed_values]
        
        # Resolve column to index (reuse logic similar to highlight_column)
        def resolve_single(item):
            if isinstance(item, int):
                return item
            if isinstance(item, str):
                # header name
                col_letter = self.find_header_column(item)
                if col_letter:
                    return self.cell_letter_to_number(col_letter)
                # column letter
                if item.isalpha():
                    return self.cell_letter_to_number(item)
                # numeric string
                if item.isdigit():
                    return int(item)
            raise ValueError(f"Cannot resolve column specifier: {item}")

        col_index = resolve_single(col) if not isinstance(col, (list, tuple)) else resolve_single(col[0])

        # Prepare allowed value sets (numeric and string) for robust comparison
        # Normalizar strings a MAYÚSCULAS para comparación consistente
        numeric_allowed = set()
        string_allowed = set()
        for v in allowed_values:
            try:
                numeric_allowed.add(float(v))
            except Exception:
                # Normalizar string a MAYÚSCULAS
                normalized = str(v).strip().upper()
                string_allowed.add(normalized)

        # Ensure color format is AARRGGBB (8 chars = AARRGGBB)
        # If only 6 chars (RRGGBB), prepend FFAA (full opacity)
        if len(color) == 6:
            color = "FF" + color
        
        fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        mismatched_rows = []

        # Check data rows starting from row 4 (consistent with other helpers)
        for row in range(4, self.ws.max_row + 1):
            cell = self.ws.cell(row=row, column=col_index)
            val = cell.value
            if val is None:
                continue

            matched = False
            
            # Primero intentar comparación de string (normalizada)
            cell_val_normalized = str(val).strip().upper()
            if cell_val_normalized in string_allowed:
                matched = True
            
            # Si no coincide, intentar comparación numérica
            if not matched:
                try:
                    val_float = float(val)
                    if val_float in numeric_allowed:
                        matched = True
                except Exception:
                    pass

            if not matched:
                cell.fill = fill
                mismatched_rows.append(row)
        logger.info("highlight_not_in_list OUTPUT: %s", mismatched_rows)
        return mismatched_rows

    # --------------------------------------------------------------
    # Autosize all columns
    # --------------------------------------------------------------
    def autosize_columns(self):
        """
        Adjusts all column widths based on max text length.
        """
        logger.info("autosize_columns working...")
        for col in self.ws.columns:
            max_length = 0
            column = col[0].column_letter

            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass

            adjusted = max_length + 2
            self.ws.column_dimensions[column].width = adjusted
        logger.info("autosize_columns OK")

    # --------------------------------------------------------------
    # Save workbook
    # --------------------------------------------------------------
    def save(self, output_path: str = None):
        """
        Saves the workbook. If output_path is None, overwrites original file.
        """
        logger.info("Saving.... %s",output_path)
        if output_path:
            self.wb.save(output_path)
        else:
            self.wb.save(self.file_path)
        logger.info("Saving DONE")

    def find_header_column(self, header_name: str) -> str:
        """
        Find the column letter for a given header name in row 3.
        Normaliza el nombre buscado y los nombres en la fila 3 para comparación consistente.
        Returns the column letter (e.g. 'D') or None if not found.
        """
        logger.info("find_header_column %s",header_name)
        # Normalizar el nombre buscado
        def normalize_name(name):
            """Normalizar nombre: MAYÚSCULAS, quitar espacios, guiones, underscores y caracteres no alfanuméricos"""
            name = str(name)
            name = re.sub(r'\(.*?\)', '', name)
            # Convertir a string, quitar caracteres no alfanuméricos, convertir a mayúsculas
            normalized = re.sub(r'[^a-zA-Z0-9]', '', name).upper()
            return normalized
        
        target_normalized = normalize_name(header_name)
        
        for col in range(1, self.ws.max_column + 1):
            cell_value = self.ws.cell(row=self.start_row, column=col).value
            if cell_value:
                cell_normalized = normalize_name(str(cell_value))
                if cell_normalized == target_normalized:
                    logger.info("find_header_column OUTPUT: %s", self.ws.cell(row=self.start_row, column=col).column_letter)
                    return self.ws.cell(row=self.start_row, column=col).column_letter
        logger.info("find_header_column OUTPUT: empty")
        return None
    
    def cell_letter_to_number(self, letter: str) -> int:
        """
        Convert Excel column letter to number (e.g. 'A' -> 1, 'D' -> 4).
        """
        logger.info("cell_letter_to_number INPUT: %s", letter)
        num = 0
        if letter is None:
            return None
        else:
            for c in letter:
                if c.isalpha():
                    num = num * 26 + (ord(c.upper()) - ord('A')) + 1

        logger.info("cell_letter_to_number OUTPUT: %s", num)
        return num          
    def validate_version(self, headers: list) -> dict:
        """
        For each header in 'headers', search that column in the Excel sheet self.ws,
        extract the first numeric decimal value, convert it to hex, and format as Vxx_Tyy.

        Returns:
            A dictionary mapping each header to its formatted version string (or None if not found).
        """
        logger.info("validate_version INPUT: %s", headers)
        ws = self.ws
        results = {}

        # Convert headers of Excel sheet (first row) into a map: header -> column index
        excel_headers = {}
        for col_idx, cell in enumerate(ws[self.start_row], start=1):
            header_name = str(cell.value).strip() if cell.value else ""
            excel_headers[header_name.upper()] = col_idx


        for h in headers:
            col_let = self.find_header_column(h)
            col = self.cell_letter_to_number(col_let)
            if col is None:
                logger.warning("validate_version: header not found for %s", h)
                results[h] = None
                continue

            # ---- Search for first valid numeric decimal value in this col ----
            found_number = None
            for row in range(self.start_row + 1, ws.max_row + 1):  # data rows
                cell_value = ws.cell(row=row, column=col).value                 
                text_log = f"Checking cell {row},{col} with value: {cell_value}"
                logger.info("validate_version runing: %s", text_log)
                if cell_value is None or int(cell_value) == 0:
                    continue

                # Try to parse as int (numeric)
                try:
                    number = int(cell_value)
                    found_number = number
                    break
                except Exception:
                    continue
            text_log = f"Header '{h}': found number = {found_number}"
            logger.info("validate_version runing: %s", text_log)
            if found_number is None:
                results[h] = None
                continue

            # ---- Convert decimal to HEX and format ----
            if h == "PB DSP FW2":
                formatted = f"{found_number}"
            else: 
                hex_str = f"{found_number:04X}"  # always 4 digits
                high = hex_str[:2]
                low = hex_str[2:]
                formatted = f"V{high}_T{low}"
            results[h] = formatted
            self.insert_column(h,h,formatted)  
        logger.info("validate_version INPUT: %s", results)            
        return results
    
    
    def _collect_numeric_column(self, col: int) -> Tuple[list, list]:
        """
        Collect numeric values from a given column starting at start_row.
        Returns (x, y):
        - x: simple index (1..n) for plotting
        - y: numeric values
        Non-numeric cells are skipped.
        """
        logger.info("_collect_numeric_column INPUT: %s", col)  
        x, y = [], []
        idx = 1
        for r in range(self.start_row +1 , self.ws.max_row + 1):
            cell_val = self.ws.cell(row=r, column=col).value
            if cell_val is None:
                continue
            # try numeric coercion
            try:
                num = float(cell_val)
            except (TypeError, ValueError):
                # not numeric -> skip
                continue
            x.append(idx)
            y.append(num)
            idx += 1
        logger.info("_collect_numeric_column OK")
        return x, y

    
    def plot_headers_from_excel(self, headers: List[str],
                                output_name: Optional[str] = None) -> str:
        """
        Read an .xlsx file with openpyxl, find the given list of headers, and
        plot each header's numeric column in its own subplot. Save a single PNG
        image next to the .xlsx file and return the image path.

        Parameters
        ----------
        xlsx_path : str
            Path to the .xlsx file.
        headers : List[str]
            List of header labels to search in the header_row.
        sheet_name : str | None
            Sheet to read. If None, active sheet is used.
        header_row : int
            Row number where headers are located (1-based). Default is 1.
        output_name : str | None
            File name (without path) for the PNG. If None, auto-generated.

        Returns
        -------
        str
            Absolute path to the saved PNG.
        """
        logger.info("plot_headers_from_excel INPUT: %s", headers)
        # Prepare figure: one subplot per header (stacked vertically)
        n = len(headers)

        fig_height = max(2.5 * n, 3.5)  # heuristic for readable height
        fig, axes = plt.subplots(nrows=n, ncols=1, figsize=(8, fig_height), dpi=120)
        if n == 1:
            axes = [axes]  # normalize to list for consistent handling

        plotted_any = False
    
        for i, header in enumerate(headers):
            ax = axes[i]
            col_idx = self.cell_letter_to_number(self.find_header_column(header))
            if col_idx is None:
                ax.set_title(f"{header} (header not found)")
                ax.set_axis_off()
                continue

            x, y = self._collect_numeric_column(col=col_idx)
            if not y:
                ax.set_title(f"{header} (no numeric data)")
                ax.set_axis_off()
                continue

            ax.plot(x, y, marker="o", linestyle="-", linewidth=1.5)
            ax.set_title(header)
            ax.set_xlabel("Index")
            ax.set_ylabel("Value")
            ax.grid(True, linestyle="--", alpha=0.3)
            plotted_any = True

        plt.tight_layout()

        # Output path: same folder as xlsx
        if output_name is None:
            # e.g., MyFile_headers_plot.png
            info_path = Path(self.file_path)
            base = info_path.stem
            suffix = "_".join(h.replace(" ", "_") for h in headers[:3])  # keep name manageable
            if len(headers) > 3:
                suffix += f"_plus{len(headers)-3}"
            output_name = f"{base}_{suffix}_plot.png"

        out_path = info_path.parent / output_name
        fig.savefig(out_path, bbox_inches="tight")
        plt.close(fig)

        if not plotted_any:
            # If none of the headers produced a plot, warn the caller
            # (we still saved an image with "not found/no data" notes).
            # You can choose to raise instead.
            pass
        logger.info("plot_headers_from_excel INPUT: %s", str(out_path.resolve()))
        return str(out_path.resolve())
    
    def insert_temp_colmun(self, header: str):
        logger.info("insert_temp_colmun INPUT: %s", header)
        data = self.temp_convertion(header)
        if data is not None:
            new_header = header + "_T°C"
            self.insert_column(header, new_header)
            self.populate_column(new_header, data)
        logger.info("insert_temp_colmun OK")
        return
    def insert_current_colmun(self, header: str):
        logger.info("insert_current_colmun INPUT: %s", header)
        data = self.scale_current(header)
        if data is not None:
            new_header = header + "_[A]"
            self.insert_column(header, new_header)
            self.populate_column(new_header, data)
        logger.info("insert_current_colmun OK")
        return
    
    def temp_convertion(self, header: str) ->list:
        logger.info("temp_convertion INPUT: %s", header)
        position = self.cell_letter_to_number(self.find_header_column(header))
        if position is None:
            return None
        raw_data = [self.ws.cell(row = idx, column = position).value for idx in range(self.start_row+1, self.ws.max_row+1)]
        
        normalized = []
        for x in raw_data:
            if x is None:
                normalized.append(None)
                continue                
            if isinstance(x, str):
                x = x.replace(",", ".")
                try:
                    x = float(x)
                except:
                    normalized.append(None)
                    continue

            normalized.append(float(x))        

        if self.initial_data["inverter_model"] == "Ariston":
            result_data = [(x /10) - 55 for x in normalized]            
        else:
            result_data = [x / 256  for x in normalized]            
        logger.info("temp_convertion OK")
        return result_data
    
    def scale_current(self, header:str)->list:
        logger.info("scale current INPUT: %s", header)
        position = self.cell_letter_to_number(self.find_header_column(header))
        if position is None:
            return None
        raw_data = [self.ws.cell(row = idx, column = position).value for idx in range(self.start_row+1, self.ws.max_row+1)]
        
        normalized = []
        for x in raw_data:
            if x is None:
                normalized.append(None)
                continue                
            if isinstance(x, str):
                x = x.replace(",", ".")
                try:
                    x = float(x)
                except:
                    normalized.append(None)
                    continue

            normalized.append(float(x))        

        data = [(x /10) for x in normalized]                   
        logger.info("Scale_current OK")

        return data
    
    def highlight_over_voltage(self, headers: list, threshole:int, color: str):
        logger.info("highlight_over_voltage INPUT: %s", threshole)
        for header in headers:
            voltage_value = []
            position = self.cell_letter_to_number(self.find_header_column(header))
            if position is None:
                continue
            data = [self.ws.cell(row = idx, col = position).value for idx in range(self.start_row+1, self.ws.max_row+1)]
            voltage_value[header] = [x for x in data if x >= threshole]
            if voltage_value == []:
                self.find_and_highlight_in_list(voltage_value, header, color)       
        logger.info("highlight_over_voltage OK")
        return
    
    def highlight_under_voltage(self, headers: list, threshole: int, color: str):
        logger.info("highlight_under_voltage INPUT: %s", threshole)
        for header in headers:
            voltage_value = []
            position = self.cell_letter_to_number(self.find_header_column(header))
            if position is None:
                continue
            data = [self.ws.cell(row = idx, col = position).value for idx in range(self.start_row+1, self.ws.max_row+1)]
            voltage_value[header] = [x for x in data if x <= threshole]
            if voltage_value == []:
                self.find_and_highlight_in_list(voltage_value, header, color)       
        logger.info("highlight_under_voltage OK")
        return


    def highlight_der_temp(self, column: str, thresholds: list):
        RED_FILL = PatternFill(start_color="FFFFC7CE", end_color="FFFFC7CE", fill_type="solid")
        ORANGE_FILL = PatternFill(start_color="FFFFC000", end_color="FFFFC000", fill_type="solid")
        YELLOW_FILL = PatternFill(start_color="FFFFEB9C",end_color="FFFFEB9C",fill_type="solid")

        logger.info("highlight_der_temp INPUT: %s", thresholds)

        if not thresholds or len(thresholds) != 3:
            logger.error("Invalid thresholds provided")
            return

        low_limit, medium_limit, high_limit = thresholds
        header_name = column

        col_letter = self.find_header_column(header_name)
        if col_letter is None:
            logger.warning("Header not found: %s", header_name)
            return

        col_idx = self.cell_letter_to_number(col_letter)

        for row in range(self.start_row + 1, self.ws.max_row + 1):
            cell = self.ws.cell(row=row, column=col_idx)
            val = cell.value
            if val is None:
                continue    
            if isinstance(val, str):
                val = val.strip()
                if val == "":
                    continue
            try:
                value = float(val)
            except (TypeError, ValueError):
                continue

            if value > high_limit:
                cell.fill = RED_FILL
            elif value > medium_limit:
                cell.fill = ORANGE_FILL
            elif value > low_limit:
                cell.fill = YELLOW_FILL

        logger.info("highlight_der_temp OK")

