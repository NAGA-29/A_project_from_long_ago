import tweepy
# import requests

from pprint import pprint

import os
from os.path import join, dirname
from dotenv import load_dotenv


load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


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
    PROFILE_IMG_DIR = os.environ.get('PROFILE_IMG_DIR')
    # イベント用画像保存先
    EVENT_IMG_DIR = os.environ.get('EVENT_IMG_DIR')


    def __init__(self,CONSUMER_KEY = os.environ.get('CONSUMER_KEY'), CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET'),
            ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN'),ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET'),):

        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.API = tweepy.API(self.auth)


    def tweet(self, message:str)->bool:
        """ 
        ツイートメソッド
        """
        #ツイート内容
        TWEET_TEXT = message
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


    def tweetWithIMG(self, message, img_url, DIR=None)->bool:
        """
        ツイートメソッド 画像付き url分解機能
        """
        #ツイート内容
        TWEET_TEXT = message
        IMG_DIR = DIR if DIR else self.LIVE_TMB_IMG_DIR
        try :
            # ↓添付したい画像のファイル名
            FILE_NAME = IMG_DIR + img_url.split('/')[-2] + '.jpg'
            tweet_status = self.API.update_with_media(filename=FILE_NAME, status=TWEET_TEXT)
            if tweet_status == 200: #成功
                pprint("Succeed!")
                result = True
            else:
                result = False
        except Exception as e:
                pprint(e)
                result = False
        return result


    def tweet_With_Image(self, message, file_name):
        #ツイート内容
        TWEET_TEXT = message
        FILE_NAME = file_name
        try :
            self.API.update_with_media(filename=FILE_NAME, status=TWEET_TEXT)
        except Exception as e:
                message = e
                pprint(e)
                result = False
                return result


    def sub_tweetWithIMG(self,message,img_url):
        """
        ツイートメソッド 画像付き 
        """
        #ツイート内容
        TWEET_TEXT = message
        try :
            # ↓添付したい画像のファイル名
            FILE_NAME = self.PROFILE_IMG_DIR + img_url
            tweet_status = self.API.update_with_media(filename=FILE_NAME, status=TWEET_TEXT)
            if tweet_status == 200: #成功
                pprint("Succeed!")
                result = True
            else:
                result = False
        except Exception as e:
                pprint(e)
                result = False
        return result


    def event_tweetWithIMG(self,message,img_url):
        """
        ツイートメソッド 画像付き 
        """
        #ツイート内容
        TWEET_TEXT = message
        try :
            # ↓添付したい画像のファイル名
            FILE_NAME = self.EVENT_IMG_DIR + img_url
            tweet_status = self.API.update_with_media(filename=FILE_NAME, status=TWEET_TEXT)
            if tweet_status == 200: #成功
                pprint("Succeed!")
                result = True
            else:
                result = False
        except Exception as e:
                pprint(e)
                result = False
        return result


    def remind_tweetWithIMG(self, message:str, media:list)->bool:
        """
        ツイートメソッド 画像付き 
        """
        #ツイート内容
        TWEET_TEXT = message
        try :
            MEDIA = ','.join(media)
            MEDIA  = []
            for filename in media:
                res = self.API.media_upload(filename)
                MEDIA.append(res.media_id)
            tweet_status = self.API.update_status(media_ids=MEDIA, status=TWEET_TEXT)
            if tweet_status == 200: #成功
                pprint("Succeed!")
                result = True
            else:
                result = False
        except Exception as e:
                pprint(e)
                result = False
        return result


    def reTweet(self, tweet_id:str)->bool:
        """
        リツイートメソッド
        """
        try :
            tweet_status = self.API.retweet(tweet_id)
            if tweet_status == 200: #成功
                pprint("Succeed!")
                result = True
            else:
                result = False
        except Exception as e:
                pprint(e)
                result = False
        return result