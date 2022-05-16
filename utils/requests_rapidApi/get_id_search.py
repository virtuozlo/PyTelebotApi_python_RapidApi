import re
import requests
import json
from config_data.my_config import url_from_cities, headers
from keyboards.inline.button_citi import get_button_cities


def get_dest_id(city, locale, currency):
    """
    :param city: Город поиска
    :param locale: Локаль от выбранного языка
    :param currency: валюта от локали
    :return: keyboard or None
    """
    querystring = {"query": city,
                   "locale": locale,
                   "currency": currency}
    response = requests.request("GET", url_from_cities, headers=headers, params=querystring)
    if response:
        data = json.loads(response.text)
        entries = list(filter(lambda i_data: i_data['group'] == 'CITY_GROUP', data['suggestions']))[0]['entities']
        if not entries:
            return None
        else:
            temp_dict_button_hotel = {}
            for i_hotel in entries:
                if i_hotel['type'] == 'CITY':
                    current_city = re.sub(r'<[^.]*>\b', '', i_hotel['caption'])
                    current_city = re.sub(r'<[^.]*>', '', current_city)
                    call_dat = i_hotel["destinationId"]
                    temp_dict_button_hotel[current_city] = call_dat
            return get_button_cities(temp_dict_button_hotel)
    else:
        # logger.info('Not response')
        return None
