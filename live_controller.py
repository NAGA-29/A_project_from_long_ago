import tweepy
import requests

from pprint import pprint

import time
import datetime
from datetime import date, datetime as dt
import dateutil.parser

from apiclient.discovery import build
from apiclient.errors import HttpError

import tweepy

import os
from os.path import join, dirname
from dotenv import load_dotenv

import holo_sql
from YoutubeAPI.YoutubeAPI import Youtube_API as yApi
from Components.lines import lines
from Components.tweet import tweet_components
from Components.screenshot import ScreenShot
from ImageProcessing.photoFabrication import PhotoFabrication
from Components import bitly

'''
Initial Setting
'''
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

_API_KEY = 'YOUTUBE_API_KEY_dev2'
_api_number = 1

API_KEY = os.environ.get(_API_KEY)
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtubeObject = build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
    )

#twitter本番アカウント
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

# twitter本番アカウント My_NoriPro_project
CONSUMER_KEY_NORI = os.environ.get('CONSUMER_KEY_B')
CONSUMER_SECRET_NORI = os.environ.get('CONSUMER_SECRET_B')
ACCESS_TOKEN_NORI = os.environ.get('ACCESS_TOKEN_B')
ACCESS_TOKEN_SECRET_NORI = os.environ.get('ACCESS_TOKEN_SECRET_B')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(auth)

# 画像の読込先
LIVE_TMB_IMG_DIR = os.environ.get('LIVE_TMB_IMG_DIR')
# トリミング加工済み画像保存先
TRIM_IMG_DIR = os.environ.get('IMG_TRIM_DIR')
# スクリーンショット画像読み取り先
SCREENSHOT_FILE = os.environ.get('SCREENSHOT_DIR')

class LiveController:

    def __init__(self, belongs):
        self.Belongs = belongs

        if self.Belongs == 'hololive':
            self._VIEWER = 25000    # 通知トリガー 視聴者が25000人を超えたら通知する
            self._DIVISION_VIEWER = 30000   # 視聴者を20000で割った整数値を使用して通知判断に使用
            self._NOTIFICATION_SEC = 3600   # 通知基準 60分
            self._MANY_LIVE_NOTIFICATION_SEC = 3600     # 大量LIVE 通知基準 60分
            self.tweet = tweet_components(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            self.SCREENSHOT_URL = 'http://localhost/Hololive_Project/public/holo/live_screenshot/hololive'
            self.CHECK_LIVE_COUNT=12
        elif self.Belongs == 'noripro':
            self._VIEWER = 5000     # 通知トリガー 視聴者が5000人を超えたら通知する
            self._DIVISION_VIEWER = 10000   # 視聴者を10000で割った整数値を使用して通知判断に使用
            self._NOTIFICATION_SEC = 3600   # 通知基準 60分
            self._MANY_LIVE_NOTIFICATION_SEC = 3600     # 大量LIVE 通知基準 60分
            self.tweet = tweet_components(CONSUMER_KEY_NORI, CONSUMER_SECRET_NORI, ACCESS_TOKEN_NORI, ACCESS_TOKEN_SECRET_NORI)
            self.SCREENSHOT_URL = 'http://localhost/Hololive_Project/public/holo/live_screenshot/noripro'
            self.CHECK_LIVE_COUNT=5
            
    # ========================= メソッド ===========================
    """
    更新時間を日本時間に変換

    param time
    return updateJST:日本時間
    return None
    """
    def convertToJST(self, time):
        try:
            JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
            jst_timestamp = dateutil.parser.parse(time).astimezone(JST)
            updateJST = jst_timestamp.strftime('%Y/%m/%d %H:%M:%S')
            return updateJST
        except TypeError as err:
            # pprint('convertToJSTメソッド:{}'.format(err))
            return None

    """
    一定数のチャンネルがlive中の場合通知
    """
    def createLiveMessage(self, count:int) -> str:
        message = '現在のLIVE速報!!\n\n'
        message += '現在【 {} 】件の枠でLIVE中です🔥\n見逃さないよう注意してください!\n\n'.format(str(count))
        if self.Belongs == 'hololive':
            message += '#ホロライブ\n\n'
        elif self.Belongs == 'moripro':
            message += '#のりプロ #しぐれうい\n\n'
        message += '一覧はコチラ!!\n'
        return message

    """
    現在のlive中のチャンネルの総数を計算
    指定数以上の場合True
    """
    def liveCount(self, live_count: int)->bool:
        return True if live_count >= self.CHECK_LIVE_COUNT else False

    """
    特定のチャンネルIDかチェックする
    """
    def separate_ID(self, item:dict, live_table:dict)->bool:
        IDs = ['UC1DCedRgGHBdm81E1llLhOQ',]
        # for id in IDs:
        #     flag = False if channel_id == id else True
        if item['snippet']['channelId'] in IDs:
            if (dt.now() - live_table['notification_last_time_at']).seconds >= 7200:
                return True
            else:
                return False
        return True

    def getLiveTag(self, ID:str)->str:
        HoloName = ''
        live_tag = ''
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
        elif ID == 'UC1suqwovbL1kzsoaZgFZLKg' : HoloName,live_tag = '癒月ちょこ', '#癒月診療所'
        elif ID == 'UCp3tgHXw_HI0QMk1K8qh3gQ' : HoloName,live_tag = '癒月ちょこ', '#癒月診療所' #サブ
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
        elif ID == 'UCle1cz6rcyH0a-xoMYwLlAg' : HoloName,live_tag = '姫咲ゆずる', '姫咲ゆずる'
        elif ID == 'UCLyTXfCZtl7dyhta9Jg3pZg' : HoloName,live_tag = '鬼灯わらべ', '#鬼灯わらべ'
        elif ID == 'UCH11P1Hq4PXdznyw1Hhr3qw' : HoloName,live_tag = '夢乃リリス', '#夢乃リリス'
        elif ID == 'UCxrmkJf_X1Yhte_a4devFzA' : HoloName,live_tag = '胡桃澤もも', '#胡桃澤もも'
        elif ID == 'UCBAeKqEIugv69Q2GIgcH7oA' : HoloName,live_tag = '逢魔きらら', '#逢魔きらら'
        elif ID == 'UCIRzELGzTVUOARi3Gwf1-yg' : HoloName,live_tag = '看谷にぃあ', '#看谷にぃあ'
        return HoloName, live_tag

    def live(self, notice_times:dict):
        photo = PhotoFabrication(LIVE_TMB_IMG_DIR,TRIM_IMG_DIR)
        hSql = holo_sql.holo_sql()
        screen = ScreenShot(headless=True)
        yt = yApi()
        # line = lines()
        dt_now = dt.now()
        LiveTable = hSql.selectAllLiveTable(self.Belongs)

        # LIVEが複数の場合通知-------
        count = 0 if LiveTable == False else len(LiveTable)
        if self.liveCount(count):
            if ( dt_now - notice_times[self.Belongs] ).total_seconds() >= self._MANY_LIVE_NOTIFICATION_SEC:
                screen.screenshot(self.SCREENSHOT_URL) # 指定URLのスクリーンショット
                time.sleep(5)
                self.tweet.tweet_With_Image(self.createLiveMessage(count), SCREENSHOT_FILE+'screenshot.png')
                notice_times[self.Belongs] = dt_now
                print(notice_times)
        # END LIVEが複数の場合通知-------

        if LiveTable:
            for live_table  in LiveTable:
                update_data = []
                tubeTabelOne = hSql.selectVideoIdYoutubeVideoTable(live_table['video_id'])
                api_result = yt.videoInfo(youtubeObject,live_table['video_id'])
                items = api_result.get("items", None)
                if items:
                    for item in items:
                        if item["kind"] == "youtube#video":
                            live_title = item["snippet"]["title"]
                            '''
                            scheduledStartTime ライブ開始予定時間(太平洋標準時)
                            actualStartTime ライブ開始時間
                            actualEndTime ライブ終了時間
                            scheduledStartTimeJPT  ライブ開始予定時間(日本時間変換済)
                            status 状態:upcoming,live,none
                            '''
                            if item.get('liveStreamingDetails',None):
                                scheduledStartTime = item['liveStreamingDetails'].get('scheduledStartTime',None) #ライブ開始予定時間
                                actualStartTime = item['liveStreamingDetails'].get('actualStartTime',None) #ライブ開始時間
                                actualEndTime = item['liveStreamingDetails'].get('actualEndTime',None) #ライブ終了時間
                                concurrentViewers = item['liveStreamingDetails'].get('concurrentViewers',None) #live視聴者
                                activeLiveChatId = item['liveStreamingDetails'].get('activeLiveChatId',None) #ライブchatID
                                status = item["snippet"]["liveBroadcastContent"]
                                        
                                update_data.append([
                                    item['id'],
                                    self.convertToJST(scheduledStartTime),
                                    self.convertToJST(actualStartTime),
                                    self.convertToJST(actualEndTime),
                                    concurrentViewers,
                                    activeLiveChatId,
                                    status,
                                    live_title,
                                ])
                                # LIVE中対応
                                if status == 'live':
                                    # 通常LIVE
                                    if not concurrentViewers == None:
                                        if int(concurrentViewers) > tubeTabelOne[0]['max_concurrent_viewers']:
                                            if hSql.updateMAXViewersYoutubeVideoTable(update_data):
                                                hSql.updateViewersLiveTable(update_data)
                                        else:
                                            hSql.updateViewersLiveTable(update_data)
                                            hSql.updateTitleLiveTable(update_data)
                                        HoloName, tag = self.getLiveTag(item['snippet']['channelId'])
                                        if int(concurrentViewers) >= self._VIEWER:
                                            compared_point = (int(concurrentViewers)//self._DIVISION_VIEWER)
                                            if self.separate_ID(item, live_table):
                                                if (dt_now - live_table['notification_last_time_at']).seconds >= self._NOTIFICATION_SEC or compared_point > live_table['compared_point']:
                                                    '''
                                                    前回の通知時間から指定時間(_NOTIFICATION_SEC)以上経っている
                                                    または視聴者が3万人増える
                                                    いずれかの条件をクリアした場合に通知する
                                                    '''
                                                    message = '✨{}✨\n{}\n\n{} \n\n現在ホットなLIVE!!🔥{}人が視聴中!!👀\n{}'.format(live_table['holo_name'], tag, live_title, concurrentViewers,bitly.make_yURL(live_table['channel_url']) )
                                                    '''
                                                    DBに対応画像があるか確認
                                                    live_table[11] : 最大サイズ画像URL
                                                    live_table[12] : デフォルト画像URL
                                                    '''
                                                    if compared_point > live_table['compared_point']:
                                                        hSql.updateNotificationLiveTable(item['id'], dt_now, compared_point)
                                                    else:
                                                        hSql.updateNotificationLiveTable(item['id'], dt_now, live_table['compared_point'])
                                                    # 画像加工とツイート
                                                    img_path = (live_table['image_L'] if live_table['image_L'] else live_table['image_default'])
                                                    photo.imgTrim(img_path)
                                                    self.tweet.tweetWithIMG(message,img_path,TRIM_IMG_DIR)
                                                    print(message)
                                                
                                        print('<<{}>> {}  LIVE中!!! {}人が視聴中!!'.format(live_table['holo_name'], tubeTabelOne[0]['title'], concurrentViewers))
                                    # メンバー限定配信(人数とチャット欄が取得できない)
                                    else:
                                        print('<<{}>> {}  LIVE中!!!'.format(live_table['holo_name'], tubeTabelOne[0]['title']))
                                    hSql.updateTitleLiveTable(update_data)
                                # none対応(LIVE終了,BANなど)
                                elif status == 'none':
                                    if hSql.updateTimeYoutubeVideoTable(update_data):
                                        hSql.deletelLiveTable(item['id'])
                                        print('LIVEが終了しています')
                                # upcoming対応 この状態に変わることがあるのかわからない
                                else :
                                    print('upcomingに変わったようだ')
                else:
                    hSql.deletelLiveTable(live_table['video_id'])

        hSql.dbClose()
        hSql = None
        photo = None
        yt = None
        # tweet = None
        line = None
        return notice_times

def main(notice_times:dict):
    Live = LiveController('hololive')
    notice_times = Live.live(notice_times)
    Live=None
    Live = LiveController('noripro')
    notice_times = Live.live(notice_times)
    Live=None
    return notice_times

if __name__ == '__main__':
    last_tweet_time = dt.strptime('2010-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    notice_times = {
        'hololive': last_tweet_time,
        'noripro' : last_tweet_time,
    }
    while True:
        notice_times = main(notice_times)
        time.sleep(180)
