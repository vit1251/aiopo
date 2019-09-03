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
        await self.po.notify(
            message=MESSAGE, 
            title='AIOPO Github',
            devices=['BOB'], # not working
            url='https://github.com/vit1251/aiopo', 
            url_title='Aiopo page on github',
            sound='mechanical',
            priority=PushoverClient.PRIORITY_NORMAL,
            timestamp = datetime.now() + timedelta(seconds = 60 * 10), # or direct timestamp
            attachment = '<path to jpg>'
        )

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
