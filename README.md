````markdown
# 🎯 Hand Tracking Target Game 🖐️

A fun and interactive **hand-tracking target shooting game** using **OpenCV**, **MediaPipe**, **PyGame**, and **PyQt5** for GUI menus and leaderboards.  
The game detects your hand movements via webcam and challenges you to hit randomly spawning targets within a time limit.

---

## Features

- **Easy, Medium, and Hard difficulty levels** with different target sizes and durations.
- Real-time **hand tracking** powered by **MediaPipe Hands**.
- Scoring system with **sound effects**.
- **Pink bonus targets** that add extra time when hit.
- **High score leaderboard** saved locally in JSON files, with top 5 scores per difficulty.
- GUI menus for starting **single/multiplayer games**, instructions, and viewing leaderboards.
- Player name input collected **before the game starts**.
- Post-game leaderboard display with options to return to the **main menu** or exit.
- **Multiplayer support** with individual player scores and winner announcement.

---

## Demo Screenshot

![Demo Screenshot](path/to/screenshot.png)  
*(Add your game screenshot or gif here)*

---

## Installation

### 1. Clone this repository:

```bash
git clone https://github.com/yourusername/hand-tracking-target-game.git
cd hand-tracking-target-game
````

### 2. Set up a Python virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Dependencies

* Python 3.7+
* **OpenCV** (`opencv-python`)
* **MediaPipe** (`mediapipe`)
* **PyGame** (`pygame`)
* **PyQt5** (`PyQt5`)

The `requirements.txt` file includes all required libraries:

```
opencv-python
mediapipe
pygame
PyQt5
```

---

## Usage

### Running the Game

Run the main menu GUI:

```bash
python start_menu.py
```

This opens a window with options:

* **Single Player:** Select difficulty and start a solo game.
* **Multiplayer:** Enter number of players and their names, then select difficulty.
* **Instructions:** View gameplay instructions.
* **Exit Game:** Close the application.

### Controls

* Use your **index finger tip** to "hit" the green circular targets.
* After hitting 3 targets, a **pink square target** appears. Hitting it adds **bonus time**.
* The game runs for a fixed time based on difficulty.
* Press **`q`** at any time to quit the game.

---

## Project Structure

```
├── assets/                # Sound files and other assets
├── high_scores/           # Folder where leaderboard JSON files are saved
├── game.py                # Main gameplay logic and hand tracking
├── leaderboard.py         # Functions for leaderboard handling
├── start_menu.py          # PyQt5 main menu GUI
├── instructions.py        # Instructions page GUI (if implemented)
├── README.md              # This file
├── requirements.txt       # Python dependencies
```

---

## How it Works

* **Hand tracking:** Uses **MediaPipe** to detect hand landmarks via webcam.
* **Game logic:** Spawns targets, checks if the index finger tip hits targets, updates score and timer.
* **Leaderboard:** Scores are saved per difficulty level in JSON files inside the `high_scores` folder.
* **GUI:** PyQt5 interfaces handle user input (player names, difficulty selection) and show leaderboard with options to restart or exit.

---

## Contributing

Contributions are **welcome**!
Please follow these steps:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature-name`).
3. Make your changes.
4. Commit and push (`git commit -m 'Add feature' && git push`).
5. Open a Pull Request.

---

## Known Issues

* Ensure your **webcam** works with OpenCV.
* The game requires a reasonably powerful CPU to maintain **real-time hand tracking**.
* Sound file paths (`assets/score.wav` and `assets/laser_score.wav`) must be correct.

---

## License

MIT License © \[Abhijith p v]

---

## Contact

For questions or suggestions, open an issue or contact me at **\[[abhijithpv32@gmail.com](mailto:abhijithpv32@gmail.com)]**.

---

Enjoy playing! 🎉
