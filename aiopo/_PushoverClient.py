
from logging import getLogger
from aiohttp import ClientSession


class PushoverClient(object):
    def __init__(self, app_token, user_key):
        self.__log = getLogger('aiopo')
        self._url = 'https://api.pushover.net/1/messages.json'
        self._app_token = app_token
        self._user_key = user_key

    async def notify(self, message):
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
        payload = {
            'token': self._app_token,
            'user': self._user_key,
            'message': message,
        }
        async with ClientSession() as session:
            async with session.post(self._url, data=payload) as resp:
                self.__log.debug("status = {status!r}".format(status=resp.status))
                if resp.status != 200:
                    raise RuntimeError('Pushover response code {status}'.format(status=resp.status))
                values = await resp.json()
                return values
