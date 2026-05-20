import os
import pandas as pd
from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QScrollArea, QWidget, QCheckBox, QComboBox,
    QLineEdit, QTextEdit, QFileDialog, QMessageBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import resurces_rc
from dictDataIntegration import sw_version

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors



class BugReportGenerator(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bug Report Generator " + "Version " + sw_version)
        self.setWindowIcon(QIcon(":/info_icon.png"))
        self.setMinimumSize(1100, 700)

        self.setStyleSheet("""
            QWidget { font-size: 14px; }
            QPushButton {
                min-height: 30px;
                padding: 8px 16px;
                background-color: #2d89ef;
                color: white;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1b5fbd;
            }
        """)

        self.dataframe = None
        self.excel_path = None
        self.bug_checkboxes = {}

        # =========================
        # TOP AREA
        # =========================
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)

        btn_browse = QPushButton("Select Excel")
        btn_browse.clicked.connect(self.load_excel)

        self.sheet_combo = QComboBox()
        self.sheet_combo.setMinimumWidth(200)
        self.sheet_combo.currentIndexChanged.connect(self.load_sheet)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.path_edit, 4)
        top_layout.addWidget(btn_browse, 1)
        top_layout.addWidget(self.sheet_combo, 2)

        # =========================
        # LEFT LIST
        # =========================
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        # =========================
        # RIGHT PANEL (SUMMARY)
        # =========================
        self.result_view = QTextEdit()
        self.result_view.setReadOnly(True)
        self.result_view.setStyleSheet("""
            background-color: white;
            border: 1px solid #cccccc;
            padding: 10px;
        """)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Bug Summary"))
        right_layout.addWidget(self.result_view)

        # =========================
        # BUTTON
        # =========================
        btn_generate = QPushButton("Generate PDF")
        btn_generate.clicked.connect(self.generate_pdf)

        bottom = QHBoxLayout()
        bottom.addStretch()
        bottom.addWidget(btn_generate)

        # =========================
        # MAIN LAYOUT
        # =========================
        container = QWidget()
        main = QVBoxLayout(container)

        main.addLayout(top_layout)

        middle = QHBoxLayout()
        middle.addWidget(self.scroll, 2)
        middle.addLayout(right_layout, 3)

        main.addLayout(middle)
        main.addLayout(bottom)

        self.setCentralWidget(container)

    # =================================================
    # LOAD EXCEL
    # =================================================
    def load_excel(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Excel", "", "*.xlsx")

        if not path:
            return

        if not path.lower().endswith(".xlsx"):
            QMessageBox.warning(self, "Error", "Only .xlsx allowed")
            return

        self.path_edit.setText(path)
        self.excel_path = path

        xl = pd.ExcelFile(path)
        self.sheet_combo.clear()
        self.sheet_combo.addItems(xl.sheet_names)

    # =================================================
    # LOAD SHEET
    # =================================================
    def load_sheet(self):
        if not self.excel_path:
            return

        sheet = self.sheet_combo.currentText()
        if not sheet:
            return

        self.dataframe = pd.read_excel(self.excel_path, sheet_name=sheet)
        self.build_bug_list()

    # =================================================
    # BUILD LIST
    # =================================================
    def build_bug_list(self):

        container = QWidget()
        layout = QVBoxLayout(container)

        self.bug_checkboxes.clear()

        for _, row in self.dataframe.iterrows():
            item = str(row.get("Item n", ""))
            issue = str(row.get("ISSUES", ""))

            text = f"{item} - {issue}"

            cb = QCheckBox(text)
            cb.stateChanged.connect(self.update_preview)

            self.bug_checkboxes[item] = cb
            layout.addWidget(cb)

        layout.addStretch()
        self.scroll.setWidget(container)

    # =================================================
    # LIVE SUMMARY ✅
    # =================================================
    def update_preview(self):

        if self.dataframe is None:
            return

        selected = [
            item for item, cb in self.bug_checkboxes.items()
            if cb.isChecked()
        ]

        if not selected:
            self.result_view.setText("No bugs selected")
            return

        html = ""

        for bug_id in selected:
            try:
                row = self.dataframe[self.dataframe["Item n"] == int(bug_id)].iloc[0]
            except Exception:
                continue

            html += f"<b>BUG {bug_id}</b><br>"

            for col in self.dataframe.columns:
                if col == "Logs":
                    continue

                value = self.format_cell(row.get(col, ""))
                
                if isinstance(value, str):
                    value = value.replace("\n", "<br>")

                if pd.isna(value):
                    value = ""

                # color status
                if col == "Status":
                    if "OPEN" in str(value):
                        value = f"<font color='red'>{value}</font>"
                    else:
                        value = f"<font color='green'>{value}</font>"

                html += f"<b>{col}:</b> {value}<br>"

            html += "<br><hr><br>"

        self.result_view.setHtml(html)

    # =================================================
    # GENERATE PDF ✅
    # =================================================


    def generate_pdf(self):

        selected = [
            item for item, cb in self.bug_checkboxes.items()
            if cb.isChecked()
        ]

        if not selected:
            QMessageBox.warning(self, "Warning", "Select at least one bug")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "*.pdf")
        if not path:
            return

        doc = SimpleDocTemplate(path, pagesize=A4)
        styles = getSampleStyleSheet()

        content = []

        content.append(Paragraph("Bug Report", styles["Title"]))
        content.append(Spacer(1, 12))

        for bug_id in selected:

            try:
                row = self.dataframe[self.dataframe["Item n"] == int(bug_id)].iloc[0]
            except Exception:
                continue

            content.append(Paragraph(f"<b>BUG {bug_id}</b>", styles["Heading2"]))
            content.append(Spacer(1, 6))

            table_data = []

            for col in self.dataframe.columns:

                if col == "Logs":
                    continue

                raw_value = row.get(col, "")
                value = self.format_cell(raw_value)

                # ✅ COLOR STATUS
                bg_color = colors.white
                if col == "Status":
                    if "OPEN" in str(raw_value):
                        bg_color = colors.lightcoral
                    elif "CLOSE" in str(raw_value):
                        bg_color = colors.lightgreen

                table_data.append([
                    Paragraph(f"<b>{col}</b>", styles["Normal"]),
                    Paragraph(value, styles["Normal"]),
                    bg_color
                ])

            table = Table(
                [[r[0], r[1]] for r in table_data],
                colWidths=[150, 300]
            )

            style = [
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]

            for i, row_data in enumerate(table_data):
                if row_data[2] != colors.white:
                    style.append(("BACKGROUND", (1, i), (1, i), row_data[2]))

            table.setStyle(TableStyle(style))

            content.append(table)
            content.append(Spacer(1, 20))

        doc.build(content)

        QMessageBox.information(self, "Done", "PDF generated successfully ✅")

    def format_cell(self, value):

        if pd.isna(value):
            return ""

        value = str(value)

        # ✅ escapar SOLO &, pero respetar HTML
        value = value.replace("&", "&amp;")

        # ✅ saltos de línea reales HTML
        value = value.replace("\n", "<br/>")

        return value