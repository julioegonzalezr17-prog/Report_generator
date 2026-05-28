
from PySide6.QtWidgets import (QSizePolicy, QWidget, QMainWindow, QLabel,
                                QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox)
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt
import resurces_rc
from dictDataIntegration import (sw_version, test_type)
import logging
import UI_report
import UI_standaloneReport
import UI_bugGenerator   
import UI_newRdP


logger = logging.getLogger(__name__)

class SelectionWindow(QMainWindow):
    """
    First window: collects test input data and opens AnalysisWindow.
    """
    def __init__(self):
        super().__init__()
        global_font = QFont()
        global_font.setPointSize(12)   # Tamaño base válido para toda la app
        self.setFont(global_font)
        self.setStyleSheet("""
                            QWidget {
                                font-size: 22px;
                            }
                            QComboBox {
                                min-height: 40px;
                                padding: 8px 16px;
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

        self.setWindowTitle("Test Analysis Setup " + "Version " + sw_version)
        self.setWindowIcon(QIcon(":/info_icon.png"))
        self.setMinimumSize(400, 300)
        self.setMaximumSize(450, 350)

        # ---- Widgets ----
        # Test type
        self.combo_machine = QComboBox()
        self.combo_machine.addItems(test_type)
        test_mode = QFormLayout()
        test_mode.addRow(self.combo_machine)

        # Buttons
        self.btn_ok = QPushButton("OK")
        self.btn_cancel = QPushButton("Cancel")

        # Container buttons
        buttons_row = QHBoxLayout()
        buttons_row.addStretch(1)
        buttons_row.addWidget(self.btn_cancel)
        buttons_row.addWidget(self.btn_ok)

        # container images
        self.img_label = QLabel()
        self.pixmap_standalone = QPixmap(":/standalone_image.png") 
        self.pixmap_integration = QPixmap(":/integration_image.png") 
        self.pixmap_bugreport = QPixmap(":/bug_image.png")
        self.pixmap_rdpreport = QPixmap(":/RDP_image.png")
        self.img_label.setScaledContents(True)
        self.img_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
        self.img_label.setFixedSize(300, 200)
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setPixmap(self.pixmap_standalone)
        self.combo_machine.currentTextChanged.connect(lambda text: self.show_image(text))

        # Container full sceen
        container = QWidget()
        v = QVBoxLayout(container)
        v.addLayout(test_mode)
        v.addWidget(self.img_label)
        v.addStretch(1)
        v.addLayout(buttons_row)
        self.setCentralWidget(container)

        # ---- Signals ----
        self.btn_ok.clicked.connect(self.on_ok_clicked)
        self.btn_cancel.clicked.connect(self.close)


    def show_image(self, test_type: str):

        if test_type == "Standalone test":
            self.img_label.setScaledContents(True)
            self.img_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
            pix = self.pixmap_standalone
            if not pix.isNull():
                scaled = pix.scaled(
                    self.img_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.img_label.setPixmap(scaled)
        elif test_type == "Integration test":
            pix = self.pixmap_integration
            if not pix.isNull():
                scaled = pix.scaled(
                    self.img_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.img_label.setPixmap(scaled)
                self.img_label.setScaledContents(True)
                self.img_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        elif test_type == "RdP report":
            pix = self.pixmap_rdpreport
            if not pix.isNull():
                scaled = pix.scaled(
                    self.img_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.img_label.setPixmap(scaled)
                self.img_label.setScaledContents(True)
                self.img_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        else:
            self.img_label.setFixedSize(300, 200)
            self.img_label.setAlignment(Qt.AlignCenter)
            self.img_label.setPixmap(self.pixmap_bugreport)
        

            
    def on_ok_clicked (self):
        if self.combo_machine.currentText() == "Standalone test":
            self.win = UI_standaloneReport.StartWindow()
            self.win.show()  
            logger.info("Opening Standalone analysis app")
            self.close()
        elif self.combo_machine.currentText() == "Integration test":
            self.win = UI_report.StartWindow()
            self.win.show()
            logger.info("Opening Integration analysis app")
            self.close()
        elif self.combo_machine.currentText() == "RdP report":
            self.win = UI_newRdP.StartWindow()
            self.win.show()
            logger.info("Opening RdP report filling app")
            self.close()
        else:
            self.win = UI_bugGenerator.BugReportGenerator()
            self.win.show()
            logger.info("Opening Bug report app")
            self.close()
        return
