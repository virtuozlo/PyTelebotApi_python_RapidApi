import requests
from config_data.my_config import RAPID_API_KEY


url = "https://hotels4.p.rapidapi.com/properties/list"
headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": RAPID_API_KEY
}


def get_properties_list(destinationId, checkIn, checkOut, sortOrder, locale, currency, pageSize):
    querystring = {"destinationId": destinationId, "pageSize": pageSize, "checkIn": checkIn,
                   "checkOut": checkOut, "adults1": "1", "sortOrder": sortOrder, "locale": locale,
                   "currency": currency}

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
