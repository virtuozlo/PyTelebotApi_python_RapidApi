import calendar
from datetime import date
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot


def create_callback_data(action, year, month, day):
    """

    :param action: Действие из создания календаря
    :param year: год
    :param month: месяц
    :param day: день
    :return: Строку для callback_data
    """
    return ";".join([action, str(year), str(month), str(day)])


def get_list_data(data):
    """
    Делает список для callback
    :param data:
    :return:
    """
    return data.split(';')


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


@bot.callback_query_handler(func=lambda call: not call.data.startswith('DAY'))
def callback_inline(call):
    """
    Ловит выбор пользователя с календаря, если было выбрано перелистывание месяца
    :param call: Выбор пользователя
    """
    if call.data.startswith('EMPTY'):
        bot.answer_callback_query(callback_query_id=call.id,
                                  text='Выберите число!')  # Применить, когда тыкает в ненужное место
    else:
        date = get_list_data(call.data)
        action = 'prev' if call.data.startswith('Prev') else 'next'
        bot.edit_message_text('Месяц', call.message.chat.id, call.message.id,
                              reply_markup=get_next_or_prev_mont(action=action, year=int(date[1]),
                                                                 month=int(date[2])))
