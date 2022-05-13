from loader import bot
import handlers
from database.user_db import set_up_db
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':
    # bot.stop_bot()
    set_default_commands(bot)
    set_up_db()
    # bot.infinity_polling()
    bot.polling(none_stop=True)
