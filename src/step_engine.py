import logging

logger = logging.getLogger(__name__)


class StepEngine:
    def __init__(self, styler, test_config, test_num):
        """
        styler: instancia de ExcelStyler
        test_config: diccionario con datos del test desde el JSON
        debe contener la llave 'steps'
        tdm_dict: (opcional) diccionario creado por Read_TDM_error.load_tdm_once()
        formato: {fault_code: {"FAULT NAME": str, "ERROR LIST NAME FOR MANUAL": str}, ...}
        """
        self.styler = styler
        self.test_config = test_config
        self.test_num = test_num
        self.tdm_dict = styler.tdm_dict if hasattr(styler, 'tdm_dict') else {}

    def _resolve_columns(self, col_spec):
        """
        Convierte un especificador de columna en algo que puede manejar
        el styler.

        - Si es una cadena y existe en la configuración inicial como lista,
            se devuelve esa lista (la búsqueda ignora mayúsculas/minúsculas).
        - En cualquier otro caso se devuelve el valor tal cual.
        """
        if isinstance(col_spec, str):
            # buscar de forma case‑insensitive entre las llaves
            norm = col_spec.strip().upper()
            for key, cfg in self.test_config["tests"][str(self.test_num)].items():
                if isinstance(key, str) and key.strip().upper() == norm:
                    return cfg
        return col_spec

    def _resolve_value_list(self, value_spec):
        """
        A partir de ``value_spec`` devuelve una lista de valores a usar en
        highlight/not‑in‑list o find‑and‑highlight.

        - "Faults Expected" → claves del diccionario de tdm_dict.
        - nombre de clave de ``test_config`` cuyo valor sea una lista.
        - nombre de campo interno de las entradas de ``tdm_dict``.
        - lista directa de valores → se retorna tal cual
        - cualquier otro valor no nulo se devuelve en lista de un elemento.
        """
        # Si ya es una lista, procesar cada elemento
        if isinstance(value_spec, (list, tuple)):
            result = []
            for item in value_spec:
                # Resolver recursivamente cada elemento
                resolved = self._resolve_value_list(item)
                result.extend(resolved)    
            return result
        # Caso especial: "Faults Expected"
        if isinstance(value_spec, str):
            norm_spec = value_spec.strip().upper()
            # 1. Buscar llave en configuración JSON primero (insensible a mayúsculas)
            for key, cfg_val in self.test_config["tests"][str(self.test_num)].items():
                if isinstance(key, str) and key.strip().upper() == norm_spec:
                    if isinstance(cfg_val, (list, tuple)):
                        return list(cfg_val)
                    if cfg_val is not None:
                        return [cfg_val]
                

            # # 2. Caso especial: "Faults Expected" si no existe en la config
            # if norm_spec == "FAULTS EXPECTED":
            #     return list(self.tdm_dict.keys()) if self.tdm_dict else []

            # 3. clave interna de tdm_dict: buscar entre los nombres de campo
            if self.tdm_dict:
                out = []
                for entry in self.tdm_dict.values():
                    for fld, val in entry.items():
                        if isinstance(fld, str) and fld.strip().upper() == norm_spec and val is not None:
                            out.append(val)
                if out:
                    # eliminar duplicados manteniendo orden
                    seen = set()
                    return [x for x in out if not (x in seen or seen.add(x))]

        # cualquier otro valor
        if value_spec is not None:
            return [value_spec]

        return []

    def execute(self)-> dict:
        """
        Execute JSON steps.
        """
        results_dict = {}
        steps = self.test_config["tests"][str(self.test_num)].get("steps", [])

        for step in steps:
            action = step["action"]
            text_log = f"action doing:, {action}"
            logger.info("Json step: %s", text_log)           

            if "color" not in step:
                color = "FFFF00"  # default amarillo
                # raise ValueError(f"Cada paso debe incluir 'color' – acción: {action}")
            else:
                color = step["color"]

            # -----------------------------
            # 0. Validate fault codes against TDM dictionary
            # -----------------------------
            if action == "validate_fault_codes":
                allowed_codes = list(self.tdm_dict.keys()) if self.tdm_dict else []
                col = self._resolve_columns(step.get("column", "FAULT_CODE"))
                mismatches = self.styler.highlight_not_in_list(
                    allowed_codes, col=col, color=color
                )

            # -----------------------------
            # 1. Highlight entire column
            # -----------------------------
            elif action == "highlight_column":
                # Column can be a string (header name) or list of header names
                col = self._resolve_columns(step["column"])
                self.styler.highlight_column(col, color)

            # -----------------------------
            # 2. Highlight cells with value not in allowed list
            # If "value" is "Faults Expected", use TDM fault codes
            # Otherwise, treat as single value
            # -----------------------------
            elif action == "highlight_not_in_list":
                col = self._resolve_columns(step["column"])
                value_spec = step.get("value")
                
                # Determine allowed values
                allowed_values = self._resolve_value_list(value_spec)
                if not allowed_values:
                    logger.warning("validation error: %s", value_spec) 
                    continue
                
                mismatches = self.styler.highlight_not_in_list(allowed_values, col=col, color=color)
                if mismatches:
                    results_dict["Faults_Not_expected"] = self.styler.populate_error_codes(mismatches)

            # -----------------------------
            # 3. Highlight specific cells (exact value match)
            # -----------------------------
            elif action == "find_and_highlight":
                col = self._resolve_columns(step["column"])
                
                # col puede ser string o lista; extraer primer elemento si es lista
                col_str = col[0] if isinstance(col, (list, tuple)) else col
                col_letter = self._get_column_letter(col_str)
                
                value_spec = step.get("value") or step.get("text")
                
                # Resolver valores usando la nueva helper; esto también maneja
                # "Faults Expected" consultando primero la configuración.
                resolved = self._resolve_value_list(value_spec)
                if not resolved:
                    logger.warning("validation error: %s", value_spec) 
                    continue

                # Si la lista resultante tiene más de un elemento, usar
                # el método de conjunto para mayor eficiencia.
                col_name = col_str
                if len(resolved) > 1:
                    matches = self.styler.find_and_highlight_in_list(resolved, col=col_name, color=color)

                else:
                    target = resolved[0]
                    matches = self.styler.find_and_highlight(col_letter, target, color)
                logger.info("values highlight: %s", matches) 

            # -----------------------------
            # 4. Highlight event pattern (custom ExcelStyler helper)
            # -----------------------------
            elif action == "highlight_event":
                # column(s) to inspect and values to look for
                col = self._resolve_columns(step["column"])
                value_spec = step.get("value") or step.get("values")
                event_values = self._resolve_value_list(value_spec)
                if not event_values:
                    logger.warning("validation error: %s", value_spec)
                    continue
                rows = self.styler.highlight_event(col, event_values, color)
                logger.info("Row highlight: %s", rows)

            # -----------------------------
            # 5. Insert column
            # -----------------------------
            elif action == "insert_column":
                col = step["column"]
                value = step["value"]
                self.styler.insert_column(col, value, None)

            # -----------------------------
            # 6. Append column
            # -----------------------------
            elif action == "append_column":
                header = step["column"]
                default = step.get("default", None)
                self.styler.append_column(header, default)

            # -----------------------------
            # 7. Fill fault names based on fault codes using TDM dictionary
            #     This is a custom action that populates a new column "FAULT NAME"
            # -----------------------------
            elif action == "populate_column_fault":
                header = step["column"]
                code_names = self.styler.populate_fault_names()
                self.styler.populate_column(header, code_names)

            # -----------------------------
            # 8. validate version
            # -----------------------------
            elif action == "validate_version":
                columns = step["column"]
                results_dict = self.styler.validate_version(columns)
            # -----------------------------
            # 9. insert_temperature
            # -----------------------------
            elif action == "insert_temp_colmun":
                column = step["column"]
                self.styler.insert_temp_colmun(column)
            # -----------------------------
            # 10. insert_plot analysis
            # -----------------------------
            elif action == "plot_headers_from_excel":
                column = step["column"]
                results_dict["plot_path"] = self.styler.plot_headers_from_excel(column)
            # -----------------------------
            # 11. highlight_over_voltage
            # -----------------------------
            elif action == "highlight_over_voltage":
                column = step["column"]
                if "AC input over voltage protection limit Vac" in self.test_config["tests"][str(self.test_num)].key():
                    data_col = self._resolve_columns("AC input over voltage protection limit Vac")
                    data = self._resolve_value_list(data_col)
                    self.styler.highlight_over_voltage(column, data, color)
                elif "Max DC limit (CMP on) [V]" in self.test_config["tests"][str(self.test_num)].key():
                    data = self._resolve_value_list(data_col)
                    self.styler.highlight_over_voltage(column, data, color)
            # -----------------------------
            # 12. highlight_under_voltage
            # -----------------------------
            elif action == "highlight_under_voltage":
                column = step["column"]
                if "AC input under voltage protection limit Vac" in self.test_config["tests"][str(self.test_num)].key():
                    data_col = self._resolve_columns("AC input under voltage protection limit Vac")
                    data = self._resolve_value_list(data_col)
                    self.styler.highlight_under_voltage(column, data, color)
            # -----------------------------
            # 13. Fill fault names based on fault codes using LIN dictionary
            #     This is a custom action that populates a new column "Lin_fault_name"
            # -----------------------------
            elif action == "populate_lin_fault":
                header = step["column"]
                code_names = self.styler.populate_lin_fault()
                self.styler.populate_column(header, code_names)   
            # -----------------------------
            # 14. Insert current values correct units to plot
            # -----------------------------     
            elif action == "insert_current_colmun":
                column = step["column"]
                self.styler.insert_current_colmun(column)          
            # -----------------------------
            # 15. Custom error if unsupported action
            # -----------------------------
            else:
                logger.warning("Unsupported action in JSON: %s", action)
                raise ValueError(f"Unsupported action in JSON: {action}")

        return results_dict

    def _resolve_column_single(self, col_spec):
        """
        Resolve a single column specifier (int, letter, or header name) to column index.
        Returns the column index (1-based).
        """
        if isinstance(col_spec, int):
            return col_spec
        if isinstance(col_spec, str):
            # Try header name first
            col_letter = self.styler.find_header_column(col_spec)
            if col_letter:
                return self.styler.cell_letter_to_number(col_letter)
            # Try as column letter (A, B, AA, etc)
            if col_spec.isalpha():
                return self.styler.cell_letter_to_number(col_spec)
            # Try as numeric string
            if col_spec.isdigit():
                return int(col_spec)
        raise ValueError(f"Cannot resolve column: {col_spec}")

    def _get_column_letter(self, col_spec):
        """
        Resolve a single column specifier (int, letter, or header name) to Excel column letter.
        Returns the column letter (e.g., 'D').
        """
        if isinstance(col_spec, str):
            # Try header name first
            col_letter = self.styler.find_header_column(col_spec)
            if col_letter:
                return col_letter
            # If already a column letter (A, B, AA, etc)
            if col_spec.isalpha():
                return col_spec
        # If int or numeric string, convert to letter
        col_index = self._resolve_column_single(col_spec)
        # Convert index to letter using openpyxl utilities
        from openpyxl.utils import get_column_letter
        return get_column_letter(col_index)

    def get_fault_info(self, fault_code):
        """
        Obtiene información de un fault code desde el diccionario TDM.
        
        Parameters:
            fault_code: código de falla (int)
            
        Returns:
            dict con "FAULT NAME" y "ERROR LIST NAME FOR MANUAL", o None si no existe
        """
        return self.tdm_dict.get(int(fault_code))
    
    def get_all_fault_codes(self):
        """
        Obtiene la lista de todos los códigos de falla disponibles.
        
        Returns:
            list de códigos de falla (int)
        """
        return list(self.tdm_dict.keys())
    
