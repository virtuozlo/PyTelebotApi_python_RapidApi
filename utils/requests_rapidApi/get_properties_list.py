import json
from typing import List, Optional

import requests
from config_data.my_config import url_from_properties, headers


# @logger.catch
def get_distance_to_centre(landmarks: List[dict], user_id: int) -> Optional[str]:
    """
    Функция проверки наличия в словаре дистанции до центра
    :param user_id: Идентификатор пользователя
    :param landmarks: Список со словарём, где могут быть расстояние до центра города/достопримечательности
    :return: str Расстояние. Либо None
    """
    # logger.info(f'{user_id} Вызвана функция get_distance_to_centre(propert)')
    for i in landmarks:
        if i['label'] == 'Центр города' or i['label'] == 'City center':
            return i['distance']
        else:
            # logger.debug(KeyError)
            return None


# @logger.catch
def get_adress(adress: dict, user_id: int) -> str:
    """
    Функция проверки наличия адреса отеля.
    :param user_id: Идентификатор пользователя
    :param adress: dict
    :return: str Адрес
    """
    # logger.info(f'{user_id} Вызвана функция get_adress(propert)')
    if 'streetAddress' in adress:
        return adress['streetAddress']
    return adress['locality']


# @logger.catch()
def get_rating(hotel: dict, user_id: int) -> Optional[int]:
    """
    Функция проверки наличия рейтинга отеля
    :param user_id: Идентификатор пользователя
    :param hotel: dict
    :return: int/None
    """
    # logger.info(f'{user_id} Вызвана функция get_rating(propert)')
    if 'starRating' in hotel:
        return hotel['starRating']
    else:
        # logger.debug(KeyError)
        return None


def get_properties_list(destinationid, checkin, checkout, sortorder, locale, currency, pagesize, user_id):
    querystring = {"destinationId": destinationid,
                   "pageSize": pagesize,
                   "checkIn": checkin,
                   "checkOut": checkout,
                   "sortOrder": sortorder,
                   "locale": locale,
                   "currency": currency}

    response = requests.request("GET", url_from_properties, headers=headers, params=querystring)
    if response:
        try:
            data = json.loads(response.text)['data']['body']['searchResults']['results']
            return get_normalize_str(data, user_id)
        except KeyError:
            return 'Ошибка ответа сервера, попробуйте еще раз. /start'
    else:
        # logger.debug(response.text)
        print(response.text)


def get_normalize_str(hotels, user_id):
    if hotels:
        normalize_str = {}
        for num, i_hotel in enumerate(hotels):
            description = f'Отель - {i_hotel["name"]}\n ' \
                          f'Адрес - {get_adress(i_hotel["address"], user_id)}\n' \
                          f'Цена за ночь - {i_hotel["ratePlan"]["price"]["current"]} \n' \
                          f'Сайт отеля: https://ru.hotels.com/ho{i_hotel["id"]}\n'
            distance = get_distance_to_centre(i_hotel['landmarks'], user_id)
            rating = get_rating(i_hotel, user_id)
            if distance:
                description += f'Расстояние до центра  - {distance}\n'
            if rating:
                description += f'Рейтинг отеля: {rating}\n'

            normalize_str[i_hotel['id']] = description
        return normalize_str
    else:
        return "По вашему запросу ничего не найдено. Попробуйте снова /start"

