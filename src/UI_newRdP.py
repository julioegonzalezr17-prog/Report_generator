import sys, os
from typing import Dict, Any
from PySide6.QtWidgets import (QSizePolicy, QWidget, QMainWindow, QLabel, QLineEdit, QTextEdit,
                                QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox,
                                QFileDialog, QComboBox, QTableView, QHeaderView, QFrame, QDialog,
                                QScrollArea, QListWidget, QListWidgetItem)
from PySide6.QtGui import QIcon, QStandardItemModel, QStandardItem, QPixmap
from PySide6.QtCore import Qt
from ExcelStyler import ExcelStyler
from step_engine import StepEngine
import json_motor
import re
from pathlib import Path
import Read_report_file
import resurces_rc
from dictDataIntegration import (inverter, 
                        header_default_table, 
                        header_row_default, 
                        time_data_set,
                        sw_version)
import logging
from pprint import pprint
from openpyxl import load_workbook

import fill_RDP_report


logger = logging.getLogger(__name__)


class StartWindow(QMainWindow):
    """
    First window: collects test input data and opens AnalysisWindow.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Analysis Setup " + "Version " + sw_version)
        self.setWindowIcon(QIcon(":/info_icon.png"))
        self.setMinimumSize(700, 900)
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
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
        self.user_input = {}
        self.test_summary = {}

        # ---- Widgets ----
        # Report configuration
        self.report_config = QLineEdit()
        self.report_config.setPlaceholderText("Select the RDP report...")
        self.report_config_browse = QPushButton("Browse")
        self.report_config_browse.clicked.connect(self.on_browse_report_config)
        report_config_row = QHBoxLayout()
        report_config_row.addWidget(self.report_config)
        report_config_row.addWidget(self.report_config_browse)

        self.report = QLineEdit()
        self.report.setPlaceholderText("Select the test report folder...")
        self.report_browse = QPushButton("Browse")
        self.report_browse.clicked.connect(self.on_browse_report)
        report_row = QHBoxLayout()
        report_row.addWidget(self.report)
        report_row.addWidget(self.report_browse)

        self.report_data = QLineEdit()
        self.report_data.setPlaceholderText("Select the test data folder...")
        self.report_data_browse = QPushButton("Browse")
        self.report_data_browse.clicked.connect(self.on_browse_report_data)
        report_data_row = QHBoxLayout()
        report_data_row.addWidget(self.report_data)
        report_data_row.addWidget(self.report_data_browse)

        # Report to fill
        self.report_file = QLineEdit()
        self.report_file.setPlaceholderText("Enter Report file ...")
        self.report_file_browse = QPushButton("Browse")
        self.report_file_browse.clicked.connect(self.on_browse_report_file)
        self.report_file_row = QHBoxLayout()
        self.report_file_row.addWidget(self.report_file)
        self.report_file_row.addWidget(self.report_file_browse)

        # Machine model
        self.combo_machine = QComboBox()
        self.combo_machine.addItems(list(inverter.keys()))

        # Inverter model
        self.combo_inverter = QComboBox()
        self.combo_inverter.addItems(inverter["Pacman 5"][:])
        self.combo_machine.currentTextChanged.connect(lambda text: self.update_inverter_list(text))
        self.combo_inverter.currentTextChanged.connect(lambda text: self.version_selection(text))

        # TDM model
        self.combo_TDM = QComboBox()
        self.combo_TDM.addItems(["TDM 4", "TDM 3"])

        # EEPROM
        self.inverter_eepromX = QLineEdit()
        self.inverter_eepromX.setPlaceholderText("Vxx")
        self.inverter_eepromX.setEnabled(True)
        self.inverter_eepromY = QLineEdit()
        self.inverter_eepromY.setPlaceholderText("Tyy")
        self.inverter_eepromY.setEnabled(True)
        self.inverter_EPR = QHBoxLayout()
        self.inverter_EPR.addWidget(self.inverter_eepromX)
        self.inverter_EPR.addWidget(self.inverter_eepromY)

        # DSP
        self.inverter_DSPX = QLineEdit()
        self.inverter_DSPX.setPlaceholderText("Vxx")
        self.inverter_DSPX.setEnabled(True)
        self.inverter_DSPY = QLineEdit()
        self.inverter_DSPY.setPlaceholderText("Tyy")
        self.inverter_DSPY.setEnabled(True)
        self.inverter_DSPZ = QLineEdit()
        self.inverter_DSPZ.setPlaceholderText("zz")
        self.inverter_DSPZ.setEnabled(False)
        self.inverter_DSP = QHBoxLayout()
        self.inverter_DSP.addWidget(self.inverter_DSPX)
        self.inverter_DSP.addWidget(self.inverter_DSPY)
        self.inverter_DSP.addWidget(self.inverter_DSPZ)

        # ARM
        self.inverter_ARMX = QLineEdit()
        self.inverter_ARMX.setPlaceholderText("Vxx")
        self.inverter_ARMX.setEnabled(False)
        self.inverter_ARMY = QLineEdit()
        self.inverter_ARMY.setPlaceholderText("Tyy")
        self.inverter_ARMY.setEnabled(False)
        self.inverter_ARM = QHBoxLayout()
        self.inverter_ARM.addWidget(self.inverter_ARMX)
        self.inverter_ARM.addWidget(self.inverter_ARMY)

        # PFC
        self.inverter_PFCX = QLineEdit()
        self.inverter_PFCX.setPlaceholderText("Vxx")
        self.inverter_PFCX.setEnabled(False)
        self.inverter_PFCY = QLineEdit()
        self.inverter_PFCY.setPlaceholderText("Tyy")
        self.inverter_PFCY.setEnabled(False)
        self.inverter_PFC = QHBoxLayout()
        self.inverter_PFC.addWidget(self.inverter_PFCX)
        self.inverter_PFC.addWidget(self.inverter_PFCY)

        # Control BD
        self.CBX = QLineEdit()
        self.CBX.setPlaceholderText("Vxx")
        self.CBX.setEnabled(True)
        self.CBY = QLineEdit()
        self.CBY.setPlaceholderText("Tyy")
        self.CBY.setEnabled(True)
        self.CBZ = QLineEdit()
        self.CBZ.setPlaceholderText("zz")
        self.CBZ.setEnabled(True)
        self.CB = QHBoxLayout()
        self.CB.addWidget(self.CBX)
        self.CB.addWidget(self.CBY)
        self.CB.addWidget(self.CBZ)

        # TDM
        self.TDMX = QLineEdit()
        self.TDMX.setPlaceholderText("Vxx")
        self.TDMY = QLineEdit()
        self.TDMY.setPlaceholderText("Tyy")
        self.TDMZ = QLineEdit()
        self.TDMZ.setPlaceholderText("zz")
        self.TDM = QHBoxLayout()
        self.TDM.addWidget(self.TDMX)
        self.TDM.addWidget(self.TDMY)
        self.TDM.addWidget(self.TDMZ)

        # User Name
        self.rdp_data = QLineEdit()
        self.rdp_data.setPlaceholderText("Enter RDP number ...")
        self.requester_name = QLineEdit()
        self.requester_name.setPlaceholderText("Requested by ...")
        self.tester_name = QLineEdit()
        self.tester_name.setPlaceholderText("Enter your name")

        # ---- Preview area ----
        self.preview_list = QListWidget()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.preview_list)
        self.scroll_area.setMinimumHeight(150)

        # Buttons
        self.btn_ok = QPushButton("OK")
        self.btn_cancel = QPushButton("Cancel")

        # ---- Layout ----
        form = QFormLayout()
        form.addRow("RdP report file*", report_config_row)
        form.addRow("Test report folder*", report_row)
        form.addRow("Test data folder*", report_data_row)
        form.addRow("Test report file*", self.report_file_row)
        form.addRow("Machine model", self.combo_machine)
        form.addRow("Inverter model", self.combo_inverter)
        form.addRow("TDM model", self.combo_TDM)
        form.addRow("Inverter EEPROM Vxx.Tyy*", self.inverter_EPR)
        form.addRow("Inverter DSP Vxx.Tyy.zz*", self.inverter_DSP)
        form.addRow("Inverter ARM Vxx.Tyy*", self.inverter_ARM)
        form.addRow("Inverter PFC Vxx.Tyy*", self.inverter_PFC)
        form.addRow("Control Board XX.YY.ZZ*", self.CB)
        form.addRow("TDM Version XX.YY.ZZ*", self.TDM)
        form.addRow("RDP number*", self.rdp_data)
        form.addRow("Requested By*", self.requester_name)
        form.addRow("Tester Name*", self.tester_name)

        # Container buttons
        buttons_row = QHBoxLayout()
        buttons_row.addStretch(1)
        buttons_row.addWidget(self.btn_cancel)
        buttons_row.addWidget(self.btn_ok)

        # Container full sceen
        container = QWidget()
        v = QVBoxLayout(container)
        v.addLayout(form)
        v.addStretch(1)
        v.addWidget(QLabel("Preview of Tests"))
        v.addWidget(self.scroll_area)
        v.addStretch(1)
        v.addLayout(buttons_row)
        self.setCentralWidget(container)

        # ---- Signals ----
        self.btn_ok.clicked.connect(self.on_ok_clicked)
        self.btn_cancel.clicked.connect(self.close)

    def update_preview(self, tests):
        """
        Llena la lista visual con los tests (preview dinámica)
        """
        self.preview_list.clear()

        for test in tests:
            text = f"Test {test['num']} | {test['notes']} | {test['result']}"
            
            item = QListWidgetItem(text)

            # Color según resultado
            if test["result"] == "PASS":
                item.setBackground(Qt.green)
            elif test["result"] == "FAIL":
                item.setBackground(Qt.red)
            else:
                item.setBackground(Qt.lightGray)

            self.preview_list.addItem(item)

    def on_browse_report(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Test report folder",
            ""  # ruta inicial opcional
        )

        if folder_path:
            self.report.setText(folder_path)

    def on_browse_report_data(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Test data folder",
            ""  # ruta inicial opcional
        )

        if folder_path:
            self.report_data.setText(folder_path)


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

    # brwose report  File
    def on_browse_report_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select report file",
            "",
            "All Files (*)"
        )
        if file_path:
            self.report_file.setText(file_path)
            self.test_summary = self.build_tests_from_excel(file_path)
            self.update_preview(self.test_summary)
    # Update inverter list considering machine model
    def update_inverter_list(self, machine_model):
        self.combo_inverter.clear()
        self.combo_inverter.addItems(inverter.get(machine_model, []))

    # Input data validation
    def version_selection(self,inverter_model):
        match inverter_model:
            case "ID1PH_R290":        
                self.inverter_eepromX.setPlaceholderText("Vxx")
                self.inverter_eepromX.clear()
                self.inverter_eepromX.setEnabled(True) 
                self.inverter_eepromY.setPlaceholderText("Tyy")
                self.inverter_eepromY.clear()
                self.inverter_eepromY.setEnabled(True) 
                self.inverter_DSPX.setPlaceholderText("Vxx")
                self.inverter_DSPX.clear()
                self.inverter_DSPX.setEnabled(True)
                self.inverter_DSPY.setPlaceholderText("Tyy")
                self.inverter_DSPY.clear()
                self.inverter_DSPY.setEnabled(True)
                self.inverter_DSPZ.setPlaceholderText("zz")
                self.inverter_DSPZ.clear() 
                self.inverter_DSPZ.setEnabled(False)
                self.inverter_ARMX.setPlaceholderText("Vxx")
                self.inverter_ARMX.clear()
                self.inverter_ARMX.setEnabled(True)
                self.inverter_ARMY.setPlaceholderText("Tyy")
                self.inverter_ARMY.clear()
                self.inverter_ARMY.setEnabled(True)
                self.inverter_PFCX.setPlaceholderText("Vxx")
                self.inverter_PFCX.clear()
                self.inverter_PFCX.setEnabled(False)
                self.inverter_PFCY.setPlaceholderText("Tyy")
                self.inverter_PFCY.clear()
                self.inverter_PFCY.setEnabled(False)
                self.CBX.setPlaceholderText("Vxx")
                self.CBX.clear()
                self.CBX.setEnabled(False)
                self.CBY.setPlaceholderText("Tyy")
                self.CBY.clear()
                self.CBY.setEnabled(False)
                self.CBZ.setPlaceholderText("zz")
                self.CBZ.clear()
                self.CBZ.setEnabled(False)
            case "Ariston":       
                self.inverter_eepromX.setPlaceholderText("Vxx")
                self.inverter_eepromX.clear()
                self.inverter_eepromX.setEnabled(False) 
                self.inverter_eepromY.setPlaceholderText("Tyy")
                self.inverter_eepromY.clear()
                self.inverter_eepromY.setEnabled(False) 
                self.inverter_DSPX.setPlaceholderText("Vxx")
                self.inverter_DSPX.clear()
                self.inverter_DSPX.setEnabled(True)
                self.inverter_DSPY.setPlaceholderText("Tyy")
                self.inverter_DSPY.clear()
                self.inverter_DSPY.setEnabled(True)
                self.inverter_DSPZ.setPlaceholderText("zz") 
                self.inverter_DSPZ.clear() 
                self.inverter_DSPZ.setEnabled(True)
                self.inverter_ARMX.setPlaceholderText("Vxx")
                self.inverter_ARMX.clear()
                self.inverter_ARMX.setEnabled(False)
                self.inverter_ARMY.setPlaceholderText("Tyy")
                self.inverter_ARMY.clear()
                self.inverter_ARMY.setEnabled(False)
                self.inverter_PFCX.setPlaceholderText("Vxx")
                self.inverter_PFCX.clear()
                self.inverter_PFCX.setEnabled(False)
                self.inverter_PFCY.setPlaceholderText("Tyy")
                self.inverter_PFCY.clear()
                self.inverter_PFCY.setEnabled(False)
                self.CBX.setPlaceholderText("Vxx")
                self.CBX.clear()
                self.CBX.setEnabled(True)
                self.CBY.setPlaceholderText("Tyy")
                self.CBY.clear()
                self.CBY.setEnabled(True)
                self.CBZ.setPlaceholderText("zz")
                self.CBZ.clear()
                self.CBZ.setEnabled(True)
            case "RD4018":
                self.inverter_eepromX.setPlaceholderText("Vxx")
                self.inverter_eepromX.clear()
                self.inverter_eepromX.setEnabled(True) 
                self.inverter_eepromY.setPlaceholderText("Tyy")
                self.inverter_eepromY.clear()
                self.inverter_eepromY.setEnabled(True) 
                self.inverter_DSPX.setPlaceholderText("Vxx")
                self.inverter_DSPX.clear()
                self.inverter_DSPX.setEnabled(True)
                self.inverter_DSPY.setPlaceholderText("Tyy")
                self.inverter_DSPY.clear()
                self.inverter_DSPY.setEnabled(True)
                self.inverter_DSPZ.setPlaceholderText("zz")
                self.inverter_DSPZ.clear() 
                self.inverter_DSPZ.setEnabled(False)
                self.inverter_ARMX.setPlaceholderText("Vxx")
                self.inverter_ARMX.clear()
                self.inverter_ARMX.setEnabled(False)
                self.inverter_ARMY.setPlaceholderText("Tyy")
                self.inverter_ARMY.clear()
                self.inverter_ARMY.setEnabled(False)
                self.inverter_PFCX.setPlaceholderText("Vxx")
                self.inverter_PFCX.clear()
                self.inverter_PFCX.setEnabled(True)
                self.inverter_PFCY.setPlaceholderText("Tyy")
                self.inverter_PFCY.clear()
                self.inverter_PFCY.setEnabled(True)
                self.CBX.setPlaceholderText("Vxx")
                self.CBX.clear()
                self.CBX.setEnabled(True)                
                self.CBY.setPlaceholderText("Tyy")
                self.CBY.clear()
                self.CBY.setEnabled(True)
                self.CBZ.setPlaceholderText("zz")
                self.CBZ.clear()
                self.CBZ.setEnabled(True)
            case _:
                self.inverter_eepromX.setPlaceholderText("Vxx")
                self.inverter_eepromX.clear()
                self.inverter_eepromX.setEnabled(True) 
                self.inverter_eepromY.setPlaceholderText("Tyy")
                self.inverter_eepromY.clear()
                self.inverter_eepromY.setEnabled(True) 
                self.inverter_DSPX.setPlaceholderText("Vxx")
                self.inverter_DSPX.clear()
                self.inverter_DSPX.setEnabled(True)
                self.inverter_DSPY.setPlaceholderText("Tyy")
                self.inverter_DSPY.clear()
                self.inverter_DSPY.setEnabled(True)
                self.inverter_DSPZ.setPlaceholderText("zz") 
                self.inverter_DSPZ.clear()
                self.inverter_DSPZ.setEnabled(False)
                self.inverter_ARMX.setPlaceholderText("Vxx")
                self.inverter_ARMX.clear()
                self.inverter_ARMX.setEnabled(False)
                self.inverter_ARMY.setPlaceholderText("Tyy")
                self.inverter_ARMY.clear()
                self.inverter_ARMY.setEnabled(False)
                self.inverter_PFCX.setPlaceholderText("Vxx")
                self.inverter_PFCX.clear()
                self.inverter_PFCX.setEnabled(False)
                self.inverter_PFCY.setPlaceholderText("Tyy")
                self.inverter_PFCY.clear()
                self.inverter_PFCY.setEnabled(False)
                self.CBX.setPlaceholderText("Vxx")
                self.CBX.clear()
                self.CBX.setEnabled(True)
                self.CBY.setPlaceholderText("Tyy")
                self.CBY.clear()
                self.CBY.setEnabled(True)
                self.CBZ.setPlaceholderText("zz")
                self.CBZ.clear()
                self.CBZ.setEnabled(True)

    # Collect the data provided by the user in a dict
    def _collect_input(self) -> Dict[str, Any]:
        """
        Gather form data into a dict.
        """
        self.user_input = {
            "report_config": self.report_config.text().strip(),
            "test_report": self.report.text().strip(),
            "test_data": self.report_data.text().strip(),
            "report_file": self.report_file.text().strip(),
            "machine_model": self.combo_machine.currentText(),
            "inverter_model": self.combo_inverter.currentText(),
            "tdm_model": self.combo_TDM.currentText(),
            "inverter_eeprom": [self.inverter_eepromX.text().strip(),
                                self.inverter_eepromY.text().strip()],
            "inverter_dsp": [self.inverter_DSPX.text().strip(),
                            self.inverter_DSPY.text().strip(),
                            self.inverter_DSPZ.text().strip()],
            "inverter_arm":[self.inverter_ARMX.text().strip(),
                            self.inverter_ARMY.text().strip()],
            "inverter_pfc": [self.inverter_PFCX.text().strip(),
                            self.inverter_PFCY.text().strip()],                 
            "control_board": [self.CBX.text().strip(),
                            self.CBY.text().strip(),
                            self.CBZ.text().strip()],
            "tdm_version": [self.TDMX.text().strip(),
                            self.TDMY.text().strip(),
                            self.TDMZ.text().strip()],
            "rdp_number": self.rdp_data.text().strip(),
            "requester_name": self.requester_name.text().strip(),
            "tester_name": self.tester_name.text().strip()          
        }
        return self.user_input

    # Validate input data
    def _validate(self, data: Dict[str, Any]) -> bool:
        """
        Basic validation: required fields must not be empty.
        """
        missing = []
        if not data["report_config"]:
            missing.append("Report Config")
        if not data["test_report"]:
            missing.append("Test report folder")
        if not data["test_data"]:
            missing.append("Test data folder")
        if not data["report_file"]:
            missing.append("Report File")
        for i in range(self.inverter_EPR.count()):
            item = self.inverter_EPR.itemAt(i)
            if item is None:
                continue
            element = item.widget()
            if element is None:
                continue
            if element.isEnabled():
                if not data["inverter_eeprom"][i]:
                    missing.append("Inverter EEPROM")
        for i in range(self.inverter_DSP.count()):
            item = self.inverter_DSP.itemAt(i)
            if item is None:
                continue
            element = item.widget()
            if element is None:
                continue
            if element.isEnabled():
                if not data["inverter_dsp"][i]:
                    missing.append("Inverter DSP")
        for i in range(self.inverter_ARM.count()):
            item = self.inverter_ARM.itemAt(i)
            if item is None:
                continue
            element = item.widget()
            if element is None:
                continue
            if element.isEnabled():
                if not data["inverter_arm"][i]:
                    missing.append("Inverter ARM")
        for i in range(self.inverter_PFC.count()):
            item = self.inverter_PFC.itemAt(i)
            if item is None:
                continue
            element = item.widget()
            if element is None:
                continue
            if element.isEnabled():
                if not data["inverter_pfc"][i]:
                    missing.append("Inverter PFC")            
        for i in range(self.CB.count()):
            item = self.CB.itemAt(i)
            if item is None:
                continue
            element = item.widget()
            if element is None:
                continue
            if element.isEnabled():
                if not data["control_board"][i]:
                    missing.append("Control Board") 
        for i in range(self.TDM.count()):
            item = self.TDM.itemAt(i)
            if item is None:
                continue
            element = item.widget()
            if element is None:
                continue
            if element.isEnabled():
                if not data["tdm_version"][i]:
                    missing.append("TDM Version")
        if not data["rdp_number"]:
            missing.append("RDP Number")
        if not data["requester_name"]:
            missing.append("Requester Name")
        if not data["tester_name"]:
            missing.append("Tester Name")
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

    def _format_machine_value(self) -> str:
        machine = str(self.user_input.get("machine_model", "")).strip()
        inverter = str(self.user_input.get("inverter_model", "")).strip()
        return f"{machine} {inverter}".strip()
    
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

    def on_ok_clicked(self):
        """
        Validate input fields, file type, and load XLSX configuration (if applicable)
        before opening the analysis window.
        """
        data = self._collect_input()
        if not self._validate(data):
            return
        # file validation
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
        for i in range(self.inverter_EPR.count()):
            item = self.inverter_EPR.itemAt(i)
            if item is None:
                continue
            element = item.widget()
            if element is None:
                continue
            if element.isEnabled():
                if not data["inverter_eeprom"][i].isdigit():
                    
                    if isinstance(element, QLineEdit):
                        element.clear()

                    elif isinstance(element, QLabel):
                        element.setText("")

                    QMessageBox.warning(
                    self,
                    "Invalid data type",
                    f"Eeprom version must be a numeric value"
                    )
                    return
        
        for i in range(self.inverter_DSP.count()):
            item = self.inverter_DSP.itemAt(i)
            if item is None:
                continue
            element = item.widget()
            if element is None:
                continue
            if element.isEnabled():
                if not data["inverter_dsp"][i].isdigit():
                    if isinstance(element, QLineEdit):
                        element.clear()

                    elif isinstance(element, QLabel):
                        element.setText("")
                    QMessageBox.warning(
                    self,
                    "Invalid data type",
                    f"DSP version must be a numeric value"
                    )
                    return

        for i in range(self.inverter_ARM.count()):
            item = self.inverter_ARM.itemAt(i)
            if item is None:
                continue
            element = item.widget()
            if element is None:
                continue
            if element.isEnabled():
                if not data["inverter_arm"][i].isdigit():
                    if isinstance(element, QLineEdit):
                        element.clear()

                    elif isinstance(element, QLabel):
                        element.setText("")
                    QMessageBox.warning(
                    self,
                    "Invalid data type",
                    f"ARM version must be a numeric value"
                    )
                    return

        for i in range(self.inverter_PFC.count()):
            item = self.inverter_PFC.itemAt(i)
            if item is None:
                continue
            element = item.widget()
            if element is None:
                continue
            if element.isEnabled():
                if not data["inverter_pfc"][i].isdigit():
                    if isinstance(element, QLineEdit):
                        element.clear()

                    elif isinstance(element, QLabel):
                        element.setText("")
                    QMessageBox.warning(
                    self,
                    "Invalid data type",
                    f"PFC version must be a numeric value"
                    )
                    return
                
        for i in range(self.CB.count()):
            item = self.CB.itemAt(i)
            if item is None:
                continue
            element = item.widget()
            if element is None:
                continue
            if element.isEnabled():
                if not data["control_board"][i].isdigit():
                    if isinstance(element, QLineEdit):
                        element.clear()

                    elif isinstance(element, QLabel):
                        element.setText("")
                    QMessageBox.warning(
                    self,
                    "Invalid data type",
                    f"Control Board version must be a numeric value"
                    )
                    return

        for i in range(self.TDM.count()):
            item = self.TDM.itemAt(i)
            if item is None:
                continue
            element = item.widget()
            if element is None:
                continue
            if element.isEnabled():
                if not data["tdm_version"][i].isdigit():
                    if isinstance(element, QLineEdit):
                        element.clear()

                    elif isinstance(element, QLabel):
                        element.setText("")
                    QMessageBox.warning(
                    self,
                    "Invalid data type",
                    f"TDM version must be a numeric value"
                    )
                    return
        
        header_data = self._build_header_data()
        self.test_summary = self.build_tests_from_excel(self.user_input["report_file"])

                # Call update_excel_template
        try:
            self.rdp_path = template_path
            fill_RDP_report.update_excel_template(
                template_path=template_path,
                output_path=None,
                data_path=self.report_data.text().strip(),
                test_path =self.report.text().strip(), 
                header_data=header_data,
                tests=self.test_summary
            )
            QMessageBox.information(self, "Success", "RDP report updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update RDP report: {str(e)}")
        
        self.close()  # Close the start window after opening the analysis window
        # Optionally hide start window (or close it if you want)
        # self.hide()

    def build_tests_from_excel(self, excel_path):
        """
        Lee el Excel y devuelve la lista `tests` con la misma estructura
        que ya usabas en tu código.
        """

        wb = load_workbook(excel_path, data_only=True)
        ws = wb.active

        # -------------------------
        # Detectar columnas
        # -------------------------
        headers = {}
        header_row = None

        for row in ws.iter_rows(min_row=1, max_row=20):
            for cell in row:
                if cell.value:
                    headers[str(cell.value).strip()] = cell.column

            if "Test N°" in headers and "Analysis" in headers:
                header_row = cell.row
                break

        if header_row is None:
            logger.info("No headers in report")
            raise ValueError("No se encontraron las columnas esperadas")

        # -------------------------
        # Función para evaluar resultado
        # -------------------------
        def get_result_from_analysis(analysis):
            if not analysis:
                return "FAIL"

            text = str(analysis).upper()

            # regla: si hay al menos un FAIL → FAIL
            if "FAIL" in text:
                return "FAIL"

            if "PASS" in text:
                return "PASS"

            return "FAIL"

        # -------------------------
        # Construcción de tests
        # -------------------------
        tests = []

        for row in ws.iter_rows(min_row=header_row + 1):

            test_num = row[headers["Test N°"] - 1].value
            if test_num == "N/A" or test_num == "n/a":
                continue

            # ignorar filas vacías
            if test_num is None:
                continue

            test_desc = ""
            if "Test Env" in headers:
                test_desc = row[headers["Test Env"] - 1].value or ""

            test_notes = ""
            if "Test scope" in headers:
                test_notes = row[headers["Test scope"] - 1].value or ""

            analysis = row[headers["Analysis"] - 1].value
            test_result = get_result_from_analysis(analysis)

            tests.append({
                "num": test_num,
                "desc": test_desc,
                "notes": test_notes,
                "result": test_result
            })

        return tests