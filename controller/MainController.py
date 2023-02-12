# 
# youtubeチャンネル登録者,動画本数,再生回数の監視
# 
import tweepy
from pyasn1.type.univ import Boolean, Null
import requests
from requests_oauthlib import OAuth1Session
import urllib.request, urllib.error

from pprint import pprint

import time
import datetime
from datetime import datetime as dt
import dateutil.parser
import schedule

from apiclient.discovery import build
from apiclient.errors import HttpError

import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv

'''
Original Modules
'''
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from Components.tweet import tweet_components
from Components import holo_data
from Components import logging as log
# import tube_subscriber
# from service.twitter import twitter_follower as tw
# from service.youtube import test_tube_subscriber as yt
from service import twitter_follower as tw
from service import TrendWatcher
from service import youtube_subscriber as yt

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

# ==========================================================================
#twitterアカウントAPI
# MyHoloP　アカウント用
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
# MyNoriP　アカウント用
CONSUMER_KEY_B = os.environ.get('CONSUMER_KEY_B')
CONSUMER_SECRET_B = os.environ.get('CONSUMER_SECRET_B')
ACCESS_TOKEN_B = os.environ.get('ACCESS_TOKEN_B')
ACCESS_TOKEN_SECRET_B = os.environ.get('ACCESS_TOKEN_SECRET_B')
# ==========================================================================

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(auth)

auth_B = tweepy.OAuthHandler(CONSUMER_KEY_B, CONSUMER_SECRET_B)
auth_B.set_access_token(ACCESS_TOKEN_B, ACCESS_TOKEN_SECRET_B)
API_B = tweepy.API(auth_B)

# ==========================================================================
# 画像の保存先
LIVE_TMB_IMG_DIR = os.environ.get('LIVE_TMB_IMG_DIR')
LIVE_TMB_TMP_DIR = os.environ.get('LIVE_TMB_TMP_DIR')
# トリミング加工済み画像保存先
TRIM_IMG_DIR = os.environ.get('IMG_TRIM_DIR')
# 代表画像
DEFAULT_IMG = 'hololive.jpg'
GRAPH_IMG = 'holo_data.png'
# logging
file = os.path.splitext(os.path.basename(__file__))[0]
_FILE_NAME = f'../storage/logs/{file}.log'
# ==========================================================================

_api_key = 'YOUTUBE_API_KEY_dev3'
_api_number = 1

API_KEY = os.environ.get(_api_key)
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
# CHANNEL_ID = Channel[]

nextPagetoken = None
nextpagetoken = None

youtubeObject = build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
    )

# ==========================================================================
def youtube_sys():
    # tube_subscriber.main()
    logger = log.get_module_logger(__name__, _FILE_NAME)
    logger.info('Start youtube_sys')
    yt.main()
    logger = None

def OverallInfo():
    logger = log.get_module_logger(__name__, _FILE_NAME)
    logger.info('Start OverallInfo')
    yt.OverallInfo()
    logger = None

def twitter_sys():
    logger = log.get_module_logger(__name__, _FILE_NAME)
    logger.info('Start twitter_sys')
    tw.main()
    logger = None

def twitter_trend_watcher():
    logger = log.get_module_logger(__name__, _FILE_NAME)
    logger.info('Start twitter_trend_watcher')
    TrendWatcher(API, logger).main(True)
    logger = None

if __name__ == '__main__':
    # フォロワー検知/通知
    schedule.every().hour.at(":00").do(twitter_sys)
    schedule.every().hour.at(":15").do(twitter_sys)
    schedule.every().hour.at(":30").do(twitter_sys)
    schedule.every().hour.at(":45").do(twitter_sys)

    # トレンド検知/通知
    # schedule.every().hour.at(":01").do(twitter_trend_watcher)
    # schedule.every().hour.at(":10").do(twitter_trend_watcher)
    # schedule.every().hour.at(":20").do(twitter_trend_watcher)
    # schedule.every().hour.at(":31").do(twitter_trend_watcher)
    # schedule.every().hour.at(":40").do(twitter_trend_watcher)
    # schedule.every().hour.at(":50").do(twitter_trend_watcher)

    # チャンネル登録者検知/通知
    schedule.every().hour.at(":09").do(youtube_sys)
    # schedule.every().hour.at(":38").do(youtube_sys)
    schedule.every().hour.at(":29").do(youtube_sys)
    schedule.every().hour.at(":49").do(youtube_sys)

    # 全体登録者通知
    # schedule.every().day.at("00:05").do(OverallInfo)
    # schedule.every().day.at("00:11").do(OverallInfo)

    while True:
        schedule.run_pending()
        time.sleep(1)