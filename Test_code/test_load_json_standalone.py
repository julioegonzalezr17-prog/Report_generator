import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QScrollArea, QLabel, QComboBox
)
from PySide6.QtCore import Qt
import json


# =========================
# MOCK CATÁLOGO DE MÁQUINAS
# =========================
machine = [
    "Pacman 5",
    "Ariston X",
    "Test Bench",
    "Integration Rig"
]


# =========================
# TU FUNCIÓN (simplificada)
# =========================
def build_modbus_dict(json_path):

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = {}

    for block in data:

        slave_id = block.get("slave_id")
        slave_key = f"slave_ID_{slave_id}"

        if slave_key not in result:
            result[slave_key] = {}

        addresses = block.get("addresses", [])
        registers = block.get("registers", [])

        for addr, reg in zip(addresses, registers):
            result[slave_key][addr] = {
                "name": reg.get("name", ""),
                "is_bitmap": reg.get("is_bitmap", False),
                "bit_labels": reg.get("bit_labels", [])
            }

    return result


# =========================
# MAIN UI
# =========================
class ModbusUI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modbus Mapping UI")
        self.setMinimumSize(800, 500)

        self.modbus_dict = {}

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)

        # ----------------------------
        # BUTTON LOAD JSON
        # ----------------------------
        self.btn_load = QPushButton("Load JSON")
        self.btn_load.clicked.connect(self.load_json)

        # ----------------------------
        # SCROLL AREA (dinámico)
        # ----------------------------
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.scroll_layout = QVBoxLayout(self.container)

        self.scroll.setWidget(self.container)

        # inicialmente deshabilitado
        self.container.setEnabled(False)

        # ----------------------------
        # LAYOUT
        # ----------------------------
        main_layout.addWidget(self.btn_load)
        main_layout.addWidget(self.scroll)

    # =========================
    # LOAD JSON
    # =========================
    def load_json(self):

        # ⚠️ poner aquí tu path real
        path = r"C:\Users\gonzpidr\OneDrive - Ariston Group\Documenti\Modbus_SW\Inverter config\Ariston Extended.json"

        self.modbus_dict = build_modbus_dict(path)

        self.build_slave_list()

        # habilitar UI
        self.container.setEnabled(True)

    # =========================
    # BUILD UI DINÁMICA
    # =========================
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
            combo.addItems(machine)
            combo.setMinimumWidth(200)

            row_layout.addWidget(label)
            row_layout.addWidget(combo)
            row_layout.addStretch()

            self.scroll_layout.addWidget(row_widget)

        self.scroll_layout.addStretch()


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ModbusUI()
    win.show()
    sys.exit(app.exec())