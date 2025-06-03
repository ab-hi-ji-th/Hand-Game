from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class InstructionsPage(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Instructions")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        instructions_label = QLabel(
            "Game Instructions:\n\n"
            "1. Hit the green target to score points.\n"
            "2. After every 3 hits, a pink target will appear.\n"
            "3. Hit the pink target to extend your time.\n"
            "   - Easy: +5 seconds\n"
            "   - Medium: +3 seconds\n"
            "   - Hard: +2 seconds\n"
            "4. The game ends when time runs out.\n"
            "5. The player with the highest score wins.\n\n"
            "Press Start to play!"
        )
        instructions_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(instructions_label)
        self.setLayout(layout)
