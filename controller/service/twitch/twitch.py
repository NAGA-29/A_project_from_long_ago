# 参考サイト:https://ogp.buta3.net/

from typing import List
import requests
from pprint import pprint 

import time
import dateutil.parser
from pytz import timezone

import json

# import sys
# sys.path.append('../../../model/')
# from setting import session
# from TwitchVideo import TwitchVideo
class Twitch_Wrapper:

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


    def register_eventSub(self, my_type:str, call_back_url:str, user_id:str):
        '''
        webhook登録
        :param str my_type: サブスクリプションタイプ
        :param str call_back_url: call back先のURL
        :param str user_id: 監視先アカウントID
        '''
        URL = 'https://api.twitch.tv/helix/eventsub/subscriptions'
        call_back = call_back_url
        headers = {
                'Client-ID' : self.client_id,
                'Authorization' :  "Bearer " + self.access_token,
                'Content-Type' : 'application/json',
                }

        payload = {
                "type": my_type,
                "version": "1",
                "condition": {
                    "broadcaster_user_id": user_id,
                },
                "transport": {
                    "method": "webhook",
                    "callback": call_back,
                    "secret": self.secret
                }
            }
        r = requests.post(URL, headers=headers, data=json.dumps(payload)).json()
        return r

    def delete_eventSub(self, subscription_id, call_back_url:str, user_id:str):
        URL = 'https://api.twitch.tv/helix/eventsub/subscriptions'
        subscription_id = ''
        headers = {
                'Client-ID' : self.client_id,
                'Authorization' :  "Bearer " + self.access_token,
                'Content-Type' : 'application/json',
                }

        r = requests.delete(URL, headers=headers).json()
        # r.headers
        pprint(r)

    def eventSub_list(self,status=None):
        '''
        登録したサブスクリプションイベントの一覧を取得
        :param int status: 1:全て, 2:登録成功のみ
        :rType dict: 取得したレスポンス内容
        '''
        URL = 'https://api.twitch.tv/helix/eventsub/subscriptions'
        if status == 1:
            URL = 'https://api.twitch.tv/helix/eventsub/subscriptions?status=enabled'
        elif status == 2:
            URL = 'https://api.twitch.tv/helix/eventsub/subscriptions?status=webhook_callback_verification_pending'
        elif status == 3:
            URL = 'https://api.twitch.tv/helix/eventsub/subscriptions?status=webhook_callback_verification_failed'
        elif status == 4:
            URL = 'https://api.twitch.tv/helix/eventsub/subscriptions?status=notification_failures_exceeded'
        elif status == 5:
            URL = 'https://api.twitch.tv/helix/eventsub/subscriptions?status=authorization_revoked'
        elif status == 6:
            URL = 'https://api.twitch.tv/helix/eventsub/subscriptions?status=user_removed'

        headers = {
            'Client-ID' : self.client_id,
            'Authorization' :  "Bearer " + self.access_token,
            'Content-Type' : 'application/json',
            }
        r = requests.get(URL, headers=headers).json()
        pprint(r)
        return r


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
    # auth_url = 'https://id.twitch.tv/oauth2/token'
    client_id = 'dfgvcsi22xnzq1t9c2dpmekadihy4l'
    secret = '9yg5fc0iz3wytriy2qfm09ajx0e7eo'

    # tw_w = Twitch_Wrapper(client_id, secret)
    # r = tw_w.channel_info('_hololive')
    # pprint(r)

    # チャンネル情報
    # r = tw_w.channel_info('770319696')
    # pprint(r)
    
    # フォロワー数
    # p = tw_w.get_follower('773041510')
    # pprint(p)

    # p = tw_w.get_video_list('557359020')
    # pprint(p)
    # pprint(len(p))

    # stream = tw_w.get_stream('557359020')
    # pprint(stream)

    # webhook登録
    # url = 'https://pvgllfml6j.execute-api.ap-northeast-1.amazonaws.com/Twitch-eventSub'
    # r = tw_w.register_eventSub('stream.online', url, '770319696')
    # pprint(r)

    # tw_w.eventSub_list(1)

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

# テスト用
# 'id': '615692129',
#   'login': 'naganegi35',
# momosuzunene_hololive