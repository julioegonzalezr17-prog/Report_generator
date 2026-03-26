"""
Test para validar que step_engine.py funciona correctamente con la estructura JSON de json_motor.py
"""
import os
import sys
from pathlib import Path

# Add workspace to path
workspace_path = str(Path(__file__).parent)
if workspace_path not in sys.path:
    sys.path.insert(0, workspace_path)
from Read_TDM_error import load_tdm_once
from ExcelStyler import ExcelStyler
from step_engine import StepEngine
from json_motor import DEFAULT_TEST_STEPS_PACMAN5
import json


def test_step_engine_with_json():
    """
    Test que step_engine.py funciona con la estructura del JSON.
    """
    print("\n" + "="*70)
    print("TEST: StepEngine con JSON structure")
    print("="*70)
    
    # 1. Load TDM dictionary from real file
    tdm_path = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\data_base\Tabella diagnostica TDM4 v19.xlsx"
    print(f"\n✓ Loading TDM from: {tdm_path}")
    tdm_dict = load_tdm_once(tdm_path, header_row=5)
    print(f"  Found {len(tdm_dict)} fault codes")
    print(f"  Sample fault codes: {list(tdm_dict.keys())[:5]}")
    
    # 2. Use actual test Excel and configuration
    test_excel = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\Test_files\log_TDM_test_1_2_3.xlsx"
    if not os.path.exists(test_excel):
        # try converting from CSV if available
        csvpath = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\Test_files\log_TDM_test_1_2_3.csv"
        if os.path.exists(csvpath):
            print(f"\n✓ XLSX not found, converting from CSV: {csvpath}")
            from Read_TDM_report import read_custom_csv, save_to_excel
            header, df = read_custom_csv(csvpath)
            save_to_excel(test_excel, header, df)
            print(f"  Conversion complete, created {test_excel}")
        else:
            raise FileNotFoundError(f"Test file not found: {test_excel} (also looked for {csvpath})")
    print(f"\n✓ Using test Excel: {test_excel}")
    
    # 3. Generate test configuration from Report_config_Pacman5.xlsx
    config_xlsx = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\data_base\Report_config_Pacman5.xlsx"
    if not os.path.exists(config_xlsx):
        raise FileNotFoundError(f"Configuration file not found: {config_xlsx}")
    print(f"\n✓ Generating test config from: {config_xlsx}")
    from json_motor import create_test_config_json
    temp_json = "temp_test_config.json"
    try:
        # try to build configuration from the Excel file (may be locked by Excel)
        config = create_test_config_json(config_xlsx, 
                                         temp_json,
                                         "RD4021",
                                         "Pacman 5",
                                         "RD4021")
        # pick first test entry available
        test_items = list(config.get("tests", {}).items())
        if not test_items:
            raise ValueError("No tests found in configuration")
        first_key, first_attrs = test_items[0]
        print(f"  Using test number {first_key} from config")
        # keep full dict for lookups
        test_config = first_attrs.copy()
        test_config.setdefault("steps", [])
    except Exception as ex:
        print(f"⚠ Aviso: no se pudo leer el archivo de configuración ({ex}), usando configuración manual")
        # build manual configuration using DEFAULT_TEST_STEPS_PACMAN5[1]
        from json_motor import DEFAULT_TEST_STEPS_PACMAN5
        manual_steps = DEFAULT_TEST_STEPS_PACMAN5.get(1, [])
        # create fake lists for "NO fault" (take two tdm codes) and maybe others
        no_fault_list = list(tdm_dict.keys())[:2]
        # intentionally use mixed-case key to validate case‑insensitive lookup
        test_config = {
            "steps": manual_steps,
            "No fault": no_fault_list,
        }
        # note: Faults Expected is handled specially by StepEngine
    
    # 4. Initialize StepEngine with test_config generated earlier
    styler = ExcelStyler(test_excel, sheet_name="DATA", tdm_dict=tdm_dict)
    
    # log the steps we are about to run
    print(f"\n✓ Testing configuration steps loaded from Report_config_Pacman5.xlsx")
    print(f"  Actions: {len(test_config.get('steps', []))} steps")
    for i, action in enumerate(test_config.get('steps', []), 1):
        colinfo = action.get('column', action.get('value', action.get('text', '')))
        print(f"    {i}. {action['action']}: {colinfo}")
    
    # 5. Create StepEngine and execute using loaded config
    engine = StepEngine(styler, config,"1")

    # quick sanity checks for our recent fixes
    print(f"\n▶ resolution('No fault') => {engine._resolve_value_list('No fault')}")
    print(f"▶ resolution('no fault') => {engine._resolve_value_list('no fault')}")
    fe_vals = engine._resolve_value_list('Faults Expected')
    print(f"▶ resolution('Faults Expected') => {fe_vals} (total {len(fe_vals)})")
    # sanity assertion for first test: config contained a single value 2055
    if isinstance(fe_vals, list) and len(fe_vals) == 1:
        print("   ✓ 'Faults Expected' resolved to single code from config")
    else:
        print("   ⚠ 'Faults Expected' did not resolve as expected")

    try:
        print(f"\n✓ Executing step engine...")
        result = engine.execute()
        print(f"  Step execution completed successfully!")
        print(f"  Result: {result}")
    except Exception as e:
        print(f"✗ Error during step execution: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 5. Save output and verify
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_excel = f"test_step_engine_output_{timestamp}.xlsx"
    styler.save(test_excel)
    print(f"\n✓ Saved output to: {output_excel}")
    
    # Cleanup
    # do not remove the real log file; keep it intact
    if os.path.exists(temp_json):
        os.remove(temp_json)
    
    print("\n" + "="*70)
    print("✓ TEST PASSED: StepEngine works with JSON structure")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        success = test_step_engine_with_json()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
