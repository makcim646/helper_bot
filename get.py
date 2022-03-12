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
import requests
import re
import time
from config import argus_login, argus_pass


url = 'https://helper.ural.rt.ru/main'
log = argus_login # Логин от Аргуса
pas = argus_pass    # Пароль от Аргуса
s = requests.session()
sesion = s.post(url, data={"act":"login", "login":"{}".format(log), "password":"{}".format(pas)})


def main():
    pass

def tv_code(login_tv):
    """Получить код активации по логину услуги на приставки"""
    r = s.post(url, data={"act":"getiptvpassword","login":f"{login_tv}","bi_id":11111111})
    if r.json()['status'] == True:
        data = r.text.split('\\n')

        mac_list = []
        for d in data:
          if re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', d, re.I) != None:
            mac_list.append(d)

        mac = ''
        for m in mac_list:
            mac += str(f'`{m}`' + '\n')

        return f'Логин: {data[5]}\nКод: {data[6]}\n\n' + mac
    else:
        return 'Неверный логин услуги'

def clean_mac(mac):
    r = s.post(url, data={"act":"erasemacs","login":f"{mac}","bi_id":11111111})
    if r.json()['status'] == True:
        return "MAC удален"
    else:
        return 'Неверный MAC'


def kill_session(login):
    """Сбросит PPPOE-сесию по логину"""
    r = s.post(url, data={"act":"killpppoesession","login":f"{login}","bi_id":11111111})
    if r.json()['status'] == True:
        return r.json()['body']
    return "Не удалось сбросит сессию"

def login(login):
    """Получит информацию по логну"""

    r = s.post(url, data={"act":"getinfologin","login":f"{login}","bi_id":11111111})
    list_data = r.text.split('<br>')
    if '<hr>Сессия:  НЕ АКТИВНА' in list_data:
        return f'{login}\nСессия:  НЕ АКТИВНА'
    else:
        data = []
        data += list_data[6:10]
        data += list_data[14:16]
        text = f'{login}\n'
        for i in data:
            text += i.strip('<hr>') + '\n'
            if 'порт подключения:' in i:
                port = (i.split(':')[1]).strip(' ')

        return text


def paswd(login):
    """Получит пароль по логину"""

    r = s.post(url, data={"act":"getpppoepassword","login":f"{login}","bi_id":11111111})
    if r.json()['status'] == False:
        return "Немогу получить пароль."
    list_data = r.text.split('\\n')
    return list_data[4]


def port_login(login):
    r = s.post(url, data={"act":"measureont","login":f"{login}","bi_id":f"{login}"})
    list_data = r.text.split('</td>')
    if r.json()['status'] == False:
        return "Невозможно измерить порт\n" + port


    out =[]
    for i in list_data:
        out.append(i.split('<td>')[1])

    dic = []
    for i in range(0,14,2):
        dic.append([out[i], out[i+1]])

    text = ''
    for i in dic:
        if i[0] == 'Номер порта':
            port_searc = i[1]
        text+= f'{i[0]} {i[1]}\n'

    return text + port_searc

def see_split(port):
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

    out_text = ''


    if int(a[6]) < 33:
        for c in range(1,33):
            r = s.post(url, data={"act":"measureont","login":f"{port+str(c)}","bi_id":f"{port}"})
            list_data = r.text.split('</td>')
            if r.json()['status'] == False:
                out_text += port + ' не возможно измерить' + '\n'

            out =[]
            for i in list_data:
                out.append(i.split('<td>')[1])

            dic = []
            for i in range(0,14,2):
                dic.append([out[i], out[i+1]])

            out_text += dic[2][1] + ' ' +  dic[3][1] + '\n'

            time.sleep(0.1)

    else:
        for c in range(33, 65):
            r = s.post(url, data={"act":"measureont","login":f"{port+str(c)}","bi_id":f"{port}"})
            list_data = r.text.split('</td>')
            if r.json()['status'] == False:
                out_text += port + ' не возможно измерить' + '\n'

            out =[]
            for i in list_data:
                out.append(i.split('<td>')[1])

            dic = []
            for i in range(0,14,2):
                dic.append([out[i], out[i+1]])

            out_text += dic[2][1] + ' ' +  dic[3][1] + '\n'
            time.sleep(0.1)

    return out_text


def port(port):
    """Измерить состояние порта по порту"""
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


    r = s.post(url, data={"act":"measureont","login":f"{port}","bi_id":f"{port}"})
    list_data = r.text.split('</td>')
    if r.json()['status'] == False:
        return "Невозможно измерить порт\n" + port


    out =[]
    for i in list_data:
        out.append(i.split('<td>')[1])

    dic = []
    for i in range(0,14,2):
        dic.append([out[i], out[i+1]])

    text = ''
    for i in dic:
        if i[0] == 'Номер порта':
            port_searc = i[1]
        text+= f'{i[0]} {i[1]}\n'

    return text + port_searc


