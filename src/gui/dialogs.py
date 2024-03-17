from PyQt6.QtWidgets import *


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
