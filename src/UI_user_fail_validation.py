import sys
from PySide6.QtWidgets import (
    QApplication, QLabel, QPushButton, QScrollArea, QScrollArea,
    QVBoxLayout, QHBoxLayout, QCheckBox, QDialog, QWidget
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt
from dictDataIntegration import sw_version
import logging
import copy

logger = logging.getLogger(__name__)


class ValidationWindow(QDialog):
    """
    Popup modal to validate test results before updating the report.
    """

    def __init__(self, test_results: dict, parent=None):
        super().__init__(parent)

        self.test_results = copy.deepcopy(test_results)
        self.dgto_checkboxes = {}
        self.fault_checkboxes = {}

        # ---- Dialog setup ----
        self.setModal(True)
        self.setWindowTitle(f"Fault Validation - Version {sw_version}")
        self.setWindowIcon(QIcon(":/monitoring.png"))
        self.resize(700, 700)

        global_font = QFont()
        global_font.setPointSize(12)
        self.setFont(global_font)

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

        # ---- Widgets ----
        self.title = QLabel("Test Results")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 32px; font-weight: 600;")

        formatted_text = self.format_validation_results(self.test_results)
        self.description = QLabel(formatted_text)  # Aquí se mostrarían los resultados a validar
        self.description.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.description.setStyleSheet("""
            QLabel {
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 12px;
                background-color: white;
                font-size: 12pt;
            }
        """)

        self.explanation = QLabel("Please review the detected issues and select which ones to accept for report update:")
        self.explanation.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.explanation.setStyleSheet("font-size: 14px; font-style: italic; margin-top: 10px; margin-bottom: 10px;")

        self.selection_DGTO = QLabel("DGTO Failures")
        self.selection_DGTO.setAlignment(Qt.AlignCenter)
        self.selection_DGTO.setStyleSheet("font-size: 22px; font-weight: 600;")

        self.selection_FAULT = QLabel("FAULT Failures")
        self.selection_FAULT.setAlignment(Qt.AlignCenter)
        self.selection_FAULT.setStyleSheet("font-size: 22px; font-weight: 600;")

        dgto_items = self.test_results.get(
                    "DGTO_validation", {}
                ).get("DGTO_miss_list", [])
        
        dgto_scroll = self._create_fail_list(
            dgto_items, self.dgto_checkboxes
        )
        
        self.dgto_layout = QVBoxLayout()
        self.dgto_layout.addWidget(self.selection_DGTO)
        self.dgto_layout.addWidget(dgto_scroll)
        
        faults_not_expected = (
            self.test_results
            .get("FAULT_validation", {})
            .get("fault_data", {})
            .get("Faults_Not_expected", {})
        )

        fault_items = {}

        for fault_id, fault_info in faults_not_expected.items():
            name_list = fault_info.get("Name", [])
            fault_name = name_list[0] if name_list else "UNKNOWN"
            label = f"{fault_id} -> {fault_name}"
            fault_items[label] = fault_id


        fault_scroll = self._create_fail_list(
                    fault_items, self.fault_checkboxes
                )

        self.fault_layout = QVBoxLayout()
        self.fault_layout.addWidget(self.selection_FAULT)
        self.fault_layout.addWidget(fault_scroll)

        self.selection = QHBoxLayout()
        self.selection.addLayout(self.dgto_layout)
        self.selection.addLayout(self.fault_layout)

        self.selection_box = QVBoxLayout()
        self.selection_box.addWidget(self.explanation)
        self.selection_box.addLayout(self.selection)

        # ---- Layouts ----
        result_layout = QVBoxLayout()
        result_layout.addWidget(self.description)


        data_layout = QHBoxLayout()
        data_layout.setSpacing(60)
        data_layout.addLayout(result_layout, stretch=3)
        data_layout.addLayout(self.selection_box, stretch=2)

        # ---- Buttons ----
        self.btn_ok = QPushButton("Update Report")
        self.btn_cancel = QPushButton("Cancel")

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addWidget(self.btn_ok)

        # ---- Main Layout ----
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.title)
        main_layout.addLayout(data_layout)
        main_layout.addLayout(buttons_layout)

        # ---- Connections ----
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
    
    def format_validation_results(self, data: dict) -> str:
        lines = []

        # --- DGTO ---
        dgto = data.get("DGTO_validation", {})
        lines.append("DGTO VALIDATION")
        lines.append(f"Result: {dgto.get('result_test', 'N/A')}")

        miss_list = dgto.get("DGTO_miss_list", [])
        if miss_list:
            lines.append("Missing DGTOs:")
            for item in miss_list:
                lines.append(f"• {item}")
        else:
            lines.append("No missing DGTO detected")

        lines.append("\n--------------------------------\n")

        # --- FAULT ---
        fault = data.get("FAULT_validation", {})
        lines.append("FAULT VALIDATION")
        lines.append(f"Result: {fault.get('result_test', 'N/A')}")

        fault_data = fault.get("fault_data", {})
        if fault_data:
            lines.append("Log Analysis: ")
            for key, value in fault_data.items():
                lines.append(f"• {key}: {value}")

        lines.append("\n--------------------------------\n")

        # --- VERSION ---
        if "VERSION_validation" in data:
            version = data.get("VERSION_validation", {})
            lines.append("VERSION VALIDATION")
            lines.append(f"Result: {version.get('result_test', 'N/A')}")

            versions = version.get("versions", {})
            if versions:
                lines.append("Detected versions:")
                for key, value in versions.items():
                    lines.append(f"• {key}: {value}")

        return "\n".join(lines)
    
    # -------------------------------------------------
    # Results returned to main window
    # -------------------------------------------------
    def get_updated_data(self) -> dict:
        """
        Filters the original test_results dictionary keeping only
        the failures selected by the user.
        """

        # ---------- DGTO ----------
        dgto_validation = self.test_results.get("DGTO_validation", {})
        original_dgto_list = dgto_validation.get("DGTO_miss_list", [])

        selected_dgto = [
            dgto for dgto in original_dgto_list
            if self.dgto_checkboxes.get(dgto) and self.dgto_checkboxes[dgto].isChecked()
        ]

        if selected_dgto:
            dgto_validation["DGTO_miss_list"] = selected_dgto
            dgto_validation["result_test"] = "FAIL"
        else:
            dgto_validation["DGTO_miss_list"] = []
            dgto_validation["result_test"] = "PASS"

        # ---------- FAULT ----------
        fault_validation = self.test_results.get("FAULT_validation", {})
        original_fault_data = fault_validation.get("fault_data", {})
        faults_not_expected = original_fault_data.get("Faults_Not_expected", {})

        selected_faults = {
            fault: data
            for fault, data in faults_not_expected.items()
            if self.fault_checkboxes.get(fault) and self.fault_checkboxes[fault].isChecked()
        }

        fault_validation.setdefault("fault_data", {})
        if selected_faults:
            fault_validation["fault_data"]["Faults_Not_expected"] = selected_faults
            fault_validation["result_test"] = "FAIL"
        else:
            fault_validation["fault_data"]["Faults_Not_expected"] = {}
            fault_validation["result_test"] = "PASS"

        logger.info("Result selection: %s", self.test_results)
        return self.test_results
    
    # =================================================
    # Create scrollable checkbox list
    # =================================================
    def _create_fail_list(self, items_dict, storage_dict):
        container = QWidget()
        layout = QVBoxLayout(container)

        if not items_dict:
            lbl = QLabel("No failures detected ✅")
            lbl.setStyleSheet("color: green;")
            layout.addWidget(lbl)
        else:
            # Accept both dict and iterable of labels
            if isinstance(items_dict, dict):
                iterator = items_dict.items()
            elif isinstance(items_dict, (list, tuple, set)):
                iterator = ((item, item) for item in items_dict)
            else:
                raise TypeError("_create_fail_list expects a dict or iterable of items")

            for label, real_key in iterator:
                cb = QCheckBox(str(label))
                storage_dict[real_key] = cb   # <-- clave REAL (2055)
                layout.addWidget(cb)

        layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)
        return scroll
    # Results returned to main window