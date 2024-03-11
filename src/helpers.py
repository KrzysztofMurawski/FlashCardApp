import os

project_path = os.path.abspath(os.path.join(__file__, "../.."))
appdata_project_directory = os.path.abspath(os.path.join(os.environ["APPDATA"], "FlashCardApp"))
database_path = os.path.abspath(os.path.join(appdata_project_directory, "database.db"))
config_file_path = os.path.join(project_path, "res", "config.ini")


def create_appdata_project_folder():
    if not os.path.exists(appdata_project_directory):
        os.mkdir(appdata_project_directory)
