# 
# youtubeチャンネル登録者,動画本数,再生回数の監視
# 
import tweepy
from pyasn1.type.univ import Boolean, Null
import requests
from requests_oauthlib import OAuth1Session
import urllib.request, urllib.error

from pprint import pprint

import time
import datetime
from datetime import datetime as dt
import dateutil.parser
import schedule

from apiclient.discovery import build
from apiclient.errors import HttpError

import os
from os.path import join, dirname
from dotenv import load_dotenv

'''
Original Modules
'''
import holo_sql
from ImageProcessing import ImageProcessing
from YoutubeAPI.YoutubeAPI import Youtube_API
from ImageProcessing.photoFabrication import PhotoFabrication
from Components.tweet import tweet_components
from Components.holo_date import HoloDate
from Components.tubeAnalysts import Analyzer


load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# ==========================================================================
#twitterアカウントAPI
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
# ==========================================================================

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(auth)

# ==========================================================================
# 画像の保存先
LIVE_TMB_IMG_DIR = os.environ.get('LIVE_TMB_IMG_DIR')
LIVE_TMB_TMP_DIR = os.environ.get('LIVE_TMB_TMP_DIR')
# トリミング加工済み画像保存先
TRIM_IMG_DIR = os.environ.get('IMG_TRIM_DIR')
# 代表画像
DEFAULT_IMG = 'hololive.jpg'
# ==========================================================================

_api_key = 'YOUTUBE_API_KEY_dev3'
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
Channel_JP = {
    # ホロライブ
    '戌神ころね' :'UChAnqc_AY5_I3Px5dig3X1Q',    #戌神ころね
    'さくらみこ' : 'UC-hM6YJuNYVAmUWxeIr9FeA',     #さくらみこ
    '白上フブキ' : 'UCdn5BQ06XqgXoAxIhbqw5Rg',   #白上フブキ
    '湊あくあ' : 'UC1opHUrw8rvnsadT-iGp7Cg',     #湊あくあ
    '兎田ぺこら' : 'UC1DCedRgGHBdm81E1llLhOQ',   #兎田ぺこら
    'アキ・ローゼンタール' : 'UCFTLzh12_nrtzqBPsTCqenA',   #アキ・ローゼンタール
    'ときのそら' : 'UCp6993wxpyDPHUpavwDFqgg',     #ときのそら
    '大空スバル' : 'UCvzGlP9oQwU--Y0r9id_jnA',   #大空スバル
    'ロボ子さん' : 'UCDqI2jOz0weumE8s7paEk6g',   #ロボ子さん
    '紫咲シオン' : 'UCXTpFs_3PqI41qX2d9tL2Rw',    #紫咲シオン
    '不知火フレア' : 'UCvInZx9h3jC2JzsIzoOebWg',    #不知火フレア
    '夜空メル' : 'UCD8HOxPs4Xvsm8H0ZxXGiBw',      #夜空メル
    '癒月ちょこ' : 'UC1suqwovbL1kzsoaZgFZLKg',    #癒月ちょこ
    '癒月ちょこ(サブ)' : 'UCp3tgHXw_HI0QMk1K8qh3gQ',    #癒月ちょこ(サブ)
    '赤井はあと' : 'UC1CfXB_kRs3C-zaeTG3oGyg',    #赤井はあと
    '猫又おかゆ' : 'UCvaTdHTWBGv3MKj3KVqJVCw',    #猫又おかゆ
    '姫森ルーナ' : 'UCa9Y57gfeY0Zro_noHRVrnw',     #姫森ルーナ
    '星街すいせい' : 'UC5CwaMl1eIgY8h02uZw7u8A',   #星街すいせい
    '夏色まつり' : 'UCQ0UDLQCjY0rmuxCDE38FGg',  #夏色まつり
    '宝鐘マリン' : 'UCCzUftO8KOVkV4wQG1vkUvg',   #宝鐘マリン
    '百鬼あやめ' : 'UC7fk0CB07ly8oSl0aqKkqFg',   #百鬼あやめ
    '白銀ノエル' : 'UCdyqAaZDKHXg4Ahi7VENThQ',     #白銀ノエル
    '潤羽るしあ' : 'UCl_gCybOJRIgOXw6Qb4qJzQ',   #潤羽るしあ
    '桐生ココ' : 'UCS9uQI-jC3DE0L4IpXyvr6w',     #桐生ココ
    '天音かなた' : 'UCZlDXzGoo7d44bwdNObFacg',   #天音かなた
    '大神ミオ' : 'UCp-5t9SrOQwXMU7iIjQfARg',      #大神ミオ
    '常闇トワ' : 'UC1uv2Oq6kNxgATlCiez59hw',     #常闇トワ
    '角巻わため' : 'UCqm3BQLlJfvkTsX_hvm0UmA',   #角巻わため
    '雪花ラミィ' : 'UCFKOVgVbGmX65RxO3EtH3iw',      #雪花ラミィ
    '桃鈴ねね' : 'UCAWSyEs_Io8MtpY3m-zqILA',     #桃鈴ねね
    '獅白ぼたん' : 'UCUKD-uaobj9jiqB-VXt71mA',      #獅白ぼたん
    '尾丸ポルカ' : 'UCK9V2B22uJYu3N7eR_BT9QA' ,      #尾丸ポルカ
    # 'ALOE_ch' : 'UCgZuwn-O7Szh9cAgHqJ6vjw',      #魔乃アロエ
    
    # イノナカミュージック
    'AZKi' : 'UC0TXe_LYZ4scaW2XMyi5_kw',     #AZKi

    # 運営
    'Hololive' : 'UCJFZiqLMntJufDCHc6bQixg',   #Hololive
}

Channel_OSea = {
    #ホロライブ　EN
    '森美声' : 'UCL_qhgtOy0dy1Agp8vkySQg',    #森美声 モリ・カリオペ
    '小鳥遊キアラ' : 'UCHsx4Hqa-1ORjQTh9TYDhww',    #小鳥遊キアラ
    '一伊那尓栖' : 'UCMwGHR0BTZuLsmjY_NT5Pwg',    #一伊那尓栖 にのまえいなにす
    'がうる・くら' : 'UCoSrY_IQQVpmIRZ9Xf-y93g',    #がうる・くら
    'ワトソン・アメリア' : 'UCyl1z3jo3XHR1riLFKG5UAg',  #ワトソン・アメリア

    #ホロライブ ID
    'アユンダ・リス' : 'UCOyYb1c43VlX9rc_lT6NKQw',    #Ayunda Risu / アユンダ・リス
    'ムーナ・ホシノヴァ' : 'UCP0BspO_AMEe3aQqqpo89Dg',      #Moona Hoshinova / ムーナ・ホシノヴァ
    'アイラニ・イオフィフティーン' : 'UCAoy6rzhSf4ydcYjJw3WoVg',      #Airani Iofifteen / アイラニ・イオフィフティーン
    'クレイジー・オリー' : 'UCYz_5n-uDuChHtLo7My1HnQ',     #Kureiji Ollie / クレイジー・オリー 
    'アーニャ・メルフィッサ' : 'UC727SQYUvx5pDDGQpTICNWg',       #Anya Melfissa / アーニャ・メルフィッサ
    'パヴォリア・レイネ' : 'UChgTyjG-pdNvxxhdsXfHQ5Q',       #Pavolia Reine / パヴォリア・レイネ
}

Channel_Friends = {
    # 他
    '時雨うい' : 'UCt30jJgChL8qeT9VPadidSw', #時雨うい
    '佃煮のりお' : 'UC8NZiqKx6fsDT3AVcMiVFyA',     #佃煮のりお
    '白雪みしろ' : 'UCC0i9nECi4Gz7TU63xZwodg',  #白雪みしろ
    '愛宮みるく' : 'UCJCzy0Fyrm0UhIrGQ7tHpjg',       #愛宮みるく
    '姫咲ゆずる' : 'UCle1cz6rcyH0a-xoMYwLlAg',     #姫咲ゆずる
    '鬼灯わらべ' : 'UCLyTXfCZtl7dyhta9Jg3pZg',    #鬼灯わらべ
    '夢乃リリス' : 'UCH11P1Hq4PXdznyw1Hhr3qw',     #夢乃リリス
    '胡桃澤もも' : 'UCxrmkJf_X1Yhte_a4devFzA', #胡桃澤もも
    '逢魔きらら' : 'UCBAeKqEIugv69Q2GIgcH7oA',     #逢魔きらら
    '看谷にぃあ' : 'UCIRzELGzTVUOARi3Gwf1-yg',        #看谷にぃあ
}

Channels = [Channel_JP, Channel_OSea,]
All_Channels = [Channel_JP, Channel_OSea, Channel_Friends]

#th_val人刻みでツイートするための条件設定。th_val = 10000 なら10000人刻み
def subJudge(sub_num,value,sub_val=50000)->Boolean:
    if (sub_num // sub_val)  > (value[0]['youtube_subscriber'] // sub_val):
        return True
    else:
        return False

'''
全体の登録者を足す
'''
def OverallInfo(): 
    tw = tweet_components()
    hTime = HoloDate()
    youAPI = Youtube_API()
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
    message = '現在のHololive全体報告!\nHololive全体チャンネル登録者数は\n🌟約{}万人!🌟\n止まらないHololive!😎\n #Hololive'.format((All_Subscriber)//10000)
    tw.sub_tweetWithIMG(message,DEFAULT_IMG)
    hSql.insertHoloData(data_list)

    pprint(str(All_Subscriber+10000) + '万人')



def searchSubscriber():
    pprint('起動開始')
    tw = tweet_components()
    youAPI = Youtube_API()
    hSql = holo_sql.holo_sql()


    for Channel in All_Channels:
    # for Channel in Channels:
        for Name,channel_ID in Channel.items():
            channel_info_list = []
            message = []
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
                        if subJudge(int(subscriberCount), profile):
                            message = '速報！！ ✨{}チャンネル✨\n{}\n\nチャンネル登録者が\n🎉{}万人到達!!!🎉`\nおめでとう!!🥳\nチャンネル登録はこちら!: {}'.format(Name, profile[0]['live_tag'],(int(subscriberCount)//10000),profile[0]['channel_url'])
                            tw.sub_tweetWithIMG(message, profile[0]['image1'])
                            pprint(message)
                        hSql.insert_HoloJP_ProfileTable(channel_ID, channel_info_list)
                    elif Channel == Channel_OSea: 
                        # Hololive 海外
                        profile = hSql.selectOSHolo(channel_ID)
                        if subJudge(int(subscriberCount), profile):
                            message = '速報！！ ✨{}✨ チャンネル\n{}\n\nチャンネル登録者が\n🎉{}万人到達!!!🎉`\nおめでとう!!🥳\nチャンネル登録はこちら!: {}'.format(Name, profile[0]['live_tag'],(int(subscriberCount)//10000),profile[0]['channel_url'])
                            tw.sub_tweetWithIMG(message, profile[0]['image1'])
                            pprint(message)
                        hSql.insert_HoloOS_ProfileTable(channel_ID, channel_info_list)
                    elif Channel == Channel_Friends:
                        # Friends
                        profile = hSql.selectFriendsHolo(channel_ID)
                        if subJudge(int(subscriberCount), profile):
                            message = '速報！！ ✨{}✨ チャンネル\n{}\n\nチャンネル登録者が\n🎉{}万人到達！！🎉`\nおめでとうございます!!🥳\nチャンネル登録はこちら!: {}'.format(Name, profile[0]['live_tag'],(int(subscriberCount)//10000),profile[0]['channel_url'])
                            tw.sub_tweetWithIMG(message, profile[0]['image1'])
                            pprint(message)
                        hSql.insert_HoloFri_ProfileTable(channel_ID, channel_info_list)
                    
                    # channel_info_list = []

    hSql.dbClose()
    hSql = None
    tw = None
    youAPI = None
    pprint('終了')


# 毎時0分に実行
schedule.every().hour.at(":00").do(searchSubscriber)
schedule.every().hour.at(":30").do(searchSubscriber)
# schedule.every().hour.at(":49").do(searchSubscriber)

# PM00:05 AM12:05にjob実行
schedule.every().day.at("00:05").do(OverallInfo)
# schedule.every().day.at("12:05").do(OverallInfo)
# schedule.every().day.at("18:56").do(OverallInfo)

while True:
    schedule.run_pending()
    time.sleep(1)