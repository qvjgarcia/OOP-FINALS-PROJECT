from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication, QTextBrowser
from pathlib import Path
import sys

TEXT = """### Welcome to PicklePlay System Instructions
This GUI manages open-play court queues and tracking for up to 36 venue participants. Follow the guide below to navigate the system efficiently:

1. **Adding Players to the Queue:**
   * Type the player's name into the input text field at the top.
   * Click the **"Add to Queue Now"** button or press **Enter** to queue the player.

2. **Court Roster & Status:**
   * The table displays the status (**Available** or **Occupied**) for Court One, Court Two, and Court Three, along with active players.
   * Each court holds a maximum of 4 active players.

3. **Starting a Game:**
   * Ensure there are at least 4 players available in the general queue.
   * Click the corresponding **"Start Game"** button for your target court. The first 4 players from the queue will automatically populate that court.

4. **Finishing a Game:**
   * Once a match concludes, click the corresponding **"Finish Game"** button.
   * All active players from that court will automatically return to the back of the queued list.

5. **Removing Players in Game:**
   * Double-click on any active player cell inside the court status table to see a removal option.
   * This is important because if a player wants to leave the game, it'll be convenient.
"""

class InstructionsPage(QWidget):
    def __init__(self):
        super().__init__()
        instruction_page = QVBoxLayout()
        self.setLayout(instruction_page)
        instruction_page.setContentsMargins(24, 18, 24, 18)

        # ----- Title -----
        instructions_title = QLabel("Instructions")
        instructions_title.setObjectName("instructions_title")
        instructions_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_page.addWidget(instructions_title)

        # ----- Body Text of the Information -----
        instructions_info = QTextBrowser()
        instructions_info.setMarkdown(TEXT)
        instructions_info.setObjectName("instructions_info")
        instruction_page.addWidget(instructions_info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qss_file = Path(__file__).with_name("style.qss")
    app.setStyleSheet(qss_file.read_text())
    page = InstructionsPage()
    page.resize(700, 520)
    page.show()
    sys.exit(app.exec())
