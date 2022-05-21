import sqlite3

from utils.logger import logger


class UserDb:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.set_up_db()

    def set_up_db(self):
        """
        :return: Создание базы данных
        """
        logger.info(' ')
        with self.connection:
            return self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS User(
            userId INT PRIMARY KEY ,
            fname TEXT,
            lname TEXT,
            AGE INT NOT NULL DEFAULT 1 )
            ''')

    def check_user(self, user_id):
        """
        :param user_id: идентификатор пользователя
        :return: Наличие/отсутствие пользователя
        """
        logger.info(' ')
        with self.connection:
            result = self.cursor.execute('SELECT `userId` FROM User WHERE `userId` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id):
        """
        :param user_id: Идентификатор пользователя
        :return: Добавить пользователя  БД
        """
        logger.info(' ')
        with self.connection:
            return self.cursor.execute('INSERT INTO User(UserId) VALUES (?)', (user_id,))

    def filling_db(self, data):
        """
        Функция записи информации о пользователе из State_handlers.
        :param data: State telebot
        :return:
        """
        logger.info(' ')
        with self.connection:
            self.cursor.execute('UPDATE User SET fname=?,lname=?,AGE=? WHERE userID=?',
                                (data['name'], data['surname'], data['age'], data['id']))
