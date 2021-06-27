import pandas as pd
from apiclient.discovery import build
from apiclient.errors import HttpError
from pprint import pprint
import os
from os.path import join, dirname
from dotenv import load_dotenv
# import holo_sql

import time


class Youtube_API:
    load_dotenv(verbose=True)
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

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
        'CHOCO_ch' : 'UCp3tgHXw_HI0QMk1K8qh3gQ',    #癒月ちょこ
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
        'ALOE_ch' : 'UCgZuwn-O7Szh9cAgHqJ6vjw',      #魔乃アロエ
        'POLKA_ch' : 'UCK9V2B22uJYu3N7eR_BT9QA' ,      #尾丸ポルカ

        # イノナカミュージック
        'AZKI_ch' : 'UC0TXe_LYZ4scaW2XMyi5_kw',     #AZKi

        # 運営
        'HOLOLIVE_ch' : 'UCJFZiqLMntJufDCHc6bQixg',   #Hololive

        # 絵師他
        'SHIGURE_UI_ch' : 'UCt30jJgChL8qeT9VPadidSw', #しぐれうい
        'TAMAKI_ch' : 'UC8NZiqKx6fsDT3AVcMiVFyA',     #佃煮のりお
        'SHIRAYUKI_ch' : 'UCC0i9nECi4Gz7TU63xZwodg',  #白雪みしろ
        'MILK_ch' : 'UCJCzy0Fyrm0UhIrGQ7tHpjg',       #愛宮みるく
    }



    API_KEY = os.environ.get('YOUTUBE_API_KEY01')
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    CHANNEL_ID = Channel['']
    
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

    """
        エラー処理
    """
    def error_catch(error):
        print("NG ", error)


    """
        チャンネルの内容を返す
        @param youtubeObject 
        @param CHANNEL_ID
        @return dict
    """
    def channelInfo(youtubeObject,CHANNEL_ID):
        return  youtubeObject.channels().list(part = 'snippet,statistics',id = CHANNEL_ID).execute()   


    """
        特定チャンネル内の動画一覧を取得(一度に最高500件まで)
        @param youtubeObject 
        @param video_ID
        @return dict
    """
    def videoInfo(youtubeObject,CHANNEL_ID,NextPageToken):
        # チャンネル内の動画をリサーチメソッド
        return youtubeObject.search().list(
                part = "snippet",
                channelId = CHANNEL_ID,
                type = 'video',
                # eventType = 'completed',    # 'completed':完了したブロードキャストのみ　'live':アクティブなブロードキャストのみ  'upcoming':今後配信予定のブロードキャスト、live中を取得可能
                maxResults = 50,
                order = "date", #日付順にソート
                pageToken = NextPageToken #再帰的に指定
                ).execute()  


    """
        動画の内容を返す
        @param youtubeObject 
        @param video_ID
        @return dict
    """
    def videoInfo(youtubeObject,video_ID):
        return youtubeObject.videos().list(
                part = 'snippet,statistics,liveStreamingDetails',    #snippetがデフォ,liveStreamingDetailsにするとライブ開始予定時間が取得できる
                id = video_ID
                ).execute()


    """
        動画IDからライブ開始時間または投稿時間を取得
        liveStreamingDetails.actualStartTime　（ライブ開始時間）
        liveStreamingDetails.scheduledStartTime　（ライブ開始予定時間）
        liveStreamingDetails.actualEndTime　（ライブ終了時間）
        liveStreamingDetails.concurrentViewers　（リアルタイム視聴者数）
        liveStreamingDetails.activeLiveChatId　（チャット取得用ID）
    """
    def getLiveStartTime_JT(video_id:str) ->dict:
        video_time_datas = {}
        #　動画内容をリサーチメソッド
        video_response = youtube.videos().list(
            part = 'snippet,statistics,liveStreamingDetails',    #snippetがデフォ,liveStreamingDetailsにするとライブ開始予定時間が取得できる
            id = video_id
            ).execute()

        video_result = video_response.get("items", [])
        if video_result[0]["kind"] == "youtube#video":
            if video_result[0].get('liveStreamingDetails',False):
                video_time_datas['scheduledStartTime'] = video_result[0]['liveStreamingDetails'].get('scheduledStartTime',None), #ライブ開始予定時間
                video_time_datas['actualStartTime'] = video_result[0]['liveStreamingDetails'].get('liveStreamingDetails',None), #ライブ開始時間
                video_time_datas['actualEndTime'] = video_result[0]['liveStreamingDetails'].get('actualEndTime',None), #ライブ終了時間
                video_time_datas['concurrentViewers'] = video_result[0]['liveStreamingDetails'].get('concurrentViewers',None), #リアルタイム視聴者数
                return video_time_datas
            else:
                video_time_datas['publishedAt'] = video_result[0]['snippet']['publishedAt']   #投稿の場合はこちら,投稿された時間を取得
                return  video_time_datas
        else:
            pprint('エラー発生')
            return  video_time_datas


    # # チャンネルサーチメソッド ------------------------------------------------------------
    # チャンネルの内容が返ってくる
    channel_response = youtube.channels().list(
        part = 'snippet,statistics',
        id = CHANNEL_ID
        ).execute()
    pprint(channel_response)


    # # チャンネル情報を収集----------------------------------------------------------------
    # 
    # for channel_result in channel_response.get("items", []):
    #     if channel_result["kind"] == "youtube#channel":
    #         channels.append(
    #             [channel_result["snippet"]["title"],
    #             channel_result["statistics"]["subscriberCount"],
    #             channel_result["statistics"]["videoCount"],
    #             channel_result["snippet"]["publishedAt"]]
    #             )

    while True:
    # for channel_key,channel_value in Channel.items():
        if nextPagetoken != None:
            nextpagetoken = nextPagetoken
        
        # チャンネル内の動画をリサーチメソッド
        search_response = youtube.search().list(
            part = "snippet",
            channelId = CHANNEL_ID,
            type = 'video',
            # eventType = 'completed',    # 'completed':完了したブロードキャストのみ　'live':アクティブなブロードキャストのみ  'upcoming':今後配信予定のブロードキャスト、live中を取得可能
            maxResults = 50,
            order = "date", #日付順にソート
            pageToken = nextpagetoken #再帰的に指定
            ).execute()  

        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                searches.append(search_result["id"]["videoId"])

                # 取得したデータ内にLIVE中またはLIVE予定のデータがあれば追加で取得
                if search_result['snippet']['liveBroadcastContent'] == 'live' or 'upcoming':
                    BroadCasts.append(search_result["id"]["videoId"])
        try:
            nextPagetoken =  search_response["nextPageToken"]

        except:
            break
    pprint(len(searches))
    #　動画内容をリサーチメソッド----------------------------------------------------------------
    # searches.append('Fmn3VdPdzR4')
    for result in searches:
        #　動画内容をリサーチメソッド
        video_response = youtube.videos().list(
            part = 'snippet,statistics,liveStreamingDetails',          #snippetがデフォ,liveStreamingDetailsにするとライブ開始予定時間が取得できる
            id = result
            ).execute()

        for video_result in video_response.get("items", []):
            if video_result["kind"] == "youtube#video":
                target_url = 'https://www.youtube.com/watch?v={}'.format(video_result['id'])

                maxres_img = video_result['snippet']['thumbnails'].get('maxres',None) 
                standard_img = video_result['snippet']['thumbnails'].get('standard',None)
                high_img = video_result['snippet']['thumbnails'].get('high' ,None) 
                medium_img = video_result['snippet']['thumbnails'].get('medium' ,None)
                default_img = video_result['snippet']['thumbnails'].get('default' ,None)

                if maxres_img : #画像Max
                    maxres_img = video_result['snippet']['thumbnails']['maxres']['url']
                if standard_img :  #画像Standard
                    standard_img = standard_img = video_result['snippet']['thumbnails']['standard']['url']
                if high_img :   #画像Small
                    high_img = video_result['snippet']['thumbnails']['high']['url']
                if medium_img :   #画像XSmall
                    medium_img = video_result['snippet']['thumbnails']['medium']['url']
                if default_img :   #画像default
                    default_img = video_result['snippet']['thumbnails']['medium']['url']

                videos.append(
                    [video_result["snippet"]["title"],
                    video_result["statistics"]["viewCount"],
                    video_result["statistics"]["likeCount"],
                    video_result["statistics"]["dislikeCount"],
                    video_result["statistics"]["commentCount"],
                    video_result["snippet"]["publishedAt"],
                    target_url,
                    maxres_img,  #画像Max
                    standard_img ,   #画像Standard
                    high_img,    #画像Small
                    medium_img, #画像XSmall
                    default_img  #画像default
                    ])  


    # # ブロードキャスト用 ----------------------------------------------------------------------
    # if BroadCasts:
    #     for broadcasts in BroadCasts:
    #         livebroad_responce = youtube.liveBroadcasts().list(
    #             part = "snippet,contentDetails,status",
    #             id = broadcasts
    #         ).execute()

    #         for livebroad_result in livebroad_responce.get("items", []):
    #             if livebroad_result["kind"] == "youtube#liveBroadcast":
    #                 live_url = 'https://www.youtube.com/watch?v={}'.format(livebroad_result['id'])
    #                 lives.append(
    #                     livebroad_result['snippet']['title'],   #タイトル
    #                     live_url,   #LIVE URL
    #                     livebroad_result['status']['lifeCycleStatus'],      #ブロードキャストのステータス 
    #                     livebroad_result['id'], #動画ID
    #                     livebroad_result['snippet']['channelId'],   #チャンネルID
    #                     livebroad_result['snippet']['thumbnails']['maxres']['url'],  #画像Max
    #                     livebroad_result['snippet']['thumbnails']['standard']['url'],   #画像Standard
    #                     livebroad_result['snippet']['thumbnails']['high']['url'],    #画像Small
    #                     livebroad_result['snippet']['scheduledStartTime'],  #開始予定時間
    #                     livebroad_result['snippet']['scheduledEndTime'],    #終了予定時間
    #                     livebroad_result['snippet']['actualStartTime'],  #開始時間
    #                     livebroad_result['snippet']['actualEndTime'],    #終了時間
    #                 )
    #                 pprint(livebroad_responce)
    #                     #['status']['lifeCycleStatus']について
    #                     # complete : 放送が終了しました。
    #                     # created : ブロードキャストの設定が不完全であるため、liveまたはtestingステータスに移行する準備ができていませんが、作成されており、それ以外の場合は有効です。
    #                     # live : ブロードキャストがアクティブです。
    #                     # liveStarting : ブロードキャストがliveステータスに移行している最中です。
    #                     # ready : ブロードキャスト設定が完了し、ブロードキャストがliveまたはtestingステータスに移行できるようになりました。
    #                     # revoked : このブロードキャストは管理アクションによって削除されました。
    #                     # testStarting : ブロードキャストがtestingステータスに移行している最中です。
    #                     # testing : ブロードキャストはパートナーにのみ表示されます。
    #  ------------------------------------------------------------------------------------------------------------------------------------------


    # ホロライブ
    if CHANNEL_ID == 'UChAnqc_AY5_I3Px5dig3X1Q': HoloName = 'KORONE_ch'
    elif CHANNEL_ID == 'UC-hM6YJuNYVAmUWxeIr9FeA' : HoloName ='MIKO_ch'
    elif CHANNEL_ID== 'UCdn5BQ06XqgXoAxIhbqw5Rg' : HoloName = 'FUBUKI_ch'
    elif CHANNEL_ID == 'UC1opHUrw8rvnsadT-iGp7Cg' : HoloName = 'AQUA_ch'
    elif CHANNEL_ID == 'UC1DCedRgGHBdm81E1llLhOQ' : HoloName = 'PEKORA_ch' 
    elif CHANNEL_ID == 'UCFTLzh12_nrtzqBPsTCqenA' : HoloName = 'AKIROSE_ch'
    elif CHANNEL_ID == 'UCp6993wxpyDPHUpavwDFqgg' : HoloName = 'SORA_ch'
    elif CHANNEL_ID == 'UCvzGlP9oQwU--Y0r9id_jnA' : HoloName = 'SUBARU_ch'
    elif CHANNEL_ID == 'UCDqI2jOz0weumE8s7paEk6g' : HoloName = 'ROBOCO_ch'
    elif CHANNEL_ID == 'UCXTpFs_3PqI41qX2d9tL2Rw' : HoloName = 'SHION_ch'
    elif CHANNEL_ID == 'UCvInZx9h3jC2JzsIzoOebWg' : HoloName = 'FLARE_ch'
    elif CHANNEL_ID == 'UCD8HOxPs4Xvsm8H0ZxXGiBw' : HoloName = 'MEL_ch'
    elif CHANNEL_ID == 'UCp3tgHXw_HI0QMk1K8qh3gQ' : HoloName = 'CHOCO_ch'
    elif CHANNEL_ID == 'UC1CfXB_kRs3C-zaeTG3oGyg' : HoloName = 'HAATO_ch'
    elif CHANNEL_ID == 'UCvaTdHTWBGv3MKj3KVqJVCw' : HoloName = 'OKAYU_ch'
    elif CHANNEL_ID == 'UCa9Y57gfeY0Zro_noHRVrnw' : HoloName = 'LUNA_ch' 
    elif CHANNEL_ID == 'UC5CwaMl1eIgY8h02uZw7u8A' : HoloName = 'SUISEI_ch'
    elif CHANNEL_ID == 'UCQ0UDLQCjY0rmuxCDE38FGg' : HoloName = 'MATSURI_ch'
    elif CHANNEL_ID == 'UCCzUftO8KOVkV4wQG1vkUvg' : HoloName = 'MARINE_ch' 
    elif CHANNEL_ID == 'UC7fk0CB07ly8oSl0aqKkqFg' : HoloName = 'NAKIRI_ch'
    elif CHANNEL_ID == 'UCdyqAaZDKHXg4Ahi7VENThQ' : HoloName = 'NOEL_ch'
    elif CHANNEL_ID == 'UCl_gCybOJRIgOXw6Qb4qJzQ' : HoloName = 'RUSHIA_ch'
    elif CHANNEL_ID == 'UCS9uQI-jC3DE0L4IpXyvr6w' : HoloName = 'COCO_ch'
    elif CHANNEL_ID == 'UCZlDXzGoo7d44bwdNObFacg' : HoloName = 'KANATA_ch'
    elif CHANNEL_ID == 'UCp-5t9SrOQwXMU7iIjQfARg' : HoloName = 'MIO_ch'
    elif CHANNEL_ID == 'UC1uv2Oq6kNxgATlCiez59hw' : HoloName = 'TOWA_ch'
    elif CHANNEL_ID == 'UCqm3BQLlJfvkTsX_hvm0UmA' : HoloName = 'WATAME_ch'
    elif CHANNEL_ID == 'UCFKOVgVbGmX65RxO3EtH3iw' : HoloName = 'LAMY_ch'
    elif CHANNEL_ID == 'UCAWSyEs_Io8MtpY3m-zqILA' : HoloName = 'NENE_ch'
    elif CHANNEL_ID == 'UCUKD-uaobj9jiqB-VXt71mA' : HoloName = 'BOTAN_ch'
    elif CHANNEL_ID == 'UCK9V2B22uJYu3N7eR_BT9QA' : HoloName = 'POLKA_ch'
    # elif CHANNEL_ID == 'UCgZuwn-O7Szh9cAgHqJ6vjw' : HoloName = '魔乃アロエ'
    # イノナカミュージック
    elif CHANNEL_ID == 'UC0TXe_LYZ4scaW2XMyi5_kw' : HoloName = 'AZKI_ch'
    # 運営
    elif CHANNEL_ID == 'UCJFZiqLMntJufDCHc6bQixg' : HoloName = 'Hololive'
    # 絵師
    elif CHANNEL_ID == 'UCt30jJgChL8qeT9VPadidSw' : HoloName = 'SHIGURE_UI_ch'
    # のりプロ
    elif CHANNEL_ID == 'UC8NZiqKx6fsDT3AVcMiVFyA' : HoloName = 'TAMAKI_ch'
    elif CHANNEL_ID == 'UCC0i9nECi4Gz7TU63xZwodg' : HoloName = 'SHIRAYUKI_ch'
    elif CHANNEL_ID == 'UCJCzy0Fyrm0UhIrGQ7tHpjg' : HoloName = 'MILK_ch'


    # # live一覧CSV
    # # filename = '{}videos.csv'.format()
    # lives_report = pd.DataFrame(lives, columns=['title','LIVE_URL','Status','ID','channelID','imageL','imageM','imageS','Scheduled_start_date','Scheduled_end_date','start_date','end_date'])
    # lives_report.to_csv("lives_report.csv", index=None)
    # video一覧CSV
    file_name = '{}_videos_report.csv'.format(HoloName)
    videos_report = pd.DataFrame(videos, columns=['title', 'viewCount', 'likeCount', 'dislikeCount', 'commentCount', 'publishedAt','URL','imageL','imageM','imageS','imageXS','image_defautl'])
    videos_report.to_csv(file_name, index=None)
    # # channel用CSV
    # channel_report = pd.DataFrame(channels, columns=['title', 'subscriberCount', 'videoCount', 'publishedAt'])
    # channel_report.to_csv("channels_report.csv", index=None)


    # /Users/nagaki/Documents/naga-sample-code/python/youtubeAPI/Hololive-Project-53189f1c6d5f.json
    # export GOOGLE_APPLICATION_CREDENTIALS="/Users/nagaki/Documents/naga-sample-code/python/youtubeAPI/Hololive-Project-53189f1c6d5f.json"
