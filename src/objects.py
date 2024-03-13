from database import DatabaseHandler


class Deck:
    def __init__(self, deck_id, name):
        self.name = name
        self.deck_id = deck_id

        self.db_handler = DatabaseHandler()

    def study_deck(self):
        print(self.name, self.deck_id)


class Card:
    def __init__(self, deck_id, question, answer):
        self.deck_id = deck_id,
        self.question = question,
        self.answer = answer

