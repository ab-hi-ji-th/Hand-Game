import cv2
import mediapipe as mp
import time
import random
import pygame
import json
from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox
import sys
from leaderboard import update_leaderboard

 
def show_leaderboard_and_options(difficulty):
    try: 
        with open("leaderboard.json", "r") as f:
            data = json.load(f) 
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if difficulty in data and data[difficulty]:
        top_scores = "\n".join([f"{entry['name']}: {entry['score']}" for entry in data[difficulty]])
    else:
        top_scores = "No scores yet."

    msg_box = QMessageBox()
    msg_box.setWindowTitle("Leaderboard")
    msg_box.setText(f"Top 5 for {difficulty.capitalize()}:\n\n{top_scores}")
    msg_box.setStandardButtons(QMessageBox.Close | QMessageBox.Retry)
    msg_box.button(QMessageBox.Close).setText("Exit")
    msg_box.button(QMessageBox.Retry).setText("Main Menu")

    choice = msg_box.exec_()
    if choice == QMessageBox.Retry:
        return "main_menu"
    else:
        return "exit"


def get_player_name():
    app = QApplication.instance()  # ✅ Check if an instance already exists
    if app is None:
        app = QApplication([])

    name, ok = QInputDialog.getText(None, "Enter Name", "Please enter your name:")
    if ok and name.strip():
        player_name = name.strip()
    else:
        player_name = "Player"
    return player_name


def main_menu():
    from start_menu import StartMenu
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    window = StartMenu()
    window.show()
    app.exec_()


def run_game(difficulty, multiplayer=False):
    player_name = get_player_name()

    settings = {
        "easy": {"target_radius": 40, "pink_duration": 5, "bonus_time": 5},
        "medium": {"target_radius": 25, "pink_duration": 3, "bonus_time": 3},
        "hard": {"target_radius": 15, "pink_duration": 2, "bonus_time": 2}
    }

    config = settings[difficulty]

    pygame.mixer.init()
    pygame.mixer.music.load("assets/score.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0)
    score_sound = pygame.mixer.Sound('assets/laser_score.wav')
    score_sound.set_volume(0.5)

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    score = 0
    timer_started = False
    start_time = 0
    duration = 30
    x_enemy = random.randint(50, 600)
    y_enemy = random.randint(50, 400)
    pink_target_visible = False
    pink_target_x = 0
    pink_target_y = 0
    hit_count = 0

    video = cv2.VideoCapture(0)
    cv2.namedWindow('Hand Tracking', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Hand Tracking', 640, 480)

    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            imageHeight, imageWidth, _ = image.shape
            results = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            font = cv2.FONT_HERSHEY_SIMPLEX
            color = (255, 0, 255)
            cv2.putText(image, "Score", (480, 30), font, 1, color, 4, cv2.LINE_AA)
            cv2.putText(image, str(score), (590, 30), font, 1, color, 4, cv2.LINE_AA)

            cv2.circle(image, (x_enemy, y_enemy), config["target_radius"], (0, 200, 0), 5)

            if hit_count >= 3 and not pink_target_visible:
                pink_target_visible = True
                pink_target_x = random.randint(50, 600)
                pink_target_y = random.randint(50, 400)
                hit_count = 0
                pink_target_time = time.time()

            if pink_target_visible:
                cv2.rectangle(image, (pink_target_x - 25, pink_target_y - 25),
                              (pink_target_x + 25, pink_target_y + 25), (255, 0, 255), -1)
                if time.time() - pink_target_time > config["pink_duration"]:
                    pink_target_visible = False

            if results.multi_hand_landmarks:
                for hand in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2,
                                                                     circle_radius=2))

            if results.multi_hand_landmarks:
                for handLandmarks in results.multi_hand_landmarks:
                    for point in mp_hands.HandLandmark:
                        normalizedLandmark = handLandmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(
                            normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)

                        if pixelCoordinatesLandmark is not None:
                            if point == mp_hands.HandLandmark.INDEX_FINGER_TIP:
                                if (abs(pixelCoordinatesLandmark[0] - x_enemy) < config["target_radius"] + 5) and \
                                        (abs(pixelCoordinatesLandmark[1] - y_enemy) < config["target_radius"] + 5):
                                    x_enemy = random.randint(50, 600)
                                    y_enemy = random.randint(50, 400)
                                    score += 1
                                    hit_count += 1
                                    score_sound.play()
                                    if not timer_started:
                                        start_time = time.time()
                                        timer_started = True

                                if pink_target_visible and (
                                        abs(pixelCoordinatesLandmark[0] - pink_target_x) < 30 and
                                        abs(pixelCoordinatesLandmark[1] - pink_target_y) < 30
                                ):
                                    duration += config["bonus_time"]
                                    pink_target_visible = False
                                    hit_count = 0

            if timer_started:
                remaining_time = max(0, duration - int(time.time() - start_time))
                time_text = "Time: {:02d}:{:02d}".format(remaining_time // 60, remaining_time % 60)
                cv2.putText(image, time_text, (10, 30), font, 1, (0, 255, 255), 2)

            cv2.imshow('Hand Tracking', image)

            if timer_started and time.time() - start_time > duration:
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()
    pygame.mixer.music.stop()

    update_leaderboard(difficulty, player_name, score)

    action = show_leaderboard_and_options(difficulty)

    if action == "main_menu":
        main_menu()
    else:
        sys.exit(0)


if __name__ == "__main__":
    run_game("easy")
