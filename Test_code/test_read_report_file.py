
from openpyxl import Workbook
from Read_report_file import modify_excel_with_headers





# -----------------------------------------------------------
# 1) Create a test Excel file with 2 tables
# -----------------------------------------------------------

# def create_test_excel(path):
#     wb = Workbook()
#     ws = wb.active

#     # ---- TABLE 1 ----
#     ws.append(["Test Env", "Test N°", "Test scope", "TDM log", "Lin Log", "Modbus Log", "Analysis"])
#     ws.append(["Prod", "1", "Basic", "", "", "", ""])
#     ws.append(["Prod", "2", "Basic", "", "", "", ""])
#     ws.append(["Prod", "3", "Basic", "", "", "", ""])  # We'll target this row for test_num="3"

#     # Blank row to simulate separation
#     ws.append(["", "", "", "", "", "", ""])

#     # ---- TABLE 2 ----
#     ws.append(["Test Env", "Test N°", "Test scope", "TDM log", "Lin Log", "Modbus Log", "Analysis"])
#     ws.append(["Lab", "10", "Advanced", "", "", "", ""])
#     ws.append(["Lab", "11", "Advanced", "", "", "", ""])
#     ws.append(["Lab", "12", "Advanced", "", "", "", ""])

#     wb.save(path)


# -----------------------------------------------------------
# 2) Run test for modify_excel_with_headers()
# -----------------------------------------------------------

def test_function():
    excel_path = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\data_base\report_test\4021 Integration Test List_TDM_100.35.00.xlsx"
    #output_path = "test_output.xlsx"

    # create_test_excel(excel_path)

    search_header = {
        "TDM log": r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\Test_files\log_TDM_test_1_2_3.xlsx",
        "Lin Log": "C:/logs/lin.xlsx",
        "Modbus Log": "C:/logs/modbus.xlsx",
        "Analysis": "Test Completed"
    }

    test_num = "3"   # This will match row 4 of table 1

    modify_excel_with_headers(
        excel_path=excel_path,
        search_header=search_header,
        test_num=test_num,
        #output_path=output_path
    )

    print("✔ Test completed — check:")


# -----------------------------------------------------------
# MAIN
# -----------------------------------------------------------

if __name__ == "__main__":
    test_function()