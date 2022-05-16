import calendar
from datetime import date
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from loader import bot
from .filter import calendar_factory, my_date, for_search


def get_next_or_prev_mont(action, year, month):
    """
    Функция корректирует год и месяц если пользователь нажал на стрелочки выбора месяца
    :param action: След или предыдущий месяц
    :param year: год с коллбэка
    :param month: месяц оттуда же
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


def bot_get_keyboard_inline(year=None, month=None, command='calendar') -> InlineKeyboardMarkup:
    """
    Функция делает Inline клавиатуру-календарь

    :param command: Для формирования коллбэкДаты
    :param year: Текущий год, если не задано иное
    :param month: Текущий месяц, если не задано иное
    :return: InlineKeyboardMarkup
    """

    month = date.today().month if month is None else month
    year = date.today().year if year is None else year
    my_calendar = calendar.monthcalendar(year, month)
    for_data = my_date if command == 'calendar' else for_search
    keyboard = InlineKeyboardMarkup()
    empty_data = 'EMPTY'  # Пустая дата для месяца и дня недели

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
                row.append(InlineKeyboardButton(day, callback_data=for_data.new(year=year, month=month, day=day)))
        keyboard.add(*row, row_width=7)
    keyboard.add(
        InlineKeyboardButton('<<', callback_data=calendar_factory.new(action="prev", year=year, month=month)),
        InlineKeyboardButton('>>', callback_data=calendar_factory.new(action="next", year=year, month=month)),
    )
    return keyboard


@bot.callback_query_handler(func=None, calendar_config=calendar_factory.filter())
def callback_inline(call: CallbackQuery):
    """
    Ловит выбор пользователя с календаря, если было выбрано перелистывание месяца
    :param call: Выбор пользователя
    """
    callback_data = calendar_factory.parse(callback_data=call.data)
    print(callback_data)
    action, year, month = (callback_data['action'], int(callback_data['year']), int(callback_data['month']))
    bot.edit_message_text('Месяц', call.message.chat.id, call.message.id,
                          reply_markup=get_next_or_prev_mont(action=action, year=year,
                                                             month=month))


@bot.callback_query_handler(func=lambda call: call.data.startswith('EMPTY'))
def if_empty_callback(call: CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id,
                              text='Выберите число!')  # Применить, когда тыкает в ненужное место
