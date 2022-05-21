from telebot.types import Message

from loader import bot
from utils.logger import logger


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    logger.info(f'user_id: {message.from_user.id}')
    bot.reply_to(message, 'Бот фирмы Too Easy Travel может помочь Вам с выбором отеля\n'
                          'В начале работы будет произведен опрос в каком городе будет произведен поиск\n'
                          'Критерии поиска и бот предложит на выбор сортировку результатов\n'
                          'Бюджетные отели, сортировка по убываю цены и лучшие предложения\n'
                          'Хорошего дня!', )
