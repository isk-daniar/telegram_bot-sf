# класс конфигурации

class Config:


    # локальные константы


    # токен бота
    _TOKEN = '5779849341:AAEmaxNiwJgi1zbwNSfvr4pdDZbyddHWmIQ'

    # хост API
    _HOST = 'https://min-api.cryptocompare.com/data/price'

    # поддерживаемые валюты
    _CURRENCIES = {
        'биткоин': 'BTC',
        'btc': 'BTC',
        'евро': 'EUR',
        'eur': 'EUR',
        'доллар': 'USD',
        'usd': 'USD',
        'йена': 'JPY',
        'jpy': 'JPY',
        'юань': 'CNY',
        'cny': 'CNY',
        'стерлинг': 'GBP',
        'gbp': 'GBP'
    }

    # получить токен
    @property
    def token(self):
        return self._TOKEN

    # получить хост
    @property
    def host(self):
        return self._HOST

    # получить перечень всех поддерживаемых валют
    @property
    def currency_keys(self):
        return self._CURRENCIES.keys()

    # возвратить код валюты
    def currency_code(self, key):
        return self._CURRENCIES[key]