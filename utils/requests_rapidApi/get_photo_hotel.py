from typing import Union
import json
from config_data.my_config import url_from_photo, headers
from utils.logger import logger
from .request_univ import get_response


def get_photo_hotel(sity_id: int, count_photo: str) -> Union[str, list, bool]:
    """
    :param sity_id: Идентификатор города
    :param count_photo: Количество фото
    :return: список url фото
    """

    media = []
    querystring = {
        'id': sity_id
    }
    response = get_response(url=url_from_photo, params=querystring, header=headers)
    if isinstance(response, str):
        logger.exception(f'{response}')
        return False
    else:
        logger.info('response')
        data = json.loads(response.text)['hotelImages']
        if data:
            for photo in data:
                media.append(photo['baseUrl'].replace('{size}', 'b'))
                if len(media) >= int(count_photo):
                    break
            return media
