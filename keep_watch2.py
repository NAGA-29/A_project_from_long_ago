import tweepy
import requests

import time
import datetime
import schedule
from datetime import datetime as dt
import dateutil.parser

from apiclient.discovery import build
from apiclient.errors import HttpError

import os
from os.path import join, dirname
from dotenv import load_dotenv


from pprint import pprint
'''
Original Modules
'''
import holo_sql
from YoutubeAPI.YoutubeAPI import Youtube_API as yApi
from Components.holo_date import HoloDate
from Components.tweet import tweet_components
from Components.lines import lines
from Components import bitly
from Components.vtuber.hololive import Hololive
from Components.vtuber.noripro import NoriPro

# =========================== 設定 ==============================
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

_API_KEY = 'YOUTUBE_API_KEY_dev1'
_api_number = 1

API_KEY = os.environ.get(_API_KEY)
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtubeObject = build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
    )

# twitter本番アカウント
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

# NoriUi_Project本番アカウント
CONSUMER_KEY_B = os.environ.get('CONSUMER_KEY_B')
CONSUMER_SECRET_B = os.environ.get('CONSUMER_SECRET_B')
ACCESS_TOKEN_B = os.environ.get('ACCESS_TOKEN_B')
ACCESS_TOKEN_SECRET_B = os.environ.get('ACCESS_TOKEN_SECRET_B')

# テスト用twitterアカウント
CONSUMER_KEY_TEST = os.environ.get('CONSUMER_KEY_TEST')
CONSUMER_SECRET_TEST = os.environ.get('CONSUMER_SECRET_TEST')
ACCESS_TOKEN_TEST = os.environ.get('ACCESS_TOKEN_TEST')
ACCESS_TOKEN_SECRET_TEST = os.environ.get('ACCESS_TOKEN_SECRET_TEST')

# トリミング加工済み画像保存先
TRIM_IMG_DIR = os.environ.get('IMG_TRIM_DIR')

# APIを使用しての状態確認開始範囲 7200 = 2時間
_2HOURS = 7200
# APIを使用しての状態確認開始範囲 10800 = 3時間
_3HOURS = 10800
# (60*60*24)/300 : 288回で1日分になる
_1DAY = 288
# _1DAY = 3

# =============================================================

# ========================= メソッド ===========================
"""
更新時間を日本時間に変換
"""
# def convertToJST(time):
#     try:
#         JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
#         jst_timestamp = dateutil.parser.parse(time).astimezone(JST)
#         updateJST = jst_timestamp.strftime('%Y/%m/%d %H:%M:%S')
#         return updateJST
#     except TypeError as err:
#         # pprint('convertToJSTメソッド:{}'.format(err))
#         return None

def check_schedule_time(belongs: str):
    """live開始時間を確認

    :param belongs: 所属グループ名
    :type : str
    """
    print('LIVE時間の変更をチェックします')
    hSql = holo_sql.holo_sql()
    hTime = HoloDate()
    yt = yApi()
    line = lines()

    db_data_list = hSql.select_belongs_keep_watch(belongs)
    # db_data_list = hSql.selectAllKeepWatchTable()
    for db_data in db_data_list:
        results = yt.videoInfo(youtubeObject,db_data['video_id'])
        tube_video_live_details = results.get("items", None)
        if tube_video_live_details:
            for video_info_result in tube_video_live_details:
                if video_info_result.get('liveStreamingDetails',False):
                    scheduledStartTime = video_info_result['liveStreamingDetails'].get('scheduledStartTime',None) #ライブ開始予定時間
                    # actualStartTime = video_info_result['liveStreamingDetails'].get('actualStartTime',None) #ライブ開始時間
                    # actualEndTime = video_info_result['liveStreamingDetails'].get('actualEndTime',None) #ライブ終了時間
                    # status = video_info_result["snippet"]["liveBroadcastContent"]
                    jst = hTime.convertToJST(scheduledStartTime)
                    db_jst = db_data['scheduled_start_time_at'].strftime('%Y/%m/%d %H:%M')
                    if not jst == db_jst: # 時間変更検知
                        if belongs == 'hololive':
                            tw = tweet_components(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
                            # tw = tweet_components(CONSUMER_KEY_TEST, CONSUMER_SECRET_TEST, ACCESS_TOKEN_TEST, ACCESS_TOKEN_SECRET_TEST)
                            v_name, live_tag = Hololive.get_name_tag(db_data['channel_id'])
                        elif belongs == 'noripro':
                            tw = tweet_components(CONSUMER_KEY_B, CONSUMER_SECRET_B, ACCESS_TOKEN_B, ACCESS_TOKEN_SECRET_B)
                            # tw = tweet_components(CONSUMER_KEY_TEST, CONSUMER_SECRET_TEST, ACCESS_TOKEN_TEST, ACCESS_TOKEN_SECRET_TEST)
                            v_name, live_tag = NoriPro.get_name_tag(db_data['channel_id'])

                        if hSql.update_schedule_keep_watch(db_data['video_id'], jst) and hSql.update_schedule_youtube_videos_table(db_data['video_id'], jst):
                            message = f"LIVE開始時間の変更⏰\n{v_name}チャンネル\n{live_tag}\n\n時間変更されました。注意してください。\n配信予定時間\n{jst}🇯🇵\n{hTime.convert_To_LON(jst)}🇬🇧\n{hTime.convert_To_NY(jst)}🇺🇸🗽\n\n{db_data['title']}\n{bitly.make_yURL(db_data['channel_url'])}"
                            tw.tweetWithIMG(message, db_data['image_default'], TRIM_IMG_DIR)
                            message = f"\n{v_name}チャンネル\n時間変更⏰\n{jst}\n\n{db_data['title']}\n{db_data['channel_url']}"
                            line.lineNotify(message)

    hSql.dbClose()
    hSql = None
    hTime = None
    yt = None

def table_cleaning():
    '''指定時間にtableを検査,ゴミデータを削除する
    '''
    print('テーブルのクリーニングを開始します')
    hTime = HoloDate()
    hSql = holo_sql.holo_sql()
    yt = yApi()
    db_data_list = hSql.selectAllKeepWatchTable()
    for db_data in db_data_list:
        results = yt.videoInfo(youtubeObject,db_data['video_id'])
        update_time = []
        tube_video_live_details = results.get("items", None)
        if tube_video_live_details:
            for video_info_result in tube_video_live_details:
                if video_info_result.get('liveStreamingDetails',False):
                    live_title = video_info_result["snippet"]["title"]
                    scheduledStartTime = video_info_result['liveStreamingDetails'].get('scheduledStartTime',None) #ライブ開始予定時間
                    actualStartTime = video_info_result['liveStreamingDetails'].get('actualStartTime',None) #ライブ開始時間
                    actualEndTime = video_info_result['liveStreamingDetails'].get('actualEndTime',None) #ライブ終了時間
                    concurrentViewers = video_info_result['liveStreamingDetails'].get('concurrentViewers',None) #live視聴者
                    activeLiveChatId = video_info_result['liveStreamingDetails'].get('activeLiveChatId',None) #ライブchatID
                    status = video_info_result["snippet"]["liveBroadcastContent"]
                    
                    if status == 'live':
                        pass
                    elif status == 'upcoming':
                        pass
                    else:
                        update_time.append([
                            video_info_result['id'],
                            hTime.convertToJST(scheduledStartTime),
                            hTime.convertToJST(actualStartTime),
                            hTime.convertToJST(actualEndTime),
                            concurrentViewers,
                            activeLiveChatId,
                            status,
                            live_title,
                            ])
                        # @TODO youtube_videosテーブル内の該当video_idのstatusをnoneに変更しないといけない
                        if hSql.updateTimeYoutubeVideoTable(update_time):
                            hSql.deleteKeepWatchTable(db_data['video_id'])
                            pprint('何らかの理由で削除、または非公開になった枠を削除しました')
                            pprint(update_time)
        else:
            # @TODO youtube_videosテーブル内の該当video_idのstatusをnoneに変更しないといけない
            hSql.deleteKeepWatchTable(db_data['video_id'])
    hSql.dbClose()
    hSql = None
    hTime = None
    yt = None

# =============================================================
def main():
    hTime = HoloDate()
    hSql = holo_sql.holo_sql()
    yt = yApi()
    dt_now = dt.now()
    # dt_now = dt.now(datetime.timezone( datetime.timedelta(hours=9) ))
    db_data_list = hSql.selectAllKeepWatchTable()

    for db_data in db_data_list:
        update_time = []
        if db_data['scheduled_start_time_at']:
            time_lag = db_data['scheduled_start_time_at'] - dt_now
        else:
            time_lag = db_data['actual_start_time_at'] - dt_now
        '''
        2hour = 7200 sec   2時間以内
        time_lag.days >= 0 予定時前
        time_lag.days < 0  予定時間より過ぎている
        '''
        if time_lag.days >= 0:
            min, sec = divmod(time_lag.seconds, 60)
            hours, min= divmod(min, 60)
            if time_lag.days == 0:
                if time_lag.seconds <= _3HOURS :
                    # @TODO IDが存在しなかった場合はwatchテーブルから削除しなくてはいけない なんとエラーが出るかわからない調査が必要
                    results = yt.videoInfo(youtubeObject,db_data['video_id'])
                    tube_video_live_details = results.get("items", None)
                    if tube_video_live_details:
                        for video_info_result in tube_video_live_details:
                            if video_info_result["kind"] == "youtube#video":
                                '''
                                scheduledStartTime ライブ開始予定時間(太平洋標準時)
                                actualStartTime ライブ開始時間
                                actualEndTime ライブ終了時間
                                scheduledStartTimeJPT  ライブ開始予定時間(日本時間変換済)
                                status 状態:upcoming,live,none
                                '''
                                if video_info_result.get('liveStreamingDetails',False):
                                    scheduledStartTime = video_info_result['liveStreamingDetails'].get('scheduledStartTime',None) #ライブ開始予定時間
                                    actualStartTime = video_info_result['liveStreamingDetails'].get('actualStartTime',None) #ライブ開始時間
                                    actualEndTime = video_info_result['liveStreamingDetails'].get('actualEndTime',None) #ライブ終了時間
                                    concurrentViewers = video_info_result['liveStreamingDetails'].get('concurrentViewers',None) #live視聴者
                                    activeLiveChatId = video_info_result['liveStreamingDetails'].get('activeLiveChatId',None) #ライブchatID
                                    status = video_info_result["snippet"]["liveBroadcastContent"]
                                    _title = video_info_result["snippet"]["title"]

                                    update_time.append([
                                        db_data['video_id'],
                                        hTime.convertToJST(scheduledStartTime),
                                        hTime.convertToJST(actualStartTime),
                                        hTime.convertToJST(actualEndTime),
                                        concurrentViewers,
                                        activeLiveChatId,
                                        status,
                                        _title,
                                    ])

                                    if status == 'upcoming':
                                        hSql.updateKeepWatchTable(update_time)
                                        hSql.updateTimeYoutubeVideoTable(update_time)
                                    # LIVE開始前倒し対策
                                    elif status == 'live':
                                        print('liveが前倒で開始されています')
                                        # if hSql.insertLiveKeepWatchTable(db_data,update_time):
                                        if hSql.insertLiveKeepWatchTable_test(db_data,update_time):
                                            hSql.deleteKeepWatchTable(db_data['video_id'])
                                    # none対策
                                    else:
                                        if hSql.updateTimeYoutubeVideoTable(update_time):
                                            hSql.deleteKeepWatchTable(db_data['video_id'])
                                    '''
                                    hours == 1                 予定時間まで1時間以上時間がある場合
                                    hours == 0 and min > 1     1時間以内かつ1分以上ある場合
                                    その他                      1分未満かつ0秒以上ある場合
                                    '''
                                    if hours == 1:
                                        print('LIVEが{}時間{}分後にスタートします!'.format(hours,min))
                                    elif hours == 0 and min > 1:
                                        print('LIVEが{}分後にスタートします!'.format(min))
                                    else:
                                        print('LIVEが始まります!いますぐ待機してください!')
                    else:
                        hSql.deleteKeepWatchTable(db_data['video_id'])
                else:
                    '''
                    hours < 24 and hours > 2    予定時間まで24時間以内かつ,2時間以上時間がある場合
                    '''
                    print('LIVE開始まで,あと{}時間{}分!'.format(hours,min))
                    # hours_minute = datetime.timedelta(seconds=time_lag.seconds)
                    # print('あと{}後にスタート予定!'.format(hours_minute))
                    # print('LIVEが{}時間{}分後にスタートします!'.format(hours,min))

                    # スケジュール時間に変更がないかチェック
                    # APIで再度時間を取得
                    # if 時間が変っているか？
                        # 変っているならテーブルの値を変更
                    # エラー　IDが消えている
                        # 枠が消された可能性あり　テーブルから削除
            else:
                print('LIVE開始まで,あと{}日と{}時間{}分!'.format(time_lag.days,hours,min))
        else:
            # time_lag = dt_now - db_data[7]
            if db_data['scheduled_start_time_at']:
                time_lag = dt_now - db_data['scheduled_start_time_at']
            else:
                time_lag = dt_now - db_data['actual_start_time_at']

            min, sec = divmod(time_lag.seconds, 60)
            hours, min= divmod(min, 60)
            print('開始時間過ぎています')
            print('{}日と{}時間{}分経過しています'.format(time_lag.days,hours,min)) if time_lag.days > 0 else print('{}時間{}分経過しています'.format(hours,min))
            # hSql.deleteKeepWatchTable(db_data[1])    #削除する
            # @TODO IDが存在しなかった場合はwatchテーブルから削除しなくてはいけない なんとエラーが出るかわからない調査が必要
            results = yt.videoInfo(youtubeObject, db_data['video_id'])
            tube_video_live_details = results.get("items", None)
            if tube_video_live_details:
                for video_info_result in tube_video_live_details:
                    if video_info_result["kind"] == "youtube#video":
                        live_title = video_info_result["snippet"]["title"]
                        '''
                        scheduledStartTime ライブ開始予定時間(太平洋標準時)
                        actualStartTime ライブ開始時間
                        actualEndTime ライブ終了時間
                        scheduledStartTimeJPT  ライブ開始予定時間(日本時間変換済)
                        status 状態:upcoming,live,none
                        '''
                        if video_info_result.get('liveStreamingDetails',False):
                            scheduledStartTime = video_info_result['liveStreamingDetails'].get('scheduledStartTime',None) #ライブ開始予定時間
                            actualStartTime = video_info_result['liveStreamingDetails'].get('actualStartTime',None) #ライブ開始時間
                            actualEndTime = video_info_result['liveStreamingDetails'].get('actualEndTime',None) #ライブ終了時間
                            concurrentViewers = video_info_result['liveStreamingDetails'].get('concurrentViewers',None) #live視聴者
                            activeLiveChatId = video_info_result['liveStreamingDetails'].get('activeLiveChatId',None) #ライブchatID
                            status = video_info_result["snippet"]["liveBroadcastContent"]
                            
                            # scheduledStartTimeJPT = convertToJST(scheduledStartTime)
                            update_time.append([
                                video_info_result['id'],
                                hTime.convertToJST(scheduledStartTime),
                                hTime.convertToJST(actualStartTime),
                                hTime.convertToJST(actualEndTime),
                                concurrentViewers,
                                activeLiveChatId,
                                status,
                                live_title,
                            ])
                            if status == 'live':
                                # if hSql.insertLiveKeepWatchTable(db_data, update_time):
                                if hSql.insertLiveKeepWatchTable_test(db_data, update_time):
                                    hSql.deleteKeepWatchTable(db_data['video_id'])
                            elif status == 'upcoming':
                                hSql.updateKeepWatchTable(update_time)
                                hSql.updateTimeYoutubeVideoTable(update_time)
                            else:   # none
                                if hSql.updateTimeYoutubeVideoTable(update_time):
                                    hSql.deleteKeepWatchTable(db_data['video_id'])
            else:
                hSql.deleteKeepWatchTable(db_data['video_id'])

    hSql.dbClose()
    hSql = None
        # time.sleep(300)

def sub():
    check_schedule_time('hololive')
    check_schedule_time('noripro')

schedule.every(5).minutes.do(main)

schedule.every().hour.at(":00").do(sub)
schedule.every().hour.at(":20").do(sub)
schedule.every().hour.at(":40").do(sub)

schedule.every().day.at("03:00").do(table_cleaning)

if __name__ == '__main__':

    main()

    while True:
        schedule.run_pending()
        time.sleep(1)