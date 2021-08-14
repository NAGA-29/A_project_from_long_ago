# 
# ニコニコ動画 RSSから最新の動画を取得して通知する
# 
import feedparser
import pandas as pd
import numpy as np
from pyasn1.type.univ import Boolean, Null
import tweepy
import urllib.request, urllib.error

from pprint import pprint

import time
from datetime import datetime as dt
import dateutil.parser

from apiclient.discovery import build
from apiclient.errors import HttpError

import os
from os.path import join, dirname
from dotenv import load_dotenv
import shutil
import json
import sys
'''
Original Modules
'''
sys.path.append('../service/niconico/')
from niconico import NicoNico_Wrapper as nico

sys.path.append('../../model/')
from setting import session
from NicoNicoVideo import NicoNicoVideo

sys.path.append('../../')
import holo_sql
from Components.holo_date import HoloDate
from Components.tweet import tweet_components
from Components.lines import lines
from Components import bitly

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

#twitter本番アカウント
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

# ##twitterテストアカウント
# CONSUMER_KEY = "OgUS1y3y7vuxy54NoKZvlOdq9"
# CONSUMER_SECRET = "hCRRA4WX5cEe50ScugCkF4MvFJeFvU8YFAiwGDBi2vkJ9PqyZL"
# ACCESS_TOKEN = "1000217159446945793-0LiJPmZvvyfaQvNhiY1pgL52pCTnuW"
# ACCESS_TOKEN_SECRET = "enagarkdimg1cdR4w8ZFZhEr0kyjVj8ekNRzmiZviz4z8"

# 所属
BELONGS = 'hololive'

# 画像の保存先
LIVE_TMB_IMG_DIR = os.environ.get('LIVE_TMB_IMG_DIR')
LIVE_TMB_TMP_DIR = os.environ.get('LIVE_TMB_TMP_DIR')


def rssImgDownload(img_url:str, video_id:str, dir_path:str) -> bool:
    """
    画像のダウンロード
    """
    path = dir_path + video_id + '.jpg'
    try:
        response = urllib.request.urlopen(url=img_url)
        with open(path, "wb") as f:
            f.write(response.read())
        print('Image Download OK ' + img_url)
        return True
    except Exception as err:
        error_catch(err, 'ダウンロードが失敗しました')
        return False


def error_catch(error, message:str, line:lines):
    """
    エラー通知
    """
    print("NG ", error)
    line.lineNotify(f'{message} : {error} : {os.path.basename(__file__)}')

# ---------------------------------------Main---------------------------------------
# ----------------------------------------------------------------------------------
if __name__ == '__main__':
    while True:
        hTime = HoloDate()
        print('##########################開 始##########################')
        w2525 = nico()
        url = 'https://ch.nicovideo.jp/hololive/video?rss=2.0'
        rss = feedparser.parse(url).entries

        videos = []
        if rss:
            for i in rss:
                if i['nicoch_ispremium'] == 'true':
                    videos.append(i)
                else:
                    continue
                
        for vi in videos:
            tw = tweet_components(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            line = lines()

            link = vi['link'] #URL
            published = vi['published'] #未使用
            published_parsed = vi['published_parsed'] #公開時間
            title = vi['title'] #動画タイトル

            video_id = link.split('/')[-1]
            img = w2525.search_thumbnail(video_id) #サムネURLの検出
            if not img:
                line.lineNotify('サムネの検出に失敗しました')
                continue

            # DBからidを検索
            result = session.query(NicoNicoVideo).filter(NicoNicoVideo.video_id==video_id).all()

            if not result:
            # 同じIDがない(新規)
                newdata = True
                download_Result = rssImgDownload(img, video_id, '../../storage/niconico/')
                if not download_Result:
                    newdata = False
                    imgPro = None
                    continue

                jpt_str = w2525.parse_time(published_parsed)
                JST = w2525.nico_convertToJST(jpt_str)
                
                # dbに保存
                # try:
                nico = NicoNicoVideo()
                nico.name = 'hololive'
                nico.belongs = 'hololive'
                nico.title = title
                nico.video_id = video_id
                nico.url = link
                nico.published_at = JST
                nico.thumbnail_url  = img
                nico.notification_last_time_at = '2000-01-01 00:00:00'
                session.add(nico)
                session.commit()
                # except:
                #     pprint('SQLAlchemy でエラー')

                message = 'ニコ動検知テストだお\n\nNew Niconico Video🆕\n\nHololive official fan club\n{}\n\n投稿時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n\n{}'.format('#hololive', JST, hTime.convert_To_LON(JST), hTime.convert_To_NY(JST), title, link)
                # message = 'New Niconico Video🆕\n\nHololive official fan club\n{}\n\n投稿時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n\n{}'.format('#hololive', JST, hTime.convert_To_LON(JST), hTime.convert_To_NY(JST), title, link)
                line.lineNotify_Img('\nNew NicoNico Video🆕\n\nHololive official fan club\n{}\n\n投稿時間\n{}🇯🇵\n\n{}\n{}'.format('#hololive', JST, title, link), f'../../storage/niconico/{video_id}.jpg')
                tw.tweet_With_Image(message, f'../../storage/niconico/{video_id}.jpg')
            else:
            # 同じIDがある(既存)
                continue

            # 後始末
            nico = None
            # sql = None
            line = None
        
        time.sleep(60*10)