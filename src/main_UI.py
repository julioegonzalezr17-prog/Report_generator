import os
os.environ["QT_LOGGING_RULES"] = "*.debug=false; *.warning=false"
import sys
from PySide6.QtWidgets import QApplication 
from PySide6.QtGui import QFont
import magic_logger
import logging
from PySide6.QtCore import qInstallMessageHandler


# code create exe -> pyinstaller --noconsole --onefile --icon=iconos/app_imag.ico --add-data "iconos;iconos" --collect-all PySide6 src/main_UI.py
# codigo limpio exe -> pyinstaller ReportGenerator.spec --clean
# pyside6-rcc resurces.qrc -o resurces_rc.py


# git checkout v2-development
# git add .
# git commit -m "Automatic RDP working"
# git tag -a 2.2.0 -m "automatic rdp working"
# git push origin v2-development
# git push origin tag 2.2.0


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
    def qt_message_handler(mode, context, message):
        if "QFont::setPointSize" in message:
            return  # ignorar este warning
        print(message)

    qInstallMessageHandler(qt_message_handler)

    


    import UI_selection 
    #import UI_user_fail_validation

    app = QApplication(sys.argv)    

    # # Optional: light/dark style (uncomment to use a simple dark theme)
    # dark = """
    #     QWidget { background-color: #1e1e1e; color: #e0e0e0; }
    #     QLineEdit, QTextEdit { background-color: #2a2a2a; border: 1px solid #444; }
    #     QPushButton { background-color: #3a3a3a; border: 1px solid #555; padding: 6px 12px; }
    #     QPushButton:hover { background-color: #4a4a4a; }
    # """
    # app.setStyleSheet(dark)

    #win = UI_user_fail_validation.ValidationWindow()
    win = UI_selection.SelectionWindow()
    win.show()   

    exit_code = app.exec() 
    magic_logger.logging.shutdown()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()