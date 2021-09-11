# from pytwitcasting.auth import TwitcastingApplicationBasis
# from pytwitcasting.api import API
from pytwitcasting.utils import get_access_token_prompt_implicit

import requests
from pprint import pprint 

import time
import dateutil.parser
from pytz import timezone

import base64

import sys
# sys.path.append('../../../model/')
# from setting import session
# from setting import *
# from TwitchVideo import TwitchVideo

class Twitcasting_Oauth2:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        OAth_URL = 'https://apiv2.twitcasting.tv/oauth2/authorize?client_id=' + self.client_id +'&response_type=token'
        response = requests.get(url=OAth_URL)

        Headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            }

        Params = {
            'code' : self.code,
            'grant_type' : 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri' : self.redirect_uri,
            }

        response = requests.post(url=OAth_URL, params=Params, headers=Headers)
        # self.access_token = response.json()
        pprint(response)


class Twitcasting_Wrapper():
    _Api_Base_url = 'https://apiv2.twitcasting.tv'
    _HEADER = {}
    def __init__(self, client_id, secret, access_token):
        self.client_id = client_id
        self.secret  = secret
        self.access_token = access_token
        
        self._AUT_PARAMS = {'client_id': self.client_id,
                    'client_secret': self.secret,
                    'grant_type': 'client_credentials'
                    }

        self._HEADER = {
            'Accept' : 'application/json',
            'X-Api-Version' : '2.0',
            'Authorization' : 'Bearer ' + self.access_token,
        }
        base_64 = f"{self.client_id}:{self.secret}"
        self.BASE64_ENCODED_STRING = base64.b64encode(base_64.encode()).decode()

    def get_user_info(self, id:str)->dict:
        '''
        ツイキャス ユーザー情報取得
        :param str id: idまたはscreen_id
        :rtype dict
        '''
        BASE_URL = 'https://apiv2.twitcasting.tv/users/'
        URL = BASE_URL + id
        return requests.get(URL, headers= self._HEADER).json()


    def get_live_thumbnail_image(self, id, position=None)->str:
        '''
        ツイキャス live中のサムネ取得
        :param str id: idまたはscreen_id
        :return: サムネURL
        :rtype str
        '''
        param = ''
        if position == 'beginning':
            param = '&position=beginning'

        BASE_URL = 'https://apiv2.twitcasting.tv/users/'
        URL = BASE_URL + id + '/live/thumbnail?size=large' + param
        return requests.get(URL).url


    def get_movie_info(self, movie_id:str)->dict:
        '''
        ツイキャス ライブ(動画)情報取得 (個別の動画の情報)
        :param str movie_id: 動画ID
        :rtype dict
        '''
        BASE_URL = 'https://apiv2.twitcasting.tv/movies/'
        URL = BASE_URL + movie_id
        return requests.get(URL, headers= self._HEADER).json()


    def get_movies_by_user(self, id:str, offset=None,limit=None)->dict:
        '''
        ツイキャス ユーザーが保有する過去ライブ（録画）の一覧を作成日時の降順で取得
        :param str id: idまたはscreen_id
        :param int offset: 先頭からの位置 default 0
        :param int limit: 最大取得件数 default 50
        :rtype: dict or list
        '''
        Offset = 0
        Limit = 50
        if offset:
            if offset >= 1 and offset <= 1000:
                Offset = offset
        if limit:
            if limit >= 0 and limit <= 50:
                Limit = limit

        BASE_URL = 'https://apiv2.twitcasting.tv/users/'
        URL = BASE_URL + id + '/movies?offset=' + str(Offset) + '&limit=' + str(Limit)
        return requests.get(URL, headers= self._HEADER).json()


    def get_current_live(self, id:str)->dict:
        '''
        ツイキャス 特定ユーザーが配信中の場合、ライブ情報を取得
        :param str id: idまたはscreen_id
        :rtype: dict
        '''
        URL = 'https://apiv2.twitcasting.tv/users/' + id + '/current_live'
        return requests.get(URL, headers= self._HEADER).json()


    def get_comments(self, movie_id:str, limit=None,offset=None,all=False):
        '''
        ツイキャス コメントを作成日時の降順で取得する。
        処理がおわるまでに時間が掛かる
        :param str movie_id: 動画ID
        :param int offset: 先頭からの位置 default 0　
        :param int limit: 最大取得件数 default 50 
        :rtype: dict
        '''
        base_url = 'https://apiv2.twitcasting.tv/movies/'
        if not all:
            Offset = 0
            Limit = 50
            if offset:
                if offset >= 0:
                    Offset = offset
            if limit:
                if limit >= 1 and limit <= 50:
                    Limit = limit
            params = {'offset':Offset, 'limit':Limit,}
            URL = base_url + movie_id + '/comments' 
            return requests.get(URL, params=params, headers= self._HEADER).json()
        else:
            Offset = 0
            Limit = 50
            params = {'offset':Offset, 'limit':Limit,}
            URL = base_url + movie_id + '/comments' 
            data = requests.get(URL, params=params, headers= self._HEADER).json()
            comments = [x for x in data['comments']]
            count = len(comments)
            all_count = data['all_count']
            while True:
                Offset = count + 1
                params = {'offset':Offset, 'limit':Limit,}
                data = requests.get(URL, params=params, headers=self._HEADER).json()
                if data['comments'] or all_count > count:
                    for m in data['comments']:
                        comments.append(m)
                    count = len(comments)
                    time.sleep(2)
                else:
                    break
            return comments


    def get_webhook_list(self)->dict:
        '''
        ツイキャス webhookに登録中のリストを取得
        :rtype dict
        '''
        URL = 'https://apiv2.twitcasting.tv/webhooks'
        header = {
            'Accept' : 'application/json',
            'X-Api-Version' : '2.0',
            'Authorization' : 'Basic ' + self.BASE64_ENCODED_STRING
        }
        return requests.get(URL, headers= header).json()


    def register_webhook(self, id: str):
        '''
        ツイキャス webhookに登録
        :param str id: 特定ユーザーのユーザーID
        '''
        URL = 'https://apiv2.twitcasting.tv/webhooks'
        header = {
            'Accept' : 'application/json',
            'X-Api-Version' : '2.0',
            'Authorization' : 'Basic ' + self.BASE64_ENCODED_STRING
        }
        data = '{"user_id": "' + id + '", "events": ["livestart", "liveend"]}'
        return requests.post(URL, data= data, headers= header).json()


    def remove_webhook(self, id:str, livestart=False, liveend=False):
        '''
        ツイキャス 登録中webhookイベントを削除
        :param str id: 特定ユーザーのユーザーID
        :param livestart bool: 削除するか判定
        :param liveend bool: 削除するか判定
        '''
        URL = 'https://apiv2.twitcasting.tv/webhooks'
        headers = {
            'Accept' : 'application/json',
            'X-Api-Version' : '2.0',
            'Authorization' : 'Basic ' + self.BASE64_ENCODED_STRING
        }

        events = []
        if livestart:
            events.append('livestart')
        if liveend:
            events.append('liveend')

        params = {'user_id' : id, 'events[]': events,}
        return requests.delete(URL, headers=headers, params=params).json()


    def convertToJST(self,time):
        '''
        日本時間に変換
        '''
        try:
            jst_timestamp = dateutil.parser.parse(time).astimezone(timezone('Asia/Tokyo'))
            updateJST = jst_timestamp.strftime('%Y/%m/%d %H:%M')
            return updateJST
        except Exception as err:
            return None


if __name__ == '__main__':
    client_id = 'cnagaki.be009e418b38e1c58bc43679760c8b7e2dc13db8598ca9e5557b5d1c47402cf5'
    client_secret = '6cc3c1bf8b54751629a4c9105c50690fad27de44c0cb0d34831b9d41829a8935'
    redirect_uri = 'https://twitter.com/HololiveP'
    # access_token = get_access_token_prompt_implicit(client_id=client_id)
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjdiYWUwODU0MDg4YTA2ZTM1NTg4Njg0ZGZmZDM0YTEzNWY4MzEwYzI4YzUzY2NhMzBiYzJjOGViNDcxNjAwZjE5NGM3NjM4YzEwZjZhMDRkIn0.eyJhdWQiOiJjbmFnYWtpLmJlMDA5ZTQxOGIzOGUxYzU4YmM0MzY3OTc2MGM4YjdlMmRjMTNkYjg1OThjYTllNTU1N2I1ZDFjNDc0MDJjZjUiLCJqdGkiOiI3YmFlMDg1NDA4OGEwNmUzNTU4ODY4NGRmZmQzNGExMzVmODMxMGMyOGM1M2NjYTMwYmMyYzhlYjQ3MTYwMGYxOTRjNzYzOGMxMGY2YTA0ZCIsImlhdCI6MTYyODQxOTgzMSwibmJmIjoxNjI4NDE5ODMxLCJleHAiOjE2NDM5NzE4MzEsInN1YiI6IjEyOTUzNDEzMDEzMzY5NjUxMjAiLCJzY29wZXMiOlsicmVhZCIsIndyaXRlIl19.tkzgPiiKL0nWa2P_pJ1xH9NwIjK7MDIEixd8n6652FqvyOsL9lIqqNAuTQc0l3p1duOJ0xinPiW5ENDyLUIt_3cL78s28DU8WiaqLRwaZCtm2xCPvFR7Zl-QVae4R9t4UyPPTuakOVqhLQwNmrV9p2yZr3RwKN32Rg0H_y93Im4bL_-aaZXvMFqUZGiTjjM8-_S7PPHaf2pzMOqjI4J90phM1vLNKWlwe3w1hjtapkCOOUYDAQZHp-kr4fZtQFgJebg88u0QQYpQ5Q9iWmL6_kP6AVoXMUH4dpQ8g4isRQ5t6Wqg6yEcJ6SCcBB_5VtOsZcq9TeqjZUiRkS8qhgfHQ'
    # oauth = Twitcasting_Oauth2(client_id, client_secret, redirect_uri)
    twc_w = Twitcasting_Wrapper(client_id, client_secret, access_token)
    # t = twc_w.get_user_info('c:nagaki')
    # pprint(t)

    # video = twc_w.get_movies_by_user('oozorasubaru')
    # pprint(video)

    # webhook = twc_w.get_webhook_list()
    # pprint(webhook)
    # webhook = twc_w.register_webhook('c:nagaki')
    # pprint(webhook)
    # rm = twc_w.remove_webhook('1024528894940987392', liveend=True)
    # pprint(rm)
    # comments = twc_w.get_comments('679488595',limit=50, offset=0)

    # mv = twc_w.get_movie_info('695864158')
    # pprint(mv)

    # comments = twc_w.get_comments('679488595',all=True)
    # pprint(comments)
    # pprint(len(comments))

# oozorasubaru
# 1027853566780698624

# shirakamifubuki
# 997786053124616192

# natsuiromatsuri
# 996645451045617664

# nekomataokayu
# 1109751762733301760

# himemoriluna
# 1200396798281445376

# yozoramel
# 985703615758123008

# yuzukichococh
# 1024970912859189248

# robocosan
# 960340787782299648

# akirosenthal
# 996643748862836736

# akaihaato
# 998336069992001537

# minatoaqua
# 1024528894940987392
