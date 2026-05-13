import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from UI_report import AnalysisWindow
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestVersionValidation:
    normalize_name = AnalysisWindow.normalize_name
    Version_SW_validation = AnalysisWindow.Version_SW_validation


def build_step_dic(test_num: str):
    return {
        "tests": {
            test_num: {
                "steps": [
                    {
                        "action": "validate_version",
                        "column": [
                            "DSP_MAIN_VERSION_EcoKing",
                            "PB_DSP_FW2",
                            "HW_VERSION_EcoKing",
                            "EEPROM_VERSION_EK_RD",
                        ],
                    }
                ]
            }
        }
    }


def test_rd4021_fail_mismatch():
    """Test case where user enters V00_T02 but fault_data has V00_T03 (mismatch)"""
    print("\n=== TEST: RD4021 FAIL (version mismatch) ===")
    test = TestVersionValidation()
    
    # Simula lo que devuelve Fault_code_validation (engine.execute())
    result_fault_validation = {
        "result_test": "PASS",
        "fault_data": {
            "Faults_Not_expected": {},
            "EEPROM_VERSION_EK_RD": "V00_T03",  # User expects V00_T02, but got V00_T03
            "DSP_MAIN_VERSION_EcoKing": "V00_T0F",
        }
    }
    
    user_data = {
        "inverter_model": "RD4021",
        "inverter_eeprom": ["0", "2"],  # Expects V00_T02
        "inverter_dsp": ["0", "15", ""],  # Expects V00_T0F
        "inverter_arm": ["", ""],
        "inverter_pfc": ["", ""],
    }
    
    data = {
        "test_num": "1",
        "step_dic": build_step_dic("1"),
        "user_data": user_data,
        "versions": result_fault_validation,
    }
    
    result = test.Version_SW_validation(data)
    print(f"Result: {result}")
    assert result["result_test"] == "FAIL", f"Expected FAIL due to mismatch, got {result['result_test']}"
    print("✓ PASS")


def test_rd4021_pass_match():
    """Test case where user enters V00_T02 and fault_data has V00_T02 (match)"""
    print("\n=== TEST: RD4021 PASS (version match) ===")
    test = TestVersionValidation()
    
    result_fault_validation = {
        "result_test": "PASS",
        "fault_data": {
            "Faults_Not_expected": {},
            "EEPROM_VERSION_EK_RD": "V00_T02",  # Matches user expectation
            "DSP_MAIN_VERSION_EcoKing": "V00_T0F",  # Matches user expectation
        }
    }
    
    user_data = {
        "inverter_model": "RD4021",
        "inverter_eeprom": ["0", "2"],  # Expects V00_T02
        "inverter_dsp": ["0", "15", ""],  # Expects V00_T0F
        "inverter_arm": ["", ""],
        "inverter_pfc": ["", ""],
    }
    
    data = {
        "test_num": "1",
        "step_dic": build_step_dic("1"),
        "user_data": user_data,
        "versions": result_fault_validation,
    }
    
    result = test.Version_SW_validation(data)
    print(f"Result: {result}")
    assert result["result_test"] == "PASS", f"Expected PASS, got {result['result_test']}"
    print("✓ PASS")


def test_ariston_with_pb_dsp_fw2():
    """Test Ariston model with DSP + PB_DSP_FW2"""
    print("\n=== TEST: Ariston with PB_DSP_FW2 ===")
    test = TestVersionValidation()
    
    result_fault_validation = {
        "result_test": "PASS",
        "fault_data": {
            "Faults_Not_expected": {},
            "DSP_MAIN_VERSION_EcoKing": "V00_T0F",  # V=0x00=0, T=0x0F=15
            "PB_DSP_FW2": "12",  # Direct integer value
        }
    }
    
    user_data = {
        "inverter_model": "Ariston",
        "inverter_eeprom": ["", ""],
        "inverter_dsp": ["0", "15", "12"],  # V=0, T=15, Z=12
        "inverter_arm": ["", ""],
        "inverter_pfc": ["", ""],
    }
    
    data = {
        "test_num": "3",
        "step_dic": build_step_dic("3"),
        "user_data": user_data,
        "versions": result_fault_validation,
    }
    
    result = test.Version_SW_validation(data)
    print(f"Result: {result}")
    assert result["result_test"] == "PASS", f"Expected PASS, got {result['result_test']}"
    print("✓ PASS")


def test_missing_fault_data():
    """Test when fault_data is missing or None"""
    print("\n=== TEST: Missing/None fault_data values ===")
    test = TestVersionValidation()
    
    result_fault_validation = {
        "result_test": "PASS",
        "fault_data": {
            "Faults_Not_expected": {},
            # Missing EEPROM_VERSION_EK_RD
            "DSP_MAIN_VERSION_EcoKing": "V00_T0F",
        }
    }
    
    user_data = {
        "inverter_model": "RD4021",
        "inverter_eeprom": ["0", "2"],
        "inverter_dsp": ["0", "15", ""],
        "inverter_arm": ["", ""],
        "inverter_pfc": ["", ""],
    }
    
    data = {
        "test_num": "1",
        "step_dic": build_step_dic("1"),
        "user_data": user_data,
        "versions": result_fault_validation,
    }
    
    result = test.Version_SW_validation(data)
    print(f"Result: {result}")
    # Should FAIL because eeprom is missing/None
    assert result["result_test"] == "FAIL", f"Expected FAIL due to missing eeprom, got {result['result_test']}"
    print("✓ PASS")


if __name__ == "__main__":
    try:
        test_rd4021_pass_match()
        test_rd4021_fail_mismatch()
        test_ariston_with_pb_dsp_fw2()
        test_missing_fault_data()
        print("\n✓✓✓ All debug tests passed ✓✓✓\n")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        sys.exit(1)
