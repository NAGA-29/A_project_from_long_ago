# 
# youtubeチャンネル登録者,動画本数,再生回数の監視
# 
import tweepy
from pyasn1.type.univ import Boolean, Null
from requests_oauthlib import OAuth1Session
import urllib.request, urllib.error
from pprint import pprint
import time
import datetime
# from datetime import datetime as dt
import dateutil.parser
import pickle
import schedule

from apiclient.discovery import build
from apiclient.errors import HttpError

import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Original Modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
import holo_sql
from YoutubeAPI.YoutubeAPI import Youtube_API
from Components.vtuber.hololive import Hololive
from Components.vtuber.noripro import NoriPro
from Components.tweet import tweet_components
from Components.holo_date import HoloDate
from Components.matplotlib import holo_data

from sqlalchemy import func
from model import HoloData
from model import HoloProfile
from model.setting import session as se

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../../../.env')
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

# ==========================================================================
# 代表画像
DEFAULT_IMG = 'hololive.jpg'
GRAPH_IMG = 'holo_data.png'
# BASE_PATH = 'Profile_Images'
# ==========================================================================

_api_key = 'YOUTUBE_API_KEY_dev4'
_api_number = 1

API_KEY = os.environ.get(_api_key)
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

nextPagetoken = None
nextpagetoken = None

youtubeObject = build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
    )

# ==========================================================================
Channel_JP, Channel_OSea = Hololive.get_video_ids()
Channel_Friends = NoriPro.get_video_ids()
Channels = [Channel_JP, Channel_OSea,]
All_Channels = [Channel_JP, Channel_OSea, Channel_Friends]


#th_val人刻みでツイートするための条件設定。th_val = 10000 なら10000人刻み
def subJudge(sub_num, value, belongs)->Boolean:
    sub_val = 0
    if belongs == 'hololive':
        sub_val = 50000
    elif belongs == 'noripro':
        sub_val = 10000

    if (sub_num // sub_val)  > (value[0]['youtube_subscriber'] // sub_val):
        return True
    else:
        return False


# 登録者直前判定
def just_before_judge(_tube_sub:int, _sub_val=50000):
    quotient, remainder = divmod(_tube_sub, _sub_val) # quotient:商 remainder:余り
    result = _sub_val - remainder
    if result <= 3000:
        return result
    else:
        return False


def read_pickle_notice_log(file=None)->dict:
    if file == None:
        file = 'service/youtube/ini/subscriber_notice_time.pkl'
        file_path = os.path.join(os.getcwd(), file)
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except EOFError as err:
        print(f'EOFError on load pickle file: {err}')
        return None


def write_pickle_notice_log(log_dict:dict, file=None):
    if file == None:
        file = 'service/youtube/ini/subscriber_notice_time.pkl'
        file_path = os.path.join(os.getcwd(), file)
    try:
        # pklファイルに保存
        with open(file_path, 'wb') as f:
            pickle.dump(log_dict, f)
    except Exception as err:
        print(f'ERROR on save pickle file: {err}')


def OverallInfo(): 
    '''
    全体の登録者を足す
    '''
    tw = tweet_components()
    hTime = HoloDate()
    # youAPI = Youtube_API()

    # DBからidを検索
    # result = session.query(HoloData).all()
    # n = len(result) - 1
    # result = session.query(HoloData).filter(HoloData.id == n).all()
    hSql = holo_sql.holo_sql()
    All_Subscriber = 0  # 全体の登録者
    All_VideoCount = 0 #　全体の公開中のビデオ本数
    All_ViewCount = 0 # 全体の再生回数
    data_list = []
    now = datetime.datetime.now()
    updated_at = now.strftime('%Y-%m-%d %H:%M:%S')

    for Channel in Channels:
        for Name,channel_ID in Channel.items():
            message = []

            if Channel == Channel_JP: 
                # Hololive
                profile = hSql.selectHolo(channel_ID)
                All_Subscriber = All_Subscriber + profile[0]['youtube_subscriber']
                All_VideoCount = All_VideoCount +  profile[0]['youtube_videoCount']    #　全体の公開中のビデオ本数
                All_ViewCount = All_ViewCount +  profile[0]['youtube_viewCount']    # 全体の再生回数
            elif Channel == Channel_OSea: 
                # Hololive 海外
                profile = hSql.selectOSHolo(channel_ID)
                All_Subscriber = All_Subscriber + profile[0]['youtube_subscriber']
                All_VideoCount = All_VideoCount +  profile[0]['youtube_videoCount']   #　全体の公開中のビデオ本数
                All_ViewCount = All_ViewCount +  profile[0]['youtube_viewCount']    # 全体の再生回数

    data_list.append([All_Subscriber, All_VideoCount, All_ViewCount, hTime.convertToJST(updated_at)])
    # pprint(f'data_list:{data_list}')
    # pprint('日付:{}'.format(datetime.date.today() - datetime.timedelta(days=1)))
    # yestarday_data = session.query(HoloData).filter(func.date(HoloData.updated_at) == (datetime.date.today() - datetime.timedelta(days=1)) ).all()
    yestarday_data = se.query(HoloData).filter(func.date(HoloData.updated_at) == (datetime.date.today() - datetime.timedelta(days=1))).all()
    # pprint(f'yestarday_data: {yestarday_data}')
    All_Subscriber_previous_day = (All_Subscriber//10000) - (yestarday_data[0].all_youtube_subscriber//10000)
    All_VideoCount_previous_day = All_VideoCount - yestarday_data[0].all_youtube_videoCount
    All_ViewCount_previous_day = All_ViewCount - yestarday_data[0].all_youtube_viewCount

    message = 'Hololive全体報告!\n\n全体チャンネル登録者数\n🌟約{:,}万人 (+{:,}万人)\n全体動画数\n🌟{:,}本 (+{:,}本)\n全体再生回数\n🌟{:,}回 (+{:,}回)\n\n #Hololive'.format(
                                                                                    (All_Subscriber)//10000, All_Subscriber_previous_day, 
                                                                                    All_VideoCount, All_VideoCount_previous_day, 
                                                                                    All_ViewCount, All_ViewCount_previous_day)

    hSql.insertHoloData(data_list)
    hSql.dbClose()
    hSql = None

    holo_data.make_holo_data_graph()
    # tw.sub_tweetWithIMG(message,DEFAULT_IMG)
    tw.matplotlib_tweetWithIMG(message,GRAPH_IMG)
    pprint(str(All_Subscriber+10000) + '万人')


def searchSubscriber(belongs: str, hSql=None, youAPI=None):
    """
    登録者検知/通知

    Param
    -------
    belongs : str 所属グルーブ
    """
    pprint('起動開始')
    if youAPI == None:
        youAPI = Youtube_API()
    if hSql == None:
        hSql = holo_sql.holo_sql()

    Channel_JP, Channel_OSea, Channel_Friends = None, None, None
    if belongs == 'hololive':
        Channel_JP, Channel_OSea = Hololive.get_video_ids()
        All_Channels = [Channel_JP, Channel_OSea]
    elif belongs == 'noripro':
        Channel_Friends = NoriPro.get_video_ids()
        All_Channels = [Channel_Friends]

    for Channel in All_Channels:
        for Name,channel_ID in Channel.items():
            channel_info_list = []
            message = ''
            channel_datas = youAPI.channelInfo(youtubeObject, channel_ID) # youtube APIを使用してチャンネル情報を取得
            CHANNEL_DATAS = channel_datas.get("items", None)
            if CHANNEL_DATAS:
                if not CHANNEL_DATAS[0]['statistics']['hiddenSubscriberCount']:
                    subscriberCount = CHANNEL_DATAS[0]['statistics'].get('subscriberCount', None) #チャンネル登録者
                    videoCount = CHANNEL_DATAS[0]['statistics'].get('videoCount', None) #ビデオ本数
                    viewCount = CHANNEL_DATAS[0]['statistics'].get('viewCount', None) #ビデオ再生回数
                    channel_info_list.append(int(subscriberCount))
                    channel_info_list.append(int(videoCount))
                    channel_info_list.append(int(viewCount))

                    if Channel == Channel_JP: 
                        # Hololive 日本
                        tw = tweet_components()
                        profile = hSql.selectHolo(channel_ID)
                        # holo_prf = se.query(HoloProfile).filter(HoloProfile.channel_id == channel_ID).all() # dbよりプロフィールを取得
                        if subJudge(int(subscriberCount), profile, belongs):
                            # tw = tweet_components()
                            message = '速報！\n{}✨\n{}\n\n<Youtube>チャンネル登録者が\n\n【{}万人】到達!🔥\n\nおめでとうございます！\n\nデビュー日:{}\n誕生日:{}\n{}'.format(
                                Name, profile[0]['live_tag'], (int(subscriberCount)//10000), 
                                profile[0]['debut'].strftime('%Y/%m/%d'),
                                profile[0]['birthday'].strftime('%m/%d'),
                                profile[0]['channel_short_url'])
                            tw.sub_tweetWithIMG(message, profile[0]['image1'])
                            pprint(message)
# ===========================FIXME:
                        else:
                            result = just_before_judge(int(subscriberCount))
                            log_pkl = read_pickle_notice_log()
                            if not log_pkl[belongs].get(channel_ID, None):
                                log_pkl[belongs][channel_ID] = '2022-01-01 00:00:00' # 初期値
                            plus12hours = datetime.datetime.strptime(log_pkl[belongs][channel_ID], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=24)
                            if result and (datetime.datetime.now() >= plus12hours):
                                message = 'Hololiveお知らせ\n\n{}✨\n{}\n\n<Youtube>チャンネル登録者が\n\nあと{:,}人で\n【{}万人】到達します!🔥\n\n応援をよろしくお願いします！\n\n{}'.format(
                                                                    Name, profile[0]['live_tag'], result, ((int(subscriberCount)+result)//10000), profile[0]['channel_short_url'])
                                log_pkl[belongs][channel_ID] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                write_pickle_notice_log(log_pkl)
                                print(message)
                                tw.sub_tweetWithIMG(message, profile[0]['image1'])
# ===========================
                        hSql.insert_HoloJP_ProfileTable(channel_ID, channel_info_list)
                        
                    elif Channel == Channel_OSea: 
                        # Hololive 海外
                        tw = tweet_components()
                        profile = hSql.selectOSHolo(channel_ID)
                        if subJudge(int(subscriberCount), profile, belongs):
                            message = '速報！\n{}✨\n{}\n\n<Youtube>チャンネル登録者が\n\n【{}万人】到達!🔥\n\nおめでとうございます！\n\nデビュー日:{}\n誕生日:{}\n{}'.format(
                                Name, profile[0]['live_tag'], (int(subscriberCount)//10000), 
                                profile[0]['debut'].strftime('%Y/%m/%d'),
                                profile[0]['birthday'].strftime('%m/%d'),
                                profile[0]['channel_short_url'])
                            tw.sub_tweetWithIMG(message, profile[0]['image1'])
                            pprint(message)
# ===========================FIXME:
                        else:
                            result = just_before_judge(int(subscriberCount))
                            log_pkl = read_pickle_notice_log()
                            # pprint(log_pkl[belongs].get(channel_ID, None))
                            if not log_pkl[belongs].get(channel_ID, None):
                                log_pkl[belongs][channel_ID] = '2022-01-01 00:00:00' # 初期値
                            plus12hours = datetime.datetime.strptime(log_pkl[belongs][channel_ID], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=24)
                            if result and (datetime.datetime.now() >= plus12hours):
                                message = 'Hololiveお知らせ\n\n{}✨\n{}\n\n<Youtube>チャンネル登録者が\n\nあと{:,}人で\n【{}万人】到達します!🔥\n\n応援をよろしくお願いします！\n\n{}'.format(
                                                                    Name, profile[0]['live_tag'], result, ((int(subscriberCount)+result)//10000), profile[0]['channel_short_url'])
                                log_pkl[belongs][channel_ID] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                write_pickle_notice_log(log_pkl)
                                print(message)
                                tw.sub_tweetWithIMG(message, profile[0]['image1'])
# ===========================
                        hSql.insert_HoloOS_ProfileTable(channel_ID, channel_info_list)

                    elif Channel == Channel_Friends:
                        # Friends
                        profile = hSql.selectFriendsHolo(channel_ID)
                        if subJudge(int(subscriberCount), profile, belongs):
                            tw = tweet_components(CONSUMER_KEY_B, CONSUMER_SECRET_B, ACCESS_TOKEN_B, ACCESS_TOKEN_SECRET_B)
                            message = '速報！\n{}✨\n{}\n\n<Youtube>チャンネル登録者が\n\n【{}万人】到達!🔥\n\nおめでとうございます！\n\n{}'.format(Name, profile[0]['live_tag'], (int(subscriberCount)//10000), profile[0]['channel_short_url'])
                            tw.sub_tweetWithIMG(message, profile[0]['image1'])
                            pprint(message)

                        hSql.insert_HoloFri_ProfileTable(channel_ID, channel_info_list)

    hSql.dbClose()
    hSql = None
    tw = None
    youAPI = None
    pprint('終了')

def main():
    searchSubscriber('hololive')
    searchSubscriber('noripro')


if __name__ == '__main__':
    main()
#     # 登録者検知/通知
#     # schedule.every().hour.at(":00").do(main)
#     # schedule.every().hour.at(":20").do(main)
#     # schedule.every().hour.at(":40").do(main)

#     # 全体登録者通知
#     # schedule.every().day.at("00:05").do(OverallInfo)
#     schedule.every().day.at("00:38").do(OverallInfo)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)