# 参考サイト: https://developer.twitter.com/en/docs/twitter-api/spaces/search/introduction
# 開発者ツール : https://developer.twitter.com/en/docs/twitter-api/tools-and-libraries

import requests
from typing import List
from pprint import pprint 

import time
import dateutil.parser
from pytz import timezone

import json

# import sys
# sys.path.append('../../../model/')
# from setting import session
# from TwitchVideo import TwitchVideo

class Twitter_Wrapper:

    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) -> None:
        self.CONSUMER_KEY = CONSUMER_KEY
        self.CONSUMER_SECRET = CONSUMER_SECRET
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.ACCESS_TOKEN_SECRET = ACCESS_TOKEN_SECRET

        
    def get_bearer_token(self):
        URL = 'https://api.twitter.com/oauth2/token'
        data = {
            'grant_type': 'client_credentials'
            }
        bearer_token = requests.post(URL, data=data, auth=(self.CONSUMER_KEY, self.CONSUMER_SECRET))
        return bearer_token.text

if __name__ == '__main__':

    CONSUMER_KEY_TEST = "OgUS1y3y7vuxy54NoKZvlOdq9"
    CONSUMER_SECRET_TEST = "hCRRA4WX5cEe50ScugCkF4MvFJeFvU8YFAiwGDBi2vkJ9PqyZL"
    ACCESS_TOKEN_TEST = "1000217159446945793-0LiJPmZvvyfaQvNhiY1pgL52pCTnuW"
    ACCESS_TOKEN_SECRET_TEST = "enagarkdimg1cdR4w8ZFZhEr0kyjVj8ekNRzmiZviz4z8"
    BEARER_TOKEN_TEST = 'AAAAAAAAAAAAAAAAAAAAAOqpBwEAAAAABIZV9k5aalFvNSy7Ay4NXQ7tOuo%3DvJhN33HjSVUpTzfS6mvf5OBSnagRk4TfVtQ2ckkibII7unjjep'
    tw = Twitter_Wrapper(CONSUMER_KEY_TEST, CONSUMER_SECRET_TEST, ACCESS_TOKEN_TEST, ACCESS_TOKEN_SECRET_TEST)

    baseUrl = 'https://api.twitter.com'
    url = f"{baseUrl}/2/spaces/:id?space.fields=host_ids&expansions=speaker_ids&user.fields=profile_image_url"

    payload={}
    headers = {
        'Authorization': 'Bearer ' + BEARER_TOKEN_TEST
        }

    response = requests.request("GET", url, headers=headers, data=payload)

    pprint(response.text)




# if __name__ == '__main__':

    # tw_w = Twitter_Wrapper()

    # r = tw_w.channel_info('usadapekora_hololive')

    
    # r = tw_w.channel_info('615692129')
    # pprint(r)
    
    # p = tw_w.get_follower('664278586')
    # pprint(p)

    # p = tw_w.get_video_list('557359020')
    # pprint(p)
    # pprint(len(p))

    # stream = tw_w.get_stream('557359020')
    # pprint(stream)

    # url = 'https://pvgllfml6j.execute-api.ap-northeast-1.amazonaws.com/Twitch-eventSub'
    # r = tw_w.register_eventSub('stream.online', url, '615692129')
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