import sqlite3


def set_up_db():
    """
    Создание базы данных
    :return:
    """
    con = sqlite3.connect('user.db')
    with con:
        con.execute('''
        CREATE TABLE IF NOT EXISTS User(
        userId INT PRIMARY KEY ,
        fname TEXT,
           lname TEXT,
           AGE INT NOT NULL )
        ''')


def filling_db(data):
    """
    Функция записи информации о пользователе из State_handlers.Если пользователь есть, то обновляет данные
    :param data: State telebot
    :return:
    """
    cur = sqlite3.connect('user.db')
    with cur:
        cur.execute('SELECT userId FROM User WHERE userId = (?)', (data['id'],))
        dat = cur.cursor().fetchall()
        if len(dat) != 0:
            cur.execute('UPDATE User SET fname=?,lname=?,AGE=? WHERE userID=?',
                        (data['name'], data['surname'], data['age'], data['id']))
        else:
            cur.execute('''
            INSERT INTO User(userID,fname,lname,AGE)
            VALUES (?,?,?,?)''', (data['id'], data['name'], data['surname'], data['age']))
