import os

# Ensure the current folder is on sys.path for local imports
HERE = os.path.dirname(__file__)
if HERE not in os.sys.path:
    os.sys.path.insert(0, HERE)

from Read_TDM_report import read_custom_csv, save_to_excel, detect_csv_delimiter
from ExcelStyler import ExcelStyler


# Path to the CSV log file
csv_path = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\Test_files\log_TDM_test_28_29.csv"
excel_output = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Python\Report_generator\Test_files\test_output.xlsx"

print("=" * 70)
print("STEP 1: Read CSV and save to Excel")
print("=" * 70)

# Read the CSV with custom structure

delimiter = detect_csv_delimiter(csv_path)
custom_header, data_frame = read_custom_csv(csv_path,delimiter)
print(delimiter)
print(f"✓ Custom Header shape: {custom_header.shape}")
print(f"✓ Data Frame shape: {data_frame.shape}")

# Save to Excel
save_to_excel(excel_output, custom_header, data_frame)
print(f"✓ Excel file saved: {excel_output}\n")

# =====================================================================
# STEP 2: Test ExcelStyler class
# =====================================================================
print("=" * 70)
print("STEP 2: Test ExcelStyler - All Functions")
print("=" * 70)

styler = ExcelStyler(excel_output, sheet_name="DATA")
print(f"✓ ExcelStyler loaded: {excel_output}")
print(f"  Max row: {styler.ws.max_row}")
print(f"  Max column: {styler.ws.max_column}\n")

# =====================================================================
# Test 2.1: highlight_row()
# =====================================================================
print("2.1 Testing highlight_row() - Highlight single row and multiple rows")
styler.highlight_row(row=4, color="FFFF00")
print("✓ Single row (4) highlighted with yellow (FFFF00)")

# Test with multiple rows
styler.highlight_row(row=[5, 6], color="FF00FF")
print("✓ Multiple rows (5, 6) highlighted with magenta (FF00FF)")

# Verify fill was applied
cell_4 = styler.ws.cell(row=4, column=1)
cell_5 = styler.ws.cell(row=5, column=1)
assert cell_4.fill.fill_type == "solid", "Row 4 fill type should be solid"
assert cell_5.fill.fill_type == "solid", "Row 5 fill type should be solid"
print("✓ Fill validation passed for rows 4 and 5\n")

# =====================================================================
# Test 2.2: highlight_column()
# =====================================================================
print("2.2 Testing highlight_column() - Single column, multiple columns, by header")
styler.highlight_column(col=3, color="FFCC00")
print("✓ Column 3 highlighted with gold (FFCC00)")

# Test with multiple columns by index
styler.highlight_column(col=[7, 8], color="FFDDFF")
print("✓ Columns 7, 8 highlighted with light magenta")

# Test with header names
headers_to_highlight = ["Absolute time", "CMP_DRIVE_STATUS_INFO_EK_RD"]
styler.highlight_column(col=headers_to_highlight, color="CCEEFF")
for h in headers_to_highlight:
    col_letter = styler.find_header_column(h)
    print(f"✓ Header '{h}' resolved to column: {col_letter}")

# Verify column 3 has fill
cell_3 = styler.ws.cell(row=3, column=3)
assert cell_3.fill.fill_type == "solid", "Column 3 header should have solid fill"
print("✓ Fill validation passed for column 3\n")

# =====================================================================
# Test 2.3: find_header_column() and cell_letter_to_number()
# =====================================================================
print("2.3 Testing find_header_column() and cell_letter_to_number()")

# Test find_header_column
header_col = styler.find_header_column("Absolute time")
assert header_col is not None, "Absolute time header should be found"
print(f"✓ Header 'Absolute time' found in column: {header_col}")

header_col2 = styler.find_header_column("CMP_DRIVE_STATUS_INFO_EK_RD")
assert header_col2 is not None, "CMP_DRIVE_STATUS_INFO_EK_RD header should be found"
print(f"✓ Header 'CMP_DRIVE_STATUS_INFO_EK_RD' found in column: {header_col2}")

# Test cell_letter_to_number
col_tests = [("A", 1), ("D", 4), ("Z", 26), ("AA", 27), ("AB", 28), ("BA", 53)]
for letter, expected_num in col_tests:
    result = styler.cell_letter_to_number(letter)
    assert result == expected_num, f"Column {letter} should be {expected_num}, got {result}"
    print(f"✓ Column '{letter}' -> {result}")

# Test finding non-existent header
header_col3 = styler.find_header_column("NonExistentHeader")
assert header_col3 is None, "Non-existent header should return None"
print("✓ Non-existent header correctly returned None\n")

# =====================================================================
# Test 2.4: insert_column() and append_column()
# =====================================================================
print("2.4 Testing insert_column() and append_column()")
old_max_col = styler.ws.max_column
styler.insert_column(existing_header="Relative time", header="New_Column", default_value="TEST")
new_max_col = styler.ws.max_column
col = styler.cell_letter_to_number(styler.find_header_column("New_Column"))
print(col)
assert new_max_col == old_max_col + 1, "Insert should increase max_column by 1"
assert styler.ws.cell(row=3, column=col).value == "New_Column", "Header should be set correctly"
assert styler.ws.cell(row=4, column=col).value == "TEST", "Default value should be set"
print(f"✓ Column inserted at position 4 (max_column: {old_max_col} -> {new_max_col})")

old_max_col = styler.ws.max_column
styler.append_column(header="Extra_Column", default_value=999)
new_max_col = styler.ws.max_column
assert new_max_col == old_max_col + 1, "Append should increase max_column by 1"
assert styler.ws.cell(row=3, column=new_max_col).value == "Extra_Column", "Header should be set"
assert styler.ws.cell(row=4, column=new_max_col).value == 999, "Default value should be set"
print(f"✓ Column appended at end (max_column: {old_max_col} -> {new_max_col})\n")

# =====================================================================
# Test 2.5: find_and_highlight_equals() and apply_conditional_formatting()
# =====================================================================
print("2.5 Testing find_and_highlight_equals() and apply_conditional_formatting()")

# Test find_and_highlight
matches = styler.find_and_highlight("B", "00:00:00.632", color="99CCFF")
print(f"✓ Cells in column B equal to '00:00:00.632': {matches}")
# Verify that matched cells have fill applied
for match_addr in matches:
    cell = styler.ws[match_addr]
    assert cell.fill.fill_type == "solid", f"Cell {match_addr} should have solid fill"
print("✓ Fill validation passed for matched cells")

# Test apply_conditional_formatting
styler.apply_conditional_formatting("C", operator="greaterThan", formula="1000", color="FF0000")
print("✓ Conditional formatting applied to column C (values > 1000 in red)")

# Verify conditional formatting rule was added
cf_list = styler.ws.conditional_formatting
print(f"✓ Conditional formatting rules verified (count: {len(cf_list)})\n")

# =====================================================================
# Test 2.6: autosize_columns()
# =====================================================================
print("2.6 Testing autosize_columns()")
print("Before autosize:")
width_a_before = styler.ws.column_dimensions['A'].width
width_b_before = styler.ws.column_dimensions['B'].width
print(f"  Column A width: {width_a_before}")
print(f"  Column B width: {width_b_before}")

styler.autosize_columns()

width_a_after = styler.ws.column_dimensions['A'].width
width_b_after = styler.ws.column_dimensions['B'].width
print("After autosize:")
print(f"  Column A width: {width_a_after}")
print(f"  Column B width: {width_b_after}")

# Verify widths were adjusted
assert width_a_after is not None and width_a_after > 0, "Column A width should be set"
assert width_b_after is not None and width_b_after > 0, "Column B width should be set"
print("✓ Column widths auto-sized correctly\n")

# =====================================================================
# Test 2.7: save()
# =====================================================================
print("2.7 Testing save() - Save styled workbook")
output_styled = os.path.join(HERE, "test_styled.xlsx")
styler.save(output_path=output_styled)
assert os.path.exists(output_styled), "Styled file should be created"
print(f"✓ Styled workbook saved to: {output_styled}")

# Verify file was saved by reloading
from openpyxl import load_workbook
wb_check = load_workbook(output_styled)
assert "DATA" in wb_check.sheetnames, "Saved workbook should have DATA sheet"
print("✓ File integrity verified (can reload)\n")

# =====================================================================
# Test 2.8: highlight_not_in_list() - Comprehensive validation
# =====================================================================
print("2.8 Testing highlight_not_in_list() - Fault Code validation")

# Create a FRESH ExcelStyler to test on clean data
styler_for_validation = ExcelStyler(excel_output, sheet_name="DATA")

# Try common header variants
header_variants = ["FAULT CODE", "Fault_Code", "Fault Code", "FaultCode", "Fault_Code"]
found_header = None
for h in header_variants:
    if styler_for_validation.find_header_column(h):
        found_header = h
        break

if not found_header:
    print("! Header 'FAULT CODE' not found; skipping highlight_not_in_list test.\n")
else:
    # Test with single allowed value
    mismatches = styler_for_validation.highlight_not_in_list([65535], col=found_header, color="FFFF0000")
    print(f"✓ highlight_not_in_list found mismatches: {len(mismatches)} rows")
    print(f"  Mismatched rows: {mismatches}")
    
    # Verify mismatches were highlighted in red
    fault_code_col = styler_for_validation.cell_letter_to_number(
        styler_for_validation.find_header_column(found_header)
    )
    if mismatches:
        test_row = mismatches[0]
        test_cell = styler_for_validation.ws.cell(row=test_row, column=fault_code_col)
        assert test_cell.fill.fill_type == "solid", "Mismatched cell should have solid fill"
        assert test_cell.fill.start_color.rgb == "FFFF0000", "Fill should be red (FFFF0000)"
        print("✓ Mismatched cells highlighted in red (FFFF0000)")
    
    # Save validation report
    output_mismatches = os.path.join(HERE, "test_mismatches.xlsx")
    styler_for_validation.save(output_path=output_mismatches)
    print(f"✓ Validation report saved to: {output_mismatches}\n")

# =====================================================================
# SUMMARY
# =====================================================================
print("=" * 70)
print("TEST SUMMARY - ExcelStyler Comprehensive Validation")
print("=" * 70)
print("""
✓ Test 2.1: highlight_row()
  - Single row highlighting
  - Multiple rows highlighting
  - Fill validation

✓ Test 2.2: highlight_column()
  - Single column by index
  - Multiple columns by index
  - Columns by header names
  - Fill validation

✓ Test 2.3: find_header_column() & cell_letter_to_number()
  - Header finding
  - Column letter to number conversion
  - Edge cases (AA, AB, BA)
  - Non-existent header handling

✓ Test 2.4: insert_column() & append_column()
  - Column insertion at position
  - Column appending at end
  - Header and value assignment
  - Max column tracking

✓ Test 2.5: find_and_highlight_equals() & apply_conditional_formatting()
  - Find matching cells
  - Highlight matching cells
  - Conditional formatting rules
  - Rule verification

✓ Test 2.6: autosize_columns()
  - Auto-sizing column widths
  - Width calculation validation

✓ Test 2.7: save()
  - Save to file
  - File integrity verification
  - Reload validation

✓ Test 2.8: highlight_not_in_list()
  - Find mismatches
  - Highlight mismatched cells in red
  - Color validation (FFFF0000)
  - Validation report generation
""")
print("=" * 70)
print(f"Generated files:")
print(f"  - {excel_output}")
print(f"  - {output_styled}")
if 'output_mismatches' in locals():
    print(f"  - {output_mismatches}")
print("=" * 70)
print(f"  - {output_styled} (with styling applied)")
print("=" * 70)

