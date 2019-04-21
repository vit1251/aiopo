#!/usr/bin/python

from logging import getLogger, basicConfig, DEBUG
from asyncio import get_event_loop
from aiopo import PushoverClient

APP_TOKEN = '...'
USER_KEY = '...'
MESSAGE = 'Hello, world!'

class Application(object):
    def __init__(self):
        self.__log = getLogger('aiopo-example')
        self.loop = None
        self.po = None

    async def start(self):
        """ Start corotine
        """
        self.po = PushoverClient(app_token=APP_TOKEN, user_key=USER_KEY)
        await self.po.notify(message=MESSAGE)

    async def stop(self):
        """ Stop corotine
        """

    def run(self):
        self.loop = get_event_loop()
        #
        self.loop.create_task(self.start())
        self.loop.run_forever()

if __name__ == "__main__":
    basicConfig(filename="debug.log", level=DEBUG)
    app = Application()
    app.run()
