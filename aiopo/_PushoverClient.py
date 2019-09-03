
from logging import getLogger
from aiohttp import ClientSession, FormData
from datetime import datetime
import mimetypes
import os.path

class PushoverClient(object):

    PRIORITY_LOWEST=-2
    PRIORITY_LOW=-1
    PRIORITY_NORMAL=0
    PRIORITY_HIGH=1
    PRIORITY_EMERGENCY=2

    sounds = ['pushover', 'bike', 'bugle', 'cashregister', 'classical', 'cosmic', 'falling', 'gamelan', 'incoming', 'intermission', 'magic', 'mechanical', 'pianobar', 'siren', 'spacealarm', 'tugboat', 'alien', 'climb', 'persistent', 'echo', 'updown', 'none']

    def __init__(self, app_token, user_key=None):
        self.__log = getLogger('aiopo')
        self._url = 'https://api.pushover.net/1/messages.json'
        self._app_token = app_token
        self._user_key = user_key

    async def notify(self, message, title=None, url=None, url_title=None, devices=None, priority=None, sound = None, timestamp=None, attachment=None):
        """ Push message

        Pushover API request is HTTPS POST request:

          token (required) - your application's API token
          user (required) - the user/group key (not e-mail address) of your user (or you), viewable when logged into our dashboard (often referred to as USER_KEY in our documentation and code examples)
          message (required) - your message 

        Some optional parameters may be included:

          attachment - an image attachment to send with the message; see attachments for more information on how to upload files
          device - your user's device name to send the message directly to that device, rather than all of the user's devices (multiple devices may be separated by a comma)
          title - your message's title, otherwise your app's name is used
          url - a supplementary URL to show with your message
          url_title - a title for your supplementary URL, otherwise just the URL is shown
          priority - send as -2 to generate no notification/alert, -1 to always send as a quiet notification, 1 to display as high-priority and bypass the user's quiet hours, or 2 to also require confirmation from the user
          sound - the name of one of the sounds supported by device clients to override the user's default sound choice
          timestamp - a Unix timestamp of your message's date and time to display to the user, rather than the time your message is received by our API 

        Response:

        DEBUG:aiopo:200
        DEBUG:aiopo:{"status":1,"request":"c36a3056-4377-4d88-9543-f6e5da94c781"}

        """
        form_data = FormData()
        payload = {
            'token': self._app_token,
            'user': self._user_key,
            'message': message,
        }
        files = []
        if title is not None : payload['title'] = title
        if url is not None : payload['url'] = url
        if url_title is not None : payload['url_title'] = url_title 
        # @todo: devices not working, if devices does'nt exists every body will get messages :'(
        if devices is not None : payload['devices'] = ','.join(devices)
        if priority is not None : payload['priority'] = priority
        if priority == PushoverClient.PRIORITY_EMERGENCY:
            payload['retry'] = 120
            payload['expire'] = 3600
        if sound is not None and sound in self.sounds : payload['sound'] = sound
        if timestamp is not None :
            if type(timestamp) == datetime:
                payload['timestamp'] = timestamp.strftime("%s")
            else:
                payload['timestamp'] = timestamp
        for key, value in payload.items():
            form_data.add_field(key, str(value))
        # @todo: test attachment 2.5Mo limit
        if attachment is not None:
            if os.path.isfile(attachment):
                form_data.add_field('attachment', open(attachment,"rb").read(), content_type=mimetypes.guess_type(attachment)[0], filename="32476688_544383832626131_3047482993925947392_n.jpg")
        
        async with ClientSession() as session:
            async with session.post(self._url, data=form_data) as resp:
                self.__log.debug("status = {status!r}".format(status=resp.status))
                if resp.status != 200:
                    raise RuntimeError('Pushover response code {status}'.format(status=resp.status))
                values = await resp.json()
                return values
