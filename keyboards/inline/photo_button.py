from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.filter import for_photo
from utils.logger import logger


def get_button_photo(state: str) -> InlineKeyboardMarkup:
    """
    Делает две кнопки для необходимости фото
    :return: клавиатура
    """
    keyboard = InlineKeyboardMarkup()
    try:
        keyboard.add(InlineKeyboardButton('Фото нужны', callback_data=for_photo.new(photo='True', state=state)),
                     InlineKeyboardButton('Фото не нужны', callback_data=for_photo.new(photo='False', state=state)))
        logger.info(' ')
    except ValueError:
        logger.exception()
    return keyboard
