from keyboards.inline.calendar_inline.inline_calendar import bot_get_keyboard_inline


def get_list_data(data):
    """
    Делает список для callback
    :param data:
    :return:
    """
    return data.split(';')


def exit_string_date(data):
    """

    :param data: Информация с коллбэк календаря
    :return: Строку для вывода
    """
    date = data.split(';')[1:]
    exit_string = '/'.join(date)
    return f'Выбранная вами дата: {exit_string}'


def get_next_or_prev_mont(action, year, month):
    """
    Функция корректирует год и месяц если пользователь нажал на стрелочки выбора месяца
    :param action: След или предыдущий месяц
    :param year: год с коллбэка
    :param month: месяц оттудаже
    :return: клавиатуру с новыми данными
    """
    if action == 'next':
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
    else:
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    return bot_get_keyboard_inline(year=year, month=month)
