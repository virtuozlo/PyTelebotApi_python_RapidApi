from states.survey_user_states import MyStates
from loader import bot, db_user
from telebot.types import Message


@bot.message_handler(commands=['survey'])
def start_ex(message: Message) -> None:
    """
    Команда старт. Присваивается этап 'name'
    """
    if not db_user.check_user(message.from_user.id):
        db_user.add_user(message.from_user.id)
    bot.set_state(message.from_user.id, MyStates.name, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['id'] = message.from_user.id
    bot.send_message(message.chat.id, 'Привет! Напиши свое имя.')


@bot.message_handler(state=MyStates.name)
def name_get(message: Message) -> None:
    """
    1 этап. Запуск метода когда у пользователя state=name
    """
    bot.send_message(message.chat.id, f'Теперь напиши свою фамилию')
    bot.set_state(message.from_user.id, MyStates.surname, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text


@bot.message_handler(state=MyStates.surname)
def ask_age(message: Message) -> None:
    """
    Этап 2. Запуск метода когда у пользователя state=surname.
    """
    bot.send_message(message.chat.id, "Сколько тебе лет?")
    bot.set_state(message.from_user.id, MyStates.age, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['surname'] = message.text


@bot.message_handler(state=MyStates.age, is_digit=True)
def ready_for_answer(message: Message) -> None:
    """
    Этап 3. Запуск метода когда у пользователя state=age.Идет проверка на ввод числа
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = int(message.text)
        bot.send_message(message.chat.id,
                         "Готово. Твоя информация:\n<b>Имя: {name}\nФамилия: {surname}\nВозраст: {age}</b>".format(
                             name=data['name'], surname=data['surname'], age=message.text), parse_mode="html")
        db_user.filling_db(data)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.age, is_digit=False)
def age_incorrect(message: Message) -> None:
    """
    Если при вводе возраста ввели не число
    """
    bot.send_message(message.chat.id, 'Ты ввел не цифру, а строку! Пожалуйста, введи свой возраст в цифрах!')
