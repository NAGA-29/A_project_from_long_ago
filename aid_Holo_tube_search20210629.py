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

import time
import datetime
from datetime import datetime as dt
import schedule

import os
import sys 
import os
from os.path import join, dirname
from dotenv import load_dotenv

from bs4 import BeautifulSoup
import requests

import pandas as pd
import numpy as np

from pprint import pprint

from apiclient.discovery import build
from apiclient.errors import HttpError
'''
Original Modules
'''
# sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
# import holo_sql
# from Components.lines import lines
'''
Original Modules
'''
# import mysql.connector as mydb
from model.holo_sql import holo_sql
from ImageProcessing import ImageProcessing
from YoutubeAPI.YoutubeAPI import Youtube_API as yApi
from ImageProcessing.photoFabrication import PhotoFabrication
from Components.holo_date import HoloDate
from Components.tweet import tweet_components
from Components.lines import lines
from Components import bitly

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
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

        self._api_key = 'YOUTUBE_API_KEY01'
        self._api_number = 1
        self.API_KEY = os.environ.get(self._api_key)
        self.YOUTUBE_API_SERVICE_NAME = 'youtube'
        self.YOUTUBE_API_VERSION = 'v3'
        # CHANNEL_ID = Channel[]

        # channels = [] #チャンネル情報を格納する配列
        # searches = [] #video idを格納する配列
        # videos = [] #各動画情報を格納する配列
        # BroadCasts = [] #LIVE用データ集計配列
        # lives = [] #LIVE用データ集計最終配列
        self.nextPagetoken = None
        self.nextpagetoken = None

        self.youtubeObject = build(
            self.YOUTUBE_API_SERVICE_NAME, 
            self.YOUTUBE_API_VERSION,
            developerKey=self.API_KEY
            )
        
        # 画像の保存先
        self.LIVE_TMB_IMG_DIR = os.environ.get('LIVE_TMB_IMG_DIR')
        self.LIVE_TMB_TMP_DIR = os.environ.get('LIVE_TMB_TMP_DIR')
        # トリミング加工済み画像保存先
        self.TRIM_IMG_DIR = os.environ.get('IMG_TRIM_DIR')

        #twitter本番アカウント
        self.CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
        self.CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
        self.ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
        self.ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

        self.Channel = {
            # ホロライブ
            # 'KORONE_ch' :'UChAnqc_AY5_I3Px5dig3X1Q',    #戌神ころね
            # 'MIKO_ch' : 'UC-hM6YJuNYVAmUWxeIr9FeA',     #さくらみこ
            # 'FUBUKI_ch' : 'UCdn5BQ06XqgXoAxIhbqw5Rg',   #白上フブキ
            # 'AQUA_ch' : 'UC1opHUrw8rvnsadT-iGp7Cg',     #湊あくあ
            'PEKORA_ch' : 'UC1DCedRgGHBdm81E1llLhOQ',   #兎田ぺこら
            # 'AKIROSE_ch' : 'UCFTLzh12_nrtzqBPsTCqenA',   #アキ・ローゼンタール
            # 'SORA_ch' : 'UCp6993wxpyDPHUpavwDFqgg',     #ときのそら
            # 'SUBARU_ch' : 'UCvzGlP9oQwU--Y0r9id_jnA',   #大空スバル
            # 'ROBOCO_ch' : 'UCDqI2jOz0weumE8s7paEk6g',   #ロボ子さん
            # 'SHION_ch' : 'UCXTpFs_3PqI41qX2d9tL2Rw',    #紫咲シオン
            # 'FLARE_ch' : 'UCvInZx9h3jC2JzsIzoOebWg',    #不知火フレア
            # 'MEL_ch' : 'UCD8HOxPs4Xvsm8H0ZxXGiBw',      #夜空メル
            # 'CHOCO_ch' : 'UCp3tgHXw_HI0QMk1K8qh3gQ',    #癒月ちょこ サブ
            # 'CHOCO_Main_ch' : 'UC1suqwovbL1kzsoaZgFZLKg', #癒月ちょこ メイン
            # 'HAATO_ch' : 'UC1CfXB_kRs3C-zaeTG3oGyg',    #赤井はあと
            # 'OKAYU_ch' : 'UCvaTdHTWBGv3MKj3KVqJVCw',    #猫又おかゆ
            # 'LUNA_ch' : 'UCa9Y57gfeY0Zro_noHRVrnw',     #姫森ルーナ
            # 'SUISEI_ch' : 'UC5CwaMl1eIgY8h02uZw7u8A',   #星街すいせい
            # 'MATSURI_ch' : 'UCQ0UDLQCjY0rmuxCDE38FGg',  #夏色まつり
            # 'MARINE_ch' : 'UCCzUftO8KOVkV4wQG1vkUvg',   #宝鐘マリン
            # 'NAKIRI_ch' : 'UC7fk0CB07ly8oSl0aqKkqFg',   #百鬼あやめ
            # 'NOEL_ch' : 'UCdyqAaZDKHXg4Ahi7VENThQ',     #白銀ノエル
            # 'RUSHIA_ch' : 'UCl_gCybOJRIgOXw6Qb4qJzQ',   #潤羽るしあ
            # 'COCO_ch' : 'UCS9uQI-jC3DE0L4IpXyvr6w',     #桐生ココ
            # 'KANATA_ch' : 'UCZlDXzGoo7d44bwdNObFacg',   #天音かなた
            # 'MIO_ch' : 'UCp-5t9SrOQwXMU7iIjQfARg',      #大神ミオ
            # 'TOWA_ch' : 'UC1uv2Oq6kNxgATlCiez59hw',     #常闇トワ
            # 'WATAME_ch' : 'UCqm3BQLlJfvkTsX_hvm0UmA',   #角巻わため
            # 'LAMY_ch' : 'UCFKOVgVbGmX65RxO3EtH3iw',      #雪花ラミィ
            # 'NENE_ch' : 'UCAWSyEs_Io8MtpY3m-zqILA',     #桃鈴ねね
            # 'BOTAN_ch' : 'UCUKD-uaobj9jiqB-VXt71mA',      #獅白ぼたん
            # # 'ALOE_ch' : 'UCgZuwn-O7Szh9cAgHqJ6vjw',      #魔乃アロエ
            # 'POLKA_ch' : 'UCK9V2B22uJYu3N7eR_BT9QA' ,      #尾丸ポルカ

            # # イノナカミュージック
            # 'AZKI_ch' : 'UC0TXe_LYZ4scaW2XMyi5_kw',     #AZKi

            # #ホロライブ　EN
            # 'CALLIOPE_ch' : 'UCL_qhgtOy0dy1Agp8vkySQg',    #森美声 モリ・カリオペ
            # 'KIARA_ch' : 'UCHsx4Hqa-1ORjQTh9TYDhww',    #小鳥遊キアラ
            # 'INANIS_ch' : 'UCMwGHR0BTZuLsmjY_NT5Pwg',    #一伊那尓栖 にのまえいなにす
            # 'GawrGura_ch' : 'UCoSrY_IQQVpmIRZ9Xf-y93g',    #がうる・くら
            # 'AMELIA_ch' : 'UCyl1z3jo3XHR1riLFKG5UAg',  #ワトソン・アメリア

            # #ホロライブ　ID
            # 'IOFIFTEEN_ch' : 'UCAoy6rzhSf4ydcYjJw3WoVg',    #Airani Iofifteen / アイラニ・イオフィフティーン
            # 'MOONA_ch' : 'UCP0BspO_AMEe3aQqqpo89Dg',    #Moona Hoshinova / ムーナ・ホシノヴァ
            # 'RISU_ch' : 'UCOyYb1c43VlX9rc_lT6NKQw',    #Ayunda Risu / アユンダ・リス

            # # 運営
            # 'HOLOLIVE_ch' : 'UCJFZiqLMntJufDCHc6bQixg',   #Hololive
        }

    def select_name_tag(self,ID):
        '''
        channel_idから誰のチャンネルか判定
        @param ID string チャンネルID
        @return HoloName string
        @return live_tag string
        '''
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
        print(HoloName)
        return HoloName,live_tag

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

    def main(self):
        hSql = holo_sql()
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
            res = requests.get(url)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")

            elems = soup.select('div#all > div.container > div.row > div > div.row > div > a')
            if elems:
                video_list = []
                for elem in elems:
                    # pprint(elem)
                    try:
                        url = elem.get("href").split('?v=')
                        video_list.append( url[1] )
                    except IndexError:
                        continue
            else:
                line.lineNotify('サイト構造が変更された可能性があります')

            pprint('##########################')
            for video_id in video_list:
                result = hSql.searchVideoIdFromYoutubeVideoTable_test(video_id)
                if result == False:
                # 同じIDがない(新規)
                    line.lineNotify('今までのより早く検出したドン！！！頑張ったドン！')

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
                        HoloName, live_tag = self.select_name_tag(video_info_result['snippet']["channelId"]) # channelIdから誰のチャンネルか判定

                        download_result = self.ImgDownload(line, high_img, self.LIVE_TMB_IMG_DIR)
                        if not download_result:
                            # 画像のダウンロードに失敗した場合は作業を中断し、スキップする
                            continue

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
                        get_news.append([ 
                            video_info_result["snippet"]["title"],
                            video_info_result["id"],
                            video_info_result["snippet"]["channelId"],
                            bitly.make_yURL(target_url),
                            updateJST,
                            high_img,
                            scheduledStartTimeJPT if scheduledStartTimeJPT else updateJST,
                            ])
                else:
                    # 同じIDがある(既存)
                    pprint(video_id)
                    pass
            time.sleep(1)

        for new in get_news:
            message = '新着!🆕\n{}チャンネル\n{}\n\n配信予定時間\n{}🇯🇵\n{}🇬🇧\n{}🇺🇸🗽\n\n{}\n{}'.format(HoloName, live_tag, new[6], hTime.convert_To_LON(new[6]), hTime.convert_To_NY(new[6]), new[0], new[3])
            line.lineNotify_Img('\n{}チャンネル 新着!🆕\n配信予定時間:{}\n\n{}\n{}'.format(HoloName, new[6], new[0], new[3]), new[5])
            photo.imgTrim(new[5])
            tw.tweetWithIMG(message, new[5], self.TRIM_IMG_DIR)

        for videos_data in videos_datas:
            if videos_data[22] == 'live' or videos_data[22] == 'upcoming':
                hSql.insertKeepWatchTable(videos_data)
            hSql.insertYoutubeVideoTable_R(videos_data)
            # dataDone.append(videos_data)
            pprint(videos_data)
            time.sleep(1)

if __name__ == '__main__':
    while True:
        y_c_m = YoutubeChannelMonitor(True)
        y_c_m.main()
        y_c_m = None
        time.sleep(20)