import telebot
from config import TOKEN, keys
from extensions import TryException, CurrencyConvert, TheRules

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', ])
def start(message: telebot.types.Message):
    chat = TheRules.rules()
    bot.send_message(message.chat.id, f'Привет {message.chat.username}\n{chat}!')


@bot.message_handler(commands=['help', ])
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, TheRules.command())


# Список доступных валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)
# Конвертер валют через API
@bot.message_handler(content_types=['text', ])
def convent(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise TryException(f'Неверное количество значений\n{TheRules.remind()}')
        quote, base, amount = values
        total_base = CurrencyConvert.convert(quote, base, amount)
    except TryException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {keys[quote]} в {keys[base]} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

