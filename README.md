# Hand Tracking Game with High Score Tracking

This repository contains a Python-based hand tracking game that allows users to score points by interacting with on-screen objects using hand gestures. The game utilizes the webcam to detect hand movements and provides a high score system that saves and loads the player's best score. The game displays real-time feedback on the score, high score, and remaining time.

## Features

- **Hand Gesture Detection**: The game uses the webcam to track hand movements and detects finger positions.
- **Score System**: Players score points by interacting with a randomly moving enemy object.
- **High Score**: The game stores the highest score and player's name in a local JSON file (`high_score.json`).
- **Background Music**: Background music is played during the game to enhance the experience.
- **Sound Effects**: A sound effect is played each time the player scores a point.
- **Timer**: The game has a time limit, and the score is reset after the time expires.
- **Final Score Display**: At the end of the game, the final score and the high score are displayed.
- **Customizable**: The window size and other settings are adjustable.

## Dependencies

The following libraries are required to run this game:

- **OpenCV**: For real-time video capture and image processing.
- **MediaPipe**: For hand landmark detection.
- **Pygame**: For playing sound effects and background music.
- **JSON**: For saving and loading the high score data.

### To install the required libraries, run:

```bash
pip install opencv-python mediapipe pygame
```

## How to Play

1. **Start the Game**: Run the script to start the game. Ensure that your webcam is connected and accessible.
2. **Gameplay**:
   - Move your hand in front of the webcam.
   - Score points by bringing your hand close to the moving green enemy circle.
   - The score will increase each time you interact with the enemy.
   - The game will automatically start a timer, and when the time expires, the final score will be displayed.
3. **High Score**: If your score beats the current high score, you will be prompted to enter your name. This name will be saved along with your score in the `high_score.json` file.
4. **Exit**: To exit the game at any time, press the 'Q' key.

## Game Flow

1. **Hand Detection**: The game uses MediaPipe to track the user's hand landmarks in real-time.
2. **Point Scoring**: The game continuously checks if the player's index finger tip comes close to the enemy object. If so, the player scores a point, and the enemy object moves to a new random position.
3. **Timer**: The game runs for a fixed duration (30 seconds) and stops when the timer reaches zero.
4. **High Score**: After the game ends, if the player achieves a new high score, they will be asked to provide their name, which will then be saved in the `high_score.json` file.
5. **Final Display**: The final score and high score are shown on the screen for 5 seconds after the game ends before the program exits.

## Code Explanation

### 1. **High Score Functions**
   - `load_high_score()`: Loads the high score data from the `high_score.json` file. If the file doesn't exist or is empty, it returns default values.
   - `save_high_score(name, score)`: Saves the new high score with the player's name to the `high_score.json` file.

### 2. **Sound Functions**
   - `play_background_music()`: Plays the background music (`score.wav`) when the game starts.
   - `play_score_sound()`: Plays a sound effect (`laser_score.wav`) whenever the player scores a point.

### 3. **Main Game Loop**
   - The game loop captures frames from the webcam, processes them to detect hand landmarks, and checks if the player's index finger interacts with the enemy object.
   - The score is updated each time the player successfully interacts with the enemy.
   - The timer counts down, and when the time is up, the final score is displayed, and the game ends.

### 4. **Timer Logic**
   - The remaining time is displayed on the screen in the format `Time: MM:SS`.
   - The game checks whether the timer has expired and updates the high score if needed.

### 5. **Enemy Object Logic**
   - The enemy object is drawn as a green circle that moves randomly on the screen.
   - The enemy moves to a new random location when the player scores a point.

### 6. **End of Game**
   - When the timer expires, the game will prompt the user to enter their name if they beat the high score.
   - The final score and the high score are displayed on the screen for 5 seconds.

## Files in the Repository

- `game.py`: The main script that runs the game.
- `high_score.json`: Stores the high score and the player's name.
- `score.wav`: Background music played during the game.
- `laser_score.wav`: Sound effect played when the player scores a point.

## To Run the Game

1. Clone this repository to your local machine.
2. Ensure the required libraries (`opencv-python`, `mediapipe`, and `pygame`) are installed.
3. Run the `game.py` script in your terminal or IDE.

```bash
python game.py
```

The game will start, and you can interact with it using your hand in front of the webcam.

## Notes

- Ensure your webcam is properly connected and accessible by OpenCV.
- If you want to change the game's duration, you can modify the `duration` variable in the code.
- You can also adjust the window size or disable the full-screen mode by modifying the `cv2.resizeWindow()` settings.

---

