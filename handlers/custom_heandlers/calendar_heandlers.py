from loader import bot
from datetime import date
from keyboards.inline.calendar_inline.inline_calendar import bot_get_keyboard_inline
from keyboards.inline.filter import my_date


@bot.message_handler(commands=['calendar'])
def bot_get_keyboard(message):
    bot.send_message(message.chat.id, 'Ваш календарь', reply_markup=bot_get_keyboard_inline())


@bot.callback_query_handler(func=None, my_date_config=my_date.filter())
def callback_inline(call):
    """
    Ловит выбор пользователя с календаря. Выводит дату либо меняет месяц
    :param call: Выбор пользователя
    """
    print('calendar_handler')
    data = my_date.parse(callback_data=call.data)
    print(data)
    my_exit_date = date(year=int(data['year']), month=int(data['month']), day=int(data['day']))
    bot.edit_message_text(my_exit_date, call.message.chat.id, call.message.id)
