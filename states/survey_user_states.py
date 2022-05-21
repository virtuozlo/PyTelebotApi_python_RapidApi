from telebot.handler_backends import State, StatesGroup  # States

# States storage
from telebot.storage import StateMemoryStorage

# Now, you can pass storage to bot.
from utils.logger import logger


state_storage = StateMemoryStorage()  # you can init here another storage


# States group.
class MyStates(StatesGroup):
    # Just name variables differently
    logger.info(' ')
    id = State()
    name = State()  # creating instances of State class is enough from now
    surname = State()
    age = State()
