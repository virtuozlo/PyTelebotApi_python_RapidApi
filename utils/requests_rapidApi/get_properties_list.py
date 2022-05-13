import requests

url = "https://hotels4.p.rapidapi.com/properties/list"
headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": "45ca137abamsh5d62bed4e61a537p1d864bjsn0d950981ab77"
}


def get_properties_list(destinationId, checkIn, checkOut, sortOrder, locale, currency, pageSize):
    querystring = {"destinationId": destinationId, "pageSize": pageSize, "checkIn": checkIn,
                   "checkOut": checkOut, "adults1": "1", "sortOrder": sortOrder, "locale": locale,
                   "currency": currency}

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
