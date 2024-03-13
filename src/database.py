import sqlite3
from helpers import database_path


class DatabaseHandler:
    def __init__(self):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()
        self.create_tables_if_dont_exist()

    def insert_new_deck(self, deck_name):
        self.cursor.execute(f"INSERT INTO deck VALUES ( '{deck_name}' )")
        self.commit()

    def insert_new_card(self, deck_id, question, answer):
        self.cursor.execute("INSERT INTO card VALUES (?, ?, 0, ?, 1)", (question, answer, None))
        card_id = self.cursor.lastrowid
        self.cursor.execute("INSERT INTO deck_card VALUES (?, ?)", (deck_id, card_id))
        self.commit()

    def get_all_decks(self):
        self.cursor.execute("SELECT rowid, * FROM deck")
        return self.cursor.fetchall()

    def get_all_cards(self):
        self.cursor.execute("SELECT rowid, * FROM card")
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def create_tables_if_dont_exist(self):
        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS deck (
                deck_name text
            )""")

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS card (
                    question TEXT,
                    answer TEXT,
                    repeats INTEGER DEFAULT 0,
                    last_reviewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_confidence INTEGER DEFAULT 1
                )""")

            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS deck_card (
                deck_id INTEGER,
                card_id INTEGER,
                FOREIGN KEY (deck_id) REFERENCES deck(deck_id),
                FOREIGN KEY (card_id) REFERENCES card(card_id),
                PRIMARY KEY (deck_id, card_id)
            )""")
            self.commit()
        except sqlite3.OperationalError as e:
            print("ERROR creating tables", e)


