"""
В перспективе сделать утилиты для вывода разных даты по выбранной дате: str,list,date и пр.
"""
import datetime


def calendar_calldate_list(data):
    """
    :param data:Список с действием и датой
    :return:Дату списком [year,month,day]
    """
    return [int(elem) for elem in data.split(';')[1:]]


def format_call_from_date(data) -> datetime.date:
    """
    :param data: список с действием и датой
    :param data: меняется на список с числами даты
    :return: datetime.date
    """
    data = calendar_calldate_list(data)
    calendar_date = {
        'year': data[0],
        'month': data[1],
        'day': data[2],
    }
    return datetime.date(year=calendar_date['year'], month=calendar_date['month'], day=calendar_date['day'])


def exit_string_date(data):
    """
    :param data: Информация с коллбэк календаря
    :return: Строку для вывода в чат бота
    """
    data = format_call_from_date(data)
    return f'Выбранная вами дата: {data}'
