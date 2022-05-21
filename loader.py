from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import my_config
from database.user_db import UserDb
from database.user_history_db import HistoryUserDb

storage = StateMemoryStorage()
bot = TeleBot(token=my_config.BOT_TOKEN, state_storage=storage)
db_user = UserDb('user.db')
db_hisory = HistoryUserDb('history_user.db')

