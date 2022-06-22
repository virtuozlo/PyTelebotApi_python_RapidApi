from handlers.search_handlers.highprice import user_is_ready_high
from handlers.search_handlers.lowprice import user_is_ready_low
from loader import bot
from states.search_info import BestDealStates, HighPriceStates, LowPriceStates
from utils.logger import logger
from datetime import date, datetime
from keyboards.inline.calendar_inline.inline_calendar import bot_get_keyboard_inline
from keyboards.inline.filter import my_date, for_search, for_photo
from telebot.types import Message, CallbackQuery


@bot.message_handler(commands=['calendar'])
def bot_get_keyboard(message: Message) -> None:
    """
    Отзыв на команду выдать календарь
    """
    logger.info(f'user_id: {message.from_user.id}')
    bot.send_message(message.chat.id, 'Ваш календарь', reply_markup=bot_get_keyboard_inline())


@bot.callback_query_handler(func=None, my_date_config=my_date.filter())
def callback_inline(call: CallbackQuery) -> None:
    """
    Ловит выбор пользователя с календаря. Выводит дату либо меняет месяц
    :param call: Выбор пользователя
    """
    logger.info(f'user_id: {call.from_user.id}')
    data = my_date.parse(callback_data=call.data)
    my_exit_date = date(year=int(data['year']), month=int(data['month']), day=int(data['day']))
    bot.edit_message_text(my_exit_date, call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=None, search_config=for_search.filter(
    state=('dest_start_date', 'low_start_date', 'high_start_date')))
def callback_start_date(call: CallbackQuery) -> None:
    """
    :param call: Выбор пользователя начала поездки
    """
    logger.info(f'user_id {call.from_user.id}')
    data = for_search.parse(callback_data=call.data)
    my_exit_date = date(year=int(data['year']), month=int(data['month']), day=int(data['day']))
    current_date = date.today() <= my_exit_date
    command = ''
    state = ''
    if current_date:
        if data['state'] == 'dest_start_date':
            bot.set_state(call.from_user.id, BestDealStates.end_date, call.message.chat.id)
            command = 'bestdeal'
            state = 'dest_end_date'
        elif data['state'] == 'low_start_date':
            bot.set_state(call.from_user.id, LowPriceStates.start_date, call.message.chat.id)
            command = 'lowprice'
            state = 'low_end_date'
        elif data['state'] == 'high_start_date':
            bot.set_state(call.from_user.id, HighPriceStates.end_date, call.message.chat.id)
            command = 'highprice'
            state = 'high_end_date'
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            bot.send_message(call.message.chat.id, 'Выберите дату уезда',
                             reply_markup=bot_get_keyboard_inline(command=command, state=state))
            logger.info(f'user_id {call.from_user.id} {my_exit_date}')
            data['startday'] = my_exit_date
            bot.edit_message_text(f'Дата заезда: {my_exit_date}', call.message.chat.id, call.message.id)
    else:
        bot.edit_message_text('Выбранная дата не может быть раньше текущей.\nВыберите дату позднее',
                              call.message.chat.id, call.message.id,
                              reply_markup=bot_get_keyboard_inline(command=data['state'], state=data['state']))



@bot.callback_query_handler(func=None, search_config=for_search.filter())
def callback_end_date(call: CallbackQuery) -> None:
    """
    :param call: Окончание поездки
    """
    logger.info(f'user_id {call.from_user.id}')
    data = for_search.parse(callback_data=call.data)
    my_exit_date = date(year=int(data['year']), month=int(data['month']), day=int(data['day']))
    command = ''
    state = ''
    if data['state'] == 'dest_end_date':
        command = 'bestdeal'
        state = 'dest_end_date'
    elif data['state'] == 'low_end_date':
        command = 'lowprice'
        state = 'low_end_date'
    elif data['state'] == 'high_end_date':
        command = 'highprice'
        state = 'high_end_date'
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        logger.info(f'user_id {call.from_user.id} {my_exit_date}')
        data['endday'] = my_exit_date
        data['all_days'] = data['endday'] - data['startday']
        if data['startday'] > data['endday']:
            logger.error(f'user_id {call.from_user.id} перепутал даты, но всё исправили')
            bot.send_message(call.message.chat.id, f'Выберите дату после даты заезда {data["startday"]}')
            bot.send_message(call.message.chat.id, 'Выберите дату уезда',
                             reply_markup=bot_get_keyboard_inline(command=command, state=state))
        else:
            bot.edit_message_text(f'Дата выезда: {my_exit_date}', call.message.chat.id, call.message.id)
            if state.startswith('high'):
                bot.set_state(call.from_user.id, HighPriceStates.count_hotels, call.message.chat.id)
            elif state.startswith('low'):
                bot.set_state(call.from_user.id, LowPriceStates.count_hotels, call.message.chat.id)
            else:
                bot.set_state(call.from_user.id, BestDealStates.count_hotels, call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Сколько отелей выводить? ( не более 10)')


@bot.callback_query_handler(func=None, is_photo=for_photo.filter())
def photo_info(call: CallbackQuery) -> None:
    """
    :param call: Обработчик кнопки "фото"
    :return: None
    """
    data = for_photo.parse(callback_data=call.data)
    if data['photo'] == 'False':
        logger.info(f'user_id {call.from_user.id}')
        if data['state'] == 'best_state':
            bot.edit_message_text(f'Введите минимальную цену за ночь', call.message.chat.id, call.message.id)
            bot.set_state(call.from_user.id, BestDealStates.min_price, call.message.chat.id)
        elif data['state'] == 'High_state':
            bot.edit_message_text('Вывожу список отелей', call.message.chat.id, call.message.id)
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                logger.info(f'user_id {call.from_user.id}')
                data['photo'] = ''
            user_is_ready_high(call.message, call.from_user.id, call.message.chat.id)
        elif data['state'] == 'low_photo':
            bot.edit_message_text('Вывожу список отелей', call.message.chat.id, call.message.id)
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                logger.info(f'user_id {call.from_user.id}')
                data['photo'] = ''
            user_is_ready_low(call.message, call.from_user.id, call.message.chat.id)
    if data['photo'] == 'True':
        if data['state'] == 'best_state':
            bot.set_state(call.from_user.id, BestDealStates.count_photo, call.message.chat.id)
        elif data['state'] == 'High_state':
            bot.set_state(call.from_user.id, HighPriceStates.count_photo, call.message.chat.id)
        elif data['state'] == 'low_photo':
            bot.set_state(call.from_user.id, LowPriceStates.count_photo, call.message.chat.id)
        bot.edit_message_text('Сколько фото выводить?(Не более 10)', call.message.chat.id, call.message.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['photo'] = True
