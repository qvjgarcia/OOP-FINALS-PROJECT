from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QBoxLayout, QHBoxLayout, QVBoxLayout, QCheckBox, 
                            QWidget, QStackedWidget, QLineEdit, QMessageBox, QListWidget, QDateEdit, QTableWidget, QHeaderView, QTableWidgetItem)
from PyQt6.QtCore import Qt, QDate, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QColor, QPixmap
from dashboard import VenueManager
from sidebar import Sidebar
from pathlib import Path
import sys, os

class PicklePlaySys(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PicklePlay, Open Play Court Queue Management System")
        self.setFixedSize(1050, 800)
        self.setWindowOpacity(0.0)
        self.manager_system = VenueManager()
        self.manager_system.changed.connect(self.update_court_status)
        self.fade = QPropertyAnimation(self, b"windowOpacity")
        self.fade.setDuration(650)
        self.fade.setStartValue(0.0)
        self.fade.setEndValue(1.0)
        self.fade.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade.start()
    
        # ----- Widgets -----
        self.title = QLabel("PicklePlay")
        self.subtitle = QLabel ("Open Play Queue Management System")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Please Input Your Name.")
        self.capacity_label = QLabel("Venue Capacity: 0/36")
        self.queue_btn = QPushButton("Add to Queue Now")
        self.queue_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.queue_btn.setFixedSize(150, 50)
        self.name_input.setFixedWidth(500)
        
        # ----- Title Icon -----
        self.title_icon_container = QHBoxLayout()
        self.title_icon_container.setContentsMargins(0, 0, 0, 0)
        self.title_icon_container.setSpacing(10)
        self.icon_label = QLabel()
        icon_path = Path(__file__).with_name("pickleball_icon.png")
        if icon_path.exists():
            pixmap = QPixmap(str(icon_path))
            scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.icon_label.setPixmap(scaled_pixmap)
        else:
            self.icon_label.setText("[Icon]")
            
        self.title_icon_container.addWidget(self.icon_label)
        self.title_icon_container.addWidget(self.title)
        self.title_icon_container.addStretch()
        
        # ----- Court Section -----
        self.court_section = QTableWidget()
        self.court_section.setColumnCount(3)
        self.court_section.setRowCount(5)
        self.court_section.setHorizontalHeaderLabels(["Court One", "Court Two", "Court Three"])
        self.court_section.verticalHeader().setVisible(False)
        self.court_section.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        header = self.court_section.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.court_section.setFixedHeight(220)
        self.court_section.cellDoubleClicked.connect(self.inspect_and_remove)
        
        # ----- Players List -----
        self.players_list = QListWidget()
        self.players_list.setFixedSize(500, 200)
        
        # ----- Layouts -----
        button = QHBoxLayout()
        button.addWidget(self.queue_btn)
        button.addWidget(self.queue_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        layout = QVBoxLayout()
        layout.addLayout(self.title_icon_container)
        layout.addSpacing(30)
        layout.addWidget(self.subtitle)
        layout.addWidget(self.name_input)
        layout.addWidget(self.capacity_label)
        layout.addWidget(QLabel("Court Status & Roster:"))
        layout.addWidget(self.court_section)
        layout.addWidget(QLabel("All Queued Players:"))
        layout.addWidget(self.players_list)
        layout.addStretch()
        layout.addLayout(button)
        self.setLayout(layout)
        
        # ----- Signals and Slots -----
        self.queue_btn.clicked.connect(self.queue_player)
        
        # ----- Styling a Widget -----
        self.title.setObjectName("title")
        self.subtitle.setObjectName("subtitle")
        self.queue_btn.setObjectName("queue_btn")
        self.capacity_label.setObjectName("capacity_label")
        self.title.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignTop)
        
    def queue_player(self):
        # ----- Queue Functionalities -----
        name = self.name_input.text().strip()
            
        if not name:
            QMessageBox.warning(
                self, "Error", "Invalid, Please Put a Valid Username"
            )
            return
        
        success = self.manager_system.add_player(name)
        if not success:
            QMessageBox.warning(
                self, "Error", "This Court is Fully Occupied."
            )
            return
        
        self.players_list.addItem(name)
        
        QMessageBox.information(
            self, "Success!", "You Have Successfully Queued"
        )
        
        self.update_court_status()    
        self.name_input.clear()
        self.name_input.setFocus()
        
    def update_court_status(self):
        # ----- Court Updates Functionalities -----
        for col_idx, courts in enumerate(self.manager_system.courts):
            is_full = len(courts.players) >= 4
            status_text = "Occupied" if is_full else "Available"
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setForeground(QColor("#dc2626") if is_full else QColor("#16a43a"))
            self.court_section.setItem(0, col_idx, status_item)
            
            for slot_idx in range(4):
                row_idx = slot_idx + 1
                if slot_idx < len(courts.players):
                    player_name = courts.players[slot_idx]
                    item = QTableWidgetItem(player_name)
                else:
                    item = QTableWidgetItem("Empty")
                    item.setForeground(QColor("#94a3b8"))
                    
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.court_section.setItem(row_idx, col_idx, item)
                
            current_count = len(self.manager_system.players)
            self.capacity_label.setText(
                f"Venue Capacity: {current_count}/{self.manager_system.venue_capacity}"
            )
            
            self.players_list.clear()
            for player in self.manager_system.players:
                self.players_list.addItem(player)
        
    def inspect_and_remove(self, row, column):
        # ----- Inspect Option on Players to Remove or No Functionality -----
        if row == 0:
            return
        
        item_remove = self.court_section.item(row, column)
        if item_remove and item_remove.text() != "Empty":
            player_name = item_remove.text()
            
            confirm = QMessageBox.question(
                self, "Remove Player", 
                f"Remove {player_name} from Queue/Court?", 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if confirm == QMessageBox.StandardButton.Yes:
                self.manager_system.remove_player(player_name)
                QMessageBox.information(self, "Removed", f"{player_name} is Removed")
            
        
app = QApplication(sys.argv)
qss_file = Path(__file__).with_name("style.qss")
app.setStyleSheet(qss_file.read_text())
window = PicklePlaySys()
window.show()
app.exec() 
