from datetime import date

from telebot.types import InputMediaPhoto, Message, CallbackQuery

from loader import bot
from utils.logger import logger
from states.search_info import HighPriceStates
from keyboards.inline.filter import for_search, for_button, for_photo, for_start
from keyboards.inline.calendar_inline.inline_calendar import bot_get_keyboard_inline
from keyboards.inline.photo_button import get_button_photo
from utils.requests_rapidApi.get_properties_list import get_properties_list
from utils.requests_rapidApi.get_id_search import get_dest_id
from utils.requests_rapidApi.get_photo_hotel import get_photo_hotel


@bot.callback_query_handler(func=None, start_config=for_start.filter(action='highprice'))
def start_highprice(call):
    """
    Выбор возрастания цены
    :param call:
    :return:
    """
    logger.info(' ')
    bot.set_state(call.from_user.id, HighPriceStates.cities, call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Отлично! Вы выбрали поиск топовых отелей. Выберите город для поиска.')


@bot.message_handler(commands=['highprice'])
def start_highprice(message: Message) -> None:
    """
    Начало работы команды поиска дешёвых отелей
    :param message:
    :return:
    """
    logger.info(f'user_id {message.from_user.id}')
    bot.set_state(message.from_user.id, HighPriceStates.cities, message.chat.id)
    bot.send_message(message.chat.id, 'Отлично! Вы выбрали поиск топовых отелей. Выберите город для поиска.')


@bot.message_handler(state=HighPriceStates.cities)
def get_cities_request(message: Message) -> None:
    """
    Вывод кнопок городов и их обработка
    :param message:
    :return:
    """
    logger.info(f'user_id {message.from_user.id}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['id'] = message.from_user.id
        data['SortOrder'] = 'PRICE_HIGHEST_FIRST'
        data['locale'] = 'ru_RU'
        data['currency'] = 'USD'
        data['city'] = message.text
        logger.info(f'user_id {message.from_user.id}')
        keyboard = get_dest_id(message.text, data['locale'], data['currency'], state='High_state')
        if not isinstance(keyboard,str):
            logger.info(f'user_id {message.from_user.id} {message.text}')
            bot.send_message(message.chat.id, 'Выберите подходящий город:', reply_markup=keyboard)
        else:
            logger.error(f'user_id {message.from_user.id}')
            bot.send_message(message.chat.id, f'{keyboard}')
            bot.set_state(message.from_user.id, HighPriceStates.cities)


@bot.callback_query_handler(func=None, button_config=for_button.filter(state='High_state'))
def button_callback(call: CallbackQuery) -> None:
    """
    Обработка кнопок городов
    :param call:
    :return:
    """
    logger.info(f'user_id {call.from_user.id}')
    bot.set_state(call.from_user.id, HighPriceStates.start_date, call.message.chat.id)
    callback_data = for_button.parse(callback_data=call.data)
    name, destid = callback_data['name'], int(callback_data['destid'])
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['destid'] = destid
        data['city'] = name
        logger.info(f'user_id {call.from_user.id}{destid, name}')
        bot.edit_message_text(f'Отличный выбор {name}', call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, f'Выберите даты заезда',
                     reply_markup=bot_get_keyboard_inline(command='highprice', state='high_start_date'))


@bot.message_handler(state=HighPriceStates.count_hotels, is_digit=True, count_digit=True, )
def get_photo_info(message: Message) -> None:
    """
    Запрос фотографий отелей. Запись количества отелей
    :param message:
    :return:
    """
    logger.info(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, f'Буду выводить {message.text} отелей')
    bot.send_message(message.chat.id, f'Нужны фото отелей?',
                     reply_markup=get_button_photo(state='High_state'))
    bot.set_state(message.from_user.id, HighPriceStates.photo, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_hotels'] = message.text


@bot.message_handler(state=HighPriceStates.count_photo, is_digit=True, count_digit=True)
def get_photo_info(message: Message) -> None:
    """
    Запись количества фото отелей. Здесь нужно вызывать функцию обработки
     информации(в которой будет отправка сообщения в чат с результатами)
    :param message:
    :return:
    """
    logger.info(f'user_id {message.from_user.id, message.text}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_photo'] = message.text
        bot.send_message(message.chat.id,'Вывожу отели...')
    user_is_ready_high(message)


@bot.message_handler(state=HighPriceStates.count_hotels, is_digit=True, count_digit=False)
def dont_check_count(message: Message) -> None:
    """
    Ввели числа не в диапазоне
    :param message:
    :return:
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Введите число в диапазоне от 1 до 10')


@bot.message_handler(state=HighPriceStates.count_hotels, is_digit=False)
def count_incorrect(message: Message) -> None:
    """
    Ввел не цифру
    :param message:
    :return:
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Введите количество в цифрах')


@bot.message_handler(state=HighPriceStates.count_photo, is_digit=False)
def count_incorrect(message: Message) -> None:
    """
    Ввел не цифру
    :param message:
    :return:
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Введите количество в цифрах')


@bot.message_handler(state=HighPriceStates.count_photo, is_digit=True, count_digit=False)
def dont_check_count(message: Message) -> None:
    """
    Ввели числа не в диапазоне
    :param message:
    :return:
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Введите число в диапазоне от 1 до 10')


def user_is_ready_high(message: Message, user_id=None, chat_id=None) -> None:
    """
    Отсюда вызывается метод для обнаружения всех отелей. Здесь же будет записи в БД, может Pickle.
    Всё будет в модуле utils
    :param message: Message
    :param user_id: На случай перехода с коллбека
    :param chat_id: На случай перехода с коллбека
    :return:
    """
    logger.info(f'user_id {message.from_user.id}')
    user_id = message.from_user.id if not user_id else user_id
    chat_id = message.chat.id if not chat_id else chat_id
    with bot.retrieve_data(user_id, chat_id) as data:
        ex_str = get_properties_list(data['destid'], data["startday"], data["endday"], data['SortOrder'],
                                     data['locale'],
                                     data['currency'], data['count_hotels'], user_id, command='higiprice',
                                     total_days=abs(data['all_days'].days))
        if isinstance(ex_str, dict):
            logger.info(f'user_id {message.from_user.id, ex_str}')
            for key, value in ex_str.items():
                bot.send_message(chat_id, f'{value}')
                if data['photo']:
                    url_photo = get_photo_hotel(key, data['count_photo'])
                    if url_photo:
                        logger.info(f'user_id {message.from_user.id}')
                        bot.send_media_group(chat_id, media=[InputMediaPhoto(media=link) for link in url_photo])
                    else:
                        logger.error(f'user_id {message.from_user.id}')
                        bot.send_message(chat_id, 'Фото не нашлось')
        else:
            bot.send_message(message.chat.id, f'{ex_str}')
            logger.error(f'user_id {message.from_user.id, ex_str}')
    bot.delete_state(user_id, chat_id)
