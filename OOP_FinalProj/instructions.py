from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication
from pathlib import Path
import sys

TEXT = """
<h3>Welcome to PicklePlay System Instructions</h3>
<p>This GUI manages open-play court queues and tracking for up to 36 venue participants. Follow the guide below to navigate the system efficiently:</p>

<ol>
    <li><b>Adding Players to the Queue:</b>
        <ul>
            <li>Type the player's name into the input text field at the top.</li>
            <li>Click the <b>"Add to Queue Now"</b> button or press <b>Enter</b> to queue the player.</li>
        </ul>
    </li>
    <li><b>Court Roster & Status:</b>
        <ul>
            <li>The table displays the status (<b>Available</b> or <b>Occupied</b>) for Court One, Court Two, and Court Three, along with active players.</li>
            <li>Each court holds a maximum of 4 active players.</li>
        </ul>
    </li>
    <li><b>Starting a Game:</b>
        <ul>
            <li>Ensure there are at least 4 players available in the general queue.</li>
            <li>Click the corresponding <b>"Start Game"</b> button for your target court. The first 4 players from the queue will automatically populate that court.</li>
        </ul>
    </li>
    <li><b>Finishing a Game:</b>
        <ul>
            <li>Once a match concludes, click the corresponding <b>"Finish Game"</b> button.</li>
            <li>All active players from that court will automatically return to the back of the queued list.</li>
        </ul>
    </li>
    <li><b>Removing Players in Game:</b>
        <ul>
            <li>Double-click on any active player cell inside the court status table to see a removal option.</li>
            <li>This is important because if a player wants to leave the game, it'll be convenient.</li>
        </ul>
    </li>
</ol>
"""

class InstructionsPage(QWidget):
    def __init__(self):
        super().__init__()
        instruction_page = QVBoxLayout(self)
        instruction_page.setContentsMargins(24, 18, 24, 18)

        # ----- Title -----
        instructions_title = QLabel("Instructions")
        instructions_title.setObjectName("instructions_title")
        instructions_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_page.addWidget(instructions_title)

        # ----- Body Text of the Information -----
        instructions_info = QLabel(TEXT)
        instructions_info.setWordWrap(True)
        instructions_info.setTextFormat(Qt.TextFormat.RichText)
        instructions_info.setAlignment(Qt.AlignmentFlag.AlignTop)
        instructions_info.setObjectName("instructions_info")
        instruction_page.addWidget(instructions_info)
        instruction_page.addStretch()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qss_file = Path(__file__).with_name("style.qss")
    app.setStyleSheet(qss_file.read_text())
    page = InstructionsPage()
    page.resize(700, 520)
    page.show()
    sys.exit(app.exec())
