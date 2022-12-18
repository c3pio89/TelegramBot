from config import TOKEN
import telebot
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Вас приветствует БОТ конвертер валют\nВведите /help для инструкций пользования БОТом")


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, "Пример ввода валют\nUSD RUB 100\nUSD(имя валюты, курс которой хотите узнать)\nRUB(имя валюты, в которой надо узнать курс)\n100(количество валюты)\n/help - Помощь в использовании бота\n/values - Вывод всех доступных валют")

@bot.message_handler(commands=['values'])
def handler_message(message):
    list_sp = Converter.getValut()
    str_res = ' '
    i = 1
    for list1 in list_sp:
        a = list1[:3]
        b = list1[3:]
        c = str(i) + ") " + str(a) + "-" + str(b)
        str_res += "\n" + c
        i += 1
    bot.send_message(message.chat.id, "Валюты доступные для конвертации\n" + str_res[1:] + "\n/help - Помощь в использовании бота")


@bot.message_handler(regexp="[a-zA-Z]{3} [a-zA-Z]{3} -?[0-9]+")
def handler_message(message):
    base = message.text[0:3].upper()
    quote = message.text[4:7].upper()
    amount = float(message.text[8:])
    if amount < 0:
        e = APIException('Введите число. которое больше 0')
        bot.send_message(message.chat.id, e)
        return
    t = Converter.get_price(base, quote, amount)
    if not t:
        e = APIException('Такой валюты нет')
        bot.send_message(message.chat.id, e)
    else:
        bot.send_message(message.chat.id, t)


@bot.message_handler(content_types=['text'])
def after_text(message):
    bot.send_message(message.chat.id, "Неверно введены данные\nДля помощи введите запрос /help")


bot.infinity_polling()
