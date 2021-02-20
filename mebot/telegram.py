"""
Copyright (c) 2021 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
import requests, time
from .tool import log as logger
from itertools import count
from queue import Queue
from threading import Thread, active_count
from .coordinator import BaseCoordinator

log = logger("telegram")

incoming_queue = Queue()

class CheckingInputData:
    '''
    Проверка данных на входе. Если сообщение от пользователя не текст,
    то игнорируем обработку этого сообщения.
    '''
    def __init__(self, fun):
        self.function = fun

    def __call__(self, *args, **kwargs):
        try:
            telegram = args[0]
            if "message" not in telegram.keys():
                raise ValueError("{}".format( str(telegram) ))
            if "text" not in telegram["message"].keys():
                raise ValueError("{}".format( str(telegram["message"]) ))

            result = self.function(*args, **kwargs)
            
            # breakpoint()
            log.info("[Client id: %d] - [Command: %s]", telegram["message"]["from"]["id"], telegram["message"]["text"])

            return result
        except ValueError as e:
            log.error("[ %s ]", e , exc_info=True)
            return

@CheckingInputData
def task_service( item, queue, Coordinator ):
    coordinator = Coordinator( item )
    coordinator()
    queue.task_done()

def queue_service(*args, **kwargs):
    
    Coordinator=args[0]
    
    while True:
        item = incoming_queue.get()

        thr = Thread(target=task_service, args=(item, incoming_queue, Coordinator), daemon=True)
        thr.start()
        log.info("Thread active / Активные потоки: %d", active_count())


class Telegram:

    def __init__(self, token):
        self.token     = token
        self.update_id = None
        self.api_url   = "https://api.telegram.org/bot{}/".format(self.token)
        self.timeout   = 10

    def get_updates(self):
        while True:
            method = 'getUpdates'
            params = {'timeout': self.timeout, 'offset': self.update_id}
            try:
                resp = requests.get(self.api_url + method, params,timeout=self.timeout*2)
                message_list = resp.json()['result']
                return message_list
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as Er:
                log.error("Error connect %s. reconnect", Er)
                time.sleep(5)

    def get_update(self):
        method = 'getUpdates'
        params = { 'timeout': self.timeout, 'offset': self.update_id }
        try:
            resp = requests.get(self.api_url + method, params, timeout=self.timeout*2)
            data = resp.json()

            if "result" in data.keys():
                message_list = data['result']
            else:
                return

            if message_list:
                if self.update_id is None:
                    self.update_id = message_list[0]['update_id']
                return message_list[0]
            else:
                return
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as Er:
            log.info("Error connect %s. reconnect", Er)
            time.sleep(5)


    def _echo(self):

        for _ in count():
            update = self.get_update()
            if not update:
                break
            # log.info("Data: %s", update)
            # New logic

            # ==========
            self.update_id += 1
            update.update({"api_url" : self.api_url})
            incoming_queue.put( update )


    def echo(self):
        log.info("Start MeBot")
        try:
            self.update_id = self.get_updates()[0]['update_id']
        except IndexError:
            pass

        while True:
            try:
                self._echo()
            except KeyboardInterrupt:
                log.info("Ctr + C (Break)")
                break

        log.info("Stop telegram bot")


    def main(self):
        self.echo()

def main(*args, **kwargs):
    
    TOKEN = kwargs.setdefault("token", None)
    Coordinator = kwargs.setdefault("coordinator", None)
    
    if not TOKEN :
        raise ValueError("Please Set Telegram TOKEN = (https://romua1d.ru/kak-poluchit-token-bota-telegram-api/) ")

    if not Coordinator:
        raise ValueError("coordinator error!")

    
    Thread(target=queue_service, args=(Coordinator,), daemon=True).start()
    bot = Telegram(TOKEN)
    bot.main()

if __name__ == '__main__':
    main()


