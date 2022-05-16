from loader import bot
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup

from telebot.storage import StateMemoryStorage

state_storage = StateMemoryStorage()


class LowPriceStates(StatesGroup):
    cities = State()
    count_hotels = State()
    photo = State()
    count_photo = State()
    start_date = State()
    end_date = State()


class HighPriceStates(StatesGroup):
    cities = State()
    count_hotels = State()
    photo = State()
    count_photo = State()
    start_date = State()
    end_date = State()


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
