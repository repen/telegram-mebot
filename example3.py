"""
Copyright (c) 2021 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License

Пример с сохранением состояния телеграм бота. 
Т.е если отключить бот, то данные безопасно можно скидывать на диск, а при включении легко их подгрузить.
В качестве базы данных используется модуль shelve.
Обратите внимание, что база данных доступна только приложению.

Рекомендуется хранить разумный размер данных.

"""
from mebot.telegram import main as mebot, BaseCoordinator
import os, shelve

TOKEN = os.getenv("TOKEN", "")

db = shelve.open( "application.ns" )

class AppStorage:

    cache = {}

    def __init__(self, *args, **kwargs):
        self.db = db
        self._id = str(args[0])

    def get_storage(self):
        # breakpoint()
        if self._id not in self.db.keys():
            self.db[self._id] = {}

        if self._id not in AppStorage.cache.keys():
            AppStorage.cache[self._id] = self.db[self._id]

        return AppStorage.cache[self._id]
        # return self.db[self._id]

    def dump_storage(self, data):
        self.db[self._id] = data
        AppStorage.cache[self._id] = data

    def setitem(self, key, value):
        self.db[self._id][key] = value


    def getitem(self, key):
        if key not in self.db[self._id].keys():
            return None
        return self.db[self._id][key]


class Command( BaseCoordinator, AppStorage ):
    """ 
    Атрибуты класса:
    'tg_object' --  данные от телеграма
    'chat_id' -- чат id
    'api_url' -- урл с токеном
    'command' -- команда которая была вызвана
    'storage' -- словарь для хранения различных данных для каждого клиента
    
    Доступ осуществляется через self.tg_object, self.chat_id и т.д.
    """

    def __init__(self, tg_object):
        BaseCoordinator.__init__(self, tg_object)
        AppStorage.__init__(self, self.chat_id)
        self.dict = self.get_storage()


    def _counter(self):
        '''команда счетчик, при запуске увеличивает значение на 1'''
        print(self.dict)
        if not self.getitem("i"):
            self.dict["i"] = 0

        result = self.dict["i"]
        self.dict["i"] += 1
        # self.dump_storage(self.dict)
        return 'Count: {}'.format( result )


def close_db():
    '''Закрываем полку при уничтожения главного объекта'''
    db.close()


if __name__ == '__main__':

    mebot( token=TOKEN, coordinator = Command, callback_delete=[ close_db, ] )
