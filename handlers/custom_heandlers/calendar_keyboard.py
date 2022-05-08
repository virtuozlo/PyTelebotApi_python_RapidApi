from loader import bot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import calendar
from datetime import date
from keyboards.inline.calendar_inline.inline_calendar import bot_get_keyboard_inline


@bot.message_handler(commands=['calendar'])
def bot_get_keyboard(message):
    bot.send_message(message.chat.id, 'Ваша клавиатура', reply_markup=bot_get_keyboard_inline())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswich('DAY'):
        bot.send_message(call.message.chat.id, f'{call.data}')
    elif call.data.startswich('Prev'):
        bot.send_message(call.message.chat.id, 'Выбран пред месяц')
    elif call.data.startswich('Next'):
        bot.send_message(call.message.chat.id, 'Выбран след месяц')
    else:
        bot.answer_callback_query(callback_query_id=call.id, text='ssss')  # Применить, когда тыкает в ненужное место
    print(call.data)
