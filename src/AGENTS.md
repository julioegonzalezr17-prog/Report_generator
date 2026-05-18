# AGENTS.md

Last updated: 2026-05-18
Project root scanned: `Report_generator`

## Purpose
This document tracks the current architecture of the Report Generator project and must be updated whenever modules, data flow, or interfaces change.

## High-Level Architecture

### Entry Point
- **`main_UI.py`** - Application launcher with PySide6 QApplication initialization.

### UI Layer (PySide6 Desktop App)
Multi-window interface orchestration:
- **`UI_selection.py`**: `SelectionWindow` - First window, collects test mode selection (Standalone/Integration test, test type selection from inverter/model).
- **`UI_report.py`**: 
  - `StartWindow` - Second window, collects file inputs (report config XLSX, TDM error dict XLSX, TDM config CSV, TDM log CSV).
  - `AnalysisWindow` - Main analysis window with test table and per-row actions.
- **`UI_standaloneReport.py`**: `StartWindow` - Alternative UI for standalone test reports.
- **`UI_update_RDP.py`** - Window for updating RDP reports.
- **`UI_user_fail_validation.py`**: `ValidationWindow` - Validation/error display window.

### Configuration & Data Integration
- **`dictDataIntegration.py`** - Centralized config data:
  - Software version (`sw_version = "2.4.00"`)
  - Test types: `Standalone test`, `Integration test`
  - Inverter models: `Pacman 5`, `1 UP`
  - Default table headers (machine-specific)
  - LIN error dictionary (codes 0-21 with names and types)
  - TDM status dictionary (status codes with descriptions)
  - Default test steps for Pacman 5 (DEFAULT_TEST_STEPS_PACMAN5) defining automated actions for report processing
  - Time dataset options: `Absolute time`, `Relative Time`
- **`Load_configuration_test.py`** - Loads test definitions from XLSX sheet (inverter-specific).
- **`TDM_config_load.py`** - Loads DGTO configuration from CSV with encoding/separator fallback.
- **`Read_TDM_error.py`** - Loads fault dictionary from TDM XLSX with in-memory caching.
- **`Read_TDM_report.py`** - Parses custom TDM report CSV format and can export to Excel.

### Report Processing
- **`fill_RDP_report.py`** - Fills RDP (Report Data Process) report templates:
  - Handles merged cells, colors, formatting
  - Password protection
  - Auto-detects table start rows
  - Applies cell styling (fill colors: green #C6EFCE for PASS, red #FFC7CE for FAIL)
  - Table headers: `["Test #", "Description", "Logs", "Notes", "Result"]`
- **`Read_report_file.py`** - Utility functions for reading/parsing report files. Handles header updates and writes Supporting Data images with fallback to text when needed.

### Analysis/Processing Engine
- **`step_engine.py`** - Executes JSON-like step actions:
  - `highlight_column`, `find_and_highlight`, `highlight_not_in_list`, `validate_version`, etc.
  - Works in conjunction with `ExcelStyler`.
- **`json_motor.py`** - Default step catalog (`DEFAULT_TEST_STEPS_PACMAN5`) and normalization helpers.
- **`ExcelStyler.py`** - Low-level workbook editing:
  - Cell/column highlighting
  - Validations and fault enrichment
  - Helper operations used by `StepEngine`

### Utilities & Support
- **`magic_logger.py`** - Custom logging setup per run with file rotation.
- **`resurces.qrc`**, **`resurces_rc.py`** - Qt resources (icons).
- **`iconos/`** - Application icons storage.

## UI Flow (Current)

```
main_UI.py::main()
    ↓
QApplication initialized
    ↓
SelectionWindow (UI_selection.py)
    ├─ Select test mode (Standalone/Integration)
    ├─ Select inverter model (Pacman 5 / 1 UP)
    └─ OK → launch StartWindow
         ↓
    StartWindow (UI_report.py)
         ├─ Collect file paths:
         │  ├─ Report config XLSX
         │  ├─ TDM error dict XLSX
         │  ├─ TDM config CSV
         │  └─ TDM log CSV
         ├─ Load via:
         │  ├─ load_test_definition_xlsx() → test dict
         │  ├─ load_tdm_once() → fault dict
         │  ├─ load_tdm_config() → DGTO config
         │  └─ read_custom_csv() → TDM data
         └─ Open → AnalysisWindow
              ↓
         AnalysisWindow (UI_report.py)
              ├─ Display test table from config
              ├─ Per-row action button:
              │  ├─ Read TDM log CSV
              │  ├─ Compare CSV headers vs DGTO names
              │  ├─ Run validation/analysis
              │  ├─ Write result to TEST SUMMARY cell
              │  ├─ Store detailed results in `self.test_results[test_num]`
              │  └─ Store widget-level result state in `container._test_result` for PASS/FAIL reading
              └─ Export to Excel via fill_RDP_report.py (includes analysis details)
                  **NEW**: Validates all tests analyzed before allowing RDP update
```

## Module Responsibilities

| Module | Purpose |
|--------|---------|
| **UI_selection.py** | First UI window; test mode & inverter selection |
| **UI_report.py** | StartWindow (file input) + AnalysisWindow (main table, actions). Validates all tests analyzed before RDP update, launches bug selection/report dialogs, and converts LIN/Modbus logs to Excel. |
| **UI_buglist.py** | `BugSelectionWindow` dialog for selecting tests with bugs and preparing bug report data. |
| **UI_BugReport.py** | `BugReportWindow` dialog for generating bug reports from selected tests and external buglist files. |
| **UI_standaloneReport.py** | Alternative UI for standalone test workflows |
| **UI_update_RDP.py** | Update/modify RDP report templates. Builds `header_data` from `StartWindow` values and passes `tests` summary to `fill_RDP_report.update_excel_template`. |
| **UI_user_fail_validation.py** | Validation error display window |
| **main_UI.py** | Application entry point; QApplication setup |
| **dictDataIntegration.py** | Shared configuration (versions, inverter models, headers, error dicts) |
| **Load_configuration_test.py** | Parse test definition XLSX → test config dict |
| **TDM_config_load.py** | Parse TDM config CSV → DGTO configuration dict |
| **Read_TDM_error.py** | Load TDM error/fault XLSX → fault code dict (cached) |
| **Read_TDM_report.py** | Parse custom TDM report CSV format || **lin_to_excel.py** | Convert LIN CSV logs to Excel workbooks with fill and formatting support. |
| **modbus_to_excel.py** | Convert Modbus CSV logs to Excel workbooks with fill and timestamp normalization. || **fill_RDP_report.py** | Fill Excel templates with styling, colors, protection |
| **Read_report_file.py** | Report file parsing utilities |
| **step_engine.py** | Execute JSON step actions; coordinate ExcelStyler |
| **json_motor.py** | Default step catalog; normalization helpers |
| **ExcelStyler.py** | Low-level Excel editing (highlight, format, validate) |
| **magic_logger.py** | Per-run logging with rotation |
### Recent changes

- 2026-05-18: Updated version to 2.4.00. Modified dictDataIntegration.py to reflect current project state and version. Updated version_info.txt to reflect new version (2, 4, 0, 0).
## Data Contracts (Key)

### Test Configuration Dict
```python
{
    int test_number: {
        str ATTRIBUTE: Any value,
        "TEST EVENTS": str,
        "TEST SCOPE": str,
        "FAULTS EXPECTED": str,
        "TDM LOG FILE": str,
        "MODBUS LOG FILE": str,        # for "1 UP" model
        "LIN LOG FILE": str,           # for "1 UP" model
        "TEST RESULT": str,
        "TEST SUMMARY": str,
        ...
    }
}
```

### TDM Fault Dict (from TDM error XLSX)
```python
{
    int fault_code: {
        "FAULT NAME": str,
        "ERROR LIST NAME FOR MANUAL": str
    }
}
```

### TDM Config Dict (from DGTO CSV)
```python
{
    str basename: {
        "DGTO": [...],
        "reg_DGTO": [...],
        "name_DGTO": [...],
        "info_DGTO": [...]
    }
}
```

### LIN Error Dict (from dictDataIntegration.py)
```python
{
    str error_code: {
        "Name": str,
        "error_type": str  # "Status", "Error", "Final error", "Warning"
    }
}
```

## Source Directory Snapshot

### Main UI Modules (src/)
```
src/
├── main_UI.py                      # Entry point
├── UI_selection.py                 # SelectionWindow (mode & inverter selection)
├── UI_report.py                    # StartWindow + AnalysisWindow (main analysis)
├── UI_standaloneReport.py          # Standalone test UI
├── UI_update_RDP.py                # RDP report update
├── UI_user_fail_validation.py      # ValidationWindow (error display)
├── UI_buglist.py                   # Bug selection dialog
├── UI_BugReport.py                 # Bug report dialog
├── lin_to_excel.py                 # LIN CSV → Excel helper
├── modbus_to_excel.py              # Modbus CSV → Excel helper
├── dictDataIntegration.py          # Shared config & constants
├── fill_RDP_report.py              # Excel template filling & styling
├── Read_report_file.py             # Report parsing utilities
├── Load_configuration_test.py      # Test config XLSX loader
├── TDM_config_load.py              # DGTO config CSV loader
├── Read_TDM_error.py               # TDM error dict XLSX loader
├── Read_TDM_report.py              # TDM report CSV parser
├── step_engine.py                  # Step action executor
├── json_motor.py                   # Step catalog & normalization
├── ExcelStyler.py                  # Excel editing & styling
├── magic_logger.py                 # Logging utilities
├── resurces.qrc                    # Qt resource definitions
├── resurces_rc.py                  # Qt compiled resources
├── iconos/                         # Application icons
└── .vscode/                        # VSCode config
```

### Test Directory (Test_code/)
```
Test_code/
├── __init__.py
├── test_copy_files.py
├── test_fill_rdp.py
├── test_motor_json.py
├── test_read_report_file.py
├── Test_read_tdm_error.py
├── Test_read_tdm_report.py
├── test_simple_engine.py
├── test_step_engine.py
├── test_step_engine_all_actions.py
├── test_TDM_config_load.py
└── validation_window.py
```

## Key Window Class References

| Window | File | Class | Purpose |
|--------|------|-------|---------|
| Selection | UI_selection.py | `SelectionWindow(QMainWindow)` | Test mode & inverter model selection |
| Start (Report) | UI_report.py | `StartWindow(QMainWindow)` | File input collection & validation |
| Analysis | UI_report.py | `AnalysisWindow(QMainWindow)` | Main test table with per-row actions |
| Standalone | UI_standaloneReport.py | `StartWindow(QMainWindow)` | Standalone report workflow |
| Validation | UI_user_fail_validation.py | `ValidationWindow(QDialog)` | Error/validation feedback |

## File Dependencies Map

```
main_UI.py
    └── UI_selection.py (SelectionWindow)
            └── UI_report.py (StartWindow → AnalysisWindow)
                    ├── Load_configuration_test.py
                    ├── TDM_config_load.py
                    ├── Read_TDM_error.py
                    ├── Read_TDM_report.py
                    ├── UI_buglist.py
                    ├── UI_BugReport.py
                    ├── lin_to_excel.py
                    ├── modbus_to_excel.py
                    ├── step_engine.py
                    │   └── json_motor.py
                    │       └── ExcelStyler.py
                    ├── fill_RDP_report.py
                    └── dictDataIntegration.py

magic_logger.py (centralized logging)
```

## Configuration Constants (from dictDataIntegration.py)

| Constant | Values | Purpose |
|----------|--------|---------|
| `sw_version` | `"2.4.00"` | Application version |
| `test_type` | `["Standalone test", "Integration test"]` | Test mode selection |
| `inverter` | `{"Pacman 5": [...], "1 UP": [...]}` | Inverter models & variants |
| `header_row_default` | `5` | Default TDM XLSX header row |
| `header_default_table` | Machine-specific list | UI table column headers |
| `time_data_set` | `["Absolute time", "Relative Time"]` | Time format options |
| `error_list_LIN` | Dict keyed by error code | LIN protocol error definitions |

## Update Policy (Keep This File Updated)

Update this file in the same commit whenever:
- New/removed Python module in `src/`
- New UI window/class added
- Changed function signatures between modules
- Changed runtime flow in `main_UI.py` or window classes
- Changed dict schema/keys in loaders or engine
- New action types in `step_engine.py`
- Modified inverter models or constants in `dictDataIntegration.py`
- Moved/renamed test files

**Minimum update checklist:**
1. Update `Last updated` date at top
2. Verify "High-Level Architecture" sections
3. Check "File Dependencies Map" for new connections
4. Verify "Data Contracts" if any key names/types changed
5. Update "Module Responsibilities" table
6. Confirm "Directory Snapshot" reflects all .py files
7. Add new test file to "Test Coverage"

**Quick verification commands:**
- `ls -la src/*.py` - verify source files
- `ls -la Test_code/*.py` - verify test files
- `grep -r "class.*Window" src/` - verify UI windows

### Excel Report Headers Mapping
- **`update_excel_template` headers**: `["Test #", "Description", "Logs", "Notes", "Result"]`
- **UI Table columns mapping** (Pacman 5):
  - "Test #" ← Column 0: "Test Number"
  - "Description" ← Column 1: "TEST EVENTS"  
  - "Notes" ← Column 2: "TEST SCOPE"
  - "Result" ← Column 6: "TEST RESULT"
- **Color Coding**:
  - PASS: Green (#C6EFCE)
  - FAIL: Red (#FFC7CE)
- `rg -n "class |def |if __name__ == '__main__'" UI_report.py step_engine.py ExcelStyler.py`
- `Get-ChildItem Test_code -File`
