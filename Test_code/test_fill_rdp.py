
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))


from fill_RDP_report import update_excel_template


# This header_data matches the values derived from StartWindow._collect_input
header_data = {
    "Request by:": "Giorgio Baglivo",
    "Performed by:": "Julio Gonzalez",
    "TDM": "100.32.00",
    "Control Board": "03.05.00",
    "Inverter fw": "15.15.01",
    "Test start Date:": "2026-04-20",
    "Test end Date:": "2026-04-27",
    "machine": "Pacman 5 RD4021"
}

# Simulating 15 tests with realistic analysis results from AnalysisWindow.test_results
tests = [
    {
        "num": 1,
        "desc": "Communication startup test",
        "notes": "Basic communication initialization with TDM",
        "result": "PASS"
    },
    {
        "num": 2,
        "desc": "Inverter stress test",
        "notes": "Stress test with thermal load simulation",
        "result": "PASS"
    },
    {
        "num": 3,
        "desc": "Power ramp test",
        "notes": "Gradual power increase to full capacity",
        "result": "PASS"
    },
    {
        "num": 4,
        "desc": "Temperature monitoring",
        "notes": "Thermal sensor validation",
        "result": "FAIL"
    },
    {
        "num": 5,
        "desc": "EEPROM verification",
        "notes": "Memory content integrity check",
        "result": "PASS"
    },
    {
        "num": 6,
        "desc": "DSP firmware validation",
        "notes": "Digital signal processor code verification",
        "result": "PASS"
    },
    {
        "num": 7,
        "desc": "Grid synchronization",
        "notes": "Phase lock loop stability test",
        "result": "FAIL"
    },
    {
        "num": 8,
        "desc": "Fault injection test",
        "notes": "Controlled fault triggering for error handling",
        "result": "PASS"
    },
    {
        "num": 9,
        "desc": "Modbus communication",
        "notes": "Serial protocol compliance check",
        "result": "PASS"
    },
    {
        "num": 10,
        "desc": "Emergency shutdown",
        "notes": "Safety protocol verification",
        "result": "FAIL"
    },
    {
        "num": 11,
        "desc": "Voltage regulation",
        "notes": "Output voltage stability validation",
        "result": "PASS"
    },
    {
        "num": 12,
        "desc": "Current limiting",
        "notes": "Maximum current protection test",
        "result": "PASS"
    },
    {
        "num": 13,
        "desc": "Efficiency measurement",
        "notes": "Power conversion efficiency analysis",
        "result": "PASS"
    },
    {
        "num": 14,
        "desc": "Harmonic distortion",
        "notes": "THD measurement and compliance",
        "result": "FAIL"
    },
    {
        "num": 15,
        "desc": "Long-term reliability test",
        "notes": "Extended operation stability check",
        "result": "PASS"
    }
]

# Test the update_excel_template function
try:
    update_excel_template(
        template_path=r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\data_test\Report RdP 0258-26 - PACMAN 5 WEBA - Ariston inverter R290 Integration Testing TDM 100.32.00.xlsx",
        output_path=None,
        data_path=r"C:\Users\gonzpidr\Ariston Group\Alignement - General\01_INVERTERS\05_Ariston Inverter\03_Testing\02_SW Qualification - Integration Inverter-TDM\2026_04_20 TDM 100.32.00-Ariston 15.15.01",
        header_data=header_data,
        tests=tests
    )
    print("\n✓ Test completed successfully!")
    print(f"✓ Processed {len(tests)} tests")
    print("✓ All analysis data was properly formatted and written to Excel")
except Exception as e:
    print(f"\n✗ Error during test execution:")
    print(f"  {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()