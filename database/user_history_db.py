import sqlite3
import json


class HistoryUserDb:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.set_up_table()

    def set_up_table(self):
        with self.connection:
            return self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserHistory(
            userID INT,
            search_date datetime DEFAULT CURRENT_DATE,
            command TEXT,
            data json)
            ''')

    def set_data(self, user_id: int, command: str, data: dict) -> sqlite3.connect('history_user.db').cursor():
        """
        Запись в БД пользователя, введенной команды и словаря отелей
        :param user_id: идентификатор пользователя
        :param command: команда поиска отелей
        :param data:
        :return:
        """
        with self.connection:
            return self.cursor.execute('''
            INSERT INTO UserHistory(`userId`,`command`,`data`)
            VALUES (?,?,?)''', (user_id, command, json.dumps(data)))
