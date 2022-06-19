import json
from typing import List, Optional, Union
from .request_univ import get_response
import requests
from config_data.my_config import url_from_properties, headers
from loader import db_hisory
from utils.logger import logger


def get_distance_to_centre(landmarks: List[dict], user_id: int) -> Optional[str]:
    """
    Функция проверки наличия в словаре дистанции до центра
    :param user_id: Идентификатор пользователя
    :param landmarks: Список со словарём, где могут быть расстояние до центра города/достопримечательности
    :return: str Расстояние. Либо None
    """
    logger.info(f'{user_id} Вызвана функция get_distance_to_centre(propert)')
    for i in landmarks:
        if i['label'] == 'Центр города' or i['label'] == 'City center':
            return i['distance']
        else:
            logger.error(KeyError)
            return None


def get_adress(adress: dict, user_id: int) -> str:
    """
    Функция проверки наличия адреса отеля.
    :param user_id: Идентификатор пользователя
    :param adress: dict
    :return: str Адрес
    """
    logger.info(f'{user_id} Вызвана функция get_adress(propert)')
    if 'streetAddress' in adress:
        return adress['streetAddress']
    return adress['locality']


def get_rating(hotel: dict, user_id: int) -> Optional[int]:
    """
    Функция проверки наличия рейтинга отеля
    :param user_id: Идентификатор пользователя
    :param hotel: dict
    :return: int/None
    """
    logger.info(f'{user_id} Вызвана функция get_rating(propert)')
    if 'starRating' in hotel:
        return hotel['starRating']
    else:
        logger.error(KeyError)
        return None


def get_properties_list(destination_id: int, checkin: str, checkout: str, sort_order: str, locale: str, currency: str,
                        pagesize: str, user_id: int, command: str, total_days: int,
                        best_string: dict = None) -> Optional[Union[str, dict]]:
    """
    Получение отелей
    :param total_days: Всего дней путешествия
    :param command: Введеная команда
    :param destination_id: Ид города
    :param checkin: Дата заезда
    :param checkout: Дата выезда
    :param sort_order: Сортировка вывода
    :param locale: Откуда поиск
    :param currency: Валюта
    :param pagesize: Количество отелей
    :param user_id: идентификатор пользователя
    :param best_string: доп. querystring
    :return: 
    """
    logger.info(' ')
    querystring = {"destinationId": destination_id,
                   "pageSize": pagesize,
                   "checkIn": checkin,
                   "checkOut": checkout,
                   "sortOrder": sort_order,
                   "locale": locale,
                   "currency": currency}
    if best_string:
        logger.info('BestDeal')
        querystring.update(best_string)
    response = get_response(url=url_from_properties, params=querystring, header=headers)
    if isinstance(response, str):
        return response
    else:
        logger.info('response')
        data = json.loads(response.text)['data']['body']['searchResults']['results']
        if data:
            return get_normalize_str(data, user_id, command, total_days)
        else:
            logger.error('No data')
            return 'По вашему запросу ничего не найдено. Попробуйте снова /start'


def get_normalize_str(hotels: dict, user_id: int, command: str, total_days: int) -> Optional[Union[dict, str]]:
    """
    Вывод строки для бота
    :param total_days:
    :param command:
    :param hotels:
    :param user_id:
    :return:
    """
    logger.info(' ')
    if hotels:
        normalize_str = {}
        for num, i_hotel in enumerate(hotels):
            description = f'Отель - {i_hotel["name"]}\n ' \
                          f'Адрес - {get_adress(i_hotel["address"], user_id)}\n' \
                          f'Цена за ночь - {i_hotel["ratePlan"]["price"]["current"]} \n' \
                          f'Сайт отеля: https://ru.hotels.com/ho{i_hotel["id"]}\n' \
                          f'Всего стоимость за {total_days} ночи : {int(i_hotel["ratePlan"]["price"]["exactCurrent"]) * total_days}$\n'
            distance = get_distance_to_centre(i_hotel['landmarks'], user_id)
            rating = get_rating(i_hotel, user_id)
            if distance:
                description += f'Расстояние до центра  - {distance}\n'
            if rating:
                description += f'Рейтинг отеля: {rating}\n'

            normalize_str[i_hotel['id']] = description
        db_hisory.set_data(user_id, command, normalize_str)
        logger.info(' ')
        return normalize_str
    else:
        logger.error('Not hotels')
        return "По вашему запросу ничего не найдено. Попробуйте снова /start"
