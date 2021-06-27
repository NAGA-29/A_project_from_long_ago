import requests

import os
from os.path import join, dirname
from dotenv import load_dotenv


class lines:

    '''
    Initial Setting
    '''
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    def __init__(self, line_notify_token = os.environ.get('LINE_NOTIFY_TOKEN')):
        self._line_notify_api = 'https://notify-api.line.me/api/notify'
        self._line_notify_token = line_notify_token
        pass

    '''
    LINE
    '''
    def lineNotify(self,message):
        line_notify_token = os.environ.get('LINE_NOTIFY_TOKEN')
        line_notify_api = 'https://notify-api.line.me/api/notify'
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        requests.post(line_notify_api, data=payload, headers=headers,)

    '''
    画像用LINE
    '''
    def lineNotify_Img(self,message,imageUrl):
        line_notify_token = os.environ.get('LINE_NOTIFY_TOKEN')
        line_notify_api = 'https://notify-api.line.me/api/notify'
        payload = { 'type': 'image',
                    'imageFullsize': imageUrl,
                    'imageThumbnail': imageUrl,
                    'message': message
                    }
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        requests.post(line_notify_api, data=payload, headers=headers,)

    #         ###LINE
    # def lineNotify(message,imageUrl):
    #     line_notify_token = os.environ.get('LINE_NOTIFY_TOKEN')
    #     line_notify_api = 'https://notify-api.line.me/api/notify'
    #     payload = {'message': message}
    #     headers = {'Authorization': 'Bearer ' + line_notify_token}
    #     requests.post(line_notify_api, data=payload, headers=headers,)