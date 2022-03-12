from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from get import *
import re
from config import telegram_token

bot = Bot(telegram_token) #Telegram bot token
dp = Dispatcher(bot)


button1 = InlineKeyboardButton("Опросить порт", callback_data='port_searc')
button2 = InlineKeyboardButton("Посмотрет пароль", callback_data='pasw_searc')
button3 = InlineKeyboardButton("Сбросить PPPOE-сесию", callback_data='kill_ses')
button4 = InlineKeyboardButton("Обновить информацию", callback_data='update')
button5 = InlineKeyboardButton("Обновить информацию", callback_data='port_update')
button6 = InlineKeyboardButton("Проверить весь сплитор", callback_data='see_split')


otvet1 = InlineKeyboardMarkup(row_width=2).add(button1,button2, button3, button4, button6)
otvet2 = InlineKeyboardMarkup().add(button5, button6)



@dp.message_handler()
async def echo_message(msg: types.Message):
    try:
        math = re.fullmatch(r'\[?\d*\.\d*.\d*\.\d*\]?.*', msg.text)
        if math:
            await bot.send_message(msg.from_user.id, port(msg.text), reply_markup=otvet2)
            return

        math = re.fullmatch(r'7766\d{7}', msg.text)
        if math:
            await bot.send_message(msg.from_user.id, login(msg.text), reply_markup=otvet1)
            await bot.send_message(msg.from_user.id, port_login(msg.text), reply_markup=otvet2)
            return

        math = re.fullmatch(r'7706\d{7}', msg.text)
        if math:
            await bot.send_message(msg.from_user.id, tv_code(msg.text), parse_mode=types.ParseMode.MARKDOWN_V2)
            return
        math = re.fullmatch(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', msg.text)
        if math:
            await bot.send_message(msg.from_user.id, clean_mac(msg.text))
            return

        await bot.send_message(msg.from_user.id, 'Введите логин услуги или порт измерения. \
        Пример для логина: 77660000000 или 77060000000.Пример для порта: [0.0.0.0] 0-0-0 или 0.0.0.0 0 0 0. \nВведите mac пиставки что бы его удалит, пример 00:00:00:00:00:00.')

    except Exception as e:
        print(repr(e))

@dp.callback_query_handler(lambda c: c.data == 'port_searc')
async def process_callback_button1(callback_query: types.CallbackQuery):
    port_out = (callback_query.message.text.split('\n')[-1].split(":")[1]).strip(" ")
    await bot.answer_callback_query(callback_query.id)
    if port_out != 'НЕ АКТИВНА':
        await bot.send_message(callback_query.from_user.id, port(port_out), reply_markup=otvet2)
    else:
        await bot.send_message(callback_query.from_user.id, 'Я не знаю порта, введи его вручную.')

@dp.callback_query_handler(lambda c: c.data == 'pasw_searc')
async def process_callback_button1(callback_query: types.CallbackQuery):
    login_out = callback_query.message.text.split('\n')[0]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, paswd(login_out))


@dp.callback_query_handler(lambda c: c.data == 'see_split')
async def process_callback_button1(callback_query: types.CallbackQuery):
    port_out = callback_query.message.text.split('\n')[-1]
    await bot.send_message(callback_query.from_user.id, 'Проверяю сплитер')
    await bot.send_message(callback_query.from_user.id, see_split(port_out))





@dp.callback_query_handler(lambda c: c.data == 'kill_ses')
async def process_callback_button1(callback_query: types.CallbackQuery):
    login_out = callback_query.message.text.split('\n')[0]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, kill_session(login_out))



@dp.callback_query_handler(lambda c: c.data == 'update')
async def process_callback_button1(callback_query: types.CallbackQuery):
    login_out = callback_query.message.text.split('\n')[0]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, login(login_out), reply_markup=otvet1)





@dp.callback_query_handler(lambda c: c.data == 'port_update')
async def process_callback_button1(callback_query: types.CallbackQuery):
    port_out = (callback_query.message.text.split('\n')[-1])
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, port(port_out), reply_markup=otvet2)




if __name__ == '__main__':
    executor.start_polling(dp)