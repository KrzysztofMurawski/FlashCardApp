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
        frame.setFrameShadow(QFrame.Shadow.Raised)
        frame.setLineWidth(3)
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


    def display_deck_tile(self, deck):
        deck_frame = QFrame(self)
        deck_frame.setFrameShape(QFrame.Shape.Box)
        deck_frame.setFrameShadow(QFrame.Shadow.Raised)
        deck_frame.setLineWidth(1)
        deck_frame.setStyleSheet("border-color: grey;")
        deck_frame.setFixedHeight(50)
        deck_frame_layout = QHBoxLayout()
        deck_frame_layout.addWidget(QLabel(deck.name))

        study_deck_button = QPushButton("Study")
        study_deck_button.clicked.connect(partial(deck.study_deck))
        deck_frame_layout.addWidget(study_deck_button)

        edit_deck_button = QPushButton("Edit")
        edit_deck_button.clicked.connect(partial(self.create_deck_editing_layout, deck))
        deck_frame_layout.addWidget(edit_deck_button)

        deck_frame.setLayout(deck_frame_layout)
        self.frame_layout.addWidget(deck_frame)

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
        frame.setFrameShadow(QFrame.Shadow.Raised)
        frame.setLineWidth(3)
        frame.setStyleSheet("border-color: black;")

        self.frame_layout = QVBoxLayout()
        self.frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Display card tiles

        cards = [Card(*args) for args in self.db_handler.get_cards_from_deck(deck.deck_id)]


        # Init layout

        frame.setLayout(self.frame_layout)
        scroll_area.setWidget(frame)

        edit_layout.addLayout(top_row)
        edit_layout.addWidget(scroll_area)
        central_widget.setLayout(edit_layout)
        self.show()

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
