import sqlite3
from src.helpers import database_path


class DatabaseHandler:
    def __init__(self):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()
        self.create_tables_if_dont_exist()

    def insert_new_deck(self, deck_name):
        self.cursor.execute(f"INSERT INTO decks VALUES ( '{deck_name}' )")
        self.commit()

    def insert_new_card(self, deck_id, question, answer):
        self.cursor.execute(f"INSERT INTO cards VALUES ('{deck_id}', '{question}', '{answer}', 1, NULL)")
        self.commit()

    def get_all_decks(self):
        self.cursor.execute("SELECT rowid, * FROM decks")
        return self.cursor.fetchall()

    def get_all_cards(self):
        self.cursor.execute("SELECT rowid, * FROM cards")
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def create_tables_if_dont_exist(self):
        try:
            self.cursor.execute("""CREATE TABLE decks (
                deck_name text
            )""")
            self.cursor.execute("""
                CREATE TABLE cards (
                    deck_id INTEGER,
                    question TEXT,
                    answer TEXT,
                    last_reviewed TIMESTAMP,
                    last_confidence INTEGER,
                    FOREIGN KEY (deck_id) REFERENCES decks(deck_id)
                )""")
            self.commit()
        except sqlite3.OperationalError:
            pass


