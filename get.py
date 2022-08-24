
import time
from config import argus_login as log, argus_pass as pas, telegram_token
import telebot
from helper import Helper


bot = telebot.TeleBot(telegram_token, parse_mode='MARKDOWN')
helper = Helper(log, pas)


def update_session():
    while True:
        time.sleep(60*60)
        helper.update_session()
      
        
def status_sesion():
    sesion = helper.update_session()
    return sesion
          

def tv_code(login_tv, msg_id):
    """Получить код активации по логину услуги на приставки"""
    text = helper.tv_info(login_tv)
    bot.send_message(msg_id, text)


def clean_mac(mac, msg_id):
    """отвязать мак от приставки"""
    text = helper.clean_mac(mac)
    bot.send_message(msg_id, text)


def kill_session(login, msg_id):
    """Сбросит PPPOE-сесию по логину"""
    text = helper.kill_session(login)
    bot.send_message(msg_id, "Не удалось сбросит сессию")


def login(login, msg_id, markup):
    """Получит информацию по логну"""
    text = helper.login_info(login)
    bot.send_message(msg_id, text, reply_markup=markup)


def paswd(login, msg_id):
    """Получит пароль по логину"""
    text = helper.paswd(login)
    bot.send_message(msg_id, text)


def port_login(login, msg_id, markup):
    """Измерить состояние порта по логину"""
    text = helper.port_login(login)
    bot.send_message(msg_id, text, reply_markup=markup)


def see_olt_port(port, msg_id):
    """Проверить порт OLT"""
    port_data = port.strip('[').split('.')
    a = port_data[0:3]
    if port_data[3][-3] == '-':
        new = port_data[3].split(' ')
        a.append(new[0].strip(']'))
        for i in new[1].split('-'):
            a.append(i)

    elif port_data[3][-2] == '-':
        new = port_data[3].split(' ')
        a.append(new[0].strip(']'))
        for i in new[1].split('-'):
            a.append(i)

    else:
        for i in port_data[3].split(' '):
            a.append(i.strip(']'))


    port = f'[{a[0]}.{a[1]}.{a[2]}.{a[3]}] {a[4]}-{a[5]}-'

    text = helper.see_olt_port(port)
    bot.send_message(msg_id, text)


def see_split(port, msg_id):
    """Проверить сплитер на котром находиться данный порт"""
    port_data = port.strip('[').split('.')
    a = port_data[0:3]
    if port_data[3][-3] == '-':
        new = port_data[3].split(' ')
        a.append(new[0].strip(']'))
        for i in new[1].split('-'):
            a.append(i)

    elif port_data[3][-2] == '-':
        new = port_data[3].split(' ')
        a.append(new[0].strip(']'))
        for i in new[1].split('-'):
            a.append(i)

    else:
        for i in port_data[3].split(' '):
            a.append(i.strip(']'))


    port = f'[{a[0]}.{a[1]}.{a[2]}.{a[3]}] {a[4]}-{a[5]}-'

    text = helper.see_split(port, a[6])
    bot.send_message(msg_id, text, )


def port(port, msg_id, markup):
    """Измерить состояние порта"""
    port_data = port.strip('[').split('.')
    a = port_data[0:3]
    if port_data[3][-3] == '-':
        new = port_data[3].split(' ')
        a.append(new[0].strip(']'))
        for i in new[1].split('-'):
            a.append(i)

    elif port_data[3][-2] == '-':
        new = port_data[3].split(' ')
        a.append(new[0].strip(']'))
        for i in new[1].split('-'):
            a.append(i)

    else:
        for i in port_data[3].split(' '):
            a.append(i.strip(']'))

    port = f'[{a[0]}.{a[1]}.{a[2]}.{a[3]}] {a[4]}-{a[5]}-{a[6]}'

    text = helper.port_info(port)
    bot.send_message(msg_id, text, reply_markup=markup)
