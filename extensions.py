import requests
import json
from config import keys

class TryException(Exception):
    pass

class CurrencyConvert():
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise TryException(
                f'Нельзя переводить одинаковые валюты.\n{TheRules.rules()}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise TryException(
                f'Не удалось обработать валюту "{base}", введите валюту из списка /values')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise TryException(f'Не удалось обработать валюту "{base}", введите валюту '
                               f'из списка /values')
        try:
            amount = float(amount)
        except ValueError:
            raise TryException(f'Не корректное число "{amount}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym='
                         f'{quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        total_base *= amount
        return total_base


class TheRules:
    @staticmethod
    def remind():
        remin = 'Ввод: <валюта из которой надо перевести> <валюта в какую перевести>' \
                ' <количество переводимой валюты>'
        return remin

    @staticmethod
    def rules():
        rule = f'Для корректной работы ChuzLightBot необходимо использовать следующую ' \
               f'инструкцию.\n{TheRules.remind()}\n' \
               f'Помощь: /help'
        return rule

    @staticmethod
    def command():
        command = 'Список команд:\n' \
                  'Инструкция: /start\n' \
                  'Список доступных валют: /values \n'

        return command

