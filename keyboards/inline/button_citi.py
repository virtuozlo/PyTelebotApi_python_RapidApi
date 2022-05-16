from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.filter import for_button


def get_button_cities(dict_buttons):
    """
    :param dict_buttons: словарь. ключ-название города значение-Destid
    :return: InlineKeyboardMarkup
    """
    if not dict_buttons:
        return 'Не нашел подходящего города'
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*[
        InlineKeyboardButton(name, callback_data=for_button.new(name=name[:10], destid=int(data)))
        for name, data in dict_buttons.items() if len(data) <= 10
    ])
    return keyboard
