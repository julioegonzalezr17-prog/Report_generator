import os
import pandas as pd
from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QScrollArea, QWidget, QCheckBox, QComboBox,
    QLineEdit, QTextEdit, QFileDialog, QMessageBox, QSizePolicy
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import resurces_rc
from dictDataIntegration import sw_version
from openpyxl import load_workbook

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import html
import urllib.parse
import math
from reportlab.lib.units import mm
from pathlib import Path


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

        self.TDM_combo = QComboBox()
        self.TDM_combo.setMinimumWidth(200)
        self.TDM_combo.addItems(["TDM 4", "TDM 3"])

        
        self.filter_tdm_combo = QComboBox()

    
        self.filter_tdm_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)       
        self.filter_tdm_combo.currentIndexChanged.connect(self.apply_filters)
        self.filter_tdm_combo.setMaximumWidth(140)


        
        self.filter_priority_combo = QComboBox()
        self.filter_priority_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.filter_priority_combo.setMaximumWidth(140)
        self.filter_priority_combo.currentIndexChanged.connect(self.apply_filters)


        tdm_layout = QHBoxLayout()
        tdm_layout.setSpacing(3)
        tdm_layout.addWidget(QLabel("Filter TDM:"))
        tdm_layout.addWidget(self.filter_tdm_combo)



        priority_layout = QHBoxLayout()
        priority_layout.setSpacing(3)
        priority_layout.addWidget(QLabel("Priority:"))
        priority_layout.addWidget(self.filter_priority_combo)


        filter_layout = QHBoxLayout()
        filter_layout.addStretch()
        filter_layout.addLayout(tdm_layout)
        filter_layout.addSpacing(15)
        filter_layout.addLayout(priority_layout)


        combo_layout = QVBoxLayout()
        combo_layout.addWidget(self.sheet_combo, 2)
        combo_layout.addWidget(self.TDM_combo, 2)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.path_edit, 4)
        top_layout.addWidget(btn_browse, 1)
        top_layout.addLayout(combo_layout, 2)

        # =========================
        # LEFT LIST
        # =========================
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        # =========================
        # RELATED BUGS PANEL
        # =========================
        self.related_scroll = QScrollArea()
        self.related_scroll.setWidgetResizable(True)

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
        main.addLayout(filter_layout)

        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Bug List"))
        left_panel.addWidget(self.scroll)

        left_panel.addWidget(QLabel("Related Bugs"))
        left_panel.addWidget(self.related_scroll)

        middle = QHBoxLayout()
        middle.addLayout(left_panel, 2)
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

        # =============================
        # 1. Detectar header real
        # =============================
        raw_df = pd.read_excel(self.excel_path, sheet_name=sheet, header=None)

        header_row = 0
        for i in range(min(30, len(raw_df))):
            row = raw_df.iloc[i].astype(str).str.upper()

            if row.str.contains("TEST").any() and row.str.contains("LOG").any():
                header_row = i
                break

        # =============================
        # 2. Leer dataframe correcto
        # =============================
        df = pd.read_excel(self.excel_path, sheet_name=sheet, header=header_row)

        # eliminar filas vacías
        df = df.reset_index(drop=True)

        # =============================
        # 3. Leer con openpyxl
        # =============================
        wb = load_workbook(self.excel_path, data_only=True)
        ws = wb[sheet]

        headers = [cell.value for cell in ws[header_row + 1]]

        # ✅ detectar SOLO Logs
        log_columns = [col for col in headers if str(col).strip().upper() == "LOGS"]


        # =============================
        # 4. Leer hyperlinks
        # =============================
        for col in log_columns:

            col_idx = headers.index(col)

            values = []

            for row in ws.iter_rows(min_row=header_row + 2):

                cell = row[col_idx]

                text = cell.value
                link = None

                if cell.hyperlink:
                    link = cell.hyperlink.target

                values.append({
                    "text": text,
                    "link": link
                })

            # ✅ asegurar mismo tamaño
            values = values[:len(df)]

            df[col] = values

        self.full_df = df
        self.filtered_df = df

        self.populate_filters()
        self.build_bug_list()
        self.filter_tdm_combo.setCurrentIndex(0)



    # =================================================
    # BUILD LIST
    # =================================================
    def build_bug_list(self):

        if self.filtered_df is None:
            return

        container = QWidget()
        layout = QVBoxLayout(container)

        self.bug_checkboxes.clear()

        for _, row in self.filtered_df.iterrows():

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

        if self.full_df is None:
            return
        
        # reset style de todos
        for cb in self.bug_checkboxes.values():
            cb.setStyleSheet("")

        selected = [
            item for item, cb in self.bug_checkboxes.items()
            if cb.isChecked()
        ]      
        
        if hasattr(self, "hidden_selected"):
            selected += list(self.hidden_selected)
            
        if not selected:
            self.result_view.setText("No bugs selected")
            self.build_related_list(set())
            return

        html_txt = ""

        for bug_id in selected:
            try:
                
                row_df = self.full_df[self.full_df["Item n"] == int(bug_id)]

                if row_df.empty:
                    continue

                row = row_df.iloc[0]

            except Exception:
                continue

            html_txt += f"<b>BUG {bug_id}</b><br>"

            for col in self.full_df.columns:

                raw_value = row.get(col, "")

                # ✅ FIX: si es dict → mostrar solo texto
                if isinstance(raw_value, dict):
                    value = raw_value.get("text", "")
                else:
                    value = raw_value

                value = self.format_cell(value)

                # color status
                if col == "Status":
                    if "OPEN" in str(value):
                        value = f"<font color='red'>{value}</font>"
                    else:
                        value = f"<font color='green'>{value}</font>"

                html_txt += f"<b>{col}:</b> {value}<br>"

            html_txt += "<br><hr><br>"

        # =========================
        # BUILD RELATED BUGS
        # =========================
        all_related = set()

        for bug_id in selected:
            ids = self.get_related_bug_ids(bug_id)
            all_related.update(ids)

        # remover los que ya están seleccionados
        all_related = all_related - set(selected)

        self.build_related_list(all_related)

        self.result_view.setHtml(html_txt)

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
        title = f"Bug Report {self.TDM_combo.currentText()} - Inverter {self.sheet_combo.currentText()}"
        content.append(Paragraph(title, styles["Title"]))
        content.append(Spacer(1, 12))

        for bug_id in selected:

            try:
                row = self.full_df[self.full_df["Item n"] == int(bug_id)].iloc[0]
            except Exception:
                continue

            content.append(Paragraph(f"<b>BUG {bug_id}</b>", styles["Heading2"]))
            content.append(Spacer(1, 6))

            table_data = []

            for col in self.full_df.columns:

                raw_value = row.get(col, "")
                value = ""
                if self.is_empty(raw_value):
                    continue
                if col == "SOLVED IN VERSION" or col == "Solved in version":
                    continue

                # ✅ FIX: detectar columna Logs correctamente
                if "LOG" in str(col).upper():

                    text = ""
                    link = None

                    if isinstance(raw_value, dict):
                        text = raw_value.get("text", "")
                        link = raw_value.get("link")
                    else:
                        text = raw_value

                    if link:    

                        link = str(link)

                        # ✅ quitar file:///
                        link = link.replace("file:///", "").replace("file://", "")

                        # ✅ decodificar espacios (%20 → espacio)
                        link = urllib.parse.unquote(link)

                        # ✅ convertir UNC paths correctamente
                        if link.startswith("\\\\"):
                            link = link.replace("\\", "/")
                            link = "//" + link.lstrip("/")

                        # ✅ fallback normal
                        link = link.replace("\\", "/")

                        visible_text = html.escape(str(text))

                        value = f'<link href="{link}"><u><font color="blue">{visible_text}</font></u></link>'

                    else:
                        value = self.format_cell(text)

                else:
                    value = self.format_cell(raw_value)

                table_data.append([
                    Paragraph(f"<b>{col}</b>", styles["Normal"]),
                    Paragraph(value, styles["Normal"]),
                    colors.white
                ])

            table = Table(
                [[r[0], r[1]] for r in table_data],
                colWidths=[150, 300]
            )

            table.setStyle(TableStyle([
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ]))

            content.append(table)
            content.append(Spacer(1, 20))

        doc.build(
            content,
            onFirstPage=self.draw_logo,
            onLaterPages=self.draw_logo
        )

        QMessageBox.information(self, "Done", "PDF generated successfully ✅")


    def is_empty(self, value):
        if value is None:
            return True
        
        if isinstance(value, float) and math.isnan(value):
            return True
        
        if isinstance(value, str) and value.strip() == "":
            return True
        
        return False
    
    # ✅ FORMATEO SEGURO
    def format_cell(self, value):

        if pd.isna(value):
            return ""

        value = str(value)
        # escapar HTML correctamente
        value = html.escape(value)

        # saltos de línea
        value = value.replace("\n", "<br/>")
        return value

    # ✅ 🔥 LECTOR EXCEL CON LINKS (VERSIÓN CORREGIDA)
    def read_excel_with_links(file_path):

        wb = load_workbook(file_path, data_only=True)
        ws = wb.active

        data = []

        # ✅ Leer headers (IMPORTANTE)
        headers = [cell.value for cell in ws[1]]

        for row in ws.iter_rows(min_row=2):
            row_data = {}

            for header, cell in zip(headers, row):

                value = cell.value

                link = None
                if cell.hyperlink:
                    link = cell.hyperlink.target

                row_data[header] = {
                    "text": value,
                    "link": link
                }

            data.append(row_data)

        return data

    def draw_logo(self, canvas, doc):
        file_path = os.path.dirname(__file__)
        folder_path = Path(file_path).parent
        logo_path = folder_path / "iconos" / "Ariston_logo.png"
        width = 100  # ancho en puntos (ajusta)
        height = 100

        x = doc.pagesize[0] - width - 80  # derecha
        y = doc.pagesize[1] - height  # arriba

        canvas.drawImage(logo_path, x, y, width=width, height=height, preserveAspectRatio=True)

    def populate_filters(self):

        df = self.full_df

        # ✅ EVITAR triggers automáticos
        self.filter_tdm_combo.blockSignals(True)
        self.filter_priority_combo.blockSignals(True)

        # PRIORITY
        if "Priority" in df.columns:
            priorities = sorted(df["Priority"].dropna().astype(str).unique())
        else:
            priorities = []

        self.filter_priority_combo.clear()
        self.filter_priority_combo.addItem("All")

        for p in priorities:
            self.filter_priority_combo.addItem(p)

        # 🟦 TDM
        if "TDM version" in df.columns:
            tdm_values = sorted(df["TDM version"].dropna().astype(str).unique())
        else:
            tdm_values = []

        self.filter_tdm_combo.clear()
        self.filter_tdm_combo.addItem("All")

        for v in tdm_values:
            self.filter_tdm_combo.addItem(v)


        # ✅ activar señales otra vez
        self.filter_tdm_combo.blockSignals(False)
        self.filter_priority_combo.blockSignals(False)


    def apply_filters(self):

        if self.full_df is None:
            return

        df = self.full_df.copy()

        # 🔵 filtro TDM
        tdm = self.filter_tdm_combo.currentText()
        if tdm != "All" and "TDM version" in df.columns:
            df = df[df["TDM version"].astype(str) == tdm]


        # 🟣 filtro PRIORITY
        priority = self.filter_priority_combo.currentText()
        if priority != "All" and "Priority" in df.columns:
            df = df[df["Priority"].astype(str) == priority]

        self.filtered_df = df

        # 🔄 reconstruir lista UI
        self.result_view.clear()
        self.build_bug_list()
        self.build_related_list(set())

    def get_related_bug_ids(self, bug_id):

        related_ids = set()
        related_ids.add(str(bug_id))

        row = self.full_df[self.full_df["Item n"].astype(str) == str(bug_id)]

        if row.empty:
            return related_ids

        col_name = None

        for col in self.full_df.columns:
            if "RELATED" in col.upper() and "BUG" in col.upper():
                col_name = col
                break

        value = row.iloc[0].get(col_name, "") if col_name else ""

        if pd.isna(value):
            return related_ids

        parts = str(value).split(",")

        for p in parts:
            p = p.strip()
            if p:
                related_ids.add(p)
        
        valid_ids = set(self.full_df["Item n"].astype(str))

        related_ids = {rid for rid in related_ids if rid in valid_ids}
        return related_ids
    
    def build_related_list(self, related_ids):

        container = QWidget()
        layout = QVBoxLayout(container)

        if not related_ids:
            layout.addWidget(QLabel("No related bugs"))
            self.related_scroll.setWidget(container)
            return

        for bug_id in sorted(related_ids):

            row = self.full_df[
                self.full_df["Item n"].astype(str) == str(bug_id)
            ]

            if row.empty:
                continue

            issue = str(row.iloc[0].get("ISSUES", ""))

            label = QLabel(f"{bug_id} - {issue}")
            label.setStyleSheet("color: blue; text-decoration: underline;")
            label.setCursor(Qt.PointingHandCursor)

            label.mousePressEvent = lambda e, bid=bug_id: self.select_bug(bid)

            layout.addWidget(label)

        layout.addStretch()
        self.related_scroll.setWidget(container)

    def select_bug(self, bug_id):

        bug_id = str(bug_id)

        # ✅ si está visible
        if bug_id in self.bug_checkboxes:
            cb = self.bug_checkboxes[bug_id]

            if not cb.isChecked():
                cb.setChecked(True)

            cb.setStyleSheet("font-weight: bold; color: green;")

        else:
            # ✅ bug oculto por filtro → igual incluir en preview
            if not hasattr(self, "hidden_selected"):
                self.hidden_selected = set()

            self.hidden_selected.add(bug_id)

            self.update_preview()
