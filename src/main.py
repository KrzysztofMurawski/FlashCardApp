import sys

from PyQt6.QtWidgets import QApplication

from database import DatabaseHandler
from helpers import create_appdata_project_folder
from gui.gui import MainWindow



def main():
    create_appdata_project_folder()
    db_handler = DatabaseHandler()

    print(db_handler.get_all_decks())
    print(db_handler.get_all_cards())

    app = QApplication(sys.argv)
    main_window = MainWindow()
    app.exec()




if __name__ == "__main__":
    main()
