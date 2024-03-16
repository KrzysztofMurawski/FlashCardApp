import sqlite3
from helpers import database_path


class DatabaseHandler:
    def __init__(self):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def update_card_question_content(self, card_id: int, new_question: str):
        self.cursor.execute("UPDATE card SET question = ? WHERE rowid = ?", (new_question, card_id))
        self.commit()

    def update_card_answer_content(self, card_id: int, new_answer: str):
        self.cursor.execute("UPDATE card SET answer = ? WHERE rowid = ?", (new_answer, card_id))
        self.commit()

    def insert_new_deck(self, deck_name):
        self.cursor.execute(f"INSERT INTO deck VALUES ( ? )", (deck_name,))
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

    def get_cards_from_deck(self, deck_id):
        self.cursor.execute("SELECT card_id FROM deck_card WHERE deck_id = ?", (deck_id,))
        card_ids = self.cursor.fetchall()
        self.cursor.execute(f"""SELECT rowid, *
                                FROM card
                                WHERE rowid IN ({", ".join([str(card_id[0]) for card_id in card_ids])})
                            """)
        return self.cursor.fetchall()

    def get_all_deck_card_pairs(self):
        self.cursor.execute("SELECT * FROM deck_card")
        return self.cursor.fetchall()

    def delete_card_from_deck(self, card_id, deck_id):
        self.cursor.execute("DELETE FROM deck_card WHERE deck_id = ? AND card_id = ?", (deck_id, card_id))
        self.cursor.execute("DELETE FROM card WHERE rowid = ?", (card_id,))
        self.commit()

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
                    revisions INTEGER DEFAULT 0,
                    last_revision TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_evaluation INTEGER DEFAULT 1
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


