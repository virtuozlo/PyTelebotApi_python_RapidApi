from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.filter import for_photo


def get_button_photo(state: str):
    """
    Делает две кнопки для необходимости фото
    :return: клавиатура
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Фото нужны', callback_data=for_photo.new(photo='True', state=state)),
                 InlineKeyboardButton('Фото не нужны', callback_data=for_photo.new(photo='False', state=state)))
    return keyboard
