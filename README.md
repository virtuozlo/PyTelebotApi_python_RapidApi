# Python_Telebot_Project_RapidApi

В версии представленны: Бот, календарь и опросник. Последние были сделаны параллельно с доработкой бота для наглядности.
Решил не удалять.

Последовательность работ.

Установить зависимости
> pip install -r requirements.txt

Создать файл `.env` и добавить туда `BOT_TOKEN` `RAPID_API_KEY`

Получить можно [Мануал по боту](https://core.telegram.org/bots) [Про RapidAPI](https://docs.rapidapi.com/docs/faqs)

Запустить бота `python main.py`

## Возможности бота

В боты представлены основные команды для поиска:

- /lowprice (Поиск отелей с сортировкой по убыванию цены)
- /highprice (Поиск отелей с сортировкой по возрастанию цены)
- /bestdeal (Корректировка поискового предложения)
- /history (История запросов(не более 10))

Так же можете воспользоваться:

- /help
- /start

Пошаговая инструкция и интуитивная "понятность" бота не позволят Вам сделать ошибок

В боте представлены доп. команды.

- /survey (Проводит опрос пользователя)
- /calendar (Выводит календарь с возможностью выбора и вывода в чат даты(гггг/мм/дд))

## Принцип работ.

При старте бота, узнается город назначения.

Проводится запрос и при успешном выполнении пользователю предлагается выбор возможных городов с последующих опросом
деталей

После опроса пользователя о деталях его путешествия, бот делает request запрос на API сайта Hotels.com

При успешном ответе, программа обработает все Ваши потребности и выведет список возможных вариантов отеля.

В боте ведется история поиска. Можете вывести до 10 последних событий