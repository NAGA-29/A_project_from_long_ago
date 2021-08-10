from typing import List
import requests
from pprint import pprint 

import time
import dateutil.parser
from pytz import timezone

import sys
sys.path.append('../../../model/')
from DB_config import session
from TwitchVideo import TwitchVideo

class Twitch_Wrapper():

    _AUTH_URL = 'https://id.twitch.tv/oauth2/token'

    def __init__(self, client_id, secret):
        self.client_id = client_id
        self.secret  = secret
        

        _AUT_PARAMS = {'client_id': self.client_id,
                    'client_secret': self.secret,
                    'grant_type': 'client_credentials'
                    }

        self._AutCall = requests.post(url=self._AUTH_URL, params=_AUT_PARAMS) 
        self.access_token = self._AutCall.json()['access_token']
        self._head = {
            'Client-ID' : self.client_id,
            'Authorization' :  "Bearer " + self.access_token
            }

    def channel_info(self, channel_name: str) -> list:
        """channel_idからチャンネル情報を取得する
        :param channel_id: チャンネルネーム
        :type str
        :rtype list
        """
        URL = 'https://api.twitch.tv/helix/users?login=' + channel_name
        return requests.get(URL, headers= self._head).json()['data']


    def get_follower(self, twitch_id: str)-> int:
        '''
        twitchのチャンネル登録者を取得
        :param twitch_id:  対象のユーザーID
        :type str
        :rtype int 登録者人数
        '''
        URL = 'https://api.twitch.tv/helix/users/follows?to_id=' + twitch_id
        return requests.get(URL, headers= self._head).json()['total']


    def get_video_list(self, twitch_id: str)-> list:
        '''
        特定ユーザーのvideoを取得する
        :param str: 対象のユーザーID
        :type str
        :rtype list 動画一覧
        '''
        cursor = 'cursor'
        video_list = []
        URL = 'https://api.twitch.tv/helix/videos?first=100&user_id=' + twitch_id
        vd = requests.get(URL, headers= self._head).json()
        video_list = [i for i in vd['data']]
        cursor = vd['pagination'].get('cursor', None)

        while cursor:
            URL = 'https://api.twitch.tv/helix/videos?first=100&user_id=' + twitch_id +'&after=' + cursor
            vd = requests.get(URL, headers= self._head).json()
            for i in vd['data']:
                video_list.append(i)
            cursor = vd['pagination'].get('cursor', None)
            time.sleep(2)
        return video_list 


    def get_stream(self, twitch_id:str)-> list:
        URL = 'https://api.twitch.tv/helix/streams?user_id=' + twitch_id
        stream = requests.get(URL, headers= self._head).json()
        return stream


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
    auth_url = 'https://id.twitch.tv/oauth2/token'
    client_id = 'dfgvcsi22xnzq1t9c2dpmekadihy4l'
    secret  = '9yg5fc0iz3wytriy2qfm09ajx0e7eo'
    tw_w = Twitch_Wrapper(client_id, secret)
    # r = tw_w.channel_info('usadapekora_hololive')

    
    # r = tw_w.channel_info('fps_shaka')
    # pprint(r)
    # p = tw_w.get_follower('664278586')
    # pprint(p)

    # p = tw_w.get_video_list('557359020')
    # pprint(p)
    # pprint(len(p))

    stream = tw_w.get_stream('557359020')


    # for da in p :
    #     twitch = TwitchVideo()
    #     twitch.holo_name = 'さくらみこ'
    #     twitch.belongs = 'hololive'
    #     twitch.title = da['title']
    #     twitch.video_id = da['id']
    #     twitch.user_id = da['user_id']
    #     twitch.user_login = da['user_login']
    #     twitch.url = da['url']
    #     twitch.view_count = da['view_count']
    #     twitch.duration = da['duration']
    #     twitch.game_name = None
    #     twitch.game_id = None
    #     twitch.published_at = tw_w.convertToJST(da['published_at'])
    #     twitch.thumbnail_url = da['thumbnail_url']
    #     twitch.viewable = da['viewable']
    #     twitch.notification_last_time_at = '2000-01-01 00:00:00'
    #     session.add(twitch)  
    #     session.commit()
