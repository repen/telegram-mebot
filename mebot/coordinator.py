"""
Copyright (c) 2021 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
from datetime import datetime
import time, re, requests, json


class BaseCoordinator:

    _dict = {}

    def __init__(self, tg_object ):
        self.tg_object= tg_object
        self.chat_id  = tg_object["message"]["chat"]["id"]
        self.api_url  = tg_object["api_url"]
        self.command  = tg_object["message"]["text"]

        self.dict = self.storage = BaseCoordinator._dict.setdefault(self.chat_id, {} )

        self.__command_list = [ x for x in dir( self ) if re.search(r"^\_{1}[A-Za-z]\w+$", x) ]

    def send_message(self, text, additional=None):
        params = {'chat_id': self.chat_id, 'text': text, "parse_mode" : "markdown"}
        method = 'sendMessage'
        if additional:
            params.update( additional )
        resp = requests.post(self.api_url + method, params)
        return resp


    def _time(self):
        """
        command /time
        """
        return "Текущее время ⏰: {}".format( datetime.now().strftime("%H:%M:%S") )

    def _sys_info(self):
        """
        command /sys_info
        """
        import platform,socket,re, uuid, json

        def getSystemInfo():
            info={}
            info['platform']=platform.system()
            info['platform-release']=platform.release()
            info['platform-version']=platform.version()
            info['architecture']=platform.machine()
            info['hostname']=socket.gethostname()
            info['ip-address']=socket.gethostbyname(socket.gethostname())
            info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
            info['processor']=platform.processor()
            return info

        return "`{}`".format( json.dumps( getSystemInfo(), sort_keys=True, indent=4 ) )

    def _favorite_url(self):
        """
        command /favorite_url
        Markdown
        """
        string = """
*Favorite url list* ⭐ ⭐ ⭐

0. [google](https://google.com)
1. [yandex](https://ya.ru)
""".strip()
        return string

    def _author(self):
        """
        command /author
        Markdown
        """
        string = """
Feedback Plugin Andrey 😍:

0. [Github](https://github.com/repen)
1. [Linkdin](https://www.linkedin.com/in/%D0%B0%D0%BD%D0%B4%D1%80%D0%B5%D0%B9-%D0%BF%D0%BB%D1%83%D0%B3%D0%B8%D0%BD-782147b8/)
2. Email = 9keepa@gmail.com
        """.strip()
        return string

    def _about(self):
        string = "Я телеграм бот `Py-Telegram`."
        string += "Мои исходные коды существуют тут [py-telegram](https://github.com/repen/py-telegram)."
        string += "\n Пожалуйста заглядывате ко мне в гости. Вы можете улучшить меня."
        return string

    def _o1t2h3e4r(self):
        string = "Извините но мне не запрограмировали эту команду. \n"
        string += "`{}` . Спасибо за понимание. ".format( self.command )
        return string

    def __call__(self, *args, **kwargs):
        if not re.search(r"^\/[A-z]", self.command):
            return
        
        cmd = self.command[1:]
        cmd = re.findall(r"^\w+", cmd)[0]
        cmd = "".join(["_", cmd])

        if cmd in self.__command_list:
            result = getattr(self, cmd)
        else:
            result = getattr(self, "_o1t2h3e4r")
        text = result()
        if text:
            return self.send_message( text )
