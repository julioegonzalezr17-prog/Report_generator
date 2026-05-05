import sys, os
from typing import Dict, Any
from PySide6.QtWidgets import (QSizePolicy, QWidget, QMainWindow, QLabel, QLineEdit, QTextEdit,
                                QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox,
                                QFileDialog, QComboBox, QTableView, QHeaderView, QFrame, QDialog)
from PySide6.QtGui import QIcon, QStandardItemModel, QStandardItem, QPixmap
from PySide6.QtCore import Qt
import fill_RDP_report
import re
from pathlib import Path
from dictDataIntegration import sw_version
import logging

logger = logging.getLogger(__name__)

class UpdateRDP(QDialog):
    def __init__(self):
        super().__init__()
        """
    First window: collects test input data and opens AnalysisWindow.
    """
    def __init__(self, user_input: Dict[str, Any],
                test_summary: Dict[str, Any]):
        super().__init__()

        self.user_input = user_input
        self.test_summary = test_summary
        self.setWindowTitle("RDP automatic report  " + "Version " + sw_version)
        self.setWindowIcon(QIcon(":/info_icon.png"))
        self.setMinimumSize(500, 300)

        # ---- Widgets ----
        # Report configuration
        self.report_config = QLineEdit()
        self.report_config.setPlaceholderText("Select the RDP report...")
        self.report_config_browse = QPushButton("Browse")
        self.report_config_browse.clicked.connect(self.on_browse_report_config)
        report_config_row = QHBoxLayout()
        report_config_row.addWidget(self.report_config)
        report_config_row.addWidget(self.report_config_browse)

        # Buttons
        self.btn_ok = QPushButton("OK")
        self.btn_cancel = QPushButton("Cancel")

        # ---- Layout ----
        form = QFormLayout()
        form.addRow("RDP Report File*", report_config_row)

        # Container buttons
        buttons_row = QHBoxLayout()
        buttons_row.addStretch(1)
        buttons_row.addWidget(self.btn_cancel)
        buttons_row.addWidget(self.btn_ok)

        # Container full sceen

        v = QVBoxLayout(self)
        v.addLayout(form)
        v.addStretch(1)
        v.addLayout(buttons_row)

        # ---- Signals ----
        self.btn_ok.clicked.connect(self.on_ok_clicked)
        self.btn_cancel.clicked.connect(self.close)

    # brwose report config File
    def on_browse_report_config(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select RDP report config file",
            "",
            "All Files (*)"
        )
        if file_path:
            self.report_config.setText(file_path)

    # Collect the data provided by the user in a dict
    def _collect_input(self) -> Dict[str, Any]:
        """
        Gather form data into a dict.
        """
        return {
            "report_config": self.report_config.text().strip()         
        }

    # Validate input data
    def _validate(self, data: Dict[str, Any]) -> bool:
        """
        Basic validation: required fields must not be empty.
        """
        missing = []
        if not data["report_config"]:
            missing.append("Report Config")
        if missing:
            QMessageBox.warning(
                self,
                "Missing required fields",
                "Please fill the following fields:\n- " + "\n- ".join(missing)
            )
            return False
        return True

    def _format_version_value(self, version_value: Any) -> str:
        if isinstance(version_value, (list, tuple)):
            return ".".join([str(v).strip() for v in version_value if str(v).strip()])
        return str(version_value or "")

    def _build_header_data(self) -> Dict[str, str]:
        return {
            "Request by:": self.user_input.get("requester_name", ""),
            "Performed by:": self.user_input.get("tester_name", ""),
            "TDM": self._format_version_value(self.user_input.get("tdm_version", "")),
            "Control Board": self._format_version_value(self.user_input.get("control_board", "")),
            "Inverter fw": self._format_version_value(self.user_input.get("inverter_dsp", "")),
            "Inverter EEPROM":self._format_version_value(self.user_input.get("inverter_eeprom", "")),
            "machine": self._format_machine_value()
        }

    def _format_machine_value(self) -> str:
        machine = str(self.user_input.get("machine_model", "")).strip()
        inverter = str(self.user_input.get("inverter_model", "")).strip()
        return f"{machine} {inverter}".strip()

    def on_ok_clicked(self):
        """
        Validate input fields, file type, and load XLSX configuration (if applicable)
        before opening the analysis window.
        """
        if not self._validate(self._collect_input()):
            return
        template_path = self.report_config.text().strip()
        logger.info("Report RDP file selected: %s", template_path)
        if not os.path.isfile(self.user_input["report_file"]):
            QMessageBox.warning(
                self,
                "File not found",
                f"Report file not found: {self.user_input['report_file']}"
            )
            return
        ext = os.path.splitext(self.user_input["report_file"])[1].lower()
        if ext not in [".xlsx", ".xls",".csv"]:
            QMessageBox.warning(
                self,
                "Invalid file type",
                f"The file must be an Excel or CSV file (.xlsx or .xls or .csv): {ext}"
            )
            return

        data_path = Path(self.user_input["report_file"]).parent
        
        header_data = self._build_header_data()
        
        # Call update_excel_template
        try:
            fill_RDP_report.update_excel_template(
                template_path=template_path,
                output_path=None,
                data_path=str(data_path),
                header_data=header_data,
                tests=self.test_summary
            )
            QMessageBox.information(self, "Success", "RDP report updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update RDP report: {str(e)}")
        
        self.close()
