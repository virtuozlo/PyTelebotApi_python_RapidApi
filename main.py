from loader import bot
from keyboards.inline.calendar_inline.filter import bind_filters
import handlers
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':
    set_default_commands(bot)
    bind_filters(bot)
    bot.polling(none_stop=True)
