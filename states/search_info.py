from utils.logger import logger
from telebot.handler_backends import State, StatesGroup


class HistoryStates(StatesGroup):
    """
    State класс для команды history
    """
    logger.info(' ')
    count = State()


class LowPriceStates(StatesGroup):
    """
    State класс для команды LowPrice
    """
    logger.info(' ')
    city = State()
    cities = State()
    count_hotels = State()
    photo = State()
    count_photo = State()
    start_date = State()
    end_date = State()


class HighPriceStates(StatesGroup):
    """
    State класс для команды HighPrice
    """
    logger.info(' ')
    city = State()
    cities = State()
    count_hotels = State()
    photo = State()
    count_photo = State()
    start_date = State()
    end_date = State()


class BestDealStates(StatesGroup):
    """
    State класс для команды BestDeal
    """
    logger.info(' ')
    city = State()
    cities = State()
    count_hotels = State()
    photo = State()
    count_photo = State()
    start_date = State()
    end_date = State()
    min_price = State()
    max_price = State()
    distance = State()
