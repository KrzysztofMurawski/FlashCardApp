from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from config_provider import config
from database import DatabaseHandler
from objects import Deck, Card


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.frame_scrollable = None
        self.frame_layout = None
        self.db_handler = DatabaseHandler()
        self.setWindowTitle("FlashCardApp")
        self.resize(config.get_window_width(), config.get_window_height())
        self.create_initial_layout()

    def create_initial_layout(self):
        self.setWindowTitle("FlashCardApp")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        initial_layout = QVBoxLayout()

        # toolbar buttons

        tool_bar_buttons_layout = QHBoxLayout()

        new_deck_button = QPushButton("New deck")
        new_deck_button.clicked.connect(self.new_deck)
        tool_bar_buttons_layout.addWidget(new_deck_button)

        import_deck_button = QPushButton("Import deck")
        tool_bar_buttons_layout.addWidget(import_deck_button)

        # Label

        decks_label = QLabel("Your decks: ")
        decks_label.setFixedHeight(20)

        # Decks container

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        frame = QFrame(self)
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setLineWidth(1)
        frame.setStyleSheet("border-color: black;")

        self.frame_layout = QVBoxLayout()
        self.frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        decks = [Deck(*d) for d in self.db_handler.get_all_decks()]
        for deck in decks:
            self.display_deck_tile(deck)

        frame.setLayout(self.frame_layout)
        scroll_area.setWidget(frame)
        # Final layout

        initial_layout.addLayout(tool_bar_buttons_layout)
        initial_layout.addWidget(decks_label)
        initial_layout.addWidget(scroll_area)
        central_widget.setLayout(initial_layout)
        self.show()

    def create_deck_editing_layout(self, deck):
        self.setWindowTitle(f"Edit {deck.name} deck")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        edit_layout = QVBoxLayout()

        # top row with buttons and label

        top_row = QHBoxLayout()

        exit_btn = QPushButton("Go back")
        exit_btn.clicked.connect(partial(self.create_initial_layout))
        top_row.addWidget(exit_btn)

        new_card_btn = QPushButton("New card")
        new_card_btn.clicked.connect(partial(self.new_card, deck))
        top_row.addWidget(new_card_btn)

        # Scrollable Frame for card tiles

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        frame = QFrame(self)
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setLineWidth(1)
        frame.setStyleSheet("border-color: black;")

        self.frame_layout = QVBoxLayout()
        self.frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Display card tiles

        cards = [Card(*args) for args in self.db_handler.get_cards_from_deck(deck.deck_id)]
        for card in cards:
            self.display_card_tile(card, deck)

        # Init layout

        frame.setLayout(self.frame_layout)
        scroll_area.setWidget(frame)

        edit_layout.addLayout(top_row)
        edit_layout.addWidget(scroll_area)
        central_widget.setLayout(edit_layout)
        self.show()

    def create_deck_studying_layout(self, deck: Deck):
        self.setWindowTitle(f"FlashCardApp: {deck.name}")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        studying_layout = QVBoxLayout()

        # question section
        question_label = QLabel("Question:")
        question_label.setFixedHeight(30)

        question_scroll_area = QScrollArea()
        question_scroll_area.setWidgetResizable(True)

        question_content_frame = QFrame(self)
        question_content_frame.setFrameShape(QFrame.Shape.Box)
        question_content_frame.setLineWidth(1)
        question_content_frame.setStyleSheet("border-color: black;")

        question_content_layout = QVBoxLayout()
        question_content_label = QLabel("There will be question \n\n\n maybe multiline")
        question_content_layout.addWidget(question_content_label)
        question_content_frame.setLayout(question_content_layout)

        question_scroll_area.setWidget(question_content_frame)

        # answer section

        answer_label = QLabel("Answer:")
        answer_label.setFixedHeight(30)

        answer_scroll_area = QScrollArea()
        answer_scroll_area.setWidgetResizable(True)

        answer_content_frame = QFrame(self)
        answer_content_frame.setFrameShape(QFrame.Shape.Box)
        answer_content_frame.setLineWidth(1)
        answer_content_frame.setStyleSheet("border-color: black;")

        answer_content_layout = QVBoxLayout()
        answer_content_label = QLabel()
        answer_content_layout.addWidget(answer_content_label)
        answer_content_frame.setLayout(answer_content_layout)

        answer_scroll_area.setWidget(answer_content_frame)

        # Bottom buttons bar

        buttons_bar = QHBoxLayout()

        exit_studying_button = QPushButton("Exit")
        exit_studying_button.clicked.connect(partial(self.create_initial_layout))

        show_answer_button = QPushButton("Show answer")

        difficulty_rating_label = QLabel("Difficulty rating: ")


        buttons_bar.addWidget(exit_studying_button)
        buttons_bar.addWidget(show_answer_button)
        buttons_bar.addWidget(difficulty_rating_label)


        # Init layout

        studying_layout.addWidget(question_label)
        studying_layout.addWidget(question_scroll_area)
        studying_layout.addWidget(answer_label)
        studying_layout.addWidget(answer_scroll_area)
        studying_layout.addLayout(buttons_bar)
        central_widget.setLayout(studying_layout)
        self.show()

    def display_deck_tile(self, deck: Deck):
        deck_frame = QFrame(self)
        deck_frame.setFrameShape(QFrame.Shape.Box)
        deck_frame.setLineWidth(1)
        deck_frame.setStyleSheet("border-color: grey;")
        deck_frame.setFixedHeight(50)
        deck_frame_layout = QHBoxLayout()
        deck_frame_layout.addWidget(QLabel(deck.name))

        study_deck_button = QPushButton("Study")
        study_deck_button.clicked.connect(partial(self.create_deck_studying_layout, deck))
        deck_frame_layout.addWidget(study_deck_button)

        edit_deck_button = QPushButton("Edit")
        edit_deck_button.clicked.connect(partial(self.create_deck_editing_layout, deck))
        deck_frame_layout.addWidget(edit_deck_button)

        deck_frame.setLayout(deck_frame_layout)
        self.frame_layout.addWidget(deck_frame)


    def display_card_tile(self, card: Card, deck: Deck):
        card_frame = QFrame(self)
        card_frame.setFrameShape(QFrame.Shape.Box)
        card_frame.setLineWidth(1)
        card_frame.setStyleSheet("border-color: grey;")
        card_frame.setContentsMargins(1, 1, 1, 1)

        card_frame.setFixedHeight(75)
        card_frame_layout = QHBoxLayout()

        question_edit = QTextEdit()
        question_edit.setText(card.question)
        question_edit.textChanged.connect(partial(self.question_editing_finished, card, question_edit))
        card_frame_layout.addWidget(question_edit)

        answer_edit = QTextEdit()
        answer_edit.setText(card.answer)
        answer_edit.textChanged.connect(partial(self.answer_editing_finished, card, answer_edit))
        card_frame_layout.addWidget(answer_edit)

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(partial(self.delete_card, card, deck))
        card_frame_layout.addWidget(delete_btn)

        card_frame.setLayout(card_frame_layout)
        self.frame_layout.addWidget(card_frame)

    def new_deck(self):
        dialog = DeckNameInputDialog()
        dialog.exec()
        deck_name = dialog.deck_name
        if deck_name:
            self.db_handler.insert_new_deck(deck_name)
            index = len(self.db_handler.get_all_decks())
            self.display_deck_tile(Deck(index, deck_name))

    def new_card(self, deck):
        dialog = NewCardInputDialog()
        dialog.exec()
        question = dialog.question
        answer = dialog.answer
        if question and answer:
            self.db_handler.insert_new_card(deck.deck_id, question, answer)
            self.create_deck_editing_layout(deck)

    def delete_card(self, card: Card, deck: Deck):
        self.db_handler.delete_card_from_deck(card.card_id, deck.deck_id)
        self.create_deck_editing_layout(deck)

    def question_editing_finished(self, card: Card, new_question: QTextEdit):
        self.db_handler.update_card_question_content(card.card_id, new_question.toPlainText())

    def answer_editing_finished(self, card: Card, new_answer: QTextEdit):
        self.db_handler.update_card_answer_content(card.card_id, new_answer.toPlainText())


class DeckNameInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.deck_name = None
        self.setWindowTitle("Name your deck")

        layout = QVBoxLayout()

        # Create input field
        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        # Create OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.handle_ok_button)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def handle_ok_button(self):
        input_value = self.input_field.text()
        self.deck_name = input_value
        self.accept()


class NewCardInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.question = None
        self.answer = None
        self.setWindowTitle("Create new card")

        layout = QVBoxLayout()

        self.question_input = QLineEdit()
        layout.addWidget(self.question_input)

        self.answer_input = QLineEdit()
        layout.addWidget(self.answer_input)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.handle_ok_button)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def handle_ok_button(self):
        self.answer = self.answer_input.text()
        self.question = self.question_input.text()
        self.accept()
