from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def cancel_states_button():
    """
    Reply кнопка для сброса статуса
    :return:
    """
    return KeyboardButton('/отмена')


def cancel_status_keyboard():
    """
    Функция для вызова клавиатуры с кнопкой сброса
    :return:
    """
    button = cancel_states_button()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(button)

    return keyboard
