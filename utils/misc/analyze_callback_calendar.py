"""
В перспективе сделать утилиты для вывода разных даты по выбранной дате: str,list,date и пр.
"""


def exit_string_date(data):
    """

    :param data: Информация с коллбэк календаря
    :return: Строку для вывода
    """
    date = data.split(';')[1:]
    exit_string = '/'.join(date)
    return f'Выбранная вами дата: {exit_string}'
