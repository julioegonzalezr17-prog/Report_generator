import sys, os
from typing import Dict, Any
from PySide6.QtWidgets import (QSizePolicy, QWidget, QMainWindow, QLabel, QLineEdit, QTextEdit,
                                QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox,
                                QFileDialog, QComboBox, QTableView, QHeaderView, QFrame)
from PySide6.QtGui import QIcon, QStandardItemModel, QStandardItem, QPixmap
from PySide6.QtCore import Qt
import Read_TDM_error
import Read_TDM_report
import TDM_config_load
import Load_configuration_test
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

logger = logging.getLogger(__name__)

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Analysis Setup " + "Version " + sw_version)
        self.setWindowIcon(QIcon(":/info_icon.png"))
        self.setMinimumSize(500, 300)

        # ---- Widgets ----
        # Report configuration
        self.report_config = QLineEdit()
        self.report_config.setPlaceholderText("Select the report config file...")
        self.report_config_browse = QPushButton("Browse")
        self.report_config_browse.clicked.connect(self.on_browse_report_config)
        report_config_row = QHBoxLayout()
        report_config_row.addWidget(self.report_config)
        report_config_row.addWidget(self.report_config_browse)

        # TDM fault file
        self.tdm_error = QLineEdit()
        self.tdm_error.setPlaceholderText("Enter TDM Fault file ...")
        self.tdm_error_browse = QPushButton("Browse")
        self.tdm_error_browse.clicked.connect(self.on_browse_tdm_error)
        tdm_error_row = QHBoxLayout()
        tdm_error_row.addWidget(self.tdm_error)
        tdm_error_row.addWidget(self.tdm_error_browse)

        # TDM config file
        self.tdm_config = QLineEdit()
        self.tdm_config.setPlaceholderText("Enter TDM Config file ...")
        self.tdm_config_browse = QPushButton("Browse")
        self.tdm_config_browse.clicked.connect(self.on_browse_tdm_config)
        tdm_config_row = QHBoxLayout()
        tdm_config_row.addWidget(self.tdm_config)
        tdm_config_row.addWidget(self.tdm_config_browse)

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
        self.tester_name = QLineEdit()
        self.tester_name.setPlaceholderText("Enter your name")
        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Optional notes about this test session...")

        # Buttons
        self.btn_ok = QPushButton("OK")
        self.btn_cancel = QPushButton("Cancel")

        # ---- Layout ----
        form = QFormLayout()
        form.addRow("Report Config*", report_config_row)
        form.addRow("TDM Fault File*", tdm_error_row)
        form.addRow("TDM Config File*", tdm_config_row)
        form.addRow("Report File*", self.report_file_row)
        form.addRow("Machine model", self.combo_machine)
        form.addRow("Inverter model", self.combo_inverter)
        form.addRow("Inverter EEPROM Vxx.Tyy*", self.inverter_EPR)
        form.addRow("Inverter DSP Vxx.Tyy.zz*", self.inverter_DSP)
        form.addRow("Inverter ARM Vxx.Tyy*", self.inverter_ARM)
        form.addRow("Inverter PFC Vxx.Tyy*", self.inverter_PFC)
        form.addRow("Control Board XX.YY.ZZ*", self.CB)
        form.addRow("TDM Version XX.YY.ZZ*", self.TDM)
        form.addRow("Tester Name*", self.tester_name)
        form.addRow("Notes", self.notes)

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
        v.addLayout(buttons_row)
        self.setCentralWidget(container)

        # ---- Signals ----
        self.btn_ok.clicked.connect(self.on_ok_clicked)
        self.btn_cancel.clicked.connect(self.close)

        # Keep a reference to the next window so it's not garbage-collected
        self._analysis_window = None

    # brwose report config File
    def on_browse_report_config(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Report config file",
            "",
            "All Files (*)"
        )
        if file_path:
            self.report_config.setText(file_path)

    # brwose TDM fault File
    def on_browse_tdm_error(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select TDM Error file",
            "",
            "All Files (*)"
        )
        if file_path:
            self.tdm_error.setText(file_path) 

    # brwose TDM config File
    def on_browse_tdm_config(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select TDM Config file",
            "",
            "All Files (*)"
        )
        if file_path:
            self.tdm_config.setText(file_path) 

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
        return {
            "report_config": self.report_config.text().strip(),
            "tdm_error": self.tdm_error.text().strip(),
            "tdm_config": self.tdm_config.text().strip(),
            "report_file": self.report_file.text().strip(),
            "machine_model": self.combo_machine.currentText(),
            "inverter_model": self.combo_inverter.currentText(),
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
            "tester_name": self.tester_name.text().strip(),
            "notes": self.notes.toPlainText().strip()            
        }

    # Validate input data
    def _validate(self, data: Dict[str, Any]) -> bool:
        """
        Basic validation: required fields must not be empty.
        """
        missing = []
        if not data["report_config"]:
            missing.append("Report Config")
        if not data["tdm_error"]:
            missing.append("TDM Error File")
        if not data["tdm_config"]:
            missing.append("TDM Config File")
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

    def on_ok_clicked(self):
        """
        Validate input fields, file type, and load XLSX configuration (if applicable)
        before opening the analysis window.
        """
        data = self._collect_input()
        if not self._validate(data):
            return
        # file validation
        test_config_dict = None
        tdm_config_dict = None
        tdm_fault_dict = None

        for key in ["report_config", "tdm_error", "tdm_config", "report_file"]:
            if not os.path.isfile(data[key]):
                QMessageBox.warning(
                    self,
                    "File not found",
                    f"The file specified for '{key}' does not exist:\n{data[key]}"
                )
                return
            ext = os.path.splitext(data[key])[1].lower()
            if ext not in [".xlsx", ".xls",".csv"]:
                QMessageBox.warning(
                    self,
                    "Invalid file type",
                    f"The file specified for '{key}' must be an Excel or CSV file (.xlsx or .xls or .csv):\n{data[key]}"
                )
                return
        ext = os.path.splitext(data["report_config"])[1].lower()    
        if ext in [".xlsx", ".xls"]:
            test_config_dict = Load_configuration_test.load_test_definition_xlsx(data["report_config"],data["inverter_model"])
        elif ext == ".csv":
            QMessageBox.warning(
                self,
                "Invalid file type",
                f"The file specified for 'report_config' must be an especific Excel file (.xlsx or .xls):\n{data['report_config']}"
            )
            return
        ext = os.path.splitext(data["tdm_error"])[1].lower() 
        if ext in [".xlsx", ".xls"]:
            tdm_fault_dict = Read_TDM_error.load_tdm_once(data["tdm_error"], header_row_default)
        elif ext == ".csv":
            QMessageBox.warning(
                self,
                "Invalid file type",
                f"The file specified for 'tdm_error' must be an especific Excel file (.xlsx or .xls):\n{data['tdm_error']}"
            )
            return
        ext = os.path.splitext(data["tdm_config"])[1].lower()    
        if ext == ".csv":
            tdm_config_dict = TDM_config_load.load_tdm_config(data["tdm_config"])
            print(tdm_config_dict)
        elif ext in [".xlsx", ".xls"]:
            QMessageBox.warning(
                self,
                "Invalid file type",
                f"The file specified for 'tdm_config' must be an especific CSV file (.csv):\n{data['tdm_config']}"
            )
            return
        ext = os.path.splitext(data["report_file"])[1].lower()    
        if not ext == ".xlsx":
            QMessageBox.warning(
                self,
                "Invalid file type",
                f"The file specified for 'report_file' must be an especific XLSX file (.xlsx):\n{data['report_file']}"
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

        test_step_path = str(Path(data["report_config"]).with_suffix(".json"))
        test_analysis_steps = json_motor.create_test_config_json(xlsx_path= data["report_config"],
                                        json_path = test_step_path,
                                        sheet_name = data["inverter_model"],
                                        machine_type = data["machine_model"],
                                        inverter_type = data["inverter_model"]
                                        )
        # Open AnalysisWindow and pass data
        # self._analysis_window = AnalysisWindow(initial_data=data, 
        #                                         test_config_dict=test_config_dict, 
        #                                         tdm_fault_dict=tdm_fault_dict, 
        #                                         tdm_config_dict=tdm_config_dict,
        #                                         test_steps_dic = test_analysis_steps,
        #                                         temp_json_path = test_step_path
        #                                         )
        # self._analysis_window.show()
        self.close()  # Close the start window after opening the analysis window
        # Optionally hide start window (or close it if you want)
        # self.hide()
