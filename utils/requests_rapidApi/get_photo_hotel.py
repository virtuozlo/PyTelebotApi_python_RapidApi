from typing import Optional, Union

import requests
import json
from config_data.my_config import url_from_photo, headers


def get_photo_hotel(sity_id: int, count_photo: str) -> Union[list, bool]:
    """
    :param sity_id: Идентификатор города
    :param count_photo: Количество фото
    :return: список url фото
    """
    media = []
    querystring = {
        'id': sity_id
    }
    response = requests.request("GET", url_from_photo, headers=headers, params=querystring)
    data = json.loads(response.text)['hotelImages']
    if data:
        for photo in data:
            media.append(photo['baseUrl'].replace('{size}', 'b'))
            if len(media) >= int(count_photo):
                break
        return media
    else:
        return False
