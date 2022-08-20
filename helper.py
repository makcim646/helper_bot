import requests
import re


class Helper():


    def __init__(self, login, password):
        self.url = 'https://helper.ural.rt.ru/main'
        self.s = requests.session()
        self.login = login
        self.password = password
        sesion = self.s.post(self.url, data={"act":"login", "login":"{}".format(login), "password":"{}".format(password)})




    def login_info(self,login):
        """Получит информацию по логну"""
        login_data = ['Пакеты', 'Баланс:', 'Статус', '<hr>Сессия:', 'Начало', 'Прод', 'mac-адрес:', 'порт']
        r = self.s.post(self.url, data={"act":"getinfologin","login":f"{login}","bi_id":11111111})
        list_data = r.text.split('<br>')


        if '<hr>Сессия:  НЕ АКТИВНА' in list_data:
            return f'{login}\nСессия:  НЕ АКТИВНА'

        else:
            text = f'{login}\n'
            for d in list_data:
                try:
                    if d.split()[0] in login_data:
                        text += d.strip('<hr>') + '\n'
                except:
                    pass

        return text




    def port_login(self,login):
        """Измерить состояние порта по логину"""
        r = self.s.post(self.url, data={"act":"measureont","login":f"{login}","bi_id":f"{login}"})
        list_data = r.text.split('</td>')

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
        text += port_searc

        return text




    def port_info(self, port):
        r = self.s.post(self.url, data={"act":"measureont","login":f"{port}","bi_id":f"{port}"})
        list_data = r.text.split('</td>')
        if r.json()['status'] == False:
            return "Невозможно измерить порт.\nПроверьте верность введеного ip\n"


        out =[]
        for i in list_data:
            out.append(i.split('<td>')[1])

        dic = []
        for i in range(0,14,2):
            dic.append([out[i], out[i+1]])

        text = ''
        for i in dic:
            text+= f'{i[0]} {i[1]}\n'

        text += port

        return text




    def paswd(self, login):
        """Получит пароль по логину"""
        r = self.s.post(self.url, data={"act":"getpppoepassword","login":f"{login}","bi_id":11111111})
        if r.json()['status'] == False:
            return "Немогу получить пароль."

        list_data = r.text.split('\\n')
        text = login + '\n' +list_data[4]

        return text




    def kill_session(self, login):
        """Сбросит PPPOE-сесию по логину"""
        r = self.s.post(self.url, data={"act":"killpppoesession","login":f"{login}","bi_id":11111111})
        if r.json()['status'] == True:
            return r.json()['body']

        return "Не удалось сбросит сессию"




    def clean_mac(self, mac):
        """отвязать мак от приставки"""
        r = self.s.post(self.url, data={"act":"erasemacs","login":f"{mac}","bi_id":11111111})
        if r.json()['status'] == True:
            return 'MAC удален'

        return 'Неверный MAC'




    def tv_info(self, login_tv):
        """Получить код активации по логину услуги на приставки"""
        r = self.s.post(self.url, data={"act":"getiptvpassword","login":f"{login_tv}","bi_id":11111111})
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




    def see_split(self, port, n):
        """Проверить сплитер на котром находиться данный порт"""
        text = ''

        if int(n) < 33:
            for c in range(0,33):
                r = self.s.post(self.url, data={"act":"measureont","login":f"{port+str(c)}","bi_id":f"{port}"})
                list_data = r.text.split('</td>')
                if r.json()['status'] == False:
                    return 'Невозможно измерить порт OLT \nПроверьте верность верность введеного ip'

                out =[]
                for i in list_data:
                    out.append(i.split('<td>')[1])

                text += out[5] + ' ' +  out[7] + '\n'
        else:
            for c in range(33, 65):
                r = self.s.post(self.url, data={"act":"measureont","login":f"{port+str(c)}","bi_id":f"{port}"})
                list_data = r.text.split('</td>')
                if r.json()['status'] == False:
                   return 'Невозможно измерить порт OLT \nПроверьте верность верность введеного ip'

                out =[]
                for i in list_data:
                    out.append(i.split('<td>')[1])

                text += out[5] + ' ' +  out[7] + '\n'

        return text




    def see_olt_port(self, port):
        """Проверить порт OLT"""
        text = ''
        for c in range(0,65):
                r = self.s.post(self.url, data={"act":"measureont","login":f"{port+str(c)}","bi_id":f"{port}"})
                list_data = r.text.split('</td>')
                if r.json()['status'] == False:
                    return f'Невозможно измерить порт OLT\nПроверьте верность верность введеного ip'

                out =[]
                for i in list_data:
                    out.append(i.split('<td>')[1])

                text += out[5] + ' ' +  out[7] + '\n'

        return text
    
    
    
    def update_session(self):
        sesion = self.s.post(self.url, data={"act":"login", "login":"{}".format(self.login), "password":"{}".format(self.password)})