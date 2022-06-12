# 
# RSSから最新の動画を取得して通知する
# 
from xml.sax import make_parser
import feedparser
import pandas as pd
import numpy as np
from pyasn1.type.univ import Boolean, Null
import requests
from requests_oauthlib import OAuth1Session
import tweepy
import urllib.request, urllib.error
import shutil

from pprint import pprint

import time
from datetime import datetime as dt
import dateutil.parser

from apiclient.discovery import build
from apiclient.errors import HttpError
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv
import shutil
import sys

'''
Original Modules
'''
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
# import mysql.connector as mydb
import holo_sql
# from ImageProcessing import ImageProcessing
from ImageProcessing import ImageProcessing
from YoutubeAPI.YoutubeAPI import Youtube_API as yApi
from ImageProcessing.photoFabrication import PhotoFabrication
from Components.holo_date import HoloDate
from Components.tweet import tweet_components
from Components.lines import lines
from Components import bitly
from Components import logging as log
from Components.vtuber.hololive import Hololive

from playlistWatch import playlistWatch


load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

flag = True
holder = set()
NewRssData = []
_TIMELAG = 900

#twitter本番アカウント
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

# # ##twitterテストアカウント
# CONSUMER_KEY = "OgUS1y3y7vuxy54NoKZvlOdq9"
# CONSUMER_SECRET = "hCRRA4WX5cEe50ScugCkF4MvFJeFvU8YFAiwGDBi2vkJ9PqyZL"
# ACCESS_TOKEN = "1000217159446945793-0LiJPmZvvyfaQvNhiY1pgL52pCTnuW"
# ACCESS_TOKEN_SECRET = "enagarkdimg1cdR4w8ZFZhEr0kyjVj8ekNRzmiZviz4z8"

# Logging設定
file = os.path.splitext(os.path.basename(__file__))[0]
_LOG_FILE = f'../storage/logs/{file}.log'

# V1
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(auth)

# 所属
BELONGS = 'hololive'

# 画像の保存先
LIVE_TMB_IMG_DIR = '../src/live_thumbnail_image/'
LIVE_TMB_TMP_DIR = '../src/live_temporary_image/'
# トリミング加工済み画像保存先
TRIM_IMG_DIR = '../src/Trim_Images/'
# 画像結合加工済み画像保存先
COMBINE_IMG_DIR = '../src/Combine_Image/'

BASE_TOP_NAME = '../src/live_temporary_image/'
BASE_BOTTOM_NAME = '../src/Trim_Images/'
BASE_SAVE_NAME = '../src/Combine_Image/'

_api_key = 'YOUTUBE_API_KEY01'
_api_number = 1

API_KEY = os.environ.get(_api_key)
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
# CHANNEL_ID = Channel[]

# channels = [] #チャンネル情報を格納する配列
# searches = [] #video idを格納する配列
# videos = [] #各動画情報を格納する配列
# BroadCasts = [] #LIVE用データ集計配列
# lives = [] #LIVE用データ集計最終配列
nextPagetoken = None
nextpagetoken = None

youtubeObject = build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
    )


Play_Lists = {
    # ホロライブアイドル道ラジオ
    'idol_do_radio' : 'PLOzC5vqgb2w9AVrTjx_t6WNqpNRSUncy4',
    'heikosen_scramble' : 'PLOzC5vqgb2w_r7zlJjt9zaQ4nWMrmc2F1',
}

def rssImgDownload(line, img_url:str, dir_path:str) ->Boolean:
    """
    画像のダウンロード
    """
    path = dir_path + img_url.split('/')[-2] + '.jpg'
    try:
        response = urllib.request.urlopen(url=img_url)
        with open(path, "wb") as f:
            f.write(response.read())
        print('Image Download OK ' + img_url)
    except Exception as err:
        error_catch(err)
        line.lineNotify("ダウンロードが失敗しました")
        return False
    else:
        return True


def error_catch(error):
    """
    エラー処理
    """
    print("NG ", error)

def dead_video_id(video_id):
    die = ['d1HE5cqwgCw', 'yjU-wdsBdQs']
    if video_id in die:
        return False
    return True


# ---------------------------------------Main---------------------------------------
# ----------------------------------------------------------------------------------
if __name__ == '__main__':
    while flag:
        # logging
        logger = log.get_module_logger(__name__, _LOG_FILE)
        logger.info('Start Hololive RSS Research Controller')
        # DBへ接続
        hTime = HoloDate()
        # hSql = holo_sql.holo_sql()
        photo = PhotoFabrication(LIVE_TMB_IMG_DIR,TRIM_IMG_DIR)
        tw = tweet_components(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        yt = yApi()
        line = lines()
        print('###################################################################')

        Channel_JP, Channel_OSea = Hololive.get_video_ids()
        Channel_JP.update(Channel_OSea)
        # for Name,ID in Channel.items():
        for Name,ID in Channel_JP.items():
            # ------------------------
            # param
            # ------------------------
            url = 'https://www.youtube.com/feeds/videos.xml?channel_id={}'.format(ID)
            filename = './hololive_RSS/{}_RssData.csv'.format(Name)
            getRss = []
            getRss_News = []
            listR = []
            newdata = False
            update = False
            HoloName = ''
            updateKind = ''
            videos_datas = []
            # _TIMELAG = 900
            # ------------------------

            HoloName, live_tag = Hololive.get_name_tag(ID)
            print(HoloName)


            
    # csv管理バージョンーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
            # oldData = pd.read_csv(filename,header=0,names=['title','videoid','channelid','url','updated','image'])
            # hHololive = oldData['videoid'].values.tolist()
            # hHololiveTitle = oldData['title'].values.tolist()
            # hHololiveImage = oldData['image'].values.tolist()

            # for entry in feedparser.parse(url).entries:
                # # 同じIDがない場合
                # if entry.yt_videoid not in hHololive:  
                #     newdata = True

                # # 同じIDがある場合
                # else:
                #     if entry['title'] not in hHololiveTitle :
                #         update = True
                #         updateKind += 'title'
                #     if entry['media_thumbnail'][0]['url'] not in hHololiveImage :
                #         update = True
                #         updateKind += 'image'


    # DB管理バージョンーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
            for entry in feedparser.parse(url).entries:
                hSql = holo_sql.holo_sql()
                # ------------------------
                # param
                # ------------------------
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
                # ------------------------

                # # # 緊急処置 2022/05/08 ペコら #############
                if not dead_video_id(entry['yt_videoid']):
                    hSql = None
                    print('dead video id')
                    continue
                # # # 緊急処置 2022/05/08 ペコら #############

                result = hSql.searchVideoIdFromYoutubeVideoTable(entry)  #youtube_videos
                # imgPro = ImageProcessing.ImageProcessing(entry['media_thumbnail'][0]['url'])
                imgPro = ImageProcessing.ImageProcessing(entry['media_thumbnail'][0]['url'], TMP_DIR=LIVE_TMB_TMP_DIR, IMG_DIR= LIVE_TMB_IMG_DIR)

                if not result:
                # 同じIDがない(新規)
                    newdata = True
                    download_Result = rssImgDownload(line, entry['media_thumbnail'][0]['url'], LIVE_TMB_IMG_DIR)
                    if not download_Result:
                        # # 緊急処置 2021/09/15 アーニャ #############
                        # shutil.copy('./src/Profile_Images/holo_.jpg', LIVE_TMB_IMG_DIR + entry['yt_videoid'] + '.jpg')
                        # # 緊急処置 2021/09/15 アーニャ #############
                        newdata = False
                        imgPro = None
                        continue
                else:
                # 同じIDがある(既存)
                    time_rag = dt.now() - result[0]['notification_last_time_at']
                    if time_rag.total_seconds() >= _TIMELAG:
                        download_Result = rssImgDownload(line, entry['media_thumbnail'][0]['url'], LIVE_TMB_TMP_DIR)
                        if not download_Result:
                            imgPro = None
                            continue

                        if not imgPro.imageComparison_hash() : # 画像変更検知
                            # ---------------image combination------------------
                            img_name = entry['media_thumbnail'][0]['url'].split('/')[-2] + '.jpg'
                            # TOP_NAME = './live_temporary_image/'+ img_name
                            # BOTTOM_NAME = './Trim_Images/'+ img_name
                            # SAVE_NAME = './Combine_Image/'+ img_name
                            TOP_NAME = BASE_TOP_NAME+ img_name
                            BOTTOM_NAME = BASE_BOTTOM_NAME+ img_name
                            SAVE_NAME = BASE_SAVE_NAME+ img_name
                            photo.imgTrim_Linking(TOP_NAME,BOTTOM_NAME,SAVE_NAME )
                            # -------------------------------------------------
                            shutil.move(imgPro._TMB_TMP_FilePath, imgPro._TMB_IMG_FilePath)
                            update = True
                            updateKind += 'image'

                        if entry['title'] != result[0]['title'] : # タイトル変更検知
                            update = True
                            updateKind += 'title'

                        try:
                            os.remove(imgPro._TMB_TMP_FilePath)
                        except FileNotFoundError as e:
                            pprint(e)
                    else:
                        print('更新多いのでスキップ')
                        print(time_rag.total_seconds())
                        continue

                # 更新時間を日本時間に変換
                updateJST = hTime.convertToJST(entry['published'])

                if newdata:
                # 新規
                    results = yt.videoInfo(youtubeObject,entry['yt_videoid'])
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

                        scheduledStartTimeJPT = hTime.convertToJST(scheduledStartTime)
                        status = video_info_result["snippet"]["liveBroadcastContent"]

                        videos_datas.append([
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
                            ])  

                    # Line & twitter通知用(新規)--------------------------
                    # scheduled_at = convertToJST(scheduledStartTime)
                    getRss_News.append([ 
                        entry['title'],
                        entry['yt_videoid'],
                        entry['yt_channelid'],
                        bitly.make_yURL(entry['link']),
                        updateJST,
                        entry['media_thumbnail'][0]['url'],
                        scheduledStartTimeJPT if scheduledStartTimeJPT else updateJST,
                        status,
                        ])

                # Line & twitter通知用(アップデート)--------------------------
                if update:
                    _time = result[0]['scheduled_start_time_at'].strftime('%Y/%m/%d %H:%M') if result[0]['scheduled_start_time_at'] else updateJST
                    getRss.append([ 
                        entry['title'],
                        entry['yt_videoid'],
                        entry['yt_channelid'],
                        bitly.make_yURL(entry['link']),
                        _time,
                        entry['media_thumbnail'][0]['url'],
                        '',
                        dt.now().strftime('%Y/%m/%d %H:%M:%S'),
                        updateKind
                        ])
                # ------------------------------------
                
                newdata = False
                update = False
                updateKind = ''
                imgPro = None

            # dataDone = []
            if len(getRss) + len(getRss_News) == 0:
                print('更新ナシです')
                time.sleep(1)
            else:
                for rss in getRss:
                    if rss[8:9]:
                        if rss[8:9] == ['title']:
                            # タイトル更新
                            del rss[8]
                            hSql.updateTitleYoutubeVideoTable(rss)
                            message = 'Title Change✅\n\n{}チャンネル\n{}\n\n配信予定時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n\n{}'.format(HoloName, live_tag, rss[4], hTime.convert_To_LON(rss[4]), hTime.convert_To_NY(rss[4]), rss[0], rss[3])
                            # line.lineNotify_Img('\n{}チャンネル\nタイトル更新✅\n{}\n\n{}\n{}'.format(HoloName,rss[4],rss[0],rss[3]),rss[5])
                            photo.imgTrim(rss[5])
                            # tw.tweetWithIMG(message,rss[5],TRIM_IMG_DIR)
                        elif rss[8:9] == ['image']:
                            # サムネ更新
                            del rss[8]
                            hSql.updateTitleYoutubeVideoTable(rss)
                            message = 'Image Change✅\n\n{}チャンネル\n{}\n\n配信予定時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n\n{}'.format(HoloName, live_tag, rss[4], hTime.convert_To_LON(rss[4]), hTime.convert_To_NY(rss[4]), rss[0], rss[3])
                            line.lineNotify_Img('\n{}チャンネル\n画像更新✅\n{}\n\n{}\n{}'.format(HoloName,rss[4],rss[0],rss[3]),rss[5])
                            photo.imgTrim(rss[5])
                            tw.tweetWithIMG(message,rss[5],COMBINE_IMG_DIR)
                            logger.info(f'tweet message: {message}')
                        else :
                            # タイトル・サムネ更新
                            del rss[8]
                            hSql.updateTitleYoutubeVideoTable(rss)
                            message = 'Title & Image Change✅\n\n{}チャンネル\n{}\n\n配信予定時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n\n{}'.format(HoloName, live_tag, rss[4], hTime.convert_To_LON(rss[4]), hTime.convert_To_NY(rss[4]), rss[0], rss[3])
                            line.lineNotify_Img('\n{}チャンネル\nタイトル・画像更新✅\n{}\n\n{}\n{}'.format(HoloName,rss[4],rss[0],rss[3]),rss[5])
                            photo.imgTrim(rss[5])
                            tw.tweetWithIMG(message,rss[5],COMBINE_IMG_DIR)
                            logger.info(f'tweet message: {message}')

                for getRss_New in getRss_News:
                    if getRss_New[7] == 'upcoming':
                        # message = 'New Live Schedule🆕\n\n{}チャンネル\n{}\n\n配信予定時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n\n{}'.format(HoloName, live_tag, getRss_New[6], hTime.convert_To_LON(getRss_New[6]), hTime.convert_To_NY(getRss_New[6]), getRss_New[0], getRss_New[3])
                        message = 'New Live Schedule🆕\n\n{}チャンネル\n\n配信予定時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n\n{}'.format(HoloName, getRss_New[6], hTime.convert_To_LON(getRss_New[6]), hTime.convert_To_NY(getRss_New[6]), getRss_New[0], getRss_New[3])
                    elif getRss_New[7] == 'live':
                        # message = 'New Live On Air🆕\n\n{}チャンネル\n{}\n\nLive中です!\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n\n{}'.format(HoloName, live_tag, getRss_New[6], hTime.convert_To_LON(getRss_New[6]), hTime.convert_To_NY(getRss_New[6]), getRss_New[0], getRss_New[3])
                        message = 'New Live On Air🆕\n\n{}チャンネル\n\nLive中です!\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n\n{}'.format(HoloName, getRss_New[6], hTime.convert_To_LON(getRss_New[6]), hTime.convert_To_NY(getRss_New[6]), getRss_New[0], getRss_New[3])
                    elif getRss_New[7] == 'none':
                        # message = 'New Video Upload🆕\n\n{}チャンネル\n{}\n\n投稿時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n\n{}'.format(HoloName, live_tag, getRss_New[6], hTime.convert_To_LON(getRss_New[6]), hTime.convert_To_NY(getRss_New[6]), getRss_New[0], getRss_New[3])
                        message = 'New Video Upload🆕\n\n{}チャンネル\n\n投稿時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n\n{}'.format(HoloName, getRss_New[6], hTime.convert_To_LON(getRss_New[6]), hTime.convert_To_NY(getRss_New[6]), getRss_New[0], getRss_New[3])
                    
                    line.lineNotify_Img('\n{}チャンネル 新着!🆕\n配信予定時間:{}\n\n{}\n{}'.format(HoloName, getRss_New[6], getRss_New[0], getRss_New[3]), getRss_New[5])
                    photo.imgTrim(getRss_New[5])
                    tw.tweetWithIMG(message,getRss_New[5],TRIM_IMG_DIR)
                    logger.info(f'tweet message: {message}')

                for videos_data in videos_datas:
                    if videos_data[22] == 'live' or videos_data[22] == 'upcoming':
                        hSql.insertKeepWatchTable(videos_data)
                    hSql.insertYoutubeVideoTable_R(videos_data)
                    pprint(videos_data)
                    time.sleep(1)
                hSql.dbClose()

        # # playlist ver.===============
        play_lists = playlistWatch(Play_Lists, tw, youtubeObject)
        play_lists.main()
        play_lists = None
        # # playlist ver. END==========

        # hSql.dbClose()
        hSql = None
        imgPro = None
        photo = None
        hTime = None
        tw = None
        line = None
        yt = None

        logger.info('End Hololive RSS Research Controller')
        logger = None
        time.sleep(180)
