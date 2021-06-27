import pandas as pd

from apiclient.discovery import build

import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime
from datetime import datetime as dt
import dateutil.parser

from holo_sql import holo_sql
from YoutubeAPI.YoutubeAPI import Youtube_API as yApi

from pprint import pprint



load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

_api_key = 'YOUTUBE_API_KEY_dev4'
_api_number = 1

API_KEY = os.environ.get(_api_key) #TODOこのファイル専用のAPIを取得しておく
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
# CHANNEL_ID = 
channels = [] #チャンネル情報を格納する配列
searches = [] #video idを格納する配列
videos = [] #各動画情報を格納する配列
BroadCasts = [] #LIVE用データ集計配列
lives = [] #LIVE用データ集計最終配列
nextPagetoken = None
nextpagetoken = None

youtube = build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
    )

csv_Files = [
    'MIO_ch.csv',     #大神ミオ
    'TOWA_ch.csv',    #常闇トワ
    'WATAME_ch.csv',  #角巻わため
]

csv_Files = [
    # ホロライブ
    'KORONE_ch.csv',    #戌神ころね
    'MIKO_ch.csv',     #さくらみこ
    'FUBUKI_ch.csv',   #白上フブキ
    'AQUA_ch.csv',     #湊あくあ
    'PEKORA_ch.csv',   #兎田ぺこら
    'AKIROSE_ch.csv',   #アキ・ローゼンタール
    'SORA_ch.csv',     #ときのそら
    'SUBARU_ch.csv',   #大空スバル
    'ROBOCO_ch.csv',   #ロボ子さん
    'SHION_ch.csv',   #紫咲シオン
    'FLARE_ch.csv',   #不知火フレア
    'MEL_ch.csv',     #夜空メル
    'CHOCO_ch.csv',   #癒月ちょこサブ
    'CHOCO_Main_ch.csv', #癒月ちょこメイン
    'HAATO_ch.csv',   #赤井はあと
    'OKAYU_ch.csv',   #猫又おかゆ
    'LUNA_ch.csv',    #姫森ルーナ
    'SUISEI_ch.csv',  #星街すいせい
    'MATSURI_ch.csv', #夏色まつり
    'MARINE_ch.csv',  #宝鐘マリン
    'NAKIRI_ch.csv',  #百鬼あやめ
    'NOEL_ch.csv',    #白銀ノエル
    'RUSHIA_ch.csv',  #潤羽るしあ
    'COCO_ch.csv',    #桐生ココ
    'KANATA_ch.csv',  #天音かなた
    'MIO_ch.csv',     #大神ミオ
    'TOWA_ch.csv',    #常闇トワ
    'WATAME_ch.csv',  #角巻わため
    'LAMY_ch.csv',     #雪花ラミィ
    'NENE_ch.csv',    #桃鈴ねね
    'BOTAN_ch.csv',     #獅白ぼたん
    'POLKA_ch.csv',     #尾丸ポルカ
    # 'ALOE_ch',        #魔乃アロエ
    
    # イノナカミュージック
    'AZKI_ch.csv',    #AZKi

    # #ホロライブ　EN
    'CALLIOPE_ch.csv',   #森美声 モリ・カリオペ
    'KIARA_ch.csv',   #小鳥遊キアラ
    'INANIS_ch.csv',   #一伊那尓栖 にのまえいなにす
    'GawrGura_ch.csv',   #がうる・くら
    'AMELIA_ch.csv', #ワトソン・アメリア

    # #ホロライブ ID
    'RISU_ch.csv',   #Ayunda Risu / アユンダ・リス
    'MOONA_ch.csv',     #Moona Hoshinova / ムーナ・ホシノヴァ
    'IOFIFTEEN_ch.csv',     #Airani Iofifteen / アイラニ・イオフィフティーン
    'OLLIE_ch.csv',      #Kureiji Ollie / クレイジー・オリー 
    'ANYA_ch.csv',      #Anya Melfissa / アーニャ・メルフィッサ
    'REINE_ch.csv',     #Pavolia Reine / パヴォリア・レイネ

    # # 運営
    'HOLOLIVE_ch.csv',  #Hololive

    # # 絵師他
    'SHIGURE_UI_ch.csv',#時雨うい
    'TAMAKI_ch.csv',    #佃煮のりお
    'SHIRAYUKI_ch.csv', #白雪みしろ
    'MILK_ch.csv',      #愛宮みるく
    'YUZURU_ch.csv',      #姫咲ゆずる
    'TAKUMA_ch.csv',    #熊谷タクマ
    'HOOZUKI_ch.csv',    #鬼灯わらべ
    'YUMENO_ch.csv',     #夢乃リリス
    'KURUMIZAWA_ch.csv', #胡桃澤もも
    'OUMAKI_ch.csv',     #逢魔きらら
    'NIA_ch.csv',        #看谷にぃあ

]

"""
更新時間を日本時間に変換
"""
def convertToJST(time):
    try:
        JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
        jst_timestamp = dateutil.parser.parse(time).astimezone(JST)
        updateJST = jst_timestamp.strftime('%Y/%m/%d %H:%M:%S')
        return updateJST
    except Exception as err:
        pprint(err)
        return None
"""
API交換
"""
def changeApiKey(_api_number:int):
    _api_number+=1
    _api_key = 'YOUTUBE_API_KEY_dev' + str(_api_number)
    return _api_key, _api_number

'''
channel IDからHolo Nameを決定
'''
def getHoloName(channel_ID:str)->str:
    HoloName = ''
    # ホロライブ
    if channel_ID =='UChAnqc_AY5_I3Px5dig3X1Q': HoloName = '戌神ころね'
    elif channel_ID == 'UC-hM6YJuNYVAmUWxeIr9FeA' : HoloName ='さくらみこ'
    elif channel_ID == 'UCdn5BQ06XqgXoAxIhbqw5Rg' : HoloName = '白上フブキ'
    elif channel_ID == 'UC1opHUrw8rvnsadT-iGp7Cg' : HoloName = '湊あくあ'
    elif channel_ID == 'UC1DCedRgGHBdm81E1llLhOQ' : HoloName = '兎田ぺこら'
    elif channel_ID == 'UCFTLzh12_nrtzqBPsTCqenA' : HoloName = 'アキ・ローゼンタール'
    elif channel_ID == 'UCp6993wxpyDPHUpavwDFqgg' : HoloName = 'ときのそら'
    elif channel_ID == 'UCvzGlP9oQwU--Y0r9id_jnA' : HoloName = '大空スバル'
    elif channel_ID == 'UCDqI2jOz0weumE8s7paEk6g' : HoloName = 'ロボ子さん'
    elif channel_ID == 'UCXTpFs_3PqI41qX2d9tL2Rw' : HoloName = '紫咲シオン'
    elif channel_ID == 'UCvInZx9h3jC2JzsIzoOebWg' : HoloName = '不知火フレア'
    elif channel_ID == 'UCD8HOxPs4Xvsm8H0ZxXGiBw' : HoloName = '夜空メル'
    elif channel_ID == 'UCp3tgHXw_HI0QMk1K8qh3gQ' : HoloName = '癒月ちょこ' #サブ
    elif channel_ID == 'UC1suqwovbL1kzsoaZgFZLKg' : HoloName = '癒月ちょこ' #メイン
    elif channel_ID == 'UC1CfXB_kRs3C-zaeTG3oGyg' : HoloName = '赤井はあと'
    elif channel_ID == 'UCvaTdHTWBGv3MKj3KVqJVCw' : HoloName = '猫又おかゆ'
    elif channel_ID == 'UCa9Y57gfeY0Zro_noHRVrnw' : HoloName = '姫森ルーナ'
    elif channel_ID == 'UC5CwaMl1eIgY8h02uZw7u8A' : HoloName = '星街すいせい'
    elif channel_ID == 'UCQ0UDLQCjY0rmuxCDE38FGg' : HoloName = '夏色まつり'
    elif channel_ID == 'UCCzUftO8KOVkV4wQG1vkUvg' : HoloName = '宝鐘マリン'
    elif channel_ID == 'UC7fk0CB07ly8oSl0aqKkqFg' : HoloName = '百鬼あやめ'
    elif channel_ID == 'UCdyqAaZDKHXg4Ahi7VENThQ' : HoloName = '白銀ノエル'
    elif channel_ID == 'UCl_gCybOJRIgOXw6Qb4qJzQ' : HoloName = '潤羽るしあ'
    elif channel_ID == 'UCS9uQI-jC3DE0L4IpXyvr6w' : HoloName = '桐生ココ'
    elif channel_ID == 'UCZlDXzGoo7d44bwdNObFacg' : HoloName = '天音かなた'
    elif channel_ID == 'UCp-5t9SrOQwXMU7iIjQfARg' : HoloName = '大神ミオ'
    elif channel_ID == 'UC1uv2Oq6kNxgATlCiez59hw' : HoloName = '常闇トワ'
    elif channel_ID == 'UCqm3BQLlJfvkTsX_hvm0UmA' : HoloName = '角巻わため'
    elif channel_ID == 'UCFKOVgVbGmX65RxO3EtH3iw' : HoloName = '雪花ラミィ'
    elif channel_ID == 'UCAWSyEs_Io8MtpY3m-zqILA' : HoloName = '桃鈴ねね'
    elif channel_ID == 'UCUKD-uaobj9jiqB-VXt71mA' : HoloName = '獅白ぼたん'
    elif channel_ID == 'UCK9V2B22uJYu3N7eR_BT9QA' : HoloName = '尾丸ポルカ'
    # elif channel_ID == 'UCgZuwn-O7Szh9cAgHqJ6vjw' : HoloName = '魔乃アロエ'
    # イノナカミュージック
    elif channel_ID == 'UC0TXe_LYZ4scaW2XMyi5_kw' : HoloName = 'AZKi'
    #ホロライブ　EN
    elif channel_ID == 'UCL_qhgtOy0dy1Agp8vkySQg' : HoloName = '森美声'
    elif channel_ID == 'UCHsx4Hqa-1ORjQTh9TYDhww' : HoloName = '小鳥遊キアラ'
    elif channel_ID == 'UCMwGHR0BTZuLsmjY_NT5Pwg' : HoloName = '一伊那尓栖'
    elif channel_ID == 'UCoSrY_IQQVpmIRZ9Xf-y93g' : HoloName = 'がうる・ぐら'
    elif channel_ID == 'UCyl1z3jo3XHR1riLFKG5UAg' : HoloName = 'ワトソン・アメリア'
    #ホロライブ ID
    elif channel_ID == 'UCOyYb1c43VlX9rc_lT6NKQw' : HoloName = 'アユンダ・リス'
    elif channel_ID == 'UCP0BspO_AMEe3aQqqpo89Dg' : HoloName = 'ムーナ・ホシノヴァ'
    elif channel_ID == 'UCAoy6rzhSf4ydcYjJw3WoVg' : HoloName =  'アイラニ・イオフィフティーン'
    # 運営
    elif channel_ID == 'UCJFZiqLMntJufDCHc6bQixg' : HoloName = 'Hololive'
    # 絵師
    elif channel_ID == 'UCt30jJgChL8qeT9VPadidSw' : HoloName = 'しぐれうい'
    # のりプロ
    elif channel_ID == 'UC8NZiqKx6fsDT3AVcMiVFyA' : HoloName = '犬山たまき'
    elif channel_ID == 'UCC0i9nECi4Gz7TU63xZwodg' : HoloName = '白雪みしろ'
    elif channel_ID == 'UCJCzy0Fyrm0UhIrGQ7tHpjg' : HoloName = '愛宮みるく'
    elif channel_ID == 'UCle1cz6rcyH0a-xoMYwLlAg' : HoloName = '姫咲ゆずる'
    return  HoloName


for i in csv_Files:
    pprint(i)
    csv_path = '/Users/nagaki/Documents/naga-sample-code/python/CSV_Relation/Holo_menber_video_list/{}'.format(i)
    # csv_path = './Holo_menber_video_list/{}'.format(i)
    df = pd.read_csv(csv_path,header=None)
    for video_id in df.values:
        # ------------------------
        HoloName = None
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
        # ------------------------
        # pprint(video_id)
        hSql = holo_sql()
        pprint(video_id[0].split('?v=')[-1])
        '''
        if :DBに同じvideoIDがない場合(新規)
        else :同じvideo idが存在する場合
        '''
        if not hSql.searchVideoIdYoutubeVideoTable(video_id[0].split('?v=')[-1]):
            yapi_result = yApi.videoInfo(youtube,video_id[0].split('?v=')[-1])
            video_info_results= yapi_result.get("items", [])
            for video_info_result in video_info_results:
                # hSql = holo_sql()
                # yApi = YoutubeAPI.YOUTUBE_API()
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
                    status = video_info_result['snippet']['thumbnails'].get('default' ,None)

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

                    HOLO_NAME = getHoloName(video_info_result["snippet"]["channelId"])

                    videos.append([
                        HOLO_NAME,
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
                        convertToJST( video_info_result["snippet"]["publishedAt"] ),
                        convertToJST(scheduledStartTime),
                        convertToJST(actualStartTime),
                        convertToJST(actualEndTime),
                        int(max_concurrent_viewers),
                        active_chat_id,
                        maxres_img,  #画像Max
                        standard_img ,   #画像Standard
                        high_img,    #画像Small
                        medium_img, #画像XSmall
                        default_img, #画像default
                        status
                        ])  

                    hSql.insertYoutubeVideoTable(videos)
                    hSql.dbClose()
                    hSql = None
                    videos = []








        else:
            yapi_result = yApi.videoInfo(youtube,video_id[0].split('?v=')[-1])
            video_info_results= yapi_result.get("items", [])
            for video_info_result in video_info_results:
                # hSql = holo_sql()
                # yApi = YoutubeAPI.YOUTUBE_API()
                if video_info_result["kind"] == "youtube#video":
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

                    # HOLO_NAME = getHoloName(video_info_result["snippet"]["channelId"])
                    videos.append([
                        video_id[0].split('?v=')[-1],
                        video_info_result["snippet"]["title"],
                        viewCount,
                        likeCount,
                        dislikeCount,
                        commentCount,
                        game_name,
                        tag,
                        maxres_img,  #画像Max
                        standard_img ,   #画像Standard
                        high_img,    #画像Small
                        medium_img, #画像XSmall
                        default_img, #画像default
                        ])  

                    hSql.updateScrapingYoutubeVideoTable(videos)
                    hSql.dbClose()
                    hSql = None
                    videos = []
# except Exception as err:
#     print(err)
    # _api_key, _api_number = changeApiKey()

# finally :

