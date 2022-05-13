from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from loader import bot


def boolean_keyboard(button=None):
    """
    Функция делает две кнопки с датой True или False
    :return:
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton('Нужно'),
                 KeyboardButton('Отказ'))
    if button:
        keyboard.add(button)

    return keyboard
