import sys
from pathlib import Path

# Ensure src is importable when running from the test folder
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from UI_report import AnalysisWindow


class DummyVersionValidation:
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


def run_case(test_num, user_data, versions_fault_data, expected_result):
    dummy = DummyVersionValidation()
    data = {
        "test_num": test_num,
        "step_dic": build_step_dic(test_num),
        "user_data": user_data,
        "versions": {"fault_data": versions_fault_data},
    }
    result = dummy.Version_SW_validation(data)
    print(f"[{test_num}] user={user_data['inverter_model']} -> {result}")
    assert result["result_test"] == expected_result, f"Expected {expected_result} for {test_num}, got {result}"
    return result


if __name__ == "__main__":
    # RD4021: compare eeprom + dsp
    run_case(
        test_num="1",
        user_data={
            "inverter_model": "RD4021",
            "inverter_eeprom": ["0", "2"],
            "inverter_dsp": ["0", "15", ""],
            "inverter_arm": ["", ""],
            "inverter_pfc": ["", ""],
        },
        versions_fault_data={
            "EEPROM_VERSION_EK_RD": "V00_T02",
            "DSP_MAIN_VERSION_EcoKing": "V00_T0F",
        },
        expected_result="PASS",
    )

    # ID1PH_R290: compare eeprom + dsp + arm
    run_case(
        test_num="2",
        user_data={
            "inverter_model": "ID1PH_R290",
            "inverter_eeprom": ["0", "2"],
            "inverter_dsp": ["0", "15", ""],
            "inverter_arm": ["0", "1"],
            "inverter_pfc": ["", ""],
        },
        versions_fault_data={
            "EEPROM_VERSION_EK_RD": "V00_T02",
            "DSP_MAIN_VERSION_EcoKing": "V00_T0F",
            "HW_VERSION_EcoKing": "V00_T01",
        },
        expected_result="PASS",
    )

    # Ariston: compare dsp + pb dsp fw2
    run_case(
        test_num="3",
        user_data={
            "inverter_model": "Ariston",
            "inverter_eeprom": ["", ""],
            "inverter_dsp": ["0", "15", "12"],
            "inverter_arm": ["", ""],
            "inverter_pfc": ["", ""],
        },
        versions_fault_data={
            "DSP_MAIN_VERSION_EcoKing": "V00_T0F",
            "PB_DSP_FW2": "12",
        },
        expected_result="PASS",
    )

    # RD4018: compare eeprom + dsp, pfc is user-only
    run_case(
        test_num="4",
        user_data={
            "inverter_model": "RD4018",
            "inverter_eeprom": ["0", "2"],
            "inverter_dsp": ["0", "15", ""],
            "inverter_arm": ["", ""],
            "inverter_pfc": ["0", "1"],
        },
        versions_fault_data={
            "EEPROM_VERSION_EK_RD": "V00_T02",
            "DSP_MAIN_VERSION_EcoKing": "V00_T0F",
        },
        expected_result="PASS",
    )

    print("All Version_SW_validation test cases passed.")
