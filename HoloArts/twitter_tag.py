# 
#ツイッターからタグを検索して画像を保存する
# 
import tweepy
import csv
import pandas as pd
import pytz
import copy
import urllib.request, urllib.error

import datetime
from dateutil.parser import parse
from datetime import datetime as dt
import dateutil.parser
import schedule

import os
from os.path import join, dirname
from dotenv import load_dotenv

import holo_sql

from pprint import pprint


load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

##twitterテストアカウント
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY , CONSUMER_SECRET )
auth.set_access_token(ACCESS_TOKEN , ACCESS_TOKEN_SECRET)
API = tweepy.API(auth)

_FAVORITE_COUNT = 1000


# 画像の保存先
IMG_DIR = './images/'
# -------------------- メソッド -----------------------
# 画像のダウンロード
def download(url):
    url_orig = '%s:orig' % url
    path = IMG_DIR + url.split('/')[-1]
    try:
        response = urllib.request.urlopen(url=url_orig)
        with open(path, "wb") as f:
            f.write(response.read())
        print('Image Download OK ' + url)
    except Exception as e:
        error_catch(e)

# 動画のダウンロード
def downloadVideo(video_url):
    remake_name = video_url.split('/')[-1]
    path = IMG_DIR + remake_name.split('?')[0]
    try:
        response = urllib.request.urlopen(url=video_url)
        with open(path, "wb") as f:
            f.write(response.read())
        print('Video Download OK ' + video_url)
    except Exception as e:
        error_catch(e)

def error_catch(error):
    """エラー処理
    """
    print("NG ", error)


Holo_tags = {
    'A-CHAN_tg' : ['#絵ーちゃん'],       #えーちゃん
    'MIKO_tg' : ['#miko_Art'],       #さくらみこ
    'KORONE_tg' : ['#できたてころね'],       #戌神ころね
    'KANATA_tg' : ['#かなたーと'],       #天音かなた
    'OKAYU_tg' : ['#絵かゆ'],       #猫又おかゆ
    'AKIROSE_tg' : ['#アロ絵'],       #アキロゼ
    # 'AKIROSE_tg' : ['#アロ絵','#スケべなアロ絵'],       #アキロゼ
    'MIO_tg' : ['#みおーん絵'],     #大神みお
    'SORA_tg' : ['#soraArt'],      #ときのそら
    'ROBOCO_tg' : ['#ロボ子Art'],        #ロボ子
    'SUISEI_tg' : ['#ほしまちぎゃらりー'],     #星街すいせい
    'MEL_tg' : ['#メルArt'],        #夜空メル
    'MATSURI_tg' : ['#祭絵'],      #夏色祭り
    # 'MATSURI_tg' : ['#祭絵','まつりは絵っち'],      #夏色祭り
    'FUBUKI_tg' : ['#絵フブキ'],         #白上フブキ
    'HAATO_tg' : ['#はあとart'],        #赤井はあと
    'AQUA_tg' : ['#あくあーと'],         #湊あくあ
    'NAKIRI_tg' : ['#百鬼絵巻'],         #百鬼あやめ
    'SHION_tg' : ['#シオンの書物'],     #紫咲シオン
    'CHOCO_tg' : ['#しょこらーと'],     #癒月ちょこ
    'SUBARU_tg' : ['#プロテインザスバル'],       #大空スバル
    'A-CHAN_tg' : ['#絵ーちゃん'],       #えーちゃん
    'PEKORA_tg' : ['#ぺこらーと'],       #兎田ぺこら
    'RUSHIA_tg' : ['#絵クロマンサー'],       #潤羽るしあ
    'MARINE_tg' : ['#マリンのお宝'],     #宝鐘マリン
    'NOEL_tg' : ['#ノエラート'],        #白銀ノエル
    'FLARE_tg' : ['#しらぬえ'],       #不知火フレア
    'TOWA_tg' : ['#TOWART'],          #常闇トワ
    'LUNA_tg' : ['#ルーナート'],      #姫森ルーナ
    # 'LUNA_tg' : ['#ルーナート','#セクシールーナート'],      #姫森ルーナ
    'COCO_tg' : ['#みかじ絵'],        #桐生ココ
    'WATAME_tg' : ['#つのまきあーと'],       #角巻わため
    'LAMY_tg' : ['#らみあ〜と', 'LamyArt'],      #雪花ラミィ
    'BOTAN_tg' : ['#ししらーと'],      #獅白ぼたん
    'NENE_tg' : ['#ねねアルバム'],        #桃鈴ねね
    'ALOE_tg' : ['#まのあろ絵'],       #魔乃アロエ
    'POLKA_tg' : ['#絵まる'],      #尾丸ポルカ

    'AZKI_tg' : ['#AZKiART'],        #AZKI

    'CALLIOPE_tg' : ['#callillust'],   #森美声
    'KIARA_tg' : ['#絵ニックス'],       #小鳥遊キアラ
    'INANIS_tg' : ['#inART','#いなート'],       #一伊那尓栖
    'GURA_tg' : ['#gawrt'],     #がうる・ぐら
    'AMELIA_tg' : ['#ameliaRT'],      #ワトソン・アメリア

    'RISU_tg' : ['#GambaRisu'],   #Ayunda Risu / アユンダ・リス
    'MOONA_tg' : ['#HoshinovArt'],       #Moona Hoshinova / ムーナ・ホシノヴァ
    'IOFI_tg' : ['#ioarts'],       #Airani Iofifteen / アイラニ・イオフィフティーン
    'OLLIE_tg' : ['#graveyART'],     #Kureiji Ollie / クレイジー・オリー 
    'ANYA_tg' : ['#anyatelier'],      #Anya Melfissa / アーニャ・メルフィッサ
    'REINE_tg' : ['#Reinessance'],     #Pavolia Reine / パヴォリア・レイネ

    'SHIGURE_UI_tg' : ['#ういしぐれぇ'],     #しぐれうい
    'TAMAKI_tg' : ['#たまきあーと'],     #犬山たまき
    'SHIRAYUKI_tg' : ['#みしろんあーと'],       #白雪みしろ
    'MILK_tg' : ['#みるくあるばむ'],       #愛宮みるく
    'HIMESAKI_tg' : ['#ゆずるあーと'],     #姫咲ゆずる
    'WARABE_tg' : ['#ばあちゃんこれ見て'],       #鬼灯わらべ
    'LILITH_tg' : ['#夢の中絵'],                #夢乃リリス
    'MOMO_tg' : ['#魔法少女活動報告書'],                #胡桃澤もも
    'KIRARA_tg' : ['#あくまびじゅつかん'],                #逢魔きらら
}


# pprint(tweet_url_list)

d_today = datetime.date.today()
since_day = d_today - datetime.timedelta(days=1)
csv_base = '_' + str(d_today) + '.csv'

aTime = datetime.time(00, 00, 00)
bTime = datetime.time(00, 00, 00)
aT_native = dt.combine(d_today, aTime)
bT_native = dt.combine(since_day, bTime)
today_daytime = pytz.timezone('Asia/Tokyo').localize(aT_native)
since_daytime = pytz.timezone('Asia/Tokyo').localize(bT_native)
print(today_daytime)
print(since_daytime)


# ディレクトリを作成
new_dir_path = './Tweet_Tag/{}/'.format(str(d_today))
if not os.path.exists(new_dir_path) :
    os.makedirs(new_dir_path)


hSql = holo_sql.holo_sql()  # DBインスタンス作成
# hSql.createArtsTable()  #  テーブル作成
    # タグ検索
for Account,Tag in Holo_tags.items():
    for hTag in Tag :
        MAX_ID = ''
        HoloName = ''
        # final_data = []
        print(hTag)
        # ホロライブ
        if Account == 'KORONE_tg': HoloName = '戌神ころね'
        elif Account  == 'MIKO_tg' : HoloName ='さくらみこ'
        elif Account  == 'FUBUKI_tg' : HoloName = '白上フブキ'
        elif Account  == 'AQUA_tg' : HoloName = '湊あくあ'
        elif Account  == 'PEKORA_tg' : HoloName = '兎田ぺこら'
        elif Account  == 'AKIROSE_tg' : HoloName = 'アキ・ローゼンタール'
        elif Account  == 'SORA_tg' : HoloName = 'ときのそら'
        elif Account  == 'SUBARU_tg' : HoloName = '大空スバル'
        elif Account  == 'ROBOCO_tg' : HoloName = 'ロボ子さん'
        elif Account  == 'SHION_tg'  : HoloName = '紫咲シオン'
        elif Account  == 'FLARE_tg' : HoloName = '不知火フレア'
        elif Account  == 'MEL_tg' : HoloName = '夜空メル'
        elif Account  == 'CHOCO_tg' : HoloName = '癒月ちょこ'
        elif Account  == 'HAATO_tg': HoloName = '赤井はあと'
        elif Account  == 'OKAYU_tg' : HoloName = '猫又おかゆ'
        elif Account  == 'LUNA_tg' : HoloName = '姫森ルーナ'
        elif Account  == 'SUISEI_tg' : HoloName = '星街すいせい'
        elif Account  == 'MATSURI_tg' : HoloName = '夏色まつり'
        elif Account  == 'MARINE_tg' : HoloName = '宝鐘マリン'
        elif Account  == 'NAKIRI_tg' : HoloName = '百鬼あやめ'
        elif Account  == 'NOEL_tg' : HoloName = '白銀ノエル'
        elif Account  == 'RUSHIA_tg' : HoloName = '潤羽るしあ'
        elif Account  == 'COCO_tg' : HoloName = '桐生ココ'
        elif Account  == 'KANATA_tg' : HoloName = '天音かなた'
        elif Account  == 'MIO_tg' : HoloName = '大神ミオ'
        elif Account  == 'TOWA_tg' : HoloName = '常闇トワ'
        elif Account  == 'WATAME_tg' : HoloName = '角巻わため'
        elif Account  == 'LAMY_tg' : HoloName = '雪花ラミィ'
        elif Account  == 'NENE_tg' : HoloName = '桃鈴ねね'
        elif Account  == 'BOTAN_tg' : HoloName = '獅白ぼたん'
        elif Account  == 'POLKA_tg'  : HoloName = '尾丸ポルカ'
        elif Account  == 'ALOE_tg' : HoloName = '魔乃アロエ'
        # イノナカミュージック
        elif Account  == 'AZKI_tg' : HoloName = 'AZKi'
        # えーちゃん
        elif Account  == 'A-CHAN_tg' : HoloName = 'えーちゃん'
        # ホロライブEN
        elif Account  == 'CALLIOPE_tg' : HoloName = '森美声'
        elif Account  == 'KIARA_tg' : HoloName = '小鳥遊キアラ'
        elif Account  == 'INANIS_tg' : HoloName = '一伊那尓栖'
        elif Account  == 'GURA_tg' : HoloName = 'がうる・ぐら'
        elif Account  == 'AMELIA_tg' : HoloName = 'ワトソン・アメリア'
        # ホロライブID
        elif Account  == 'RISU_tg' : HoloName = 'アユンダ・リス'
        elif Account  == 'MOONA_tg' : HoloName = 'ムーナ・ホシノヴァ'
        elif Account  == 'IOFI_tg' : HoloName = 'アイラニ・イオフィフティーン'
        elif Account  == 'OLLIE_tg' : HoloName = 'クレイジー・オリー'
        elif Account  == 'ANYA_tg' : HoloName = 'アーニャ・メルフィッサ'
        elif Account  == 'REINE_tg' : HoloName = 'パヴォリア・レイネ'
        # 絵師
        elif Account  == 'SHIGURE_UI_tg' : HoloName = 'しぐれうい'
        # のりプロ
        elif Account  == 'TAMAKI_tg' : HoloName = '犬山たまき'
        elif Account  == 'SHIRAYUKI_tg' : HoloName = '白雪みしろ'
        elif Account  == 'MILK_tg' : HoloName = '愛宮みるく'
        elif Account  == 'HIMESAKI_tg' : HoloName = '姫咲ゆずる'
        elif Account  == 'WARABE_tg' : HoloName = '鬼灯わらべ'
        elif Account  == 'LILITH_tg' : HoloName = '夢乃リリス'
        elif Account  == 'MOMO_tg' : HoloName = '胡桃澤もも'
        elif Account  == 'KIRARA_tg' : HoloName = '逢魔きらら'


        while True:
            data_count = []
            for tweet in tweepy.Cursor(API.search,q=hTag + " -filter:retweets", max_id = MAX_ID, exclude_replies = True, wait_on_rate_limit = True,tweet_mode='extended',include_entities=True).items(100):
                # favoriteが1000以上かチェック
                data_count.append([tweet.id])
                insert_data = []
                if tweet.favorite_count >= _FAVORITE_COUNT :
                    MAX_ID = tweet.id
                    # DBに同一tweetIDがないかチェック(既存データかチェック)
                    result = hSql.searchTweetId(tweet.id)
                    # pprint(result)
                    if result:
                        # 更新されているかチェックして、アップデート
                        if tweet.favorite_count != result[0][5]: 
                            hSql.updateArtsFavorite(result[0][3],tweet.favorite_count)
                        if tweet.retweet_count != result[0][6]:
                            hSql.updateArtsRetweet(result[0][3],tweet.retweet_count)
                    else:
                        # 投稿時間を日本時間に変換
                        jst_timestamp = pytz.timezone('Asia/Tokyo').localize( tweet.created_at + datetime.timedelta(hours=9) )
                        updateJST = jst_timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        tweet_url = f"https://twitter.com/user/status/{tweet.id}"
                        

# ===========================================================================================

                        # 画像保存 &　配列に追加
                        for i in range(4):
                            try :
                                if i == 0:
                                    filename = ''
                                    if tweet.extended_entities['media'][0]:
                                        if tweet.extended_entities['media'][0]['type'] == 'photo':    # 画像保存
                                            download(tweet.extended_entities['media'][0]['media_url_https'])
                                            file_name = tweet.extended_entities['media'][0]['media_url_https'].split('/')[-1]    # 画像タイトルを抽出 
                                        elif tweet.extended_entities['media'][0]['type'] == 'animated_gif':    # git保存
                                            downloadVideo(tweet.extended_entities['media'][0]['video_info']['variants'][0]['url'])
                                            file_name = tweet.extended_entities['media'][0]['video_info']['variants'][0]['url'].split('/')[-1]    # gitタイトルを抽出 
                                        elif tweet.extended_entities['media'][0]['type'] == 'video':    # 動画保存 
                                            bitrate_array = []
                                            for bitrate in tweet.extended_entities['media'][0]['video_info']['variants']: # 最大ファイルサイズを探す
                                                bitrate_array.append(bitrate.get('bitrate',0))
                                            max_index = bitrate_array.index(max(bitrate_array))
                                            downloadVideo(tweet.extended_entities['media'][0]['video_info']['variants'][max_index]['url'])
                                            remake_name = tweet.extended_entities['media'][0]['video_info']['variants'][max_index]['url'].split('/')[-1] #　動画タイトルを抽出 
                                            file_name = remake_name.split('?')[0]

                                    # 制作者のURLを抽出
                                    creator_path = 'https://twitter.com/' + tweet.extended_entities['media'][0]['expanded_url'].split('/')[3]

                                    insert_data.append([tweet.id,updateJST,tweet.full_text.replace('\n',''),tweet.favorite_count,tweet.retweet_count,file_name,creator_path,tweet_url]) #最終的に書き込むデータリスト(DB)
                                    # final_data.append([tweet.id,updateJST,tweet.text.replace('\n',''),tweet.favorite_count,tweet.retweet_count,tweet_url])  #最終的に書き込むデータリスト(CSV)

                                    # DBへ新規登録
                                    hSql.insertArtsTable(HoloName, hTag, insert_data)

                                if i >= 1:
                                    if tweet.extended_entities['media'][i]:
                                        if tweet.extended_entities['media'][i]['type'] == 'photo':    # 画像保存
                                            download(tweet.extended_entities['media'][i]['media_url_https'])
                                            file_name = tweet.extended_entities['media'][i]['media_url_https'].split('/')[-1]  # 画像タイトルを抽出 
                                        elif tweet.extended_entities['media'][0]['type'] == 'animated_gif':    # git保存
                                            downloadVideo(tweet.extended_entities['media'][0]['video_info']['variants'][0]['url'])
                                            file_name = tweet.extended_entities['media'][0]['video_info']['variants'][0]['url'].split('/')[-1] # gitタイトルを抽出 
                                        elif tweet.extended_entities['media'][0]['type'] == 'video':    # 動画保存 
                                            bitrate_array = []
                                            for bitrate in tweet.extended_entities['media'][0]['video_info']['variants']: # 最大ファイルサイズを探す
                                                bitrate_array.append(bitrate.get('bitrate',0))
                                            max_index = bitrate_array.index(max(bitrate_array))
                                            downloadVideo(tweet.extended_entities['media'][0]['video_info']['variants'][max_index]['url'])
                                            remake_name = tweet.extended_entities['media'][0]['video_info']['variants'][max_index]['url'].split('/')[-1]# 動画タイトルを抽出 
                                            file_name = remake_name.split('?')[0]
                                    
                                    # DBへ更新登録 @TODO
                                    column_num = i + 1
                                    hSql.updateArtsImage(tweet.id,file_name,column_num)

                            except AttributeError as e:
                                error_catch(e)
                                pprint('1エラー')
                                break
                            except IndexError as e2:
                                error_catch(e2)
                                pprint('このツイートにはこれ以上ファイルがありません')
                                break
                            except KeyError as e3:
                                error_catch(e3)
                                pprint('3エラー')
                                break



# ===========================================================================================
                else:
                    MAX_ID = tweet.id

            print(MAX_ID)
            MAX_ID = int(MAX_ID) - 1
            if len(data_count) < 100:
                print('ブレイク入ります')
                break

        filename = new_dir_path + Account + csv_base
        # # CSV登録
        # lives_report = pd.DataFrame(final_data)
        # # pprint(lives_report)
        # lives_report.to_csv(filename, header=False, index=False, mode='w')


hSql.dbClose()  #  DBクローズ
hSql = None
