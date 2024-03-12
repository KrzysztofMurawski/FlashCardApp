

class Deck:
    def __init__(self, deck_id, name):
        self.name = name
        self.deck_id = deck_id

    def study_deck(self):
        print(self.name, self.deck_id)