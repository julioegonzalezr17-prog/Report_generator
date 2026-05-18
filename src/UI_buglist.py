import copy
import logging
from PySide6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QScrollArea, QWidget, QCheckBox, QGroupBox, QMessageBox
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from dictDataIntegration import sw_version

logger = logging.getLogger(__name__)


class BugSelectionWindow(QDialog):

    def __init__(self, data_dict: dict, parent=None):
        super().__init__(parent)

        # ✅ NUEVA ESTRUCTURA
        self.data = copy.deepcopy(data_dict)
        self.tests_dict = self.data.get("Test", {})

        self.test_checkboxes = {}

        # ---------------- UI ----------------
        self.setModal(True)
        self.setWindowTitle("Bug Selection" + "Version " + sw_version)
        self.setWindowIcon(QIcon(":/monitoring.png"))
        self.resize(900, 700)

        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QPushButton {
                min-height: 40px;
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

        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        # ---------------- Title ----------------
        title = QLabel("Bug Selection per Test")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: 600;")

        # ---------------- Report data ----------------
        report_box = QGroupBox("Report Information")
        report_layout = QVBoxLayout(report_box)

        report_data = self.data.get("report_data", {})
        formatted_report = self._format_initial_data(report_data)

        report_label = QLabel(formatted_report)
        report_label.setWordWrap(True)
        report_label.setTextFormat(Qt.RichText)
        report_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        report_label.setStyleSheet("""
            QLabel {
                border: 1px solid #cccccc;
                border-radius: 6px;
                padding: 10px;
                background-color: white;
            }
        """)

        report_layout.addWidget(report_label)

        # ---------------- Test list ----------------
        test_scroll = self._create_test_list()

        # ---------------- Buttons ----------------
        self.btn_cancel = QPushButton("Cancel")
        self.btn_next = QPushButton("Next")

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addWidget(self.btn_next)

        # ---------------- Main layout ----------------
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title)
        main_layout.addWidget(report_box)
        main_layout.addWidget(test_scroll, stretch=1)
        main_layout.addLayout(buttons_layout)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_next.clicked.connect(self._on_next)

    # =================================================
    # FORMAT REPORT
    # =================================================
    def _format_initial_data(self, d: dict) -> str:

        def format_version_field(value):
            if not value:
                return "NA"

            if not isinstance(value, list):
                return str(value)

            padded = [v.zfill(2) for v in value]

            if len(padded) == 3:
                if "" in value:
                    return f"V00{padded[0]}_T{padded[1]}"
                return ".".join(padded)

            if len(padded) == 2:
                if "" in value:
                    return "NA"
                return f"V00{padded[0]}_T{padded[1]}"

            return "_".join(padded)

        return (
            "<b>Session data received:</b><br>"
            f"- RDP Number: {d.get('rdp_number', '')}<br>"
            f"- Test requested by: {d.get('requester_name', '')}<br>"
            f"- Tester Name: {d.get('tester_name', '')}<br>"
            f"- Machine model: {d.get('machine_model', '')}<br>"
            f"- Inverter model: {d.get('inverter_model', '')}<br>"
            f"- Inverter EEPROM version: {format_version_field(d.get('inverter_eeprom'))}<br>"
            f"- Inverter DSP version: {format_version_field(d.get('inverter_dsp'))}<br>"
            f"- Inverter ARM version: {format_version_field(d.get('inverter_arm'))}<br>"
            f"- Inverter PFC version: {format_version_field(d.get('inverter_pfc'))}<br>"
            f"- Control Board version: {format_version_field(d.get('control_board'))}<br>"
            f"- TDM version: {format_version_field(d.get('tdm_version'))}<br>"
            f"- Notes: {d.get('notes', '').replace(chr(10), '<br>')}"
        )

    # =================================================
    # CLEAN ANALYSIS
    # =================================================
    def _clean_analysis_text(self, analysis: str) -> str:
        if not analysis:
            return ""

        clean_lines = []

        for line in analysis.splitlines():
            line = line.strip()

            if "[]" in line or "{}" in line:
                if "PASS" in line:
                    clean_lines.append(line.split("PASS")[0] + "PASS")
                elif "FAIL" in line:
                    clean_lines.append(line.split("FAIL")[0] + "FAIL")
                else:
                    clean_lines.append(line)
            else:
                clean_lines.append(line)

        return "<br>".join(clean_lines)

    # =================================================
    # TEST LIST ✅
    # =================================================
    def _create_test_list(self):
        container = QWidget()
        layout = QVBoxLayout(container)

        for test_id, test_data in self.tests_dict.items():

            if not isinstance(test_data, dict):
                continue

            box = QGroupBox(f"Test {test_id}")
            vbox = QVBoxLayout(box)

            cb = QCheckBox("Bug detected in this test")
            self.test_checkboxes[test_id] = cb

            test_scope = test_data.get("test_scope", "")
            raw_analysis = test_data.get("data_print_report", {}).get("Analysis", "")
            analysis = self._clean_analysis_text(raw_analysis)

            lbl_scope = QLabel(f"<b>Test scope:</b> {test_scope}")
            lbl_scope.setWordWrap(True)

            vbox.addWidget(cb)
            vbox.addWidget(lbl_scope)

            if analysis:
                lbl_analysis = QLabel(f"<b>Analysis:</b><br>{analysis}")
                lbl_analysis.setWordWrap(True)
                lbl_analysis.setTextInteractionFlags(Qt.TextSelectableByMouse)
                vbox.addWidget(lbl_analysis)

            layout.addWidget(box)

        layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        return scroll

    # =================================================
    # NEXT BUTTON ✅
    # =================================================
    def _on_next(self):
        test_selected = []
        # ✅ actualizar BUG flags
        for test_id, cb in self.test_checkboxes.items():
            if test_id in self.tests_dict:
                self.tests_dict[test_id]["BUG"] = cb.isChecked()
                if cb.isChecked():
                    test_selected.append(test_id)
        if not test_selected:
            QMessageBox.warning(
                self,
                "No bugs selected",
                "Please select at least one test with a detected bug to proceed."
            )
            return


        logger.info("Updated BUG flags: %s", self.tests_dict)

        self.accept()

    # =================================================
    # OUTPUT ✅
    # =================================================
    def get_updated_data(self) -> dict:
        return self.data