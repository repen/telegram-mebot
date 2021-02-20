"""
Copyright (c) 2021 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
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
