import telebot
from telebot import types, AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter

calendar_factory = CallbackData("action", "year", "month", prefix="calendar")
my_date = CallbackData("year", "month", "day", prefix="my_date")
for_search = CallbackData("year", "month", "day", prefix="search")


class CalendarCallbackFilter(AdvancedCustomFilter):
    key = 'calendar_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


class CalendarGetDateCallbackFilter(AdvancedCustomFilter):
    key = 'my_date_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


class CalendarGetDateSearchCallbackFilter(AdvancedCustomFilter):
    key = 'search_config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


def bind_filters(bot: telebot.TeleBot):
    bot.add_custom_filter(CalendarCallbackFilter())
    bot.add_custom_filter(CalendarGetDateCallbackFilter())
    bot.add_custom_filter(CalendarGetDateSearchCallbackFilter())
