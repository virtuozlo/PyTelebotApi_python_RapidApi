from loader import bot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import calendar
from datetime import date
from keyboards.inline.calendar_inline.inline_calendar import bot_get_keyboard_inline
from utils.misc.analyze_callback_calendar import exit_string_date, get_next_or_prev_mont, get_list_data


@bot.message_handler(commands=['calendar'])
def bot_get_keyboard(message):
    bot.send_message(message.chat.id, 'Ваш календарь', reply_markup=bot_get_keyboard_inline())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """
    Ловит выбор пользователя с календаря. Выводит дату либо меняет месяц
    :param call: Выбор пользователя
    """
    if call.data.startswith('EMPTY'):
        bot.answer_callback_query(callback_query_id=call.id,
                                  text='Выберите число!')  # Применить, когда тыкает в ненужное место
    else:
        date = get_list_data(call.data)
        if call.data.startswith('DAY'):
            bot.edit_message_text(f'{exit_string_date(call.data)}', call.message.chat.id, call.message.id)
        elif call.data.startswith('Prev') or call.data.startswith('Next'):
            action = 'prev' if call.data.startswith('Prev') else 'next'
            bot.edit_message_text('Месяц', call.message.chat.id, call.message.id,
                                  reply_markup=get_next_or_prev_mont(action=action, year=int(date[1]),
                                                                     month=int(date[2])))
