import sys
from PySide6.QtWidgets import QApplication 
import magic_logger
import logging
import os

# code create exe -> pyinstaller --noconsole --onefile --icon=iconos/app_imag.ico --add-data "iconos;iconos" --collect-all PySide6 src/main_UI.py
# pyside6-rcc resurces.qrc -o resurces_rc.py
def main():
    log_file = magic_logger.setup_per_run_logging(app_name="TestAnalysis", 
                                                level=logging.DEBUG,
                                                keep_last=20,
                                                latest_alias=True
                                                )
    logger = logging.getLogger(__name__)    
    logger.info("Starting app: %s", log_file)
    logger.debug("Debug check")
    logger.error("Error check")

    import UI_report 
    app = QApplication(sys.argv)

    # # Optional: light/dark style (uncomment to use a simple dark theme)
    # dark = """
    #     QWidget { background-color: #1e1e1e; color: #e0e0e0; }
    #     QLineEdit, QTextEdit { background-color: #2a2a2a; border: 1px solid #444; }
    #     QPushButton { background-color: #3a3a3a; border: 1px solid #555; padding: 6px 12px; }
    #     QPushButton:hover { background-color: #4a4a4a; }
    # """
    # app.setStyleSheet(dark)

    win = UI_report.StartWindow()
    win.show()   
    exit_code = app.exec() 
    magic_logger.logging.shutdown()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()