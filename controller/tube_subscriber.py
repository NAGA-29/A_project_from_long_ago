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
from datetime import datetime as dt
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
import holo_sql
from ImageProcessing import ImageProcessing
from YoutubeAPI.YoutubeAPI import Youtube_API
from ImageProcessing.photoFabrication import PhotoFabrication
from Components.vtuber.hololive import Hololive
from Components.vtuber.noripro import NoriPro
from Components.tweet import tweet_components
from Components.holo_date import HoloDate
from Components.tubeAnalysts import Analyzer

from sqlalchemy import func
from model import HoloData
from model.setting import session

# from model import HoloData
# from model.setting import session


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

# auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# API = tweepy.API(auth)

# ==========================================================================
# 代表画像
DEFAULT_IMG = 'hololive.jpg'
# BASE_PATH = 'Profile_Images'
# ==========================================================================

_api_key = 'YOUTUBE_API_KEY_dev4'
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

def OverallInfo(): 
    '''
    全体の登録者を足す
    '''
    tw = tweet_components()
    hTime = HoloDate()
    # youAPI = Youtube_API()
    # hdata = HoloData()
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
    yestarday_data = session.query(HoloData).filter(func.date(HoloData.updated_at) == (datetime.date.today() - datetime.timedelta(days=1)) ).all()
    # pprint(yestarday_data)
    message = 'Hololive全体報告!\n全体チャンネル登録者数\n🌟約{}万人!\n全体動画数\n🌟{}本!\n全体再生回数\n🌟{}回!\n\n #Hololive'.format((All_Subscriber)//10000, All_VideoCount, All_ViewCount)
    tw.sub_tweetWithIMG(message,DEFAULT_IMG)
    hSql.insertHoloData(data_list)

    pprint(str(All_Subscriber+10000) + '万人')

def searchSubscriber(belongs: str):
    """
    登録者検知/通知
    """
    pprint('起動開始')
    youAPI = Youtube_API()
    hSql = holo_sql.holo_sql()

    for Channel in All_Channels:
    # for Channel in Channels:
        for Name,channel_ID in Channel.items():
            channel_info_list = []
            message = ''
            channel_datas = youAPI.channelInfo(youtubeObject,channel_ID)
            CHANNEL_DATAS = channel_datas.get("items", None)
            if CHANNEL_DATAS:
                if not CHANNEL_DATAS[0]['statistics']['hiddenSubscriberCount']:
                    subscriberCount = CHANNEL_DATAS[0]['statistics'].get('subscriberCount',None) #チャンネル登録者
                    videoCount = CHANNEL_DATAS[0]['statistics'].get('videoCount',None) #ビデオ本数
                    viewCount = CHANNEL_DATAS[0]['statistics'].get('viewCount',None) #ビデオ再生回数
                    channel_info_list.append(int(subscriberCount))
                    channel_info_list.append(int(videoCount))
                    channel_info_list.append(int(viewCount))

                    if Channel == Channel_JP: 
                        # Hololive
                        profile = hSql.selectHolo(channel_ID)
                        if subJudge(int(subscriberCount), profile, belongs):
                            tw = tweet_components()
                            message = '速報！！\n{}✨ チャンネル\n{}\n\nチャンネル登録者が\n\n🎉{}万人到達!!!🎉`\n\nおめでとうございます!!\nチャンネル登録がまだの方はこちらから!\n {}'.format(Name, profile[0]['live_tag'],(int(subscriberCount)//10000),profile[0]['channel_short_url'])
                            tw.sub_tweetWithIMG(message, profile[0]['image1'])
                            pprint(message)
                        hSql.insert_HoloJP_ProfileTable(channel_ID, channel_info_list)
                        
                    elif Channel == Channel_OSea: 
                        # Hololive 海外
                        profile = hSql.selectOSHolo(channel_ID)
                        if subJudge(int(subscriberCount), profile, belongs):
                            tw = tweet_components()
                            message = '速報！！\n{}✨ チャンネル\n{}\n\nチャンネル登録者が\n\n🎉{}万人到達!!!🎉`\n\nおめでとうございます!!\nチャンネル登録がまだの方はこちらから!\n {}'.format(Name, profile[0]['live_tag'],(int(subscriberCount)//10000),profile[0]['channel_short_url'])
                            tw.sub_tweetWithIMG(message, profile[0]['image1'])
                            pprint(message)
                        hSql.insert_HoloOS_ProfileTable(channel_ID, channel_info_list)

                    elif Channel == Channel_Friends:
                        # Friends
                        profile = hSql.selectFriendsHolo(channel_ID)
                        if subJudge(int(subscriberCount), profile, belongs):
                            tw = tweet_components(CONSUMER_KEY_B, CONSUMER_SECRET_B, ACCESS_TOKEN_B, ACCESS_TOKEN_SECRET_B)
                            message = '速報！！\n{}✨ チャンネル\n{}\n\nチャンネル登録者が\n\n🎉{}万人到達!!!🎉`\n\nおめでとうございます!!\nチャンネル登録がまだの方はこちらから!\n {}'.format(Name, profile[0]['live_tag'],(int(subscriberCount)//10000),profile[0]['channel_short_url'])
                            tw.sub_tweetWithIMG(message, profile[0]['image1'])
                            pprint(message)
                        hSql.insert_HoloFri_ProfileTable(channel_ID, channel_info_list)
                    
                    # channel_info_list = []

    hSql.dbClose()
    hSql = None
    tw = None
    youAPI = None
    pprint('終了')

def main():
    searchSubscriber('hololive')
    searchSubscriber('noripro')


if __name__ == '__main__':
    # 登録者検知/通知
    # schedule.every().hour.at(":00").do(main)
    # schedule.every().hour.at(":20").do(main)
    # schedule.every().hour.at(":40").do(main)

    # 全体登録者通知
    schedule.every().day.at("00:05").do(OverallInfo)
    while True:
        schedule.run_pending()
        time.sleep(1)