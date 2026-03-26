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


def resource_path(relative_path):
    """Devuelve la ruta válida para PyInstaller o en modo normal."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def _format_cell_value(value: Any) -> str:
        """
        Convert the provided value into a string suitable for display in a table cell.
        - If value is a string containing ';', split and join with new lines.
        - If value is list/tuple, join with new lines.
        - None -> ''.
        - Others -> str(value).
        """
        if value is None:
            return ""
        if isinstance(value, str):
            # Split on semicolons and trim parts
            parts = [p.strip() for p in value.split(';')]
            return "\n".join([p for p in parts if p != ""])
        if isinstance(value, (list, tuple)):
            return "\n".join(_format_cell_value(v) for v in value)
        return str(value)

class StartWindow(QMainWindow):
    """
    First window: collects test input data and opens AnalysisWindow.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Analysis Setup " + "Version " + sw_version)
        self.setWindowIcon(QIcon(":/iconos/info_icon.png"))
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
            "Select REport config file",
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
        self._analysis_window = AnalysisWindow(initial_data=data, 
                                                test_config_dict=test_config_dict, 
                                                tdm_fault_dict=tdm_fault_dict, 
                                                tdm_config_dict=tdm_config_dict,
                                                test_steps_dic = test_analysis_steps,
                                                temp_json_path = test_step_path
                                                )
        self._analysis_window.show()
        self.close()  # Close the start window after opening the analysis window
        # Optionally hide start window (or close it if you want)
        # self.hide()

class AnalysisWindow(QMainWindow):
    """
    Second window: analysis start screen, receives the data from StartWindow.
    """
    def __init__(self, initial_data: Dict[str, Any], 
                test_config_dict: Dict[str, Any], 
                tdm_fault_dict: Dict[str, Any], 
                tdm_config_dict: Dict[str, Any],
                test_steps_dic: Dict[str, Any],
                temp_json_path: str
                ):
        super().__init__()
        self.Analysis  = {"1":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation,
                            "VERSION": self.Version_SW_validation},
                        "2":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "3":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "4":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "5":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "6":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "7":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "8":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "9":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "10":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "11":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "12":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "13":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "14":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "14":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "15":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "16":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "17":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "18":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "19":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "20":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "21":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "22":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "23":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "24":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "25":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "26":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "27":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "28":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "29":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "30":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "31":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "32":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation},
                        "33":{"DGTO": self.DGTO_validation,
                            "FAULT": self.Fault_code_validation}
                    }
        self.user_data = initial_data
        self.temp_json_path = temp_json_path
        self.setWindowTitle("Test Analysis " + "Version " + sw_version)
        self.setWindowIcon(QIcon(":/iconos/monitoring.png"))
        self.setMinimumSize(700, 400)

        img_label = QLabel()
        pix = QPixmap(":/iconos/Ariston_logo.png")  # JPG, PNG, etc.
        img_label.setPixmap(pix.scaled(img_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        img_label.setScaledContents(True) 
        img_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        img_label.setMaximumSize(400, 100)  # Limit max size to prevent it from dominating the layout

        # ---- Widgets ----
        frame = QFrame()
        frame.setFrameShadow(QFrame.Raised)
        frame.setFrameShape(QFrame.Panel)        
        frame.setLineWidth(2)   
        frame.setStyleSheet("""
            QFrame {
                background-color: #fafafa;
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 8px;
            }
        """)
        title = QLabel("Test Analysis Console")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 40px; font-weight: 600;")        
        frame_layout = QHBoxLayout(frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        frame_layout.addWidget(title)   

        # ---- Center layout with frame and image side by side ----
        center_layout = QHBoxLayout()      
        center_layout.addStretch()
        center_layout.addWidget(frame) 
        center_layout.addStretch()
        center_layout.addWidget(img_label)  

        # Table View
        self.table = QTableView()
        self.table_model = QStandardItemModel()
        self.table.setModel(self.table_model)        
        self.table.setAlternatingRowColors(True)        
        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.verticalHeader().setMinimumSectionSize(50)

        # ---- Info labels at the top ----
        info = QLabel(self._format_initial_data(initial_data))
        info.setStyleSheet("font-size: 15px; font-weight: 600;")
        info.setTextInteractionFlags(Qt.TextSelectableByMouse)
        info_state = QLabel()
        info_state.setText("Waiting for files to analyse...")
        info_state.setStyleSheet("font-size: 15px; font-weight: 600;")
        info_state.setTextInteractionFlags(Qt.TextSelectableByMouse)

        info_logo = QHBoxLayout()
        info_logo.addWidget(info)
        info_logo.addStretch()
        info_logo.addWidget(info_state)

        # ---- Layout ----
        container = QWidget()
        v = QVBoxLayout(container)        
        v.setSpacing(0)
        v.setContentsMargins(10, 10, 10, 10)
        v.addLayout(center_layout)        
        v.addLayout(info_logo)
        v.addSpacing(12)
        v.addWidget(self.table)    
        self.setCentralWidget(container)
        self.load_dict_config_to_table(initial_data, test_config_dict)
        if self.user_data["machine_model"] == "Pacman 5":
            self.fill_column_by_header(["TDM LOG FILE","MODBUS LOG FILE"]) 
        else:
            self.fill_column_by_header(["TDM LOG FILE","LIN LOG FILE","MODBUS LOG FILE"])         
        self.fill_action_column("TEST RESULT", info_state, tdm_fault_dict, tdm_config_dict, test_steps_dic) # Example: connect the button in row 1, column 1 to the click handler


    def create_path_selector_cell(self)-> QWidget:
            new_container = QWidget()    
            layout = QHBoxLayout(new_container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(2)
            line = QLineEdit()
            line.setReadOnly(True)
            line.setPlaceholderText("Select file...")
            line.setStyleSheet("font-size: 12px; padding: 1px;")
            btn = QPushButton("Browse")
            btn.setFixedWidth(100)

            def browse():
                path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
                if path:
                    line.setText(path)
            btn.clicked.connect(browse)
            layout.addWidget(line)
            layout.addWidget(btn)

            new_container._text_path = line # Store reference to line edit for later retrieval
            return new_container
    ###############################
    #  function Analyse buttons
    ###############################
    def create_action_cell(self, row: int,
                            info_text: QLabel,
                            tdm_fault_data: Dict[str, Any],
                            tdm_config_data: Dict[str, Any],
                            test_steps: Dict[str, Any]) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        btn = QPushButton("Analyse Data")
        btn.setFixedWidth(100)
        btn.setStyleSheet("font-size: 12px; padding: 1px;")
        img = QLabel()
        img.setVisible(False)               # ← hiden by default, shown when clicked
        img.setScaledContents(False)
        img.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        img.setFixedWidth(20)
        layout.addWidget(btn, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(img, alignment=Qt.AlignVCenter)
        layout.addStretch(1)
        # Save references to the button and image in the container for later access
        container._cell_button = btn
        container._cell_image = img
        def on_click():
            pos = btn.mapTo(self.table.viewport(), btn.rect().center())
            index = self.table.indexAt(pos)
            loading_text = "Validating input data..."
            self.write_loaging_data(info_text, loading_text)
            if self.user_data["machine_model"] == "Pacman 5":
                path_index = self.table_model.index(row, self.get_column_index("TDM LOG FILE"))
                path_widget = self.table.indexWidget(path_index)    
                path_index_mod = self.table_model.index(row, self.get_column_index("MODBUS LOG FILE"))
                path_widget_mod = self.table.indexWidget(path_index_mod)
                path_widget_lin = None
                if not path_widget or not path_widget_mod:
                    info_text.setStyleSheet("font-size: 15px; font-weight: 600; color: red;")
                    info_text.setText("ERROR: no widget for data log found")
                    return            
                path_line = getattr(path_widget, "_text_path", None)
                path_mod = getattr(path_widget_mod, "_text_path", None)
                if  path_line.text().strip() == "" or path_mod.text().strip() == "" or not path_line.text().lower().endswith(".csv"):
                    info_text.setStyleSheet("font-size: 15px; font-weight: 600; color: red;")
                    info_text.setText("ERROR: NO data to analyse !!!!")
                    return
                else:
                    info_text.setStyleSheet("font-size: 15px; font-weight: 600; color: green;")
                    info_text.setText("Loading data and executing analysis...")
            else:
                path_index = self.table_model.index(row, self.get_column_index("TDM LOG FILE"))
                path_widget = self.table.indexWidget(path_index)    
                path_index_mod = self.table_model.index(row, self.get_column_index("MODBUS LOG FILE"))
                path_widget_mod = self.table.indexWidget(path_index_mod)
                path_index_lin = self.table_model.index(row, self.get_column_index("LIN LOG FILE"))
                path_widget_lin = self.table.indexWidget(path_index_lin)
                if not path_widget or not path_widget_mod or not path_widget_lin:
                    info_text.setStyleSheet("font-size: 15px; font-weight: 600; color: red;")
                    info_text.setText("ERROR: no widget for data log found")
                    return            
                path_line = getattr(path_widget, "_text_path", None)
                path_mod = getattr(path_widget_mod, "_text_path", None)
                path_lin = getattr(path_widget_lin, "_text_path", None)
                if  path_line.text().strip() == "" or path_mod.text().strip() == "" or path_lin.text().strip() == "":
                    info_text.setStyleSheet("font-size: 15px; font-weight: 600; color: red;")
                    info_text.setText("ERROR: NO data to analyse !!!!")
                    return
                else:
                    info_text.setStyleSheet("font-size: 15px; font-weight: 600; color: green;")
                    info_text.setText("Loading data and executing analysis...")                


            # execute the analysis function, passing the path widget and info label for updates
            test_result = self.click_action_analyse(Index = index,
                                                    container_path=path_widget,
                                                    container_mod = path_widget_mod,
                                                    container_lin = path_widget_lin,
                                                    info_text=info_text,
                                                    tdm_fault_data=tdm_fault_data,
                                                    tdm_config_data=tdm_config_data,
                                                    step_dic = test_steps
                                                    )
            def eval_result(relult_list)-> bool:
                for data in relult_list:
                    if data == "FAIL":
                        return False
                return True
            container._cell_image.setVisible(True)
            image_state = False
            pixmap_ok = QPixmap(":/iconos/check.png")  
            pixmap_fail = QPixmap(":/iconos/multiply.png")
            icon_h = 30
            scaled_ok = pixmap_ok.scaledToHeight(icon_h, Qt.SmoothTransformation)
            scaled_fail = pixmap_fail.scaledToHeight(icon_h, Qt.SmoothTransformation)
        
            lista_result_test = [
                value["result_test"]
                for value in test_result.values()
                if isinstance(value, dict) and "result_test" in value
            ]
            image_state = eval_result(lista_result_test)
            if image_state:
                container._cell_image.setPixmap(scaled_ok)
                container._cell_image.setFixedSize(scaled_ok.size())
            else:
                container._cell_image.setPixmap(scaled_fail)
                container._cell_image.setFixedSize(scaled_fail.size())


        btn.clicked.connect(on_click)   
        return container
    
    def DGTO_validation(self, data) -> dict:
        """
        Validates the given DGTO value against the TDM configuration data.
        Returns a tuple of (is_valid, DGTO_name).
        """
        # Read the DGTO value from the container_path's line edit  
        report_data = data["report"]
        tdm_config_data = data["tdm"]     
        result_test = "FAIL"
        DGTO_miss_list = []
        inner = next(iter(tdm_config_data.values()))["name_DGTO"]  # Get the "name_DGTO" list from the first (and only) inner dict
        df_headers = set(report_data.columns)
        dict_keys = set(inner)
        missing_in_report = df_headers- dict_keys            
        DGTO_miss_list = list(missing_in_report-set(time_data_set))
        if DGTO_miss_list == []:
            result_test = "PASS"
        else: 
            result_test = "FAIL"
        out_data = {"result_test": result_test, 
                    "DGTO_miss_list": DGTO_miss_list}
        return out_data
    def Fault_code_validation(self, data)->dict:
        engine = data["engine"]
        result_data = engine.execute()
        if "Faults_Not_expected" not in result_data or not result_data["Faults_Not_expected"]:
            result_test = "PASS"
        else:
            result_test = "FAIL"
        out_data = {"result_test": result_test, 
                    "fault_data": result_data}
        return out_data

    def Version_SW_validation(self, data):
        versions_read = data["versions"]
        step_dic = data["step_dic"]
        user_data = data["user_data"]
        result_test = False
        result_data = {}
        eeprom_check = False
        dsp_check = False
        arm_check = False
        pfc_check = False

        def get_column_for_action(steps, action_name):
            for step in steps:
                if step.get("action") == action_name:
                    return step.get("column")
            return None
        
        def extract_v_t(codigo: str):
            """
            'V01_T01' y returns (V, T) como int.
            """
            patron = r"V(\d+)_T(\d+)"
            match = re.match(patron, codigo)

            if not match:
                v = 0
                t = 0

            v = int(match.group(1))
            t = int(match.group(2))
            return v, t

        version_data_list = get_column_for_action(step_dic["tests"]["1"]["steps"], "validate_version")
        if not isinstance(version_data_list, list):
            version_data_list = [version_data_list]
        version_data_norm =[]    
        for ver in version_data_list:
            version_data_norm.append(self.normalize_name(ver))          

        if user_data["inverter_model"] == "RD4021":    
            if "EEPROM VERSION EK RD" in version_data_norm:
                x, y = extract_v_t(versions_read["fault_data"]["EEPROM VERSION EK RD"])
                if int(user_data["inverter_eeprom"][0]) == x and int(user_data["inverter_eeprom"][1]) == y:
                    eeprom_check = True
                else: 
                    eeprom_check = False 
                result_data = {"Eeprom": versions_read["fault_data"]["EEPROM VERSION EK RD"]}        
            if "DSP MAIN VERSION ECOKING" in version_data_norm:
                x, y = extract_v_t(versions_read["fault_data"]["DSP MAIN VERSION ECOKING"])
                if int(user_data["inverter_dsp"][0]) == x and int(user_data["inverter_dsp"][1]) == y:
                    dsp_check = True
                else: 
                    dsp_check = False
                result_data["DSP"] = versions_read["fault_data"]["DSP MAIN VERSION ECOKING"]        
            else:
                result_test = "FAIL" 
            if eeprom_check and dsp_check:
                result_test = "PASS" 
            else:
                result_test = "FAIL" 
            out_data = {"result_test": result_test, 
                        "versions": result_data}                    

        elif user_data["inverter_model"] == "ID1PH_R290":
            if "EEPROM VERSION EK RD" in version_data_norm:
                x, y = extract_v_t(versions_read["fault_data"]["EEPROM VERSION EK RD"])
                if int(user_data["inverter_eeprom"][0]) == x and int(user_data["inverter_eeprom"][1]) == y:
                    eeprom_check = True                   
                else: 
                    eeprom_check = False 
                result_data = {"Eeprom": versions_read["fault_data"]["EEPROM VERSION EK RD"]}
            if "DSP MAIN VERSION ECOKING" in version_data_norm:
                x, y = extract_v_t(versions_read["fault_data"]["DSP MAIN VERSION ECOKING"])
                if int(user_data["inverter_dsp"][0]) == x and int(user_data["inverter_dsp"][1]) == y:
                    dsp_check = True                    
                else: 
                    dsp_check = False
                result_data["DSP"] = versions_read["fault_data"]["DSP MAIN VERSION ECOKING"]   
            if "HW VERSION ECOKING" in version_data_norm:
                x, y = extract_v_t(versions_read["fault_data"]["HW VERSION ECOKING"])
                if int(user_data["inverter_arm"][0]) == x and int(user_data["inverter_arm"][1]) == y:
                    arm_check = True                   
                else: 
                    arm_check = False
                result_data["ARM"] =  versions_read["fault_data"]["HW VERSION ECOKING"]
            else:
                result_test = "FAIL" 
            if eeprom_check and dsp_check and arm_check:
                result_test = "PASS" 
            else:
                result_test = "FAIL" 
            out_data = {"result_test": result_test, 
                        "versions": result_data} 

        elif user_data["inverter_model"] == "Ariston":
            if "DSP MAIN VERSION ECOKING" in version_data_norm and "PB DSP FW2" in version_data_norm:
                x, y = extract_v_t(versions_read["fault_data"]["DSP MAIN VERSION ECOKING"])
                z = int(versions_read["fault_data"]["PB DSP FW2"])
                if int(user_data["inverter_dsp"][0]) == x and int(user_data["inverter_dsp"][1]) == y and user_data["inverter_dsp"][2] == z:
                    dsp_check = True                   
                else: 
                    dsp_check = False
                result_data["DSP"] = f"V{x}.{y}.{z}"    
            else:
                result_test = "FAIL" 
            if dsp_check:
                result_test = "PASS"
            else:
                result_test = "FAIL"
            out_data = {"result_test": result_test, 
                        "versions": result_data} 

        elif user_data["inverter_model"] == "RD4018":  
            if "EEPROM VERSION EK RD" in version_data_norm:
                x, y = extract_v_t(versions_read["fault_data"]["EEPROM VERSION EK RD"])
                if int(user_data["inverter_eeprom"][0]) == x and int(user_data["inverter_eeprom"][1]) == y:
                    eeprom_check = True                   
                else: 
                    eeprom_check = False 
                result_data = {"Eeprom": versions_read["fault_data"]["EEPROM VERSION EK RD"]}
            if "DSP MAIN VERSION ECOKING" in version_data_norm:
                x, y = extract_v_t(versions_read["fault_data"]["DSP MAIN VERSION ECOKING"])
                if int(user_data["inverter_dsp"][0]) == x and int(user_data["inverter_dsp"][1]) == y:
                    dsp_check = True                    
                else: 
                    dsp_check = False
                result_data["DSP"] = versions_read["fault_data"]["DSP MAIN VERSION ECOKING"]
            else:
                result_test = "FAIL" 
            pfc_check = True
            data_pfc = f'User data V{user_data["inverter_pfc"][0]}_T{user_data["inverter_pfc"][1]}'
            result_data["PFC"] = data_pfc
            if eeprom_check and dsp_check and pfc_check:
                result_test = "PASS"
            else:
                result_test = "FAIL"
            out_data = {"result_test": result_test, 
                        "versions": result_data}     

        return out_data
    
    def normalize_name(self, name):
        """Normalizar nombre: MAYÚSCULAS, reemplazar underscores por espacios"""
        normalized = str(name).strip().upper().replace("_", " ")
        return " ".join(normalized.split())
    
    def write_loaging_data(self, info_text: QLabel,
                            text: str):
        info_text.setStyleSheet("font-size: 15px; font-weight: 600; color: black;")
        info_text.setText(text)
        return

    def write_info_data(self, info_text: QLabel,
                        result_test: dict,
                        text:str
                        ):
        current_test = info_text.text()
        if result_test == {}:
            info_text.setStyleSheet("font-size: 15px; font-weight: 600; color: red;")
            info_text.setText(text) 
            return
        if result_test["result_test"] == "PASS":
            info_text.setStyleSheet("font-size: 15px; font-weight: 600; color: green;")
        else:
            info_text.setStyleSheet("font-size: 15px; font-weight: 600; color: red;")
        info_text.setText(current_test + "\n"+ result_test["result_test"] + text)        
        return
    
    def write_result_cell(self, Index,
                        test_result)->str:
        item = QStandardItem()
        if "DGTO_validation" in test_result:
            if test_result["DGTO_validation"]["result_test"] == "PASS":
                item.setText(f"DGTO_validation" + ": " + test_result["DGTO_validation"]["result_test"])
            else:
                miss_list_DGTO = "-".join(test_result["DGTO_validation"]["DGTO_miss_list"])
                item.setText(f"DGTO_validation" + ": " + test_result["DGTO_validation"]["result_test"] + " DGTO list: " + miss_list_DGTO)
        current_test = item.text()
        line = []
        if "FAULT_validation" in test_result:
            if test_result["FAULT_validation"]["result_test"] == "PASS":
                item.setText(current_test + "\n" f"FAULT_validation" + ": " + test_result["FAULT_validation"]["result_test"])
            else:
                for key, value in test_result["FAULT_validation"]["fault_data"]["Faults_Not_expected"].items():
                    name  = " | " .join(set(value["Name"]))
                    line.append(f"{key} → {name}") 
                extra_fault = "\n".join(line)
                item.setText(current_test + "\n" f"FAULT_validation" + ": " + test_result["FAULT_validation"]["result_test"] + " Fault list: " + extra_fault)   
        current_test = item.text()
        line = []
        if "VERSION_validation" in test_result:
            if test_result["VERSION_validation"]["result_test"] == "PASS":
                item.setText(current_test + "\n" f"VERSION_validation" + ": " + test_result["VERSION_validation"]["result_test"])
            else:
                for key, value in test_result["VERSION_validation"]["versions"].items():
                    line.append(f"{key} → {value}") 
                ver_data = "\n".join(line)
                item.setText(current_test + "\n" f"VERSION_validation" + ": " + test_result["VERSION_validation"]["result_test"] + " Version list: " + ver_data) 

        current_test = item.text()
        item.setEditable(False)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_model.setItem(Index.row(), Index.column()+1, item)

        return current_test

    
    def click_action_analyse(self, Index,
                            container_path: QWidget, 
                            container_mod:QWidget,
                            container_lin:None,
                            info_text: QLabel,
                            tdm_fault_data: Dict[str, Any], 
                            tdm_config_data: Dict[str, Any],
                            step_dic: Dict[str, Any])->dict:
        
        path_line = getattr(container_path, "_text_path", None)
        path_mod = getattr(container_mod, "_text_path", None)
        path_mod_text = str(path_mod.text().strip())
        path_lin = getattr(container_lin, "_text_path", None)
        if path_lin is not None:
            path_lin_text = str(path_lin.text().strip())
        delimiter = Read_TDM_report.detect_csv_delimiter(path_line.text().strip())
        header_cust, report_data = Read_TDM_report.read_custom_csv(path_line.text().strip(), delimiter)
        if report_data is None or header_cust is None: 
            self.write_info_data(info_text,[],"ERROR: File format is invalid.")           
            return ["ERROR: File format is invalid."]
        test_result = {}
        test_excel = str(Path(path_line.text().strip()).with_suffix(".xlsx"))
        Read_TDM_report.save_to_excel(test_excel, header_cust, report_data)
        index_test = self.table_model.index(Index.row(),0)
        test_und_eva = self.table_model.data(index_test)
        self.styler = ExcelStyler(self.user_data, test_excel, tdm_dict=tdm_fault_data, sheet_name="DATA")
        self.engine = StepEngine(self.styler, step_dic, test_und_eva) 
        plot_path = ""
        # revisar llave antes de llamar todo

        if "DGTO" in self.Analysis[str(test_und_eva)]:
            result_DGTO_validation = self.Analysis[str(test_und_eva)]["DGTO"]({"report": report_data,
                                                                            "tdm": tdm_config_data})
            test_result["DGTO_validation"]  = result_DGTO_validation
            self.write_info_data(info_text,result_DGTO_validation," DGTO Validation.")

        if "FAULT" in self.Analysis[str(test_und_eva)]:
            result_fault_validation = self.Analysis[str(test_und_eva)]["FAULT"]({"engine": self.engine})
            test_result["FAULT_validation"] = result_fault_validation
            if "plot_path" not in result_fault_validation["fault_data"]:
                plot_path = "" 
            else:
                plot_path = result_fault_validation["fault_data"]["plot_path"]
            self.write_info_data(info_text,result_fault_validation," FAULT Validation.")

        if "VERSION" in self.Analysis[str(test_und_eva)]:
            result_version_validation = self.Analysis[str(test_und_eva)]["VERSION"]({"step_dic": step_dic,
                                                                                    "versions": result_fault_validation,
                                                                                    "user_data": self.user_data})
            test_result["VERSION_validation"] = result_version_validation
            self.write_info_data(info_text,result_version_validation," VERSION Validation.")
        logger.info("Test validation results: %s", result_fault_validation)                
        self.styler.save()
        data_to_report = self.write_result_cell(Index, test_result)
        logger.debug("Test validation results: %s", data_to_report)
        if self.user_data["machine_model"] == "Pacman 5":
            data_print_report = {"TDM log" : test_excel,
                                "Modbus Log": path_mod_text,
                                "Analysis": data_to_report,
                                "Supporting Data": plot_path}        
        else:
            data_print_report = {"TDM log" : test_excel,
                                "Log LIN": path_lin_text,
                                "Modbus Log": path_mod_text,
                                "Analysis": data_to_report,
                                "Supporting Data": plot_path}
        ouput_path = Read_report_file.modify_excel_with_headers(self.user_data["report_file"],
                                                    data_print_report,
                                                    test_und_eva)
        if ouput_path == "ERROR":
            self.write_loaging_data(info_text, "ERROR opening report file ...")

        return test_result
    
    def get_column_index(self, header_name: str) -> int:
        
        for col in range(self.table_model.columnCount()):
            head = self.table_model.horizontalHeaderItem(col)
            if head and head.text().strip().upper() == header_name.strip().upper():
                return col
        return -1  # Return -1 if not found
    def fill_column_by_header(self, header_name: list):
        for h in header_name:
            col = self.get_column_index(h)
            rows = self.table_model.rowCount()        
            for r in range(rows):
                item = self.create_path_selector_cell()
                index = self.table_model.index(r, col)
                self.table.setIndexWidget(index, item)

    def fill_action_column(self, header_name: str, 
                            info_state: QLabel,
                            tdm_fault_data: Dict[str, Any],
                            tdm_config_data: Dict[str, Any],
                            test_steps_dic: Dict[str, Any]
                            ):
        col = self.get_column_index(header_name)
        if col == -1:
            return
        rows = self.table_model.rowCount()        
        for r in range(rows):
            item = self.create_action_cell(r, 
                                            info_state, 
                                            tdm_fault_data, 
                                            tdm_config_data,
                                            test_steps_dic
                                            )
            index = self.table_model.index(r, col)
            self.table.setIndexWidget(index, item)


    @staticmethod
    def _format_initial_data(d: Dict[str, Any]) -> str:
        def format_version_field(value):
            # Empty o None
            if not value:
                return "NA"

            # is list
            if not isinstance(value, list):
                return str(value)

            # Normalizar values to strings  padding
            padded = [v.zfill(2) for v in value]

            # case 3 values → 04.34.09
            if len(padded) == 3:
                for data in value:
                    if data =="":
                        return f"V00{padded[0]}_T{padded[1]}"
                return ".".join(padded)

            # case 2 valores → V004_T09
            if len(padded) == 2:
                for data in value:
                    if data =="":
                        return "NA"
                return f"V00{padded[0]}_T{padded[1]}"

            # Cualquier otro caso → concatenar igual
            return "_".join(padded)
        return (
            "<b>Session data received:</b><br>"
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
    def load_dict_config_to_table(self, initial_info: Dict[str, Any], config_dict: Dict[str, Any]):
        """
        Load a dictionary (e.g., from test config) into the table view for display.
        """
        if not config_dict or initial_info is None:
            return
        self.table_model.clear()
        headers = header_default_table.get(initial_info.get("machine_model", ""), [])
        self.table_model.setHorizontalHeaderLabels(headers)
        self.table_model.setRowCount(len(config_dict))        
        rows = list(config_dict.items())
        for r, (test_number, attrs) in enumerate(rows):
                # Columna 0: número de test
                item0 = QStandardItem(str(test_number))
                item0.setEditable(False)
                item0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.table_model.setItem(r, 0, item0)

                # Resto de columnas según headers
                for c, col_name in enumerate(headers[1:], start=1):
                    raw_val = None
                    if isinstance(attrs, dict):
                        raw_val = attrs.get(col_name, "")
                    text = _format_cell_value(raw_val)

                    item = QStandardItem(text)
                    item.setEditable(False)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.table_model.setItem(r, c, item)

                    self.table.setWordWrap(True)
    
    def get_text_from_cell(self, row: int, col_name: str) -> str:
        """
        Returns the text of the QLineEdit inside the custom cell (line+button).
        """
        col = self.get_column_index(col_name)
        if col == -1:
            return ""
        index = self.table_model.index(row, col)
        widget = self.table.indexWidget(index)

        if widget is None:
            return ""

        line_edit = widget.findChild(QLineEdit)
        if line_edit is None:
            return ""

        return line_edit.text()

    def delete_json_on_exit(self, json_path: str):
        """
        Elimina el archivo JSON indicado si existe.
        json_path: ruta completa del archivo .json
        """
        try:
            if os.path.exists(json_path):
                os.remove(json_path)
                logging.info("Clean temporary file: %s", json_path)
                
            else:
                logging.info("Temporary file does not exists: %s", json_path)
        except Exception as e:
            logging.error("Clean temporary file: %s , error: %s", json_path, e)

    def closeEvent(self, event):
        self.delete_json_on_exit(self.temp_json_path)
        event.accept()







