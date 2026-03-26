# Agents.md

Last updated: 2026-03-05
Project root scanned: `Report_generator`

## Purpose
This document tracks the current architecture of the Report Generator project and must be updated whenever modules, data flow, or interfaces change.

## High-Level Architecture
- UI layer: `UI_report.py` (PySide6 desktop app, entrypoint).
- Configuration ingestion:
  - `Load_configuration_test.py` loads test definitions from XLSX sheet (inverter-specific).
  - `TDM_config_load.py` loads DGTO configuration from CSV.
  - `Read_TDM_error.py` loads fault dictionary from TDM XLSX (with in-memory cache).
- Data ingestion:
  - `Read_TDM_report.py` reads custom TDM report CSV and can export to Excel.
- Analysis/processing engine:
  - `step_engine.py` executes JSON-like step actions.
  - `json_motor.py` contains default step definitions and normalization helpers.
- Excel transformation/styling:
  - `ExcelStyler.py` applies highlighting, column operations, validations, and fault enrichment.
- Resources:
  - `resurces.qrc`, `resurces_rc.py`, icons in `iconos/`.

## Runtime Flow (Current)
1. `UI_report.main()` starts `StartWindow`.
2. `StartWindow` collects user inputs and validates required files/fields.
3. It loads:
   - report config XLSX -> `load_test_definition_xlsx(...)`
   - TDM fault XLSX -> `load_tdm_once(...)`
   - TDM config CSV -> `load_tdm_config(...)`
4. `AnalysisWindow` is opened with the three dictionaries.
5. Table is populated from test config.
6. Per-row action button runs DGTO validation:
   - reads selected TDM log CSV via `read_custom_csv(...)`
   - compares CSV headers vs DGTO names from config
   - writes result to `TEST SUMMARY` cell.

Notes:
- `StepEngine` + `ExcelStyler` are implemented and imported, but the current UI action path performs DGTO validation only.
- `Read_TDM_error` caches fault dictionaries by file path to avoid repeated parsing.

## Module Responsibilities
- `UI_report.py`
  - GUI workflow, file selection, validation, table rendering, per-test actions.
- `Load_configuration_test.py`
  - Converts test definition spreadsheet into `{test_number: attributes}`.
- `TDM_config_load.py`
  - Robust CSV parsing with encoding/separator fallback and normalized 4-column dataset.
- `Read_TDM_report.py`
  - Parses custom report CSV format (metadata rows + header row + data rows).
- `Read_TDM_error.py`
  - Extracts `FAULT CODE -> {FAULT NAME, ERROR LIST NAME FOR MANUAL}` map.
- `step_engine.py`
  - Executes actions (`highlight_column`, `find_and_highlight`, `highlight_not_in_list`, `validate_version`, etc.) against `ExcelStyler`.
- `ExcelStyler.py`
  - Low-level workbook editing/highlighting and helper operations used by `StepEngine`.
- `json_motor.py`
  - Default step catalog (`DEFAULT_TEST_STEPS_PACMAN5`) + header/step normalization helpers.

## Data Contracts (Key)
- Test config dict:
  - `{int test_number: {str ATTRIBUTE: Any value, ...}}`
- TDM fault dict:
  - `{int fault_code: {"FAULT NAME": str, "ERROR LIST NAME FOR MANUAL": str}}`
- TDM config dict:
  - `{basename: {"DGTO": [...], "reg_DGTO": [...], "name_DGTO": [...], "info_DGTO": [...]}}`

## Directory Snapshot
- Root Python modules:
  - `UI_report.py`, `ExcelStyler.py`, `step_engine.py`, `json_motor.py`
  - `Read_TDM_report.py`, `Read_TDM_error.py`, `TDM_config_load.py`, `Load_configuration_test.py`
- Tests: `Test_code/`
- Data/support: `data_base/`, `Test_files/`, `iconos/`

## Test Coverage (Files)
- `Test_code/test_motor_json.py`
- `Test_code/Test_read_tdm_error.py`
- `Test_code/Test_read_tdm_report.py`
- `Test_code/test_step_engine.py`
- `Test_code/test_step_engine_all_actions.py`
- `Test_code/test_TDM_config_load.py`

## Update Policy (Keep This File Updated)
Update this file in the same commit whenever one of these changes:
- new/removed Python module
- changed function signatures between modules
- changed runtime flow in `UI_report.py`
- changed dict schema/keys in loaders or engine
- new action types in `StepEngine`
- moved/renamed test files

Minimum update checklist:
1. Refresh `Last updated` date.
2. Update "High-Level Architecture" and "Runtime Flow".
3. Update "Data Contracts" if any key names/types changed.
4. Update "Directory Snapshot" and "Test Coverage".

Quick scan commands:
- `rg --files -g "*.py"`
- `rg -n "class |def |if __name__ == '__main__'" UI_report.py step_engine.py ExcelStyler.py`
- `Get-ChildItem Test_code -File`
