from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

from config_provider import config
from database import DatabaseHandler
from deck import Deck


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_handler = DatabaseHandler()
        self.setWindowTitle("FlashCardApp")
        self.resize(config.get_window_width(), config.get_window_height())
        self.create_initial_layout()

    def create_initial_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        initial_layout = QVBoxLayout()

        # toolbar buttons

        tool_bar_buttons_layout = QHBoxLayout()

        new_deck_button = QPushButton("New deck")
        tool_bar_buttons_layout.addWidget(new_deck_button)

        import_deck_button = QPushButton("Import deck")
        tool_bar_buttons_layout.addWidget(import_deck_button)

        # Label

        decks_label = QLabel("Your decks: ")
        decks_label.setFixedHeight(20)

        # Decks container

        frame = QFrame(self)
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        frame.setLineWidth(3)
        frame.setStyleSheet("border-color: black;")

        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        decks = [Deck(*d) for d in self.db_handler.get_all_decks()]
        for deck in decks:
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

            deck_frame.setLayout(deck_frame_layout)
            frame_layout.addWidget(deck_frame)

        frame.setLayout(frame_layout)

        # Final layout

        initial_layout.addLayout(tool_bar_buttons_layout)
        initial_layout.addWidget(decks_label)
        initial_layout.addWidget(frame)
        central_widget.setLayout(initial_layout)
        self.show()

