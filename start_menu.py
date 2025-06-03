from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QInputDialog, QMessageBox
from instructions import InstructionsPage
from game import run_game
import sys


class StartMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Start Menu")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.single_player_button = QPushButton("Single Player")
        self.single_player_button.clicked.connect(self.single_player)

        self.multiplayer_button = QPushButton("Multiplayer")
        self.multiplayer_button.clicked.connect(self.multiplayer)

        self.instructions_button = QPushButton("Instructions")
        self.instructions_button.clicked.connect(self.show_instructions)

        self.exit_button = QPushButton("Exit Game")
        self.exit_button.clicked.connect(self.close)

        layout.addWidget(self.single_player_button)
        layout.addWidget(self.multiplayer_button)
        layout.addWidget(self.instructions_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def single_player(self):
        difficulties = ["Easy", "Medium", "Hard"]
        difficulty, ok = QInputDialog.getItem(self, "Select Difficulty", "Choose difficulty level:", difficulties, 1, False)
        if ok and difficulty:
            run_game(difficulty.lower())

    def multiplayer(self):
        num_players, ok = QInputDialog.getInt(self, "Multiplayer", "Enter number of players:", 2, 1, 10)
        if ok:
            players = []
            for i in range(num_players):
                name, ok_name = QInputDialog.getText(self, "Player Name", f"Enter name for Player {i+1}:")
                if ok_name and name:
                    players.append(name)
                else:
                    QMessageBox.warning(self, "Input Error", "Player name cannot be empty.")
                    return
            difficulties = ["Easy", "Medium", "Hard"]
            difficulty, ok_diff = QInputDialog.getItem(self, "Select Difficulty", "Choose difficulty level:", difficulties, 1, False)
            if ok_diff and difficulty:
                scores = {}
                for player in players:
                    QMessageBox.information(self, "Next Player", f"{player}, get ready!")
                    score = run_game(difficulty.lower(), multiplayer=True, player_name=player)
                    scores[player] = score
                winner = max(scores, key=scores.get)
                QMessageBox.information(self, "Game Over", f"Winner: {winner} with {scores[winner]} points!")

    def show_instructions(self):
        instructions_page = InstructionsPage()
        instructions_page.exec_()
