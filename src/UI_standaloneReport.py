import sys, os
from typing import Dict, Any
from PySide6.QtWidgets import (QScrollArea, QSizePolicy, QWidget, QMainWindow, QLabel, QLineEdit, QTextEdit,
                                QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox,
                                QFileDialog, QComboBox, QTableView, QHeaderView, QFrame)
from PySide6.QtGui import QIcon, QStandardItemModel, QStandardItem, QPixmap
from PySide6.QtCore import Qt
import Read_TDM_error
import TDM_config_load
import Load_configuration_test
import json_motor
from pathlib import Path
from dictDataIntegration import (inverter, 
                        header_default_table, 
                        header_row_default, 
                        time_data_set,
                        sw_version)
from dictDataStandalone import machines_standalone
from pprint import pprint
import json
import logging

logger = logging.getLogger(__name__)


class StartWindow(QMainWindow):
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

        # ---- Widgets ----
        # Report configuration
        self.modbus_dict = {}
        self.slave_combos = {}

        self.report_config = QLineEdit()
        self.report_config.setPlaceholderText("Select the config file used in Pymodbus...")
        self.report_config_browse = QPushButton("Browse")
        self.report_config_browse.clicked.connect(self.on_browse_report_config)
        report_config_row = QHBoxLayout()
        report_config_row.addWidget(self.report_config)
        report_config_row.addWidget(self.report_config_browse)

                # ----------------------------
        # SCROLL AREA (dinámico)
        # ----------------------------
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        # Report to fill
        self.report_file = QLineEdit()
        self.report_file.setPlaceholderText("Enter Report file ...")
        self.report_file_browse = QPushButton("Browse")
        self.report_file_browse.clicked.connect(self.on_browse_report_file)
        self.report_file_row = QHBoxLayout()
        self.report_file_row.addWidget(self.report_file)
        self.report_file_row.addWidget(self.report_file_browse)

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
        self.inverter_DSPZ.setEnabled(True)
        self.inverter_DSP = QHBoxLayout()
        self.inverter_DSP.addWidget(self.inverter_DSPX)
        self.inverter_DSP.addWidget(self.inverter_DSPY)
        self.inverter_DSP.addWidget(self.inverter_DSPZ)

        # ARM
        self.inverter_ARMX = QLineEdit()
        self.inverter_ARMX.setPlaceholderText("Vxx")
        self.inverter_ARMX.setEnabled(True)
        self.inverter_ARMY = QLineEdit()
        self.inverter_ARMY.setPlaceholderText("Tyy")
        self.inverter_ARMY.setEnabled(True)
        self.inverter_ARM = QHBoxLayout()
        self.inverter_ARM.addWidget(self.inverter_ARMX)
        self.inverter_ARM.addWidget(self.inverter_ARMY)

        # PFC
        self.inverter_PFCX = QLineEdit()
        self.inverter_PFCX.setPlaceholderText("Vxx")
        self.inverter_PFCX.setEnabled(True)
        self.inverter_PFCY = QLineEdit()
        self.inverter_PFCY.setPlaceholderText("Tyy")
        self.inverter_PFCY.setEnabled(True)
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

        # User Pump - fan
        self.pump = QLineEdit()
        self.pump.setPlaceholderText("Enter Pump Model ...")
        self.fan = QLineEdit()
        self.fan.setPlaceholderText("Enter Fan Model ...")

        # User Name
        self.rdp_data = QLineEdit()
        self.rdp_data.setPlaceholderText("Enter RDP number ...")
        self.requester_name = QLineEdit()
        self.requester_name.setPlaceholderText("Requested by ...")
        self.tester_name = QLineEdit()
        self.tester_name.setPlaceholderText("Enter your name")
        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Optional notes about this test session...")

        # Buttons
        self.btn_ok = QPushButton("OK")
        self.btn_cancel = QPushButton("Cancel")

        layout_jason = QFormLayout()
        layout_jason.addRow("Report Config*", report_config_row)

        self.container_menu = QWidget()
        self.scroll_layout = QVBoxLayout(self.container_menu)
        self.scroll.setWidget(self.container_menu)
        # inicialmente deshabilitado
        self.scroll.setVisible(False)


        # ---- Layout ----
        self.form = QFormLayout()
        self.form.addRow("Report File*", self.report_file_row)
        self.form.addRow("Inverter EEPROM Vxx.Tyy*", self.inverter_EPR)
        self.form.addRow("Inverter DSP Vxx.Tyy.zz*", self.inverter_DSP)
        self.form.addRow("Inverter ARM Vxx.Tyy*", self.inverter_ARM)
        self.form.addRow("Inverter PFC Vxx.Tyy*", self.inverter_PFC)
        self.form.addRow("Control Board XX.YY.ZZ*", self.CB)
        self.form.addRow("Pump model*", self.pump)
        self.form.addRow("Fan model*", self.fan)
        self.form.addRow("RDP number*", self.rdp_data)
        self.form.addRow("Requested By*", self.requester_name)
        self.form.addRow("Tester Name*", self.tester_name)
        self.form.addRow("Notes", self.notes)
        self.form.setEnabled(False)
        for i in range(self.form.rowCount()):
            self.form.setRowVisible(i, False)


        # Container buttons
        buttons_row = QHBoxLayout()
        buttons_row.addStretch(1)
        buttons_row.addWidget(self.btn_cancel)
        buttons_row.addWidget(self.btn_ok)

        # Container full sceen
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 1️⃣ CONFIG JSON ARRIBA
        top_box = QVBoxLayout()
        top_box.addLayout(layout_jason)

        # 3️⃣ FORMULARIO (ABAJO)
        form_box = QVBoxLayout()
        form_box.addLayout(self.form)

        # 4️⃣ BOTONES
        buttons_box = QHBoxLayout()
        buttons_box.addStretch()
        buttons_box.addWidget(self.btn_cancel)
        buttons_box.addWidget(self.btn_ok)

        # ✅ COMPOSICIÓN FINAL
        main_layout.addLayout(top_box)
        main_layout.addWidget(self.scroll)   # ✅ ocupa más espacio
        self.scroll.setMaximumHeight(150)
        main_layout.addLayout(form_box)      # ✅ menor que scroll
        main_layout.addLayout(buttons_box)

        # ---- Signals ----
        self.btn_ok.clicked.connect(self.on_ok_clicked)
        self.btn_cancel.clicked.connect(self.close)

        # Keep a reference to the next window so it's not garbage-collected
        self._analysis_window = None
    
    #Read json configuration pymodbus file
    def build_modbus_dict(self,json_path):

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        result = {}

        for block in data:

            slave_id = block.get("slave_id")
            slave_key = f"slave_ID_{slave_id}"

            # crear nodo si no existe
            if slave_key not in result:
                result[slave_key] = {}

            addresses = block.get("addresses", [])
            registers = block.get("registers", [])

            # asegurar que sean same length
            for addr, reg in zip(addresses, registers):

                result[slave_key][addr] = {
                    "name": reg.get("name", ""),
                    "is_bitmap": reg.get("is_bitmap", False),
                    "bit_labels": reg.get("bit_labels", [])
                }

        return result

    # brwose report config File
    def on_browse_report_config(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Report config file",
            "",
            "All Files (*)"
        )
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in [".json"]:
            QMessageBox.warning(
                self,
                "Invalid file type",
                f"The file must be a JSON file (.json):\n{file_path}"
            )
            return
        if file_path:
            self.report_config.setText(file_path)
            self.modbus_dict = self.build_modbus_dict(file_path)
            self.build_slave_list()
                    # habilitar UI
            self.scroll.setVisible(True)
            self.container_menu.setEnabled(True)
            self.form.setEnabled(True) 
            for i in range(self.form.rowCount()):
                self.form.setRowVisible(i, True)

    def build_slave_list(self):

        # limpiar
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # crear filas
        for slave_key in self.modbus_dict.keys():

            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)

            # etiqueta slave
            label = QLabel(slave_key)
            label.setMinimumWidth(150)

            # combobox máquinas
            combo = QComboBox()
            combo.addItems(machines_standalone)
            combo.setMinimumWidth(200)
            self.slave_combos[slave_key] = combo

            row_layout.addWidget(label)
            row_layout.addWidget(combo)
            row_layout.addStretch()

            self.scroll_layout.addWidget(row_widget)

        self.scroll_layout.addStretch()
        for slave, data in self.slave_combos.items():
            self.slave_combos[slave].currentTextChanged.connect(self.version_selection)

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

    # Input data validation
    def version_selection(self):  
        count = 0  
        if "Control Board" not in  self.slave_combos.keys():
            self.CBX.clear()
            self.CBX.setEnabled(False)
            self.CBY.clear()
            self.CBY.setEnabled(False)
            self.CBZ.clear()
            self.CBZ.setEnabled(False)
        if "LIN Pump" not in self.slave_combos.keys():
            self.pump.clear()
            self.pump.setEnabled(False)
        if "EBM Fan" not in self.slave_combos.keys():
            self.fan.clear()
            self.fan.setEnabled(False)
        if "ZA Fan" not in self.slave_combos.keys():
            self.fan.clear()
            self.fan.setEnabled(False)

        for slave_key, combo in self.slave_combos.items():            
            if combo.currentText() == "Control Board":
                self.CBX.clear()
                self.CBX.setEnabled(True)
                self.CBY.clear()
                self.CBY.setEnabled(True)
                self.CBZ.clear()
                self.CBZ.setEnabled(True)                
                continue
            if combo.currentText() == "LIN Pump":  
                self.pump.clear()
                self.pump.setEnabled(True)              
                continue
            if combo.currentText() == "EBM Fan":
                self.fan.clear()
                self.fan.setEnabled(True)                
                continue
            if combo.currentText() == "ZA Fan": 
                self.fan.clear()
                self.fan.setEnabled(True)               
                continue
            if count < 1:
                match combo.currentText():
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
            count = count + 1

    # Collect the data provided by the user in a dict
    def _collect_input(self) -> Dict[str, Any]:
        """
        Gather form data into a dict.
        """
        data_slaves = {}
        for slaves, data in self.slave_combos.items():
            data_slaves[slaves] = data.currentText()
        return {
            "report_config": self.report_config.text().strip(),
            "report_file": self.report_file.text().strip(),
            "data_slaves": data_slaves,
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
            "pump_model": self.pump.text().strip(),  
            "fan_model": self.fan.text().strip(),               
            "rdp_number": self.rdp_data.text().strip(),
            "requester_name": self.requester_name.text().strip(),
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
        if self.pump.isEnabled():
            if not data["pump_model"]:
                missing.append("Pump Model")
        if self.fan.isEnabled():
            if not data["fan_model"]:
                missing.append("Fan Model")
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

    def on_ok_clicked(self):
        """
        Validate input fields, file type, and load XLSX configuration (if applicable)
        before opening the analysis window.
        """
        data = self._collect_input()
        pprint(data)
        if not self._validate(data):
            return        
        if not os.path.isfile(data["report_file"]):
            QMessageBox.warning(
                self,
                "File not found",
                f"The file specified for '{data['report_file']}' does not exist:\n{data['report_file']}"
            )
            return
        ext = os.path.splitext(data["report_file"])[1].lower()
        if ext not in [".xlsx", ".xls"]:
            QMessageBox.warning(
                self,
                "Invalid file type",
                f"The file specified for '{data['report_file']}' must be an Excel file (.xlsx or .xls):\n{data['report_file']}"
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

        self.close()  # Close the start window after opening the analysis window
        # Optionally hide start window (or close it if you want)
        # self.hide()
