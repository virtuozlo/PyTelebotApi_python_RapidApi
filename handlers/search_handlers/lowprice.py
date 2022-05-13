from loader import bot
from states.search_info import SearchStates
from keyboards.reply.boolean_keyboard import boolean_keyboard
from keyboards.reply.cancel_states import cancel_status_keyboard, cancel_states_button
from keyboards.inline.calendar_inline.inline_calendar import bot_get_keyboard_inline
from utils.requests_rapidApi.get_properties_list import get_properties_list
from utils.misc.analyze_callback_calendar import exit_date


@bot.message_handler(commands=['lowprice', ])
def start_lowprice(message):
    """
    Начало работы команды поиска дешёвых отелей
    :param message:
    :return:
    """
    bot.set_state(message.from_user.id, SearchStates.start_date, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['id'] = message.from_user.id
        data['SortOrder'] = 'PRICE'
        data['locale'] = 'ru_RU'
        data['currency'] = 'USD'
    bot.send_message(message.chat.id, 'Отлично! Вы выбрали поиск недорогих отелей. Выберите дату заезда.',
                     reply_markup=bot_get_keyboard_inline())


#               Здесь вводить город для поиска с выводом их в кнопках


#                Здесь будут коллбэки на города и запись DestId


@bot.callback_query_handler(func=lambda call: call.data.startswith('DAY'))
def callback_inline(call):
    """
    Ловит выбор пользователя с календаря. Выводит дату либо меняет месяц
    :param call: Выбор пользователя
    """
    state = bot.get_state(call.from_user.id, call.message.chat.id)
    if state == SearchStates.start_date:
        bot.send_message(call.message.chat.id, 'Выберите дату уезда', reply_markup=bot_get_keyboard_inline())
        bot.set_state(call.from_user.id, SearchStates.end_date, call.message.chat.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['startday'] = exit_date(call.data)
            bot.edit_message_text(f'Дата заезда: {data["startday"]}', call.message.chat.id, call.message.id,
                                  )
    elif state == SearchStates.end_date:
        bot.send_message(call.message.chat.id, 'Выберите город.')
        bot.set_state(call.from_user.id, SearchStates.city, call.message.chat.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['endday'] = exit_date(call.data)
            bot.edit_message_text(f'Дата выезда: {data["endday"]}', call.message.chat.id, call.message.id)


@bot.message_handler(state=SearchStates.city)
def get_hotel_count_info(message):
    """
    Запись поискового города. Запрос на количество отелей

    :param message:
    :return:
    """
    bot.send_message(message.chat.id, f'Отличный выбор город {message.text}')
    bot.send_message(message.chat.id, f'Сколько отелей выводить? (не более 10)', reply_markup=cancel_status_keyboard())
    bot.set_state(message.from_user.id, SearchStates.count_hotels, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.message_handler(state=SearchStates.count_hotels, is_digit=True)
def get_photo_info(message):
    """
    Запрос фотографий отелей. Запись количества отелей
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, f'Буду выводить {message.text} отелей')
    bot.send_message(message.chat.id, f'Нужны фото отелей?',
                     reply_markup=boolean_keyboard(cancel_states_button()))
    bot.set_state(message.from_user.id, SearchStates.photo, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_hotels'] = message.text


@bot.message_handler(state=SearchStates.photo)
def get_photo_count_info(message):
    """
    Запрос количества фотографий отелей. Запись необходимости фото
    :return:
    """
    if message.text == 'Нужно':
        bot.send_message(message.chat.id, f'Сколько фото выводить?(Не более 10)', reply_markup=cancel_status_keyboard())
        bot.set_state(message.from_user.id, SearchStates.count_photo, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo'] = True
    elif message.text == 'Отказ':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo'] = False
        user_is_ready(message)

    else:
        bot.send_message(message.chat.id, f'Выберите(или введите) вариант с клавиатуры')


@bot.message_handler(state=SearchStates.count_photo, is_digit=True)
def get_photo_info(message):
    """
    Запись количества фото отелей. Здесь нужно вызывать функцию обработки
     информации(в которой будет отправка сообщения в чат с результатами)
    :param message:
    :return:
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_photo'] = message.text
    user_is_ready(message)


@bot.message_handler(state=SearchStates.count_hotels, is_digit=False)
def count_incorrect(message):
    """
    Ввел не цифру
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, 'Введите количество отелей в цифрах', reply_markup=cancel_status_keyboard())


def user_is_ready(message):
    """
    Отсюда вызывается метод для обнаружения всех отелей. Здесь же будет записи в БД, может Pickle.
    Всё будет в модуле utils
    :param message:
    :return:
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.send_message(message.chat.id, f'Отлично. Вот что за информацию я собрал:\n'
                                          f'Город поиска {data["city"]}\n'
                                          f'Количество отелей {data["count_hotels"]}\n'
                                          f'Фото для отелей {data["photo"]}\n'
                                          f'Их количество {data["count_photo"] if data.get("count_photo") else "Ноль"}\n'
                                          f'Дата заезда {data["startday"]}\n'
                                          f'Уезда {data["endday"]}')
        get_properties_list(1506246, data["startday"], data["endday"], data['SortOrder'], data['locale'],
                            data['currency'], data['count_hotels'])
    bot.delete_state(message.from_user.id, message.chat.id)
