# 
#  特定のチャンネルの動画を全て取得する
#  10分で理解する Selenium - Qiita https://qiita.com/Chanmoro/items/9a3c86bb465c1cce738a
"""
youtubeで新着検知をしようとしたのだが、セレクターが深く、また、live中のURLと混同して取得してしまう。
一時的には使用できるが、サイトの構造が変わる度に対応するのは手間がかかるので中止

APIを使用する方法か、ホロライブのスケジュールを直接検知した方が楽
構造もシンプルなので対応も楽そう

2021/6/13 開発中
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import SessionNotCreatedException

from webdriver_manager.chrome import ChromeDriverManager

from pyasn1.type.univ import Boolean, Null
import urllib.request, urllib.error

import pandas as pd
import numpy as np

import time
import datetime
from datetime import datetime as dt, timedelta
import schedule

import os
import sys 
import os
from os.path import join, dirname
from dotenv import load_dotenv

from bs4 import BeautifulSoup
import requests
from requests.exceptions import Timeout
import socket

from pprint import pprint

from apiclient.discovery import build
from apiclient.errors import HttpError

'''
Original Modules
'''
# import mysql.connector as mydb
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from model.holo_sql import holo_sql
from ImageProcessing import ImageProcessing
from YoutubeAPI.YoutubeAPI import Youtube_API as yApi
from ImageProcessing.photoFabrication import PhotoFabrication
from Components.holo_date import HoloDate
from Components.tweet import tweet_components
from Components.lines import lines
from Components import bitly
from Components import logging as log
from Components.vtuber.hololive import Hololive
from config import app

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
    
class YoutubeChannelMonitor:
    def __init__(self, headless=False):
        self.options = Options()
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--hide-scrollbars')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--proxy-server="direct://"')
        self.options.add_argument('--proxy-bypass-list=*')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--kiosk')
        self.options.add_argument('--start-maximized') 
        # self.options.add_argument(f'window-size={self.width}x{self.height}')
        self.options.add_argument('--force-device-scale-factor=1')
        if headless == False:
            pass
        elif headless == True:
            self.options.add_argument('--headless') # ※ヘッドレスモードを使用する場合、コメントアウトを外す

        self.Urls = {
            'https://schedule.hololive.tv/simple/hololive',
            'https://schedule.hololive.tv/simple/english',
            'https://schedule.hololive.tv/simple/indonesia',
        }

        self._error_count = 1

        self._api_key = 'YOUTUBE_API_KEY01'
        self._api_number = 1
        self.API_KEY = os.environ.get(self._api_key)
        self.YOUTUBE_API_SERVICE_NAME = 'youtube'
        self.YOUTUBE_API_VERSION = 'v3'

        self.nextPagetoken = None
        self.nextpagetoken = None

        self.youtubeObject = build(
            self.YOUTUBE_API_SERVICE_NAME, 
            self.YOUTUBE_API_VERSION,
            developerKey=self.API_KEY
            )
        
        # Logging設定
        f = os.path.splitext(os.path.basename(__file__))[0]
        self._LOG_FILE = f'../storage/logs/{f}.log'

        # 画像の保存先
        # self.LIVE_TMB_IMG_DIR = os.environ.get('LIVE_TMB_IMG_DIR')
        # self.LIVE_TMB_TMP_DIR = os.environ.get('LIVE_TMB_TMP_DIR')
        # # トリミング加工済み画像保存先
        # self.TRIM_IMG_DIR = os.environ.get('IMG_TRIM_DIR')
        self.LIVE_TMB_IMG_DIR = '../src/live_thumbnail_image/'
        self.LIVE_TMB_TMP_DIR = '../src/live_temporary_image/'
        # トリミング加工済み画像保存先
        self.TRIM_IMG_DIR = '../src/Trim_Images/'
        # print(app.IMG_TRIM_DIR)

        #twitter本番アカウント
        self.CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
        self.CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
        self.ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
        self.ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

        # #twitterテストアカウント
        # self.CONSUMER_KEY = os.environ.get('CONSUMER_KEY_TEST')
        # self.CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET_TEST')
        # self.ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
        # self.ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET_TEST')

    def ImgDownload(self, line, img_url:str, dir_path:str) ->bool:
        """
        画像のダウンロード
        @param line lines Object linesクラスオブジェクト 
        @param img_url string 保存対象パス
        @param dir_path string 保存先ディレクトリパス
        @return bool ダウンロードの成否
        """
        path = dir_path + img_url.split('/')[-2] + '.jpg'
        try:
            response = urllib.request.urlopen(url=img_url)
            with open(path, "wb") as f:
                f.write(response.read())
            print('Image Download OK ' + img_url)
        except Exception as err:
            pprint(err)
            line.lineNotify("ダウンロードが失敗しました")
            return False
        else:
            return True

    def reset_error_count(self):
        self._error_count = 1

    def main(self):
        # logging
        logger = log.get_module_logger(__name__, self._LOG_FILE)
        logger.info('Start Assist Hololive Research Controller')

        # hSql = holo_sql()
        line = lines()
        yt = yApi()
        hTime = HoloDate()
        photo = PhotoFabrication(self.LIVE_TMB_IMG_DIR, self.TRIM_IMG_DIR)
        tw = tweet_components(self.CONSUMER_KEY, self.CONSUMER_SECRET, self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        # ------------------------
        # param
        # ------------------------
        videos_datas = []
        get_news = []

        game_name = None
        tag = None
        commentCount = 0
        viewCount = 0
        likeCount = 0
        dislikeCount = 0
        scheduledStartTime = None
        actualStartTime = None
        actualEndTime = None
        max_concurrent_viewers = 0
        active_chat_id = None
        status = None
        scheduledStartTimeJPT = None
        BELONGS = 'hololive' # 所属
        # ------------------------
        #------------------------------------------pageからvideoを取得------------------------------------------
        for url in self.Urls:
            try:
                res = requests.get(url, timeout=5.0)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, "html.parser")
                elems = soup.select('div#all > div.container > div.row > div > div.row > div > a')
                if elems:
                    video_list = []
                    for elem in elems:
                        url = elem.get("href").split('?v=')
                        try:
                            video_list.append( url[1] )
                        except IndexError as err:
                            pprint(err)
                            continue
                else:
                    raise Exception('サイト構造が変更された可能性があります')
            except ConnectionResetError as err:
                pprint(err)
                pass
            except Timeout as err:
                # line.lineNotify('{}:リクエストがタイムアウトしています',format(err))
                pprint(err)
                self._error_count += 1
                pass
            except Exception as err:
                self._error_count += 1
                pprint(err)
                logger.error(err)
                continue


            pprint('##########################')
            for video_id in video_list:
                hSql = holo_sql()
                result = hSql.searchVideoIdFromYoutubeVideoTable_test(video_id)
                if result == False:
                    # # 緊急処置 2021/09/15 アーニャ
                    # if video_id == 'UTF0Qe3oQVM':
                    #     pprint('アーニャさん....')
                    #     continue
                    # 同じIDがない(新規)
                    try:
                        line.lineNotify('今までのより早く検出したドン！！！頑張ったドン！')
                    except TimeoutError as err:
                        pprint(err)
                        logger.error(f'lineNotify Error: {err}')
                        pass
                    # print('{}:これが原因？？'.format(video_id))
                    results = yt.videoInfo(self.youtubeObject, video_id)
                    # results = yApi.videoInfo(youtubeObject,entry['yt_videoid'])
                    tube_video_live_details = results.get("items", [])
                    for video_info_result in tube_video_live_details:
                        if video_info_result["kind"] == "youtube#video":
                            if video_info_result.get('liveStreamingDetails',False):
                                scheduledStartTime = video_info_result['liveStreamingDetails'].get('scheduledStartTime',None) #ライブ開始予定時間
                                actualStartTime = video_info_result['liveStreamingDetails'].get('actualStartTime',None) #ライブ開始時間
                                actualEndTime = video_info_result['liveStreamingDetails'].get('actualEndTime',None) #ライブ終了時間
                                concurrentViewers = video_info_result['liveStreamingDetails'].get('concurrentViewers',None) #リアルタイム視聴者数
                        target_url = 'https://www.youtube.com/watch?v={}'.format(video_info_result['id'])
                        viewCount = video_info_result["statistics"].get("viewCount",0)
                        commentCount = video_info_result["statistics"].get("commentCount",0) 
                        likeCount = video_info_result["statistics"].get("likeCount",0)
                        dislikeCount = video_info_result["statistics"].get("dislikeCount",0)

                        maxres_img = video_info_result['snippet']['thumbnails'].get('maxres',None) 
                        standard_img = video_info_result['snippet']['thumbnails'].get('standard',None)
                        high_img = video_info_result['snippet']['thumbnails'].get('high' ,None) 
                        medium_img = video_info_result['snippet']['thumbnails'].get('medium' ,None)
                        default_img = video_info_result['snippet']['thumbnails'].get('default' ,None)

                        if maxres_img : #画像Max
                            maxres_img = video_info_result['snippet']['thumbnails']['maxres']['url']
                        if standard_img :  #画像Standard
                            standard_img = standard_img = video_info_result['snippet']['thumbnails']['standard']['url']
                        if high_img :   #画像Small
                            high_img = video_info_result['snippet']['thumbnails']['high']['url']
                        if medium_img :   #画像XSmall
                            medium_img = video_info_result['snippet']['thumbnails']['medium']['url']
                        if default_img :   #画像default
                            default_img = video_info_result['snippet']['thumbnails']['medium']['url']
                            if not maxres_img:
                                maxres_img = video_info_result['snippet']['thumbnails']['medium']['url']

                        # 更新時間を日本時間に変換
                        updateJST = hTime.convertToJST(video_info_result['snippet']['publishedAt'])
                        scheduledStartTimeJPT = hTime.convertToJST(scheduledStartTime)
                        status = video_info_result["snippet"]["liveBroadcastContent"]
                        # HoloName, live_tag = self.select_name_tag(video_info_result['snippet']["channelId"]) # channelIdから誰のチャンネルか判定
                        HoloName, live_tag = Hololive.get_name_tag(video_info_result['snippet']["channelId"])
                        print(HoloName)

                        download_result = self.ImgDownload(line, high_img, self.LIVE_TMB_IMG_DIR)
                        if not download_result:
                            # 画像のダウンロードに失敗した場合は作業を中断し、スキップする
                            continue

                        videos_datas = [
                            HoloName,
                            video_info_result["snippet"]["title"],
                            video_info_result["id"],
                            video_info_result["snippet"]["channelId"],
                            target_url,
                            viewCount,
                            likeCount,
                            dislikeCount,
                            commentCount,
                            game_name,
                            tag,
                            hTime.convertToJST( video_info_result["snippet"]["publishedAt"] ),
                            hTime.convertToJST(scheduledStartTime),
                            hTime.convertToJST(actualStartTime),
                            hTime.convertToJST(actualEndTime),
                            int(max_concurrent_viewers),
                            active_chat_id,
                            maxres_img,  #画像Max
                            standard_img ,   #画像Standard
                            high_img,    #画像Small
                            medium_img, #画像XSmall
                            default_img, #画像default
                            status,
                            dt.now().strftime('%Y/%m/%d %H:%M:%S'),
                            BELONGS,
                            ]

                        # Line & twitter通知用(新規)--------------------------
                        get_news = [ 
                            video_info_result["snippet"]["title"],
                            video_info_result["id"],
                            video_info_result["snippet"]["channelId"],
                            bitly.make_yURL(target_url),
                            updateJST,
                            high_img,
                            scheduledStartTimeJPT if scheduledStartTimeJPT else updateJST,
                            ]

                        if status == 'upcoming':
                            # message = 'New Live Schedule🆕\n\n{}チャンネル\n{}\n\n配信予定時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n{}'.format(HoloName, live_tag, get_news[6], hTime.convert_To_LON(get_news[6]), hTime.convert_To_NY(get_news[6]), get_news[0], get_news[3])
                            message = 'New Live Schedule🆕\n\n{}チャンネル\n\n配信予定時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n{}'.format(HoloName, get_news[6], hTime.convert_To_LON(get_news[6]), hTime.convert_To_NY(get_news[6]), get_news[0], get_news[3])
                        if status == 'live':
                            # message = 'New Live On Air🆕\n\n{}チャンネル\n{}\n\nLive中です!\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n{}'.format(HoloName, live_tag, get_news[6], hTime.convert_To_LON(get_news[6]), hTime.convert_To_NY(get_news[6]), get_news[0], get_news[3])
                            message = 'New Live On Air🆕\n\n{}チャンネル\n\nLive中です!\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n{}'.format(HoloName, get_news[6], hTime.convert_To_LON(get_news[6]), hTime.convert_To_NY(get_news[6]), get_news[0], get_news[3])
                        if status == 'none':
                            # message = 'New Video Upload🆕\n\n{}チャンネル\n{}\n\n投稿時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n{}'.format(HoloName, live_tag, get_news[6], hTime.convert_To_LON(get_news[6]), hTime.convert_To_NY(get_news[6]), get_news[0], get_news[3])
                            message = 'New Video Upload🆕\n\n{}チャンネル\n\n投稿時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n{}'.format(HoloName, get_news[6], hTime.convert_To_LON(get_news[6]), hTime.convert_To_NY(get_news[6]), get_news[0], get_news[3])
                        
                        try:
                            line.lineNotify_Img('\n{}チャンネル 新着!🆕\n配信予定時間:{}\n\n{}\n{}'.format(HoloName, get_news[6], get_news[0], get_news[3]), get_news[5])
                        except TimeoutError as err:
                            logger.error(f'lineNotify Error: {err}')
                            pass
                        except TimeoutException as err:
                            logger.error(f'lineNotify Error: {err}')
                            pass

                        photo.imgTrim(get_news[5])
                        tw.tweetWithIMG(message, get_news[5], self.TRIM_IMG_DIR)
                        logger.info(message)

                    # for videos_data in videos_datas:
                        if videos_datas[22] == 'live' or videos_datas[22] == 'upcoming':
                            hSql.insertKeepWatchTable(videos_datas)
                        hSql.insertYoutubeVideoTable_R(videos_datas)
                        pprint(videos_datas)
                            
                else:
                    # 同じIDがある(既存)
                    pprint(video_id)
                    pass
                
                hSql.dbClose()
                hSql = None
            time.sleep(2)

if __name__ == '__main__':
    y_c_m = YoutubeChannelMonitor(True)
    while True:
        y_c_m.main()
        pprint(y_c_m._error_count)

        if (y_c_m._error_count / 180) == 1:
            line = lines()
            line.lineNotify('サイトの構造が変更された可能性があります')
            line = None
            y_c_m.reset_error_count()

        time.sleep(20)