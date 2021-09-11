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

'''
Original Modules
'''
# import mysql.connector as mydb
import holo_sql
from ImageProcessing import ImageProcessing
from YoutubeAPI.YoutubeAPI import Youtube_API as yApi
from ImageProcessing.photoFabrication import PhotoFabrication
from Components.holo_date import HoloDate
from Components.tweet import tweet_components
from Components.lines import lines
from Components import bitly
from Components.vtuber.noripro import NoriPro

# プレイリストバージョン
# from playlist_detect import playlist_detect


load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

flag = True
holder = set()
NewRssData = []
_TIMELAG = 900

# のりプロ用twitterアカウント
CONSUMER_KEY = os.environ.get('CONSUMER_KEY_B')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET_B')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN_B')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET_B')

# ##twitterテストアカウント
# CONSUMER_KEY = "OgUS1y3y7vuxy54NoKZvlOdq9"
# CONSUMER_SECRET = "hCRRA4WX5cEe50ScugCkF4MvFJeFvU8YFAiwGDBi2vkJ9PqyZL"
# ACCESS_TOKEN = "1000217159446945793-0LiJPmZvvyfaQvNhiY1pgL52pCTnuW"
# ACCESS_TOKEN_SECRET = "enagarkdimg1cdR4w8ZFZhEr0kyjVj8ekNRzmiZviz4z8"


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(auth)


# 所属
BELONGS = 'noripro'

# 画像の保存先
LIVE_TMB_IMG_DIR = os.environ.get('LIVE_TMB_IMG_DIR')
# LIVE_TMB_TMP_DIR = os.environ.get('LIVE_TMB_TMP_DIR') #ホロライブ用
LIVE_TMB_TMP_DIR = os.environ.get('NoriP_LIVE_TMB_TMP_DIR') #のりプロ用

# トリミング加工済み画像保存先
TRIM_IMG_DIR = os.environ.get('IMG_TRIM_DIR')
# 画像結合加工済み画像保存先
COMBINE_IMG_DIR = os.environ.get('COMBINE_IMG_DIR')

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


# Channel = {
#     # のりプロ他
#     'SHIGURE_UI_ch' : 'UCt30jJgChL8qeT9VPadidSw', #時雨うい
#     'TAKUMA_ch' : 'UCCXME7oZmXB2VFHJbz5496A',     #熊谷タクマ
#     'TAMAKI_ch' : 'UC8NZiqKx6fsDT3AVcMiVFyA',     #佃煮のりお
#     'SHIRAYUKI_ch' : 'UCC0i9nECi4Gz7TU63xZwodg',  #白雪みしろ
#     'MILK_ch' : 'UCJCzy0Fyrm0UhIrGQ7tHpjg',       #愛宮みるく
#     'YUZURU_ch' : 'UCle1cz6rcyH0a-xoMYwLlAg',     #姫咲ゆずる
#     'HOOZUKI_ch' : 'UCLyTXfCZtl7dyhta9Jg3pZg',    #鬼灯わらべ
#     'YUMENO_ch' : 'UCH11P1Hq4PXdznyw1Hhr3qw',     #夢乃リリス
#     'KURUMIZAWA_ch' : 'UCxrmkJf_X1Yhte_a4devFzA', #胡桃澤もも
#     'OUMAKI_ch' : 'UCBAeKqEIugv69Q2GIgcH7oA',     #逢魔きらら
#     'NIA_ch' : 'UCIRzELGzTVUOARi3Gwf1-yg',        #看谷にぃあ
# }

# Play_Lists = {
#     # ホロライブアイドル道ラジオ
#     'idol_do_radio' : 'PLOzC5vqgb2w9AVrTjx_t6WNqpNRSUncy4',
#     'heikosen_scramble' : 'PLOzC5vqgb2w_r7zlJjt9zaQ4nWMrmc2F1',
# }


"""
画像のダウンロード
"""
def rssImgDownload(line, img_url:str, dir_path:str) ->Boolean:
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


"""
エラー内容出力
"""
def error_catch(error):
    """エラー処理
    """
    print("NG ", error)

# ---------------------------------------Main---------------------------------------
# ----------------------------------------------------------------------------------
if __name__ == '__main__':
    while flag:
        # DBへ接続
        hTime = HoloDate()
        hSql = holo_sql.holo_sql()
        photo = PhotoFabrication(LIVE_TMB_IMG_DIR,TRIM_IMG_DIR)
        tw = tweet_components(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        yt = yApi()
        line = lines()
        print('########################################################################')

        Channel = NoriPro.get_video_ids()
        for Name,ID in Channel.items():
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

            HoloName, live_tag = NoriPro.get_name_tag(ID)
            # # 絵師V
            # if ID == 'UCt30jJgChL8qeT9VPadidSw' : HoloName,live_tag = 'しぐれうい', '#ういなま'
            # # のりプロ
            # elif ID == 'UC8NZiqKx6fsDT3AVcMiVFyA' : HoloName,live_tag = '犬山たまき', '#犬山たまき'
            # elif ID == 'UCCXME7oZmXB2VFHJbz5496A' : HoloName,live_tag = '熊谷タクマ', '#熊谷タクマ'
            # elif ID == 'UCC0i9nECi4Gz7TU63xZwodg' : HoloName,live_tag = '白雪みしろ', '#白雪みしろ'
            # elif ID == 'UCJCzy0Fyrm0UhIrGQ7tHpjg' : HoloName,live_tag = '愛宮みるく', '#愛宮みるく'
            # elif ID == 'UCle1cz6rcyH0a-xoMYwLlAg' : HoloName,live_tag = '姫咲ゆずる', '#姫咲ゆずる'
            # elif ID == 'UCLyTXfCZtl7dyhta9Jg3pZg' : HoloName,live_tag = '鬼灯わらべ', '#鬼灯わらべ'
            # elif ID == 'UCH11P1Hq4PXdznyw1Hhr3qw' : HoloName,live_tag = '夢乃リリス', '#夢乃リリス'
            # elif ID == 'UCxrmkJf_X1Yhte_a4devFzA' : HoloName,live_tag = '胡桃澤もも', '#胡桃澤もも'
            # elif ID == 'UCBAeKqEIugv69Q2GIgcH7oA' : HoloName,live_tag = '逢魔きらら', '#逢魔きらら'
            # elif ID == 'UCIRzELGzTVUOARi3Gwf1-yg' : HoloName,live_tag = '看谷にぃあ', '#看谷にぃあ'
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

                result = hSql.searchVideoIdFromYoutubeVideoTable(entry)  #youtube_videos
                imgPro = ImageProcessing.ImageProcessing(entry['media_thumbnail'][0]['url'], TMP_DIR=LIVE_TMB_TMP_DIR)
                if not result:
                # 同じIDがない(新規)
                    newdata = True
                    download_Result = rssImgDownload(line, entry['media_thumbnail'][0]['url'], LIVE_TMB_IMG_DIR)
                    if not download_Result:
                        newdata = False
                        imgPro = None
                        continue
                else:
                # 同じIDがある(既存)
                    time_lag = dt.now() - result[0]['notification_last_time_at']
                    if time_lag.total_seconds() >= _TIMELAG:
                        download_Result = rssImgDownload(line, entry['media_thumbnail'][0]['url'], LIVE_TMB_TMP_DIR)
                        if not download_Result:
                            imgPro = None
                            continue
                        if not imgPro.imageComparison_hash():
                            # ---------------image combination------------------
                            img_name = entry['media_thumbnail'][0]['url'].split('/')[-2] + '.jpg'
                            TOP_NAME = './live_temporary_image_NoriP/'+ img_name
                            BOTTOM_NAME = './Trim_Images/'+ img_name
                            SAVE_NAME = './Combine_Image/'+ img_name
                            photo.imgTrim_Linking(TOP_NAME,BOTTOM_NAME,SAVE_NAME )
                            # ---------------------------------
                            shutil.move(imgPro._TMB_TMP_FilePath, imgPro._TMB_IMG_FilePath)
                            update = True
                            updateKind += 'image'
                        if entry['title'] != result[0]['title'] :
                            update = True
                            updateKind += 'title'
                        try:
                            os.remove(imgPro._TMB_TMP_FilePath)
                        except FileNotFoundError as e:
                            pprint(e)
                    else:
                        print('更新多いのでスキップ')
                        print(time_lag.total_seconds())
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
                        ])

                # Line & twitter通知用(アップデート)--------------------------
                if update:
                    _time = result[0]['scheduled_start_time_at'].strftime('%Y/%m/%d %H:%M') if result[0]['scheduled_start_time_at'] else updateJST
                    getRss.append([ 
                        entry['title'],
                        entry['yt_videoid'],
                        entry['yt_channelid'],
                        bitly.make_yURL(entry['link']),
                        # updateJST,
                        _time,
                        # result[0][13],
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

            dataDone = []
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
                            message = 'タイトル更新✅\n{}チャンネル\n{}\n\n配信予定時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n{}'.format(HoloName, live_tag, rss[4], hTime.convert_To_LON(rss[4]), hTime.convert_To_NY(rss[4]), rss[0], rss[3])
                            # line.lineNotify_Img('\n{}チャンネル\nタイトル更新✅\n{}\n\n{}\n{}'.format(HoloName,rss[4],rss[0],rss[3]),rss[5])
                            photo.imgTrim(rss[5])
                            # tw.tweetWithIMG(message,rss[5],TRIM_IMG_DIR)
                        elif rss[8:9] == ['image']:
                            # サムネ更新
                            del rss[8]
                            hSql.updateTitleYoutubeVideoTable(rss)
                            message = '画像更新✅\n{}チャンネル\n{}\n\n配信予定時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n{}'.format(HoloName, live_tag, rss[4], hTime.convert_To_LON(rss[4]), hTime.convert_To_NY(rss[4]), rss[0], rss[3])
                            line.lineNotify_Img('\n{}チャンネル\n画像更新✅\n{}\n\n{}\n{}'.format(HoloName,rss[4],rss[0],rss[3]),rss[5])
                            photo.imgTrim(rss[5])
                            tw.tweetWithIMG(message,rss[5],COMBINE_IMG_DIR)
                        else :
                            # タイトル・サムネ更新
                            del rss[8]
                            hSql.updateTitleYoutubeVideoTable(rss)
                            message = 'タイトル・画像更新✅\n{}チャンネル\n{}\n\n配信予定時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n{}'.format(HoloName, live_tag, rss[4], hTime.convert_To_LON(rss[4]), hTime.convert_To_NY(rss[4]), rss[0], rss[3])
                            line.lineNotify_Img('\n{}チャンネル\nタイトル・画像更新✅\n{}\n\n{}\n{}'.format(HoloName,rss[4],rss[0],rss[3]),rss[5])
                            photo.imgTrim(rss[5])
                            tw.tweetWithIMG(message,rss[5],COMBINE_IMG_DIR)

                for getRss_New in getRss_News:
                    message = '新着!🆕\n{}チャンネル\n{}\n\n配信予定時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n{}'.format(HoloName, live_tag, getRss_New[6], hTime.convert_To_LON(getRss_New[6]), hTime.convert_To_NY(getRss_New[6]), getRss_New[0], getRss_New[3])
                    line.lineNotify_Img('\n{}チャンネル 新着!🆕\n配信予定時間:{}\n\n{}\n{}'.format(HoloName, getRss_New[6], getRss_New[0], getRss_New[3]), getRss_New[5])
                    photo.imgTrim(getRss_New[5])
                    tw.tweetWithIMG(message,getRss_New[5],TRIM_IMG_DIR)

                for videos_data in videos_datas:
                    if videos_data[22] == 'live' or videos_data[22] == 'upcoming':
                        hSql.insertKeepWatchTable(videos_data)
                    hSql.insertYoutubeVideoTable_R(videos_data)
                    dataDone.append(videos_data)
                    pprint(dataDone)
                    time.sleep(1)

        hSql.dbClose()
        hSql = None
        imgPro = None
        photo = None
        hTime = None
        tw = None
        line = None
        yt = None

        # # playlist ver.===============
        # subscript = playlist_detect()
        # subscript.main()
        # subscript = None
        # # playlist ver. END==========

        time.sleep(300)
