import os
import datetime
from math import sqrt
import random

project_path = os.path.abspath(os.path.join(__file__, "../.."))
appdata_project_directory = os.path.abspath(os.path.join(os.environ["APPDATA"], "FlashCardApp"))
database_path = os.path.abspath(os.path.join(appdata_project_directory, "database.db"))
config_file_path = os.path.join(project_path, "res", "config.ini")


def create_appdata_project_folder():
    if not os.path.exists(appdata_project_directory):
        os.mkdir(appdata_project_directory)


def choose_card(cards: list):
    scores = []
    for card in cards:
        last_reviewed_datetime = datetime.datetime.strptime(card[4], "%Y-%m-%d %H:%M:%S")
        time_difference = datetime.datetime.now() - last_reviewed_datetime
        scores.append(sqrt(time_difference.total_seconds()/60) * (10/card[3]) * (1/card[5]))

    combined = zip(cards, scores)
    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)
    sorted_cards = [card for card, score in sorted_combined]
    return random.choice(sorted_cards)
