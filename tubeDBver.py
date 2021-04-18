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
LIVE_TMB_TMP_DIR = os.environ.get('LIVE_TMB_TMP_DIR')
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


Channel = {
    # ホロライブ
    'KORONE_ch' :'UChAnqc_AY5_I3Px5dig3X1Q',    #戌神ころね
    'MIKO_ch' : 'UC-hM6YJuNYVAmUWxeIr9FeA',     #さくらみこ
    'FUBUKI_ch' : 'UCdn5BQ06XqgXoAxIhbqw5Rg',   #白上フブキ
    'AQUA_ch' : 'UC1opHUrw8rvnsadT-iGp7Cg',     #湊あくあ
    'PEKORA_ch' : 'UC1DCedRgGHBdm81E1llLhOQ',   #兎田ぺこら
    'AKIROSE_ch' : 'UCFTLzh12_nrtzqBPsTCqenA',   #アキ・ローゼンタール
    'SORA_ch' : 'UCp6993wxpyDPHUpavwDFqgg',     #ときのそら
    'SUBARU_ch' : 'UCvzGlP9oQwU--Y0r9id_jnA',   #大空スバル
    'ROBOCO_ch' : 'UCDqI2jOz0weumE8s7paEk6g',   #ロボ子さん
    'SHION_ch' : 'UCXTpFs_3PqI41qX2d9tL2Rw',    #紫咲シオン
    'FLARE_ch' : 'UCvInZx9h3jC2JzsIzoOebWg',    #不知火フレア
    'MEL_ch' : 'UCD8HOxPs4Xvsm8H0ZxXGiBw',      #夜空メル
    'CHOCO_ch' : 'UCp3tgHXw_HI0QMk1K8qh3gQ',    #癒月ちょこサブ
    'CHOCO_MAIN_ch' : 'UC1suqwovbL1kzsoaZgFZLKg', #癒月ちょこ
    'HAATO_ch' : 'UC1CfXB_kRs3C-zaeTG3oGyg',    #赤井はあと
    'OKAYU_ch' : 'UCvaTdHTWBGv3MKj3KVqJVCw',    #猫又おかゆ
    'LUNA_ch' : 'UCa9Y57gfeY0Zro_noHRVrnw',     #姫森ルーナ
    'SUISEI_ch' : 'UC5CwaMl1eIgY8h02uZw7u8A',   #星街すいせい
    'MATSURI_ch' : 'UCQ0UDLQCjY0rmuxCDE38FGg',  #夏色まつり
    'MARINE_ch' : 'UCCzUftO8KOVkV4wQG1vkUvg',   #宝鐘マリン
    'NAKIRI_ch' : 'UC7fk0CB07ly8oSl0aqKkqFg',   #百鬼あやめ
    'NOEL_ch' : 'UCdyqAaZDKHXg4Ahi7VENThQ',     #白銀ノエル
    'RUSHIA_ch' : 'UCl_gCybOJRIgOXw6Qb4qJzQ',   #潤羽るしあ
    'COCO_ch' : 'UCS9uQI-jC3DE0L4IpXyvr6w',     #桐生ココ
    'KANATA_ch' : 'UCZlDXzGoo7d44bwdNObFacg',   #天音かなた
    'MIO_ch' : 'UCp-5t9SrOQwXMU7iIjQfARg',      #大神ミオ
    'TOWA_ch' : 'UC1uv2Oq6kNxgATlCiez59hw',     #常闇トワ
    'WATAME_ch' : 'UCqm3BQLlJfvkTsX_hvm0UmA',   #角巻わため
    'LAMY_ch' : 'UCFKOVgVbGmX65RxO3EtH3iw',      #雪花ラミィ
    'NENE_ch' : 'UCAWSyEs_Io8MtpY3m-zqILA',     #桃鈴ねね
    'BOTAN_ch' : 'UCUKD-uaobj9jiqB-VXt71mA',      #獅白ぼたん
    'POLKA_ch' : 'UCK9V2B22uJYu3N7eR_BT9QA' ,      #尾丸ポルカ
    # 'ALOE_ch' : 'UCgZuwn-O7Szh9cAgHqJ6vjw',      #魔乃アロエ
    
    # イノナカミュージック
    'AZKI_ch' : 'UC0TXe_LYZ4scaW2XMyi5_kw',     #AZKi

    #ホロライブ　EN
    'CALLIOPE_ch' : 'UCL_qhgtOy0dy1Agp8vkySQg',    #森美声 モリ・カリオペ
    'KIARA_ch' : 'UCHsx4Hqa-1ORjQTh9TYDhww',    #小鳥遊キアラ
    'INANIS_ch' : 'UCMwGHR0BTZuLsmjY_NT5Pwg',    #一伊那尓栖 にのまえいなにす
    'GawrGura_ch' : 'UCoSrY_IQQVpmIRZ9Xf-y93g',    #がうる・くら
    'AMELIA_ch' : 'UCyl1z3jo3XHR1riLFKG5UAg',  #ワトソン・アメリア

    #ホロライブ ID
    'RISU_ch' : 'UCOyYb1c43VlX9rc_lT6NKQw',    #Ayunda Risu / アユンダ・リス
    'MOONA_ch' : 'UCP0BspO_AMEe3aQqqpo89Dg',      #Moona Hoshinova / ムーナ・ホシノヴァ
    'IOFI_ch' : 'UCAoy6rzhSf4ydcYjJw3WoVg',      #Airani Iofifteen / アイラニ・イオフィフティーン
    'OLLIE_ch' : 'UCYz_5n-uDuChHtLo7My1HnQ',     #Kureiji Ollie / クレイジー・オリー 
    'ANYA_ch' : 'UC727SQYUvx5pDDGQpTICNWg',       #Anya Melfissa / アーニャ・メルフィッサ
    'REINE_ch' : 'UChgTyjG-pdNvxxhdsXfHQ5Q',       #Pavolia Reine / パヴォリア・レイネ

    # 運営
    'HOLOLIVE_ch' : 'UCJFZiqLMntJufDCHc6bQixg',   #Hololive

    # friends他
    'SHIGURE_UI_ch' : 'UCt30jJgChL8qeT9VPadidSw', #時雨うい
    'TAMAKI_ch' : 'UC8NZiqKx6fsDT3AVcMiVFyA',     #佃煮のりお
    'SHIRAYUKI_ch' : 'UCC0i9nECi4Gz7TU63xZwodg',  #白雪みしろ
    'MILK_ch' : 'UCJCzy0Fyrm0UhIrGQ7tHpjg',       #愛宮みるく
    'YUZURU_ch' : 'UCle1cz6rcyH0a-xoMYwLlAg',     #姫咲ゆずる
    'HOOZUKI_ch' : 'UCLyTXfCZtl7dyhta9Jg3pZg',    #鬼灯わらべ
    'YUMENO_ch' : 'UCH11P1Hq4PXdznyw1Hhr3qw',     #夢乃リリス
    'KURUMIZAWA_ch' : 'UCxrmkJf_X1Yhte_a4devFzA', #胡桃澤もも
    'OUMAKI_ch' : 'UCBAeKqEIugv69Q2GIgcH7oA',     #逢魔きらら
}

Friend_Channel = {
    # friends他
    'SHIGURE_UI_ch' : 'UCt30jJgChL8qeT9VPadidSw', #時雨うい
    'TAMAKI_ch' : 'UC8NZiqKx6fsDT3AVcMiVFyA',     #佃煮のりお
    'SHIRAYUKI_ch' : 'UCC0i9nECi4Gz7TU63xZwodg',  #白雪みしろ
    'MILK_ch' : 'UCJCzy0Fyrm0UhIrGQ7tHpjg',       #愛宮みるく
    'YUZURU_ch' : 'UCle1cz6rcyH0a-xoMYwLlAg',     #姫咲ゆずる
    'HOOZUKI_ch' : 'UCLyTXfCZtl7dyhta9Jg3pZg',    #鬼灯わらべ
    'YUMENO_ch' : 'UCH11P1Hq4PXdznyw1Hhr3qw',     #夢乃リリス
    'KURUMIZAWA_ch' : 'UCxrmkJf_X1Yhte_a4devFzA', #胡桃澤もも
    'OUMAKI_ch' : 'UCBAeKqEIugv69Q2GIgcH7oA',     #逢魔きらら
    'NIA_ch' : 'UCIRzELGzTVUOARi3Gwf1-yg',        #看谷にぃあ
}


"""
ツイートメソッド
"""
def tweet(message):
    #ツイート内容
    TWEET_TEXT = message
    try :
        tweet_status = API.update_status(TWEET_TEXT)
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
def tweetWithIMG(message,img_url):
    #ツイート内容
    TWEET_TEXT = message
    try :
        # ↓添付したい画像のファイル名
        TRIM_IMG_DIR
        FILE_NAME = TRIM_IMG_DIR + img_url.split('/')[-2] + '.jpg'
        # FILE_NAME = LIVE_TMB_IMG_DIR + img_url.split('/')[-2] + '.jpg'
        tweet_status = API.update_with_media(filename=FILE_NAME, status=TWEET_TEXT)
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
def rssImgDownload(img_url:str, dir_path:str) ->Boolean:
    path = dir_path + img_url.split('/')[-2] + '.jpg'
    try:
        response = urllib.request.urlopen(url=img_url)
        with open(path, "wb") as f:
            f.write(response.read())
        print('Image Download OK ' + img_url)
    except Exception as err:
        error_catch(err)
        lineNotify("ダウンロードが失敗しました")
        return False
    else:
        return True



# """
# 画像のダウンロード
# """
# def rssImgDownload(img_url:str, dir_path:str) ->Boolean:
#     path = dir_path + img_url.split('/')[-2] + '.jpg'
#     for i in range(3):
#         try:
#             response = urllib.request.urlopen(url=img_url)
#             with open(path, "wb") as f:
#                 f.write(response.read())
#             print('Image Download OK ' + img_url)
#         except Exception as err:
#             error_catch(err)
#             time.sleep(5*i)
#             lineNotify("ダウンロード{}回失敗しました".format(i))
#         else:
#             break
#     else:
#         lineNotify("ダウンロードが失敗して停止しました。確認してください。")


"""
エラー内容出力
"""
def error_catch(error):
    """エラー処理
    """
    print("NG ", error)


"""
LINE
"""
def lineNotify(message):
    line_notify_token = os.environ.get('LINE_NOTIFY_TOKEN')
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    requests.post(line_notify_api, data=payload, headers=headers,)


"""
画像付きLINE通知
"""
def lineNotify_Img(message,imageUrl):
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


"""
動画IDからライブ開始時間または投稿時間を取得
liveStreamingDetails.actualStartTime　（ライブ開始時間）
liveStreamingDetails.scheduledStartTime　（ライブ開始予定時間）
liveStreamingDetails.actualEndTime　（ライブ終了時間）
liveStreamingDetails.concurrentViewers　（リアルタイム視聴者数）
liveStreamingDetails.activeLiveChatId　（チャット取得用ID）
"""
# def getLiveStartTime_JT(video_id:str) ->dict:
#     video_time_datas = {}
#     #　動画内容をリサーチメソッド
#     video_response = youtube.videos().list(
#         part = 'snippet,statistics,liveStreamingDetails',    #snippetがデフォ,liveStreamingDetailsにするとライブ開始予定時間が取得できる
#         id = video_id
#         ).execute()

#     video_result = video_response.get("items", [])
#     if video_result[0]["kind"] == "youtube#video":
#         if video_result[0].get('liveStreamingDetails',False):
#             video_time_datas['scheduledStartTime'] = video_result[0]['liveStreamingDetails'].get('scheduledStartTime',None), #ライブ開始予定時間
#             video_time_datas['actualStartTime'] = video_result[0]['liveStreamingDetails'].get('liveStreamingDetails',None), #ライブ開始時間
#             video_time_datas['actualEndTime'] = video_result[0]['liveStreamingDetails'].get('actualEndTime',None), #ライブ終了時間
#             video_time_datas['concurrentViewers'] = video_result[0]['liveStreamingDetails'].get('concurrentViewers',None), #リアルタイム視聴者数
#             return video_time_datas
#         else:
#             video_time_datas['publishedAt'] = video_result[0]['snippet']['publishedAt']   #投稿の場合はこちら,投稿された時間を取得
#             return  video_time_datas
#     else:
#         pprint('エラー発生')
#         return  video_time_datas
                

# ---------------------------------------Main---------------------------------------
# ----------------------------------------------------------------------------------
if __name__ == '__main__':
    while flag:
        # DBへ接続
        hTime = HoloDate()
        hSql = holo_sql.holo_sql()
        photo = PhotoFabrication(LIVE_TMB_IMG_DIR,TRIM_IMG_DIR)
        tw = tweet_components(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        print('########################################################################')

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


            # ホロライブ
            if ID == 'UChAnqc_AY5_I3Px5dig3X1Q': HoloName,live_tag = '戌神ころね', '#生神もんざえもん'
            elif ID == 'UC-hM6YJuNYVAmUWxeIr9FeA' : HoloName,live_tag ='さくらみこ', '#みこなま'
            elif ID == 'UCdn5BQ06XqgXoAxIhbqw5Rg' : HoloName,live_tag = '白上フブキ', '#フブキCh'
            elif ID == 'UC1opHUrw8rvnsadT-iGp7Cg' : HoloName,live_tag = '湊あくあ', '#湊あくあ生放送'
            elif ID == 'UC1DCedRgGHBdm81E1llLhOQ' : HoloName,live_tag = '兎田ぺこら', '#ぺこらいぶ'
            elif ID == 'UCFTLzh12_nrtzqBPsTCqenA' : HoloName,live_tag = 'アキ・ローゼンタール', '#アキびゅーわーるど'
            elif ID == 'UCp6993wxpyDPHUpavwDFqgg' : HoloName,live_tag = 'ときのそら', '#ときのそら生放送'
            elif ID == 'UCvzGlP9oQwU--Y0r9id_jnA' : HoloName,live_tag = '大空スバル', '#生スバル'
            elif ID == 'UCDqI2jOz0weumE8s7paEk6g' : HoloName,live_tag = 'ロボ子さん', '#ロボ子生放送'
            elif ID == 'UCXTpFs_3PqI41qX2d9tL2Rw' : HoloName,live_tag = '紫咲シオン', '#紫咲シオン'
            elif ID == 'UCvInZx9h3jC2JzsIzoOebWg' : HoloName,live_tag = '不知火フレア', '#フレアストリーム'
            elif ID == 'UCD8HOxPs4Xvsm8H0ZxXGiBw' : HoloName,live_tag = '夜空メル', '#メル生放送'
            elif ID == 'UCp3tgHXw_HI0QMk1K8qh3gQ' : HoloName,live_tag = '癒月ちょこ', '#癒月診療所' # サブ
            elif ID == 'UC1suqwovbL1kzsoaZgFZLKg' : HoloName,live_tag = '癒月ちょこ', '#癒月診療所'
            elif ID == 'UC1CfXB_kRs3C-zaeTG3oGyg' : HoloName,live_tag = '赤井はあと', '#はあちゃまなう'
            elif ID == 'UCvaTdHTWBGv3MKj3KVqJVCw' : HoloName,live_tag = '猫又おかゆ', '#生おかゆ'
            elif ID == 'UCa9Y57gfeY0Zro_noHRVrnw' : HoloName,live_tag = '姫森ルーナ', '#なのらいぶ'
            elif ID == 'UC5CwaMl1eIgY8h02uZw7u8A' : HoloName,live_tag = '星街すいせい', '#ほしまちすたじお'
            elif ID == 'UCQ0UDLQCjY0rmuxCDE38FGg' : HoloName,live_tag = '夏色まつり', '#夏まつch'
            elif ID == 'UCCzUftO8KOVkV4wQG1vkUvg' : HoloName,live_tag = '宝鐘マリン', '#マリン航海記'
            elif ID == 'UC7fk0CB07ly8oSl0aqKkqFg' : HoloName,live_tag = '百鬼あやめ', '#百鬼あやめch'
            elif ID == 'UCdyqAaZDKHXg4Ahi7VENThQ' : HoloName,live_tag = '白銀ノエル', '#ノエルーム'
            elif ID == 'UCl_gCybOJRIgOXw6Qb4qJzQ' : HoloName,live_tag = '潤羽るしあ', '#るしあらいぶ'
            elif ID == 'UCS9uQI-jC3DE0L4IpXyvr6w' : HoloName,live_tag = '桐生ココ', '#桐生ココ'
            elif ID == 'UCZlDXzGoo7d44bwdNObFacg' : HoloName,live_tag = '天音かなた', '#天界学園放送部'
            elif ID == 'UCp-5t9SrOQwXMU7iIjQfARg' : HoloName,live_tag = '大神ミオ', '#ミオかわいい'
            elif ID == 'UC1uv2Oq6kNxgATlCiez59hw' : HoloName,live_tag = '常闇トワ', '#トワイライブ'
            elif ID == 'UCqm3BQLlJfvkTsX_hvm0UmA' : HoloName,live_tag = '角巻わため', '#ドドドライブ'
            elif ID == 'UCFKOVgVbGmX65RxO3EtH3iw' : HoloName,live_tag = '雪花ラミィ', '#らみらいぶ'
            elif ID == 'UCAWSyEs_Io8MtpY3m-zqILA' : HoloName,live_tag = '桃鈴ねね', '#ねねいろらいぶ'
            elif ID == 'UCUKD-uaobj9jiqB-VXt71mA' : HoloName,live_tag = '獅白ぼたん', '#ぐうたらいぶ'
            elif ID == 'UCK9V2B22uJYu3N7eR_BT9QA' : HoloName,live_tag = '尾丸ポルカ', '#ポルカ公演中'
            # elif ID == 'UCgZuwn-O7Szh9cAgHqJ6vjw' : HoloName = '魔乃アロエ'
            # イノナカミュージック
            elif ID == 'UC0TXe_LYZ4scaW2XMyi5_kw' : HoloName,live_tag = 'AZKi', '#AZKi'
            #ホロライブ　EN
            elif ID == 'UCL_qhgtOy0dy1Agp8vkySQg' : HoloName,live_tag = '森美声', '#calliolive'
            elif ID == 'UCHsx4Hqa-1ORjQTh9TYDhww' : HoloName,live_tag = '小鳥遊キアラ', '#キアライブ'
            elif ID == 'UCMwGHR0BTZuLsmjY_NT5Pwg' : HoloName,live_tag = '一伊那尓栖', '#TAKOTIME'
            elif ID == 'UCoSrY_IQQVpmIRZ9Xf-y93g' : HoloName,live_tag = 'がうる・ぐら', '#gawrgura'
            elif ID == 'UCyl1z3jo3XHR1riLFKG5UAg' : HoloName,live_tag = 'ワトソン・アメリア', '#amelive'
            #ホロライブ ID
            elif ID == 'UCOyYb1c43VlX9rc_lT6NKQw' : HoloName,live_tag = 'アユンダ・リス', '#Risu_Live'
            elif ID == 'UCP0BspO_AMEe3aQqqpo89Dg' : HoloName,live_tag = 'ムーナ・ホシノヴァ', '#MoonA_Live'
            elif ID == 'UCAoy6rzhSf4ydcYjJw3WoVg' : HoloName,live_tag =  'アイラニ・イオフィフティーン', '#ioLYFE'
            elif ID == 'UCYz_5n-uDuChHtLo7My1HnQ' : HoloName,live_tag =  'クレイジー・オリー', '#Kureiji_Ollie'
            elif ID == 'UC727SQYUvx5pDDGQpTICNWg' : HoloName,live_tag =  'アーニャ・メルフィッサ', '#Anya_Melfissa'
            elif ID == 'UChgTyjG-pdNvxxhdsXfHQ5Q' : HoloName,live_tag =  'パヴォリア・レイネ', '#Pavolive'
            # 運営
            elif ID == 'UCJFZiqLMntJufDCHc6bQixg' : HoloName,live_tag = 'Hololive','#Hololive'
            # 絵師
            elif ID == 'UCt30jJgChL8qeT9VPadidSw' : HoloName,live_tag = 'しぐれうい', '#ういなま'
            # のりプロ
            elif ID == 'UC8NZiqKx6fsDT3AVcMiVFyA' : HoloName,live_tag = '犬山たまき', '#犬山たまき'
            elif ID == 'UCC0i9nECi4Gz7TU63xZwodg' : HoloName,live_tag = '白雪みしろ', '#白雪みしろ'
            elif ID == 'UCJCzy0Fyrm0UhIrGQ7tHpjg' : HoloName,live_tag = '愛宮みるく', '#愛宮みくる'
            elif ID == 'UCle1cz6rcyH0a-xoMYwLlAg' : HoloName,live_tag = '姫咲ゆずる', '#姫咲ゆずる'
            elif ID == 'UCLyTXfCZtl7dyhta9Jg3pZg' : HoloName,live_tag = '鬼灯わらべ', '#鬼灯わらべ'
            elif ID == 'UCH11P1Hq4PXdznyw1Hhr3qw' : HoloName,live_tag = '夢乃リリス', '#夢乃リリス'
            elif ID == 'UCxrmkJf_X1Yhte_a4devFzA' : HoloName,live_tag = '胡桃澤もも', '#胡桃澤もも'
            elif ID == 'UCBAeKqEIugv69Q2GIgcH7oA' : HoloName,live_tag = '逢魔きらら', '#逢魔きらら'
            elif ID == 'UCIRzELGzTVUOARi3Gwf1-yg' : HoloName,live_tag = '看谷にぃあ', '#看谷にぃあ'
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
                imgPro = ImageProcessing.ImageProcessing(entry['media_thumbnail'][0]['url'])
                if not result:
                # 同じIDがない(新規)
                    newdata = True
                    download_Result = rssImgDownload(entry['media_thumbnail'][0]['url'], LIVE_TMB_IMG_DIR)
                    if not download_Result:
                        newdata = False
                        imgPro = None
                        continue
                else:
                # 同じIDがある(既存)
                    time_lag = dt.now() - result[0]['notification_last_time_at']
                    # pprint(time_lag.total_seconds())
                    if time_lag.total_seconds() >= _TIMELAG:
                        download_Result = rssImgDownload(entry['media_thumbnail'][0]['url'], LIVE_TMB_TMP_DIR)
                        if not download_Result:
                            imgPro = None
                            continue
                        if not imgPro.imageComparison_hash():
                            # ---------------------------------
                            # img_name = entry['media_thumbnail'][0]['url'].split('/')[-2] + '.jpg'
                            # TOP_NAME = './live_temporary_image/'+ img_name
                            # BOTTOM_NAME = './Trim_Images/'+ img_name
                            # SAVE_NAME = './processed_Image/'+ img_name
                            # photo.imgTrim_Linking(TOP_NAME,BOTTOM_NAME,SAVE_NAME )
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
                    results = yApi.videoInfo(youtubeObject,entry['yt_videoid'])
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
                            ])  

                    # Line & twitter通知用(新規)--------------------------
                    # scheduled_at = convertToJST(scheduledStartTime)
                    getRss_News.append([ 
                        entry['title'],
                        entry['yt_videoid'],
                        entry['yt_channelid'],
                        entry['link'],
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
                        entry['link'],
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
                            message = '✨{}✨チャンネル\nタイトル更新✅\n{}\n\n配信予定時間:{}\n\n{}\n{}'.format(HoloName,live_tag,lines[4],lines[0],lines[3])
                            lineNotify_Img('\n{}チャンネル\nタイトル更新✅\n{}\n\n{}\n{}'.format(HoloName,lines[4],lines[0],lines[3]),lines[5])
                            photo.imgTrim(lines[5])
                            tweetWithIMG(message,lines[5])
                        elif lines[8:9] == ['image']:
                            del lines[8]
                            # hSql.updateImage(lines)
                            hSql.updateTitleYoutubeVideoTable(lines)
                            message = '✨{}チャンネル✨\n画像更新✅\n{}\n\n配信予定時間:{}\n\n{}\n{}'.format(HoloName,live_tag,lines[4],lines[0],lines[3])
                            lineNotify_Img('\n{}チャンネル\n画像更新✅\n{}\n\n{}\n{}'.format(HoloName,lines[4],lines[0],lines[3]),lines[5])
                            photo.imgTrim(lines[5])
                            tweetWithIMG(message,lines[5])
                        else :
                            del lines[8]
                            # hSql.update2Items(lines)
                            hSql.updateTitleYoutubeVideoTable(lines)
                            message = '✨{}チャンネル✨\nタイトル・画像更新✅\n{}\n\n配信予定時間:{}\n\n{}\n{}'.format(HoloName,live_tag,lines[4],lines[0],lines[3])
                            lineNotify_Img('\n{}チャンネル\nタイトル・画像更新✅\n{}\n\n{}\n{}'.format(HoloName,lines[4],lines[0],lines[3]),lines[5])
                            photo.imgTrim(lines[5])
                            tweetWithIMG(message,lines[5])
                for getRss_New in getRss_News:
                    message = '💖{}チャンネル 新着!🆕\n{}\n\n配信予定時間:{}\n\n{}\n{}'.format(HoloName, live_tag, getRss_New[6], getRss_New[0], getRss_New[3])
                    lineNotify_Img('\n{}チャンネル 新着!🆕\n配信予定時間:{}\n\n{}\n{}'.format(HoloName, getRss_New[6], getRss_New[0], getRss_New[3]), getRss_New[5])
                    photo.imgTrim(getRss_New[5])
                    tweetWithIMG(message,getRss_New[5])
                    # DBへ新規登録
                    # hSql.insert_FromRss_KeepWatchTable(HoloName,lines)
                    # hSql.insertKeepWatchTable(HoloName,lines)
                    # hSql.insertTable(HoloName,lines)
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

        time.sleep(180)
        # time.sleep(1800)
