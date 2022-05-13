# from keyboards.reply.cancel_states import cancel_states
from loader import bot


@bot.message_handler(state="*", commands='отмена')
def any_state(message):
    """
    Отмена этапов
    """
    bot.send_message(message.chat.id, "Твои этапы отменены.")
    bot.delete_state(message.from_user.id, message.chat.id)
