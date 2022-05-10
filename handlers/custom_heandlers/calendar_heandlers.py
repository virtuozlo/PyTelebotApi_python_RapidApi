from loader import bot
from keyboards.inline.calendar_inline.inline_calendar import bot_get_keyboard_inline
from utils.misc.analyze_callback_calendar import exit_string_date, format_call_from_date


@bot.message_handler(commands=['calendar'])
def bot_get_keyboard(message):
    bot.send_message(message.chat.id, 'Ваш календарь', reply_markup=bot_get_keyboard_inline())


@bot.callback_query_handler(func=lambda call: call.data.startswith('DAY'))
def callback_inline(call):
    """
    Ловит выбор пользователя с календаря. Выводит дату либо меняет месяц
    :param call: Выбор пользователя
    """
    bot.edit_message_text(f'{exit_string_date(call.data)}', call.message.chat.id, call.message.id)
    date_calendar = format_call_from_date(
        call.data)  # Отформатированная дата, можно применять для сравнений
    bot.send_message(call.message.chat.id, date_calendar)
