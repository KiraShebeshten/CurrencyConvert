import telebot
from currency_converter import CurrencyConverter
from Config import TOKEN
from telebot import types

bot = telebot.TeleBot(TOKEN)

currency =CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я помогу Вам с конвертицией валюты. Введите, пожалуйста, сумму:')
    bot.register_next_step_handler(message, summa)
def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Впишите сумму:')
        bot.register_next_step_handler(message, summa)
        return
    if amount >0:
        markup = types.InlineKeyboardMarkup(row_width=3)
        button1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        button2 = types.InlineKeyboardButton('USD/PLN', callback_data='usd/pln')
        button3 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        button4 = types.InlineKeyboardButton('EUR/PLN', callback_data='eur/pln')
        button5 = types.InlineKeyboardButton('PLN/EUR', callback_data='pln/eur')
        button6 = types.InlineKeyboardButton('PLN/USD', callback_data='pln/usd')
        markup.add(button1, button2, button3, button4, button5, button6)
        bot.send_message(message.chat.id, 'Выберите пару валют:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше 0. Впишите сумму:')
        bot.register_next_step_handler(message, summa)

@bot.message_handler(content_types=['text'])
def button(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Пожалуйста, используйте кнопки выше :)", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    values = call.data.upper().split('/')
    res = currency.convert(amount, values[0], values[1])
    bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете повторить с другой валютой. Введите число:')
    bot.register_next_step_handler(call.message, summa)


bot.polling(none_stop=True)
