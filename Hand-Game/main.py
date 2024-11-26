import json
import cv2
import mediapipe as mp
import time
import random
import pygame

# Initialize Pygame
pygame.mixer.init()

# Function to load high score data
def load_high_score():
    try:
        with open('high_score.json', 'r') as file:
            high_score_data = json.load(file)
        return high_score_data
    except (FileNotFoundError, json.JSONDecodeError):
        return {'name': '', 'score': 0}

# Function to save high score data
def save_high_score(name, score):
    high_score_data = {'name': name, 'score': score}
    with open('high_score.json', 'w') as file:
        json.dump(high_score_data, file)

# Function to play background music
def play_background_music():
    pygame.mixer.music.load("score.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0)

# Function to play score sound
def play_score_sound():
    score_sound = pygame.mixer.Sound('laser_score.wav')
    score_sound.set_volume(0.5)
    score_sound.play()

# Game setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
score = 0
timer_started = False
start_time = 0
duration = 30
x_enemy = random.randint(50, 600)
y_enemy = random.randint(50, 400)

# Load previous high score
high_score_data = load_high_score()
high_score = high_score_data['score']
high_score_name = high_score_data['name']

# Initialize webcam
video = cv2.VideoCapture(0)

# Play background music
play_background_music()

# Set window size smaller and remove frame rate control
cv2.namedWindow('Hand Tracking', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Hand Tracking', 640, 480)  # Smaller window size

# Game loop
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        imageHeight, imageWidth, _ = image.shape
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255, 0, 255)
        text = cv2.putText(image, "Score", (480, 30), font, 1, color, 4, cv2.LINE_AA)
        text = cv2.putText(image, str(score), (590, 30), font, 1, color, 4, cv2.LINE_AA)

        # Enemy logic
        cv2.circle(image, (x_enemy, y_enemy), 25, (0, 200, 0), 5)

        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2))

        # Detect finger and score points
        if results.multi_hand_landmarks:
            for handLandmarks in results.multi_hand_landmarks:
                for point in mp_hands.HandLandmark:
                    normalizedLandmark = handLandmarks.landmark[point]
                    pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(
                        normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)

                    if pixelCoordinatesLandmark is not None:  # Ensure valid coordinates
                        if point == mp_hands.HandLandmark.INDEX_FINGER_TIP:
                            if (abs(pixelCoordinatesLandmark[0] - x_enemy) < 30) and (
                                    abs(pixelCoordinatesLandmark[1] - y_enemy) < 30):
                                x_enemy = random.randint(50, 600)
                                y_enemy = random.randint(50, 400)
                                score += 1
                                play_score_sound()  # Play score sound when a point is scored
                                if not timer_started:
                                    start_time = time.time()
                                    timer_started = True

        # Game timer logic
        if timer_started:
            remaining_time = max(0, duration - int(time.time() - start_time))
            time_text = "Time: {:02d}:{:02d}".format(remaining_time // 60, remaining_time % 60)
            cv2.putText(image, time_text, (10, 30), font, 1, (0, 255, 255), 2)

        cv2.imshow('Hand Tracking', image)

        if timer_started and time.time() - start_time > duration:
            if score > high_score:
                # New high score achieved, ask for player's name
                player_name = input("Congratulations!! You have a new high score! Please enter your name: ")
                save_high_score(player_name, score)
                high_score = score
                high_score_name = player_name
            break

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Display final score and high score
font = cv2.FONT_HERSHEY_SIMPLEX
final_score_text = f"Congratulations!! You scored {score} in this game."
final_score_x = (imageWidth - cv2.getTextSize(final_score_text, font, 1, 2)[0][0]) // 2
final_score_y = (imageHeight + cv2.getTextSize(final_score_text, font, 1, 2)[0][1]) // 2
cv2.putText(image, final_score_text, (final_score_x, final_score_y), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

high_score_text = f"High Score: {high_score_name} - {high_score}"
high_score_x = (imageWidth - cv2.getTextSize(high_score_text, font, 0.8, 2)[0][0]) // 2
high_score_y = final_score_y + 50
cv2.putText(image, high_score_text, (high_score_x, high_score_y), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

cv2.imshow('Hand Tracking', image)
cv2.waitKey(5000)  # Wait for 5 seconds before closing

video.release()
cv2.destroyAllWindows()
