

class Deck:
    def __init__(self, deck_id, name):
        self.name = name
        self.deck_id = deck_id


class Card:
    def __init__(self, card_id, question, answer, revisions, last_revision, last_evaluation):
        self.card_id = card_id
        self.question = question
        self.answer = answer
        self.revisions = revisions
        self.last_revision = last_revision
        self.last_evaluation = last_evaluation

