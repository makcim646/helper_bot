#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Admin
#
# Created:     31.07.2021
# Copyright:   (c) Admin 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import telebot
from telebot import types
import requests
import re
from get import *

bot = telebot.TeleBot('1911402515:AAExtY_D7XUBlp4cSmrSeRSVfSoEn5RYrp0') # telegem bot token

otvet = types.InlineKeyboardMarkup(row_width=2)
otvet2 = types.InlineKeyboardMarkup(row_width=2)

button1 = types.InlineKeyboardButton("Опросить порт", callback_data='port_searc')
button2 = types.InlineKeyboardButton("Посмотрет пароль", callback_data='pasw_searc')
button3 = types.InlineKeyboardButton("Сбросить PPPOE-сесию", callback_data='kill_ses')
button4 = types.InlineKeyboardButton("Обновить информацию", callback_data='update')
button5 = types.InlineKeyboardButton("Обновить информацию", callback_data='port_update')

otvet.add(button1,button2, button3, button4)
otvet2.add(button5)



@bot.message_handler(content_types=['text'])
def send_help(message):
    try:
        math = re.fullmatch(r'\[?\d*\.\d*.\d*\.\d*\]?.*', message.text)
        if math:
            bot.send_message(message.chat.id, port(message.text), reply_markup=otvet2)
            return

        math = re.fullmatch(r'7766\d{7}', message.text)
        if math:
            bot.send_message(message.chat.id, login(message.text), reply_markup=otvet)
            return

        math = re.fullmatch(r'7706\d{7}', message.text)
        if math:
            bot.send_message(message.chat.id, tv_code(message.text))
            return

        bot.send_message(message.chat.id, 'Введите логин услуги или порт измерения.\n Пример для логина: 77660000000 или 77060000000.\n Пример для порта: [0.0.0.0] 0-0-0 или 0.0.0.0 0 0 0.')

    except Exception as e:
        print(repr(e))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'port_searc':
                port_out = (call.message.text.split('\n')[-1].split(":")[1]).strip(" ")

                if port_out != 'НЕ АКТИВНА':
                    bot.send_message(call.message.chat.id, port(port_out), reply_markup=otvet2)
                else:
                    bot.send_message(call.message.chat.id, 'Я не знаю порта, введи его вручную.')

            if call.data == 'pasw_searc':
                login_out = call.message.text.split('\n')[0]
                bot.send_message(call.message.chat.id, paswd(login_out))

            if call.data == 'kill_ses':
                login_out = call.message.text.split('\n')[0]
                bot.send_message(call.message.chat.id, kill_session(login_out))

            if call.data == 'update':
                login_out = call.message.text.split('\n')[0]
                bot.send_message(call.message.chat.id, login(login_out), reply_markup=otvet)

            if call.data == 'port_update':
                port_out = (call.message.text.split('\n')[-1])
                bot.send_message(call.message.chat.id, port(port_out), reply_markup=otvet2)




    except Exception as e:
        print(repr(e))






bot.polling(none_stop=True, interval=1)


