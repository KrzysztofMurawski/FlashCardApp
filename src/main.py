from database import DatabaseHandler
from helpers import create_appdata_project_folder


def main():
    create_appdata_project_folder()
    db_handler = DatabaseHandler()

    db_handler.close()


if __name__ == "__main__":
    main()
