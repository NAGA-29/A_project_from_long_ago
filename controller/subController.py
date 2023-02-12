import os
from os.path import join, dirname
import random
import sys
from dotenv import load_dotenv

import time 
import datetime
import schedule
import feedparser
from pprint import pprint

'''
Original Modules
'''
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import holo_sql
from Components.tweet import tweet_components
from Components.scraping.news import Research as reCh
from Components import bitly
from Components import logging as log
from controller.tree import Holo_nico_search

"""
指定時間にDBから検索
tweet idを取得

apiを使用してretweet


分析編
集計期間を指定
今日、昨日、1週間
・キャラ指定検索
・ランキング1週間
"""
# twitter本番アカウント My_Hololive_project
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

# twitter本番アカウント My_Hololive_Art_project
CONSUMER_KEY_A = os.environ.get('CONSUMER_KEY_A')
CONSUMER_SECRET_A = os.environ.get('CONSUMER_SECRET_A')
ACCESS_TOKEN_A = os.environ.get('ACCESS_TOKEN_A')
ACCESS_TOKEN_SECRET_A = os.environ.get('ACCESS_TOKEN_SECRET_A')

# logging
file = os.path.splitext(os.path.basename(__file__))[0]
_FILE_NAME = f'../storage/logs/{file}.log'

tw_m = tweet_components(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tw_a = tweet_components(CONSUMER_KEY_A, CONSUMER_SECRET_A, ACCESS_TOKEN_A, ACCESS_TOKEN_SECRET_A)

# _FILE = './src/news_file/news.csv'
_FILE = '../storage/news_logs/news.csv'

def artTweet():
    logger = log.get_module_logger(__name__, _FILE_NAME)
    logger.info('Start HoloArt Tweet')
    hSql = holo_sql.holo_sql()
    count = len(hSql.searchAll())
    arts_id = random.choice(range(1,count+1))
    # print(arts_id)
    # print(count)
    holo_arts = hSql.searchArtsById(arts_id)
    if holo_arts:
        try:
            tw_a.reTweet(holo_arts[0]['tweet_id'])
        except Exception as err:
            logger.error(f'Error HoloArt Tweet: {err}')
            pass
    hSql.dbClose()
    hSql = None
    logger.info('End HoloArt Tweet')
    logger = None

def holoNews():
    logger = log.get_module_logger(__name__, _FILE_NAME)
    logger.info('Start HoloNews')
    # 日本時間 - 7日前
    base_toDay = datetime.date.today() - datetime.timedelta(days=1) 
    base_fromDay = base_toDay - datetime.timedelta(days=7)
    toDay =  base_toDay.strftime('%Y-%m-%d')
    fromDay =  base_fromDay.strftime('%Y-%m-%d')

    news = reCh.NewsAPIResearch_Every(_FILE, fromDay, toDay)
    for key, val in news.items():
        title = val[0]
        short_URL = bitly.get_shortenURL(key)
    _MESSAGE = 'Hololive News!!💖\n\n{}\n{}\n#hololive'.format(title, short_URL)
    tw_m.tweet(_MESSAGE)
    reCh.csvFileWrite(_FILE, news)
    logger.info('End HoloNews')
    logger = None

def niconico_search():
    logger = log.get_module_logger(__name__, _FILE_NAME)
    logger.info('Start niconico_search')
    Holo_nico_search.main()
    logger.info('End niconico search')
    logger = None

# 毎時0分に実行
#schedule.every().hour.at(":00").do(artTweet)
#schedule.every().hour.at(":30").do(artTweet)

# PM00:05 AM12:05にjob実行
# schedule.every().day.at("06:10").do(holoNews)
# schedule.every().day.at("08:10").do(holoNews)
# schedule.every().day.at("12:10").do(holoNews)
# schedule.every().day.at("16:47").do(holoNews)
# schedule.every().day.at("19:10").do(holoNews)
# schedule.every().day.at("23:10").do(holoNews)

# # ニコ動検知
# schedule.every().day.at("00:30").do(niconico_search)
# schedule.every().day.at("06:30").do(niconico_search)
# schedule.every().day.at("12:30").do(niconico_search)
# schedule.every().day.at("18:30").do(niconico_search)
# schedule.every().day.at("22:30").do(niconico_search)

while True:
    schedule.run_pending()
    time.sleep(1)