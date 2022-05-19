from loader import bot
import handlers
from keyboards.inline.filter import bind_filters
from utils.set_bot_commands import set_default_commands
import logging.config
from utils.logger import LOGGING_CONFIG

if __name__ == '__main__':
    logging.config.dictConfig(LOGGING_CONFIG)
    set_default_commands(bot)
    bind_filters(bot)
    bot.polling(none_stop=True)
