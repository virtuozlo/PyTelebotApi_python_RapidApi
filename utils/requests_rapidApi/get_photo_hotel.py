import requests
import json
from config_data.my_config import url_from_photo, headers


def get_photo_hotel(sity_id, count_photo):
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
