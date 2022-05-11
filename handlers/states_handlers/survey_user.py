from states.survey_user_states import MyStates
from loader import bot
from database.user_db import filling_db


@bot.message_handler(commands=['survey'])
def start_ex(message):
    """
    Команда старт. Присваивается этап 'name'
    """
    bot.set_state(message.from_user.id, MyStates.name, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['id'] = message.from_user.id
    bot.send_message(message.chat.id, 'Привет! Напиши свое имя.')


@bot.message_handler(state="*", commands='cancel')
def any_state(message):
    """
    Отмена этапов
    """
    bot.send_message(message.chat.id, "Твои этапы отменены.")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.name)
def name_get(message):
    """
    1 этап. Запуск метода когда у пользователя state=name
    """
    bot.send_message(message.chat.id, f'Теперь напиши свою фамилию')
    bot.set_state(message.from_user.id, MyStates.surname, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text


@bot.message_handler(state=MyStates.surname)
def ask_age(message):
    """
    Этап 2. Запуск метода когда у пользователя state=surname.
    """
    bot.send_message(message.chat.id, "Сколько тебе лет?")
    bot.set_state(message.from_user.id, MyStates.age, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['surname'] = message.text


@bot.message_handler(state=MyStates.age, is_digit=True)
def ready_for_answer(message):
    """
    Этап 3. Запуск метода когда у пользователя state=age.Идет проверка на ввод числа
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = int(message.text)
        bot.send_message(message.chat.id,
                         "Готово. Твоя информация:\n<b>Имя: {name}\nФамилия: {surname}\nВозраст: {age}</b>".format(
                             name=data['name'], surname=data['surname'], age=message.text), parse_mode="html")
        filling_db(data)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.age, is_digit=False)
def age_incorrect(message):
    """
    Если при вводе возраста ввели не число
    """
    bot.send_message(message.chat.id, 'Ты ввел не цифру, а строку! Пожалуйста, введи свой возраст в цифрах!')
