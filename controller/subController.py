import random

import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv

import time 
import datetime
import schedule

from pprint import pprint

# Original Modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import holo_sql
from Components.tweet import tweet_components
from Components.scraping.news import Research as reCh
from Components import bitly
from model.TwitchVideo import TwitchVideo

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
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

tw_m = tweet_components(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tw_a = tweet_components(CONSUMER_KEY_A, CONSUMER_SECRET_A, ACCESS_TOKEN_A, ACCESS_TOKEN_SECRET_A)


_FILE = './src/news_file/news.csv'

def artTweet():
    hSql = holo_sql.holo_sql()
    count = len(hSql.searchAll())
    arts_id = random.choice(range(1,count+1))
    print(arts_id)
    print(count)
    holo_arts = hSql.searchArtsById(arts_id)
    if holo_arts:
        try:
            tw_a.reTweet(holo_arts[0]['tweet_id'])
        except Exception as err:
            print(err)
            pass
    hSql.dbClose()
    hSql = None

def holoNews():
    '''
    Hololive関連ニュースを取得 & tweet
    '''
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
    # if tw.tweet(_MESSAGE):
    #     reCh.csvFileWrite(_FILE, news)
    # else:
    #     pass
    # print(_MESSAGE)
    tw_m.tweet(_MESSAGE)
    reCh.csvFileWrite(_FILE, news)


# 毎時0分に実行
schedule.every().hour.at(":00").do(artTweet)
schedule.every().hour.at(":30").do(artTweet)
# schedule.every().hour.at(":15").do(holoNews)
# schedule.every().hour.at(":45").do(holoNews)

# schedule.every().hour.at(":21").do(main)
# schedule.every().hour.at(":09").do(searchSubscriber)

# PM00:05 AM12:05にjob実行
schedule.every().day.at("08:10").do(holoNews)
schedule.every().day.at("12:10").do(holoNews)
schedule.every().day.at("19:10").do(holoNews)
schedule.every().day.at("22:10").do(holoNews)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)