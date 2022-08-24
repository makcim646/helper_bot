from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
import asyncio
import re
from get import *
import threading
from config import telegram_token
bot = AsyncTeleBot(telegram_token)


threading.Thread(target = update_session, args = (), daemon = True).start()

button1 = InlineKeyboardButton("Опросить порт", callback_data='port_searc')
button2 = InlineKeyboardButton("Посмотрет пароль", callback_data='pasw_searc')
button3 = InlineKeyboardButton("Сбросить PPPOE-сесию", callback_data='kill_ses')
button4 = InlineKeyboardButton("Обновить информацию", callback_data='update')
button5 = InlineKeyboardButton("Обновить информацию", callback_data='port_update')
button6 = InlineKeyboardButton("Проверить сплитор", callback_data='see_split')
button7 = InlineKeyboardButton("Проверить порт OLT", callback_data='see_olt')


otvet1 = InlineKeyboardMarkup(row_width=2).add(button1,button2, button3, button4)
otvet2 = InlineKeyboardMarkup(row_width=2).add(button5, button6, button7)

#threading.Thread(target = hello, args = (1,), daemon = True).start()
@bot.message_handler(func=lambda message: True)
async def echo_message(msg):
    try:
        math = re.fullmatch(r'\[?\d*\.\d*.\d*\.\d*\]?.*', msg.text)
        if math:
            threading.Thread(target = port, args = (msg.text, msg.from_user.id, otvet2), daemon = True).start()
            return

        math = re.fullmatch(r'7766\d{7}', msg.text)
        if math:
            threading.Thread(target = login, args = (msg.text, msg.from_user.id, otvet1), daemon = True).start()
            return

        math = re.fullmatch(r'7706\d{7}', msg.text)
        if math:
            threading.Thread(target = tv_code, args = (msg.text, msg.from_user.id), daemon = True).start()
            return
        math = re.fullmatch(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', msg.text)
        if math:
            threading.Thread(target = clean_mac, args = (msg.text, msg.from_user.id), daemon = True).start()
            return

        await bot.send_message(msg.from_user.id, 'Введите логин услуги или порт измерения. \
        Пример для логина: 77660000000 или 77060000000.\nПример для порта: [0.0.0.0] 0-0-0 или 0.0.0.0 0 0 0.\nВведите mac пиставки что бы его удалит, пример 00:00:00:00:00:00.')
    except Exception as e:
        print(e)




@bot.callback_query_handler(lambda c: c.data == 'port_searc')
async def process_callback_button1(callback_query: types.CallbackQuery):
    port_out = callback_query.message.text.split('\n')[0]
    print(port_out)
    await bot.answer_callback_query(callback_query.id)
    threading.Thread(target = port_login, args = (port_out, callback_query.from_user.id, otvet2), daemon = True).start()




@bot.callback_query_handler(lambda c: c.data == 'pasw_searc')
async def process_callback_button1(callback_query: types.CallbackQuery):
    login_out = callback_query.message.text.split('\n')[0]
    await bot.answer_callback_query(callback_query.id)
    threading.Thread(target = paswd, args = (login_out, callback_query.from_user.id), daemon = True).start()




@bot.callback_query_handler(lambda c: c.data == 'see_split')
async def process_callback_button1(callback_query: types.CallbackQuery):
    port_out = callback_query.message.text.split('\n')[-1]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Проверяю сплитер\nВремя на проверку ~ 4мин.')
    threading.Thread(target = see_split, args = (port_out, callback_query.from_user.id), daemon = True).start()





@bot.callback_query_handler(lambda c: c.data == 'see_olt')
async def process_callback_button1(callback_query: types.CallbackQuery):
    port_out = callback_query.message.text.split('\n')[-1]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Проверяю порт OLT\nВремя на проверку ~ 8мин.')
    threading.Thread(target = see_olt_port, args = (port_out, callback_query.from_user.id), daemon = True).start()




@bot.callback_query_handler(lambda c: c.data == 'kill_ses')
async def process_callback_button1(callback_query: types.CallbackQuery):
    login_out = callback_query.message.text.split('\n')[0]
    await bot.answer_callback_query(callback_query.id)
    threading.Thread(target = kill_session, args = (login_out, callback_query.from_user.id), daemon = True).start()




@bot.callback_query_handler(lambda c: c.data == 'update')
async def process_callback_button1(callback_query: types.CallbackQuery):
    login_out = callback_query.message.text.split('\n')[0]
    await bot.answer_callback_query(callback_query.id)
    threading.Thread(target = login, args = (login_out, callback_query.from_user.id, otvet1), daemon = True).start()




@bot.callback_query_handler(lambda c: c.data == 'port_update')
async def process_callback_button1(callback_query: types.CallbackQuery):
    port_out = (callback_query.message.text.split('\n')[-1])
    await bot.answer_callback_query(callback_query.id)
    threading.Thread(target = port, args = (port_out, callback_query.from_user.id, otvet2), daemon = True).start()




asyncio.run(bot.polling())

