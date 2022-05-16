from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_button_photo():
    """
    Делает две кнопки для необходимости фото
    :return: клавиатура
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Фото нужны', callback_data='Нужны'),
                 InlineKeyboardButton('Фото не нужны', callback_data='Empty'))
    return keyboard