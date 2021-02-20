### Telegram MeBot

Многопоточный, простой Телеграм бот на Python 3.

Данный бот как личный помощник, который может выполнять различные рутиные задачи. Получать команды ввида `/command` и реагировать на них выполняя полезную работу.

Бот принимает только команды ввида `/command` или `/command text text`. Название команды привязанно к методу класса. 

Очень легко создавать методы которые будут реагировать на полученные команды. Имя метода необходимо начинать со знака `_`.

### Установка

```
pip install mebot
```

Импортировать необходимые объекты

```
from mebot.telegram import main as mebot, BaseCoordinator
```

Сюда вставить ваш телеграм токен `TOKEN = os.getenv("TOKEN", "This YOU TOKEN")`


### Пример 1

```
from mebot.telegram import main as mebot, BaseCoordinator
import os

TOKEN = os.getenv("TOKEN", "")

class Command( BaseCoordinator ):
    """ 
    Атрибуты класса:
    'tg_object' --  данные от телеграма
    'chat_id' -- чат id
    'api_url' -- урл с токеном
    'command' -- команда которая была вызвана
    'storage' -- словарь для хранения различных данных для каждого клиента
    
    Доступ осуществляется через self.tg_object, self.chat_id и т.д.
    """

    def _start(self):
        """
        command /start
        """
        return "Привет!! Это твой Телеграм Бот. Готов тебе служить!"

    def _echo(self):
        """
        command /echo
        """
        return f"{self.command}"


if __name__ == '__main__':

    mebot( token=TOKEN, coordinator = Command )
```

### Пример 2

```
from mebot.telegram import main as mebot, BaseCoordinator
import time, os

TOKEN = os.getenv("TOKEN", "")

class Command( BaseCoordinator ):
    """ 
    Атрибуты класса:
    'tg_object' --  данные от телеграма
    'chat_id' -- чат id
    'api_url' -- урл с токеном
    'command' -- команда которая была вызвана
    'storage' -- словарь для хранения различных данных для каждого клиента
    
    Доступ осуществляется через self.tg_object, self.chat_id и т.д.
    """

    def _play(self):
        '''запустить спам сообщений'''
        self.storage["play"] = True
        i = 0
        while True:
            i+=1
            if not self.storage["play"]:
                break
            self.send_message( "{}. play **I 😲 Spamer**".format(i) )
            time.sleep(2)

        return "play stop"


    def _stop(self):
        '''остановить спам собщений'''
        self.storage["play"] = False


if __name__ == '__main__':

    mebot( token=TOKEN, coordinator = Command )

```


Полный ответ от телеграмма находится в атрибуте класса `self.tg_object`.

