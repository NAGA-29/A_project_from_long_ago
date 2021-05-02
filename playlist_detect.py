# 
# RSSから最新の動画を取得して通知する
# 
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
import datetime
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
from Components import bitly

class playlist_detect:
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
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

    # ##twitterテストアカウント
    # CONSUMER_KEY = "OgUS1y3y7vuxy54NoKZvlOdq9"
    # CONSUMER_SECRET = "hCRRA4WX5cEe50ScugCkF4MvFJeFvU8YFAiwGDBi2vkJ9PqyZL"
    # ACCESS_TOKEN = "1000217159446945793-0LiJPmZvvyfaQvNhiY1pgL52pCTnuW"
    # ACCESS_TOKEN_SECRET = "enagarkdimg1cdR4w8ZFZhEr0kyjVj8ekNRzmiZviz4z8"


    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    API = tweepy.API(auth)

    # 画像の保存先
    LIVE_TMB_IMG_DIR = os.environ.get('LIVE_TMB_IMG_DIR')
    OTHER_TMB_TMP_DIR = os.environ.get('OTHER_TMB_TMP_DIR')

    # トリミング加工済み画像保存先
    TRIM_IMG_DIR = os.environ.get('IMG_TRIM_DIR')

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


    """
    ツイートメソッド
    """
    def tweet(self, message):
        #ツイート内容
        TWEET_TEXT = message
        try :
            tweet_status = self.API.update_status(TWEET_TEXT)
            if tweet_status == 200: #成功
                pprint("Succeed!")
                result = True
            else:
                # pprint(tweet_status)
                result = False
        except Exception as e:
                message = e
                pprint(e)
                result = False
        return result


    """
    ツイートメソッド テスト
    """
    def tweetWithIMG(self, message,img_url):
        #ツイート内容
        TWEET_TEXT = message
        try :
            # ↓添付したい画像のファイル名
            self.TRIM_IMG_DIR
            FILE_NAME = self.TRIM_IMG_DIR + img_url.split('/')[-2] + '.jpg'
            # FILE_NAME = LIVE_TMB_IMG_DIR + img_url.split('/')[-2] + '.jpg'
            tweet_status = self.API.update_with_media(filename=FILE_NAME, status=TWEET_TEXT)
            if tweet_status == 200: #成功
                pprint("Succeed!")
                result = True
            else:
                result = False
        except Exception as e:
                message = e
                pprint(e)
                result = False
        return result


    """
    画像のダウンロード
    """
    def rssImgDownload(self, img_url:str, dir_path:str) ->Boolean:
        path = dir_path + img_url.split('/')[-2] + '.jpg'
        try:
            response = urllib.request.urlopen(url=img_url)
            with open(path, "wb") as f:
                f.write(response.read())
            print('Image Download OK ' + img_url)
        except Exception as err:
            pprint(err)
            self.lineNotify("ダウンロードが失敗しました")
            return False
        else:
            return True



    """
    LINE
    """
    def lineNotify(self, message):
        line_notify_token = os.environ.get('LINE_NOTIFY_TOKEN')
        line_notify_api = 'https://notify-api.line.me/api/notify'
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        requests.post(line_notify_api, data=payload, headers=headers,)


    """
    画像付きLINE通知
    """
    def lineNotify_Img(self, message,imageUrl):
        line_notify_token = os.environ.get('LINE_NOTIFY_TOKEN')
        line_notify_api = 'https://notify-api.line.me/api/notify'
        # payload = {'message': 'テスト'}
        payload = {   'type': 'image',
                    'imageFullsize': imageUrl,
                    'imageThumbnail': imageUrl,
                    'message': message

                    }
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        requests.post(line_notify_api, data=payload, headers=headers,)


    Play_Lists = {
        # ホロライブアイドル道ラジオ
        'heikosen_scramble' : 'PLOzC5vqgb2w_r7zlJjt9zaQ4nWMrmc2F1',
        'idol_do_radio' : 'PLOzC5vqgb2w9AVrTjx_t6WNqpNRSUncy4',
    }

    # ---------------------------------------Main---------------------------------------
    # ----------------------------------------------------------------------------------

    def main(self):
        # DBへ接続
        hTime = HoloDate()
        hSql = holo_sql.holo_sql()
        photo = PhotoFabrication(self.LIVE_TMB_IMG_DIR, self.TRIM_IMG_DIR)
        tw = tweet_components(self.CONSUMER_KEY, self.CONSUMER_SECRET, self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        print('########################################################################')

        for Name,ID in self.Play_Lists.items():
            # ------------------------
            # param
            # ------------------------
            # url = 'https://www.youtube.com/feeds/videos.xml?channel_id={}'.format(ID)
            url = 'https://www.youtube.com/feeds/videos.xml?playlist_id={}'.format(ID)
            getRss = []
            getRss_News = []
            listR = []
            newdata = False
            update = False
            playlist_name = ''
            updateKind = ''
            videos_datas = []
            # _TIMELAG = 900
            # ------------------------

            '''
            プレイリスト判定
            '''
            if ID == 'PLOzC5vqgb2w9AVrTjx_t6WNqpNRSUncy4': playlist_name,live_tag = 'ホロライブアイドル道ラジオ～私たちの歌をきけッ！', '＃ホロのうたきけ'
            elif ID == 'PLOzC5vqgb2w_r7zlJjt9zaQ4nWMrmc2F1' : playlist_name,live_tag ='平行線すくらんぶる', '#線すく'
            print(playlist_name)


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

                result = hSql.search_VideoId_from_othervideos(entry)  #youtube_videos
                imgPro = ImageProcessing.ImageProcessing(entry['media_thumbnail'][0]['url'])
                if not result:
                # 同じIDがない(新規)
                    newdata = True
                    download_Result = self.rssImgDownload(entry['media_thumbnail'][0]['url'], self.LIVE_TMB_IMG_DIR)
                    if not download_Result:
                        newdata = False
                        imgPro = None
                        continue
                else:
                # 同じIDがある(既存)
                    time_lag = dt.now() - result[0]['notification_last_time_at']
                    # pprint(time_lag.total_seconds())
                    if time_lag.total_seconds() >= self._TIMELAG:
                        download_Result = self.rssImgDownload(entry['media_thumbnail'][0]['url'], self.OTHER_TMB_TMP_DIR)
                        if not download_Result:
                            imgPro = None
                            continue
                        if not imgPro.imageComparison_hash_other():
                            # ---------------------------------
                            shutil.move(imgPro._OTHER_TMP_FilePath, imgPro._TMB_IMG_FilePath)
                            update = True
                            updateKind += 'image'
                        if entry['title'] != result[0]['title'] :
                            update = True
                            updateKind += 'title'
                        try:
                            os.remove(imgPro._OTHER_TMP_FilePath)
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
                    results = yApi.videoInfo(self.youtubeObject,entry['yt_videoid'])
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
                            playlist_name,
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
                    getRss.append([ 
                        entry['title'],
                        entry['yt_videoid'],
                        entry['yt_channelid'],
                        bitly.make_yURL(entry['link']),
                        # updateJST,
                        result[0]['scheduled_start_time_at'] if result[0]['scheduled_start_time_at'] else updateJST,
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
                for lines in getRss:
                    if lines[8:9]:
                        if lines[8:9] == ['title']:
                            del lines[8]
                            # hSql.updateTitle(lines)
                            hSql.updateTitleYoutubeVideoTable(lines)
                            message = '✨{}✨\nタイトル更新✅\n{}\n\n投稿時間:{}\n\n{}\n{}'.format(playlist_name,live_tag,lines[4],lines[0],lines[3])
                            self.lineNotify_Img('\n{}\nタイトル更新✅\n{}\n\n{}\n{}'.format(playlist_name,lines[4],lines[0],lines[3]),lines[5])
                            photo.imgTrim(lines[5])
                            self.tweetWithIMG(message,lines[5])
                        elif lines[8:9] == ['image']:
                            del lines[8]
                            # hSql.updateImage(lines)
                            hSql.updateTitleYoutubeVideoTable(lines)
                            message = '✨{}✨\n画像更新✅\n{}\n\n投稿時間:{}\n\n{}\n{}'.format(playlist_name,live_tag,lines[4],lines[0],lines[3])
                            self.lineNotify_Img('\n{}\n画像更新✅\n{}\n\n{}\n{}'.format(playlist_name,lines[4],lines[0],lines[3]),lines[5])
                            photo.imgTrim(lines[5])
                            self.tweetWithIMG(message,lines[5])
                        else :
                            del lines[8]
                            # hSql.update2Items(lines)
                            hSql.updateTitleYoutubeVideoTable(lines)
                            message = '✨{}✨\nタイトル・画像更新✅\n{}\n\n投稿時間:{}\n\n{}\n{}'.format(playlist_name,live_tag,lines[4],lines[0],lines[3])
                            self.lineNotify_Img('\n{}\nタイトル・画像更新✅\n{}\n\n{}\n{}'.format(playlist_name,lines[4],lines[0],lines[3]),lines[5])
                            photo.imgTrim(lines[5])
                            self.tweetWithIMG(message,lines[5])
                for getRss_New in getRss_News:
                    message = '💖{} 新着!🆕\n{}\n\n投稿時間:{}\n\n{}\n{}'.format(playlist_name, live_tag, getRss_New[6], getRss_New[0], getRss_New[3])
                    self.lineNotify_Img('\n{} 新着!🆕\n投稿時間:{}\n\n{}\n{}'.format(playlist_name, getRss_New[6], getRss_New[0], getRss_New[3]), getRss_New[5])
                    photo.imgTrim(getRss_New[5])
                    self.tweetWithIMG(message,getRss_New[5])
                for videos_data in videos_datas:
                    if videos_data[22] == 'live' or videos_data[22] == 'upcoming':
                        hSql.insertKeepWatchTable(videos_data)
                    hSql.insertOtherVideoTable(videos_data)
                    dataDone.append(videos_data)
                    pprint(dataDone)
                    time.sleep(1)

        hSql.dbClose()
        hSql = None
        imgPro = None
        photo = None
        hTime = None

# i = playlist_detect()
# i.main()