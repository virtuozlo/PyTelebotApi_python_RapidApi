from telebot.types import Message
import json
from states.search_info import HistoryStates


from loader import db_hisory, bot


@bot.message_handler(commands=['history'])
def start_history(message: Message) -> None:
    """
    Начало истории
    """
    bot.send_message(message.chat.id, 'Сколько последних запросов Вам показать?(Не более 10)')
    bot.set_state(message.from_user.id, HistoryStates.count, message.chat.id)


@bot.message_handler(state=HistoryStates.count, is_digit=True, count_digit=True)
def get_history(message: Message) -> None:
    '''
    Вывод истории поиска
    '''
    data = db_hisory.get_data(message.from_user.id, message.text)
    for row in data.fetchall():
        data, command, hotels = row[0], row[1], json.loads(row[2])
        bot.send_message(message.chat.id, f'{data} выполнили команду {command} и нашли: ')
        for _ in range(len(hotels)):
            for id, description in hotels.items():
                bot.send_message(message.chat.id, f'{description}')


@bot.message_handler(state=HistoryStates.count, is_digit=False)
def bad_digit(message: Message) -> None:
    """
    :param message: не число
    """
    bot.send_message(message.chat.id, 'Введите число')


@bot.message_handler(state=HistoryStates.count, is_digit=True, count_digit=False)
def many_count(message: Message) -> None:
    """
    не тот диапазон
    """
    bot.send_message(message.chat.id, 'Введите число в диапазоне от 1 до 10')
