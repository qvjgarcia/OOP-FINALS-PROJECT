from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QBoxLayout, QHBoxLayout, QVBoxLayout, QCheckBox, 
                            QWidget, QStackedWidget, QLineEdit, QMessageBox, QListWidget, QDateEdit, QTableWidget, QHeaderView, QTableWidgetItem)
from PyQt6.QtCore import Qt, QDate, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QColor, QPixmap, QIcon
from dashboard import VenueManager
from instructions import InstructionsPage
from settings import SettingsPage
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
        self.start_btn_1 = QPushButton("Start Game")
        self.finish_btn_1 = QPushButton("Finish Game")
        self.start_btn_2 = QPushButton("Start Game")
        self.finish_btn_2 = QPushButton("Finish Game")
        self.start_btn_3 = QPushButton("Start Game")
        self.finish_btn_3 = QPushButton("Finish Game")
        self.instructions_btn = QPushButton("Instructions")
        self.settings_btn = QPushButton("Settings")
        self.queue_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.queue_btn.setFixedSize(150, 50)
        self.start_btn_1.setCursor(Qt.CursorShape.PointingHandCursor)
        self.finish_btn_1.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn_2.setCursor(Qt.CursorShape.PointingHandCursor)
        self.finish_btn_2.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn_3.setCursor(Qt.CursorShape.PointingHandCursor)
        self.finish_btn_3.setCursor(Qt.CursorShape.PointingHandCursor)
        self.instructions_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.instructions_btn.setFixedSize(120, 50)
        self.settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_btn.setFixedSize(120, 50)
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
        self.title_icon_container.addWidget(self.instructions_btn)
        self.title_icon_container.addWidget(self.settings_btn)
        
        # ----- Court Section -----
        self.court_section = QTableWidget()
        self.court_section.setColumnCount(3)
        self.court_section.setRowCount(5)
        self.court_section.setHorizontalHeaderLabels(["Court One", "Court Two", "Court Three"])
        self.court_section.verticalHeader().setVisible(False)
        self.court_section.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        header = self.court_section.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.court_section.setCursor(Qt.CursorShape.PointingHandCursor)
        self.court_section.setFixedHeight(220)
        self.court_section.cellDoubleClicked.connect(self.inspect_and_remove)
        
        # ----- Players List -----
        self.players_list = QListWidget()
        self.players_list.setFixedSize(500, 200)
        
        # ----- Layouts -----
        court_btn_layout = QHBoxLayout()
        court_btn_layout.addWidget(self.start_btn_1)
        court_btn_layout.addWidget(self.finish_btn_1)
        court_btn_layout.addWidget(self.start_btn_2)
        court_btn_layout.addWidget(self.finish_btn_2)
        court_btn_layout.addWidget(self.start_btn_3)
        court_btn_layout.addWidget(self.finish_btn_3)
        
        button = QHBoxLayout()
        button.addWidget(self.queue_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        top_bar = QWidget()
        top_bar.setObjectName("top_bar")
        
        top_bar_layout = QVBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(12, 12, 12, 12)
        top_bar_layout.addLayout(self.title_icon_container)
        top_bar_layout.addSpacing(30)
        top_bar_layout.addWidget(self.subtitle)
        top_bar_layout.addWidget(self.name_input)
        top_bar_layout.addWidget(self.capacity_label)
        
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.addWidget(QLabel("Court Status & Roster:"))
        content_layout.addWidget(self.court_section)
        content_layout.addLayout(court_btn_layout)
        content_layout.addWidget(QLabel("All Queued Players:"))
        content_layout.addWidget(self.players_list)
        content_layout.addStretch()
        content_layout.addLayout(button)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(top_bar)
        layout.addLayout(content_layout)
        self.setLayout(layout)
        
        # ----- Signals and Slots -----
        self.queue_btn.clicked.connect(self.queue_player)
        self.start_btn_1.clicked.connect(self.start_game_1)
        self.finish_btn_1.clicked.connect(self.finish_game_1)
        self.start_btn_2.clicked.connect(self.start_game_2)
        self.finish_btn_2.clicked.connect(self.finish_game_2)
        self.start_btn_3.clicked.connect(self.start_game_3)
        self.finish_btn_3.clicked.connect(self.finish_game_3)
        self.instructions_btn.clicked.connect(self.show_instructions)
        self.settings_btn.clicked.connect(self.show_settings)
        self.name_input.returnPressed.connect(self.queue_player)
        
        # ----- Styling a Widget -----
        self.title.setObjectName("title")
        self.subtitle.setObjectName("subtitle")
        self.capacity_label.setObjectName("capacity_label")
        self.queue_btn.setObjectName("queue_btn")
        self.start_btn_1.setObjectName("start_btn_1")
        self.finish_btn_1.setObjectName("finish_btn_1")
        self.start_btn_2.setObjectName("start_btn_2")
        self.finish_btn_2.setObjectName("finish_btn_2")
        self.start_btn_3.setObjectName("start_btn_3")
        self.finish_btn_3.setObjectName("finish_btn_3")
        self.title.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.update_court_status()
        
    def queue_player(self):
        # ----- Queue Functionalities -----
        name = self.name_input.text().strip()
            
        if not name:
            QMessageBox.warning(
                self, "Error", "Please Type Your Name First."
            )
            return
        
        success, message = self.manager_system.add_player(name)
        if not success:
            QMessageBox.warning(
                self, "Error", message
            )
            return
        
        QMessageBox.information(
            self, "Success", "You Have Successfully Queued!"
        )
        
        self.name_input.clear()
        self.name_input.setFocus()
        
    def start_game(self, court_num):
        success, message = self.manager_system.starting_game(court_num)
        if not success:
            QMessageBox.warning(self, "Error", message)
        else:
            QMessageBox.information(self, "Success", message)
        self.update_court_status()
        
    def finish_game(self, court_num):
        success, message = self.manager_system.finishing_game(court_num)
        if not success:
            QMessageBox.warning(self, "Error", message)
        else:
            QMessageBox.information(self, "Success", message)
        self.update_court_status()
        
    def start_game_1(self):
        self.start_game(1)

    def start_game_2(self):
        self.start_game(2)

    def start_game_3(self):
        self.start_game(3)

    def finish_game_1(self):
        self.finish_game(1)

    def finish_game_2(self):
        self.finish_game(2)

    def finish_game_3(self):
        self.finish_game(3)
        
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
                
            total_players = len(self.manager_system.players) + sum(len(c.players) for c in self.manager_system.courts)
            self.capacity_label.setText(
            f"Venue Capacity: {total_players}/{self.manager_system.venue_capacity}"
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
                
    def show_instructions(self):
        # ----- Shows the Instructions -----
        self.instructions_window = InstructionsPage()
        self.instructions_window.setWindowTitle("Instructions")
        self.instructions_window.resize(700, 520)
        self.instructions_window.show()
        
    def show_settings(self):
        # ----- Shows the Settings -----
        self.instructions_window = SettingsPage()
        self.instructions_window.setWindowTitle("Settings")
        self.instructions_window.resize(700, 520)
        self.instructions_window.show()
            
app = QApplication(sys.argv)
qss_file = Path(__file__).with_name("style.qss")
app.setStyleSheet(qss_file.read_text())
app.setWindowIcon(QIcon(str(Path(__file__).with_name("pickleball_icon.png"))))
window = PicklePlaySys()
window.show()
app.exec()
