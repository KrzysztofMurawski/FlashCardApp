import sys

from PyQt6.QtWidgets import QApplication

from src.database import DatabaseHandler
from src.helpers import create_appdata_project_folder
from src.gui.gui import MainWindow


def main():
    create_appdata_project_folder()
    db_handler = DatabaseHandler()
    print(db_handler.get_all_decks())

    app = QApplication(sys.argv)
    main_window = MainWindow()
    app.exec()



if __name__ == "__main__":
    main()
