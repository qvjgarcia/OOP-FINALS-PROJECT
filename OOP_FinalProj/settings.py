from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QCheckBox, QApplication, QPushButton, QMessageBox
from pathlib import Path
import sys

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        settings_layout = QVBoxLayout(self)
        settings_layout.setContentsMargins(24, 18, 24, 18)

        # ----- Title -----
        settings_title = QLabel("Settings")
        settings_title.setObjectName("settings_title")
        settings_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_layout.addWidget(settings_title)

        # ----- Description / Subheading -----
        settings_subhead = QLabel("Application Preferences & Configurations")
        settings_subhead.setObjectName("settings_subhead")
        settings_layout.addWidget(settings_subhead)

        # ----- Settings Options: Exit Confirmation Option -----
        self.exit_confirm_checkbox = QCheckBox("Confirmation Message Before Leaving")
        self.exit_confirm_checkbox.setChecked(True)
        self.exit_confirm_checkbox.setObjectName("exit_confirm_checkbox")
        settings_layout.addWidget(self.exit_confirm_checkbox)
        settings_layout.addStretch()
        
        # ----- Exit Button -----
        self.exit_btn = QPushButton("Exit GUI")
        self.exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exit_btn.clicked.connect(self.exit_application)
        self.exit_btn.setFixedSize(120, 50)
        settings_layout.addWidget(self.exit_btn)
        settings_layout.addStretch()
        
    def exit_application(self):
        if self.exit_confirm_checkbox.isChecked():
            confirm_exit = QMessageBox.question(
                self, "Exit Confirmation",
                "Exit?", 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm_exit == QMessageBox.StandardButton.Yes:
                QApplication.quit()
        else:
            QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qss_file = Path(__file__).with_name("style.qss")
    app.setStyleSheet(qss_file.read_text())
    Settings = SettingsPage()
    Settings.resize(700, 520)
    Settings.show()
    sys.exit(app.exec())
