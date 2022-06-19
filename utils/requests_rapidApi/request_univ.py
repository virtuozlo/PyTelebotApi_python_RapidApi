from typing import Optional, Union

import requests
from utils.logger import logger


def get_response(url: str, params: dict, header: dict, method='GET') -> Optional[Union[str, requests.Response]]:
    """
    Универсальная функция запросов к RapidAPI
    :param header: header
    :param url: Путь запроса
    :param params: Параметры запроса
    :param method: Метод запроса
    :return:response
    """
    try:
        response = requests.request(method, url, params=params, headers=header, timeout=15)
    except requests.exceptions.Timeout as e:
        logger.exception(e)
        return 'Истекло время ожидания от сервера \n/start'
    except requests.exceptions.TooManyRedirects as e:
        logger.exception(e)
        return 'Ошибка сервера, попробуйте позже \n/start'
    except requests.exceptions.RequestException as e:
        logger.exception(e)
        return 'Неизвестная ошибка, попробуйте еще раз \n/start'
    if response.status_code == 200:
        return response
    else:
        logger.error(f'{response.status_code}')
        return 'Ошибка сервера, попробуйте позже \n/start'
