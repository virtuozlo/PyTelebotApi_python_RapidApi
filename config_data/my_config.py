import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('calendar', "Запустить календарь"),
    ('lowprice', 'Поиск бюджетных отелей'),
    ('survey', 'Запустить опрос пользователя'),
    ('highprice', 'Поиск лучших отелей'),
    ('bestdeal', 'Настройка поиска')
)
url_from_cities = "https://hotels4.p.rapidapi.com/locations/v2/search"
url_from_properties = "https://hotels4.p.rapidapi.com/properties/list"
url_from_photo = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": RAPID_API_KEY
}
