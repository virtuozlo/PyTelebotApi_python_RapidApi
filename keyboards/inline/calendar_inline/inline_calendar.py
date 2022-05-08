import calendar
from datetime import date
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_callback_data(action, year, month, day):
    """

    :param action: Действие из создания календаря
    :param year: год
    :param month: месяц
    :param day: день
    :return: Строку для callback_data
    """
    return ";".join([action, str(year), str(month), str(day)])


def exit_string_data(data):
    """
    Делает список для callback
    :param data:
    :return:
    """
    return data.split(';')


def bot_get_keyboard_inline(year=None, month=None) -> InlineKeyboardMarkup:
    """
    Функция делает Inline клавиатуру-календарь

    :param year: Текущий год, если не задано иное
    :param month: Текущий месяц, если не задано иное
    :return: InlineKeyboardMarkup
    """

    month = date.today().month if month is None else month
    year = date.today().year if year is None else year
    my_calendar = calendar.monthcalendar(year, month)
    keyboard = InlineKeyboardMarkup()
    empty_data = create_callback_data('EMPTY', year, month, 0)  # Пустая дата для месяца и дня недели
    days_of_week = [InlineKeyboardButton(day, callback_data=empty_data) for day in [
        'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'
    ]]
    keyboard.add(InlineKeyboardButton(f'{calendar.month_name[month]}', callback_data=empty_data))
    keyboard.add(*days_of_week, row_width=7)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(' ', callback_data=empty_data))
            else:
                row.append(InlineKeyboardButton(day, callback_data=create_callback_data('DAY', year, month, day)))
        keyboard.add(*row, row_width=7)
    keyboard.add(
        InlineKeyboardButton('<<', callback_data=create_callback_data('Prev-month', year, month, day=1)),
        InlineKeyboardButton('>>', callback_data=create_callback_data('Next-month', year, month, day=1)),
    )
    return keyboard

