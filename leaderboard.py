import json
import os

 
def load_leaderboard(difficulty):
    os.makedirs('high_scores', exist_ok=True)
    path = os.path.join('high_scores', f"{difficulty}.json")
    if not os.path.exists(path):
        return []
    with open(path, 'r') as file:
        return json.load(file)


def save_leaderboard(difficulty, leaderboard):
    os.makedirs('high_scores', exist_ok=True)
    path = os.path.join('high_scores', f"{difficulty}.json")
    with open(path, 'w') as file:
        json.dump(leaderboard, file, indent=4)


def update_leaderboard(difficulty, name, score):
    leaderboard = load_leaderboard(difficulty)
    leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:5]
    save_leaderboard(difficulty, leaderboard)
    return leaderboard
