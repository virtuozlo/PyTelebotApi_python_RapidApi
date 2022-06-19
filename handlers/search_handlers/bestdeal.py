from datetime import date

from telebot.types import InputMediaPhoto, CallbackQuery, Message

from keyboards.inline.calendar_inline.inline_calendar import bot_get_keyboard_inline
from keyboards.inline.filter import for_button, for_search, for_photo, for_start
from keyboards.inline.photo_button import get_button_photo
from loader import bot
from utils.logger import logger
from states.search_info import BestDealStates
from utils.requests_rapidApi.get_id_search import get_dest_id
from utils.requests_rapidApi.get_photo_hotel import get_photo_hotel
from utils.requests_rapidApi.get_properties_list import get_properties_list


@bot.callback_query_handler(func=None, start_config=for_start.filter(action='bestdeal'))
def start_highprice(call):
    """
    Выбор возрастания цены
    :param call:
    :return:
    """
    logger.info(' ')
    bot.set_state(call.from_user.id, BestDealStates.cities,call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Отлично! Выбран дополнительный критерий поиска. Выберите город для поиска.')


@bot.message_handler(commands=['bestdeal'])
def start_best_deal(message: Message) -> None:
    """
    Начала работы команды bestdeal
    :return: None
    """
    logger.info(f'user_id {message.from_user.id}')
    bot.set_state(message.from_user.id, BestDealStates.cities, message.chat.id)
    bot.send_message(message.chat.id, 'Отлично! Выбран дополнительный критерий поиска. Выберите город для поиска.')


@bot.message_handler(state=BestDealStates.cities)
def get_cities_request(message: Message) -> None:
    """
    Вывод кнопок городов и их обработка
    :param message: город пользователя
    :return: None
    """
    logger.info(f'user_id {message.from_user.id}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['id'] = message.from_user.id
        data['SortOrder'] = 'STAR_RATING_HIGHEST_FIRST'
        data['locale'] = 'ru_RU'
        data['currency'] = 'USD'
        data['city'] = message.text
        keyboard = get_dest_id(message.text, data['locale'], data['currency'], state='best_state')
        if not isinstance(keyboard, str):
            logger.info(f'user_id {message.from_user.id} {message.text}')
            bot.send_message(message.chat.id, 'Выберите подходящий город:', reply_markup=keyboard)
        else:
            logger.error(f'user_id {message.from_user.id}')
            bot.send_message(message.chat.id, f'{keyboard}')
            bot.set_state(message.from_user.id, BestDealStates.cities)


@bot.callback_query_handler(func=None, button_config=for_button.filter(state='best_state'))
def button_callback(call: CallbackQuery) -> None:
    """
    Обработка кнопок городов
    :param call:
    :return:
    """
    logger.info(f'user_id {call.from_user.id}')
    callback_data = for_button.parse(callback_data=call.data)
    name, destid = callback_data['name'], int(callback_data['destid'])
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['destid'] = destid
        data['city'] = name
        bot.edit_message_text(f'Отличный выбор {name}', call.message.chat.id, call.message.id)
        logger.info(f'user_id {call.from_user.id} {name} {destid}')
    bot.set_state(call.from_user.id, BestDealStates.start_date, call.message.chat.id)
    bot.send_message(call.message.chat.id, f'Выберите даты заезда',
                     reply_markup=bot_get_keyboard_inline(command='bestdeal', state='dest_start_date'))


@bot.message_handler(state=BestDealStates.count_hotels, is_digit=True, count_digit=True, )
def get_photo_info(message: Message) -> None:
    """
    Запрос фотографий отелей. Запись количества отелей
    :param message: Количество отелей
    :return:None
    """
    logger.info(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, f'Буду выводить {message.text} отелей')
    bot.send_message(message.chat.id, f'Нужны фото отелей?',
                     reply_markup=get_button_photo(state='best_state'))
    bot.set_state(message.from_user.id, BestDealStates.photo, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        logger.info(f'user_id {message.from_user.id} {message.text}')
        data['count_hotels'] = message.text


@bot.message_handler(state=BestDealStates.count_photo, is_digit=True, count_digit=True)
def get_photo_info(message: Message) -> None:
    """
    Запись количества фото отелей. Здесь нужно вызывать функцию обработки
     информации(в которой будет отправка сообщения в чат с результатами)
    :param message:количества фото отелей
    :return: None
    """
    logger.info(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, f'Введите минимальную цену за ночь')
    bot.set_state(message.from_user.id, BestDealStates.min_price, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        logger.info(f'user_id {message.from_user.id} {message.text}')
        data['count_photo'] = message.text


@bot.message_handler(state=BestDealStates.min_price, is_digit=True)
def get_min_price(message: Message) -> None:
    """
    Запись минимальной цены за ночь
    :param message: min_price
    :return: None
    """
    logger.info(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, f'Введите максимальную цену за ночь')
    bot.set_state(message.from_user.id, BestDealStates.max_price, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        logger.info(f'user_id {message.from_user.id} {message.text}')
        data['min_price'] = int(message.text)


@bot.message_handler(state=BestDealStates.max_price, is_digit=True)
def get_max_price(message: Message) -> None:
    """
    Запись максимальной цены за ночь
    :param message: max_price
    :return: None
    """
    bot.send_message(message.chat.id, f'Введите расстояние до центра')
    bot.set_state(message.from_user.id, BestDealStates.distance, message.chat.id)
    logger.info(f'user_id {message.from_user.id}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        logger.info(f'user_id {message.from_user.id} {message.text}')
        data['max_price'] = int(message.text)
        if data['max_price'] < data['min_price']:
            logger.error(f'user_id {message.from_user.id} ввел цены наоборот')
            data['max_price'], data['min_price'] = data['min_price'], data['max_price']


@bot.message_handler(state=BestDealStates.distance, is_digit=True)
def get_distance_to_centre(message: Message) -> None:
    """
    Запись дистанции до центра
    :param message: distance
    :return: None
    """
    logger.info(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Вывожу результаты')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        logger.info(f'user_id {message.from_user.id} {message.text}')
        data['distance'] = float(message.text)
    user_is_ready(message)


@bot.message_handler(state=[BestDealStates.distance, BestDealStates.max_price, BestDealStates.min_price],
                     is_digit=False)
def not_digit_message(message: Message) -> None:
    """
    Обработчик ошибки при вводе не int
    :return: None
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Введите число больше 0!')


@bot.message_handler(state=BestDealStates.count_hotels, is_digit=True, count_digit=False)
def dont_check_count(message: Message) -> None:
    """
    Ввели числа не в диапазоне
    :return:None
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Введите число в диапазоне от 1 до 10')


def user_is_ready(message: Message) -> None:
    """
    Отсюда вызывается метод для обнаружения всех отелей. Здесь же будет записи в БД, может Pickle.
    Всё будет в модуле utils
    :return: None
    """
    logger.info(f'user_id {message.from_user.id}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        addition_str = {
            'priceMin': data['min_price'],
            'priceMax': data['max_price'],
            'landmarkIds': data['distance']
        }
        ex_str = get_properties_list(data['destid'], data["startday"], data["endday"], data['SortOrder'],
                                     data['locale'],
                                     data['currency'], data['count_hotels'], message.from_user.id,
                                     best_string=addition_str, command='bestdeal',
                                     total_days=abs(data['all_days'].days))
        if isinstance(ex_str, dict):
            logger.info(f'user_id {message.from_user.id}')
            for key, value in ex_str.items():
                bot.send_message(message.chat.id, f'{value}')
                if data['photo']:
                    logger.info(f'user_id {message.from_user.id}')
                    url_photo = get_photo_hotel(key, data['count_photo'])
                    if url_photo:
                        logger.info(f'user_id {message.from_user.id}')
                        bot.send_media_group(message.chat.id, media=[InputMediaPhoto(media=link) for link in url_photo])
                    else:
                        logger.error(f'user_id {message.from_user.id}')
                        bot.send_message(message.chat.id, 'Фото не нашлось')
        else:
            logger.error(f'user_id {message.from_user.id} {ex_str}')
            bot.send_message(message.chat.id, f'{ex_str}')
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=BestDealStates.count_hotels, is_digit=False)
def count_incorrect(message: Message) -> None:
    """
    Ввел не цифру
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Введите количество в цифрах')


@bot.message_handler(state=BestDealStates.count_photo, is_digit=False)
def count_incorrect(message: Message) -> None:
    """
    Ввел не цифру
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Введите количество в цифрах')


@bot.message_handler(state=BestDealStates.count_photo, is_digit=True, count_digit=False)
def dont_check_count(message: Message) -> None:
    """
    Ввели числа не в диапазоне
    """
    logger.error(f'user_id {message.from_user.id}')
    bot.send_message(message.chat.id, 'Введите число в диапазоне от 1 до 10')
