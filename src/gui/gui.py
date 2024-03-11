from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut
from PyQt6.QtCore import Qt

from src.config_provider import config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        frame.setLineWidth(1)
        frame.setStyleSheet("border-color: black;")

        frame_layout = QVBoxLayout()

        frame.setLayout(frame_layout)

        # Final layout

        initial_layout.addLayout(tool_bar_buttons_layout)
        initial_layout.addWidget(decks_label)
        initial_layout.addWidget(frame)
        central_widget.setLayout(initial_layout)
        self.show()

