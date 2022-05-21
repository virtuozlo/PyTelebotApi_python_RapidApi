from telebot.types import Message

from config_data.my_config import DEFAULT_COMMANDS
from loader import bot
from utils.logger import logger


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    bot.delete_state(message.from_user.id, message.chat.id)
    logger.info(f'user_id: {message.from_user.id}')
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.chat.id, 'Бот фирмы Too Easy Travel может помочь Вам с выбором отеля\n'
                                      'В начале работы будет произведен опрос в каком городе будет произведен поиск\n'
                                      'Критерии поиска и бот предложит на выбор сортировку результатов\n'
                                      'Бюджетные отели, сортировка по убываю цены и лучшие предложения\n'
                                      'Хорошего дня!')
    bot.send_message(message.chat.id, '\n'.join(text))
