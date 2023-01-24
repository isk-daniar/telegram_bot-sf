import telebot
import requests
import json

from config import Config


class Crypto:


    @staticmethod
    def get_price(quote_code, base_code, amount):
        get_request = f'?fsym={quote_code}&tsyms={base_code}'
        rate = requests.get(Config().host + get_request).content
        price = round(json.loads(rate)[base_code] * amount, 5)
        return f'{amount} {quote_code} = {price} {base_code}\n'



# класс исключений

class APIException(Exception):

    def __init__(self, inline):
        self.text = inline



# контроль ошибок входной строки

class ErrorHandler:

    @staticmethod
    def check(values):

        if len(values) < 3:
            raise APIException('недостаточно параметров')

        if len(values) > 3:
            raise APIException('слишком много параметров')

        for key in Config().currency_keys:
            for i in [0, 1]:
                if values[i][:3] == key[:3]:
                    values[i] = key

        if not values[0] in Config().currency_keys:
            raise APIException(f'валюта {values[0]} не поддерживается')

        if not values[1] in Config().currency_keys:
            raise APIException(f'валюта {values[1]} не поддерживается')

        if values[0] == values[1]:
            raise APIException('одинаковые валюты')

        try:
            x = float(values[2])
        except ValueError:
            raise APIException(f'{values[2]} - не числовое значение')

        if x <= 0:
            raise APIException(f'{values[2]} - значение должно быть положительным')



# класс приложения

class App:


    # начать работу

    @staticmethod
    def run():

        # Создать бот
        bot = telebot.TeleBot(Config().token)

        # Обработка команд start и help
        @bot.message_handler(commands=['start', 'help'])
        def start_help(message):
            bot.reply_to(message, 'Введите через пробел\nвалюта1 валюта2 сумма\nСписок доступных валют: /values')

        # Обработка команды values
        @bot.message_handler(commands=['values'])
        def values(message):
            txt = 'Доступные валюты:'
            for key in Config().currency_keys:
                txt = '\n'.join((txt, key))
            bot.reply_to(message, txt)

        # обработка запросов
        @bot.message_handler(content_types=['text'])
        def convert(message):

            # строка ответа боту
            text = ''

            try:
                # получить данные запроса от бота
                value_list = message.text.lower().split(' ')

                # проверка корректности введенных данных
                ErrorHandler.check(value_list)

                # Получить значения из списка введенных данных запроса

                # <количество первой валюты>.
                quote_key, base_key, amount = value_list[0], value_list[1], float(value_list[2])

                # выполнить прямой запрос курса и получить строку ответа
                text = Crypto.get_price(Config().currency_code(quote_key), Config().currency_code(base_key), amount)

                # выполнить инверсный запрос курса и получить строку ответа
                text += Crypto.get_price(Config().currency_code(base_key), Config().currency_code(quote_key), amount)

            except APIException as e:

                # Сформировать строку ответа об ошибке
                text = f'ошибка:\n{e.text}\nповторите запрос'

            finally:

                # Отправить ответ боту
                bot.reply_to(message, text)

        # начать прием данных от бота
        bot.polling()