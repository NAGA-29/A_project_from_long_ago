import tweepy
# import requests

from pprint import pprint
import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from config import app

class tweet_components:
    '''
    Initial Setting
    '''
    # # twitter本番アカウント My_Hololive_Project
    # CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
    # CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
    # ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    # ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

    # # twitter本番アカウント My_Hololive_Art_project
    # CONSUMER_KEY = os.environ.get('CONSUMER_KEY_A')
    # CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET_A')
    # ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN_A')
    # ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET_A')

    # #テスト用
    # CONSUMER_KEY = "OgUS1y3y7vuxy54NoKZvlOdq9"
    # CONSUMER_SECRET = "hCRRA4WX5cEe50ScugCkF4MvFJeFvU8YFAiwGDBi2vkJ9PqyZL"
    # ACCESS_TOKEN = "1000217159446945793-0LiJPmZvvyfaQvNhiY1pgL52pCTnuW"
    # ACCESS_TOKEN_SECRET = "enagarkdimg1cdR4w8ZFZhEr0kyjVj8ekNRzmiZviz4z8"

    # auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    # auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # API = tweepy.API(auth)

    # 画像の保存先
    LIVE_TMB_IMG_DIR = os.environ.get('LIVE_TMB_IMG_DIR')
    LIVE_TMB_TMP_DIR = os.environ.get('LIVE_TMB_TMP_DIR')
    # トリミング加工済み画像保存先
    TRIM_IMG_DIR = os.environ.get('IMG_TRIM_DIR')
    # プロフィール画像保存先
    # PROFILE_IMG_DIR = os.environ.get('PROFILE_IMG_DIR')
    PROFILE_IMG_DIR = app.PROFILE_IMG_DIR 
    HOLO_DATA_IMG_DIR = app.HOLO_DATA_IMG_DIR
    # イベント用画像保存先
    EVENT_IMG_DIR = os.environ.get('EVENT_IMG_DIR')


    def __init__(self, CONSUMER_KEY = os.environ.get('CONSUMER_KEY'), CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET'),
            ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN'), ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET'),):

        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.API = tweepy.API(self.auth)


    def create_msg(self, parts:list)->str:
        """ 
        メッセージ作成
        """
        #ツイート内容
        TWEET_TEXT = parts[0]
        try :
            tweet_status = self.API.update_status(TWEET_TEXT)
            if tweet_status == 200: #成功
                pprint(tweet_status)
                result = True
            else:
                pprint(tweet_status)
                result = False
        except Exception as e:
                # pprint(e)
                result = False
        return result