import os
from os.path import join, dirname
from dotenv import load_dotenv

import time 
import datetime
import schedule

"""
Original Modules
"""
import holo_sql
from Components.tweet import tweet_components


# twitter本番アカウント My_Hololive_Art_project
CONSUMER_KEY = os.environ.get('CONSUMER_KEY_A')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET_A')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN_A')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET_A')
IMG_TRIM_DIR = os.environ.get('IMG_TRIM_DIR')


def reMind():
    hSql = holo_sql.holo_sql()
    tw = tweet_components()
    today_live = hSql.selectTodayKeepWatchTable()
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    FILE_NAME = []
    message = '本日[{}/{}]のLive予定はコチラ!🌟\n'.format(month, day)
    if today_live:
        live_count = len(today_live)
        # 回した回数
        loop = 1
        count = 0
        print(live_count)
        if live_count <= 4:
            for live in today_live:
                if live['scheduled_start_time_at'].date() == today :
                    live_tag, holo_tag = getLiveTag(live['channel_id'])
                    message += '{}{}({}) : {}~\n'.format(holo_tag, live['holo_name'], live_tag, live['scheduled_start_time_at'].time().strftime('%H:%M'))
                # ↓添付したい画像のファイル名
                FILE_NAME.append(IMG_TRIM_DIR + live['video_id'] +'.jpg')
            print(message) #ツイート
            tw.remind_tweetWithIMG(message, FILE_NAME)
        else:
            for live in today_live:
                if loop <=4:
                    if live['scheduled_start_time_at'].date() == today :
                        live_tag, holo_tag  = getLiveTag(live['channel_id'])
                        message += '{}{}({}) : {}~\n'.format(holo_tag, live['holo_name'], live_tag, live['scheduled_start_time_at'].time().strftime('%H:%M'))
                        # ↓添付したい画像のファイル名
                        FILE_NAME.append(IMG_TRIM_DIR + live['video_id'] +'.jpg')
                        loop += 1
                        count += 1
                        if loop >= 5 or live_count == count :
                            print(message) #ツイート
                            tw.remind_tweetWithIMG(message, FILE_NAME)
                            FILE_NAME = []
                            message = '本日[{}/{}]のLive予定はコチラ!🌟\n'.format(month, day)
                            loop = 1
                            time.sleep(1)
    else:
        message = '現在予定はありません。'
    # print(message)
    hSql.dbClose()
    hSql = None
    pass

def tomorrowRemind():
    hSql = holo_sql.holo_sql()
    tw = tweet_components()
    tomorrow_live = hSql.selectTomorrow_KeepWatch()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    year = tomorrow.year
    month = tomorrow.month
    day = tomorrow.day
    FILE_NAME = []
    message = '明日[{}/{}]のLive予定はコチラ!🌟\n\n'.format(month, day)
    if tomorrow_live:
        live_count = len(tomorrow_live)
        # 回した回数
        loop = 1
        count = 0
        print(live_count)
        if live_count <= 4:
            for live in tomorrow_live:
                if live['scheduled_start_time_at'].date() == tomorrow :
                    live_tag, holo_tag = getLiveTag(live['channel_id'])
                    message += '{}{}({}) : {}~\n'.format(holo_tag, live['holo_name'], live_tag, live['scheduled_start_time_at'].time().strftime('%H:%M'))
                # ↓添付したい画像のファイル名
                FILE_NAME.append(IMG_TRIM_DIR + live['video_id'] +'.jpg')
            print(message) #ツイート
            tw.remind_tweetWithIMG(message, FILE_NAME)
        else:
            for live in tomorrow_live:
                if loop <=4:
                    if live['scheduled_start_time_at'].date() == tomorrow :
                        live_tag, holo_tag  = getLiveTag(live['channel_id'])
                        message += '{}{}({}) : {}~\n'.format(holo_tag, live['holo_name'], live_tag, live['scheduled_start_time_at'].time().strftime('%H:%M'))
                        # ↓添付したい画像のファイル名
                        FILE_NAME.append(IMG_TRIM_DIR + live['video_id'] +'.jpg')
                        loop += 1
                        count += 1
                        if loop >= 5 or live_count == count :
                            print(message) #ツイート
                            tw.remind_tweetWithIMG(message, FILE_NAME)
                            FILE_NAME = []
                            message = '明日[{}/{}]のLive予定はコチラ!🌟\n\n'.format(month, day)
                            loop = 1
                            time.sleep(1)
    else:
        message = '現在予定はありません。'
    hSql.dbClose()
    hSql = None
    pass


'''

'''
def getLiveTag(ID:str)->str:
    HoloName = ''
    live_tag = ''
    holo_tag  = ''
    if ID == 'UChAnqc_AY5_I3Px5dig3X1Q': HoloName, live_tag, holo_tag = '戌神ころね', '#生神もんざえもん','🥐'
    elif ID == 'UC-hM6YJuNYVAmUWxeIr9FeA' : HoloName, live_tag, holo_tag  = 'さくらみこ', '#みこなま', '🌸'
    elif ID == 'UCdn5BQ06XqgXoAxIhbqw5Rg' : HoloName, live_tag, holo_tag  = '白上フブキ', '#フブキCh', '🌽'
    elif ID == 'UC1opHUrw8rvnsadT-iGp7Cg' : HoloName, live_tag, holo_tag  = '湊あくあ', '#湊あくあ生放送', '⚓️'
    elif ID == 'UC1DCedRgGHBdm81E1llLhOQ' : HoloName, live_tag, holo_tag  = '兎田ぺこら', '#ぺこらいぶ', '👯'
    elif ID == 'UCFTLzh12_nrtzqBPsTCqenA' : HoloName, live_tag, holo_tag  = 'アキ・ローゼンタール', '#アキびゅーわーるど', '🍎'
    elif ID == 'UCp6993wxpyDPHUpavwDFqgg' : HoloName, live_tag, holo_tag  = 'ときのそら', '#ときのそら生放送', '🐻'
    elif ID == 'UCvzGlP9oQwU--Y0r9id_jnA' : HoloName, live_tag, holo_tag  = '大空スバル', '#生スバル', '🚑'
    elif ID == 'UCDqI2jOz0weumE8s7paEk6g' : HoloName, live_tag, holo_tag  = 'ロボ子さん', '#ロボ子生放送', '🤖'
    elif ID == 'UCXTpFs_3PqI41qX2d9tL2Rw' : HoloName, live_tag, holo_tag  = '紫咲シオン', '#紫咲シオン', '🌙'
    elif ID == 'UCvInZx9h3jC2JzsIzoOebWg' : HoloName, live_tag, holo_tag  = '不知火フレア', '#フレアストリーム', '🔥'
    elif ID == 'UCD8HOxPs4Xvsm8H0ZxXGiBw' : HoloName, live_tag, holo_tag  = '夜空メル', '#メル生放送', '🌟'
    elif ID == 'UC1suqwovbL1kzsoaZgFZLKg' : HoloName, live_tag, holo_tag  = '癒月ちょこ', '#癒月診療所', '💋'
    elif ID == 'UCp3tgHXw_HI0QMk1K8qh3gQ' : HoloName, live_tag, holo_tag  = '癒月ちょこ', '#癒月診療所', '💋' #サブ
    elif ID == 'UC1CfXB_kRs3C-zaeTG3oGyg' : HoloName, live_tag, holo_tag  = '赤井はあと', '#はあちゃまなう', '❤️'
    elif ID == 'UCvaTdHTWBGv3MKj3KVqJVCw' : HoloName, live_tag, holo_tag  = '猫又おかゆ', '#生おかゆ', '🍙'
    elif ID == 'UCa9Y57gfeY0Zro_noHRVrnw' : HoloName, live_tag, holo_tag  = '姫森ルーナ', '#なのらいぶ', '🍬'
    elif ID == 'UC5CwaMl1eIgY8h02uZw7u8A' : HoloName, live_tag, holo_tag  = '星街すいせい', '#ほしまちすたじお', '☄️'
    elif ID == 'UCQ0UDLQCjY0rmuxCDE38FGg' : HoloName, live_tag, holo_tag  = '夏色まつり', '#夏まつch', '🏮'
    elif ID == 'UCCzUftO8KOVkV4wQG1vkUvg' : HoloName, live_tag, holo_tag  = '宝鐘マリン', '#マリン航海記', '🏴‍☠️'
    elif ID == 'UC7fk0CB07ly8oSl0aqKkqFg' : HoloName, live_tag, holo_tag  = '百鬼あやめ', '#百鬼あやめch', '😈'
    elif ID == 'UCdyqAaZDKHXg4Ahi7VENThQ' : HoloName, live_tag, holo_tag  = '白銀ノエル', '#ノエルーム', '⚔️'
    elif ID == 'UCl_gCybOJRIgOXw6Qb4qJzQ' : HoloName, live_tag, holo_tag  = '潤羽るしあ', '#るしあらいぶ', '🦋'
    elif ID == 'UCS9uQI-jC3DE0L4IpXyvr6w' : HoloName, live_tag, holo_tag  = '桐生ココ', '#桐生ココ', '🐉'
    elif ID == 'UCZlDXzGoo7d44bwdNObFacg' : HoloName, live_tag, holo_tag  = '天音かなた', '#天界学園放送部', '💫'
    elif ID == 'UCp-5t9SrOQwXMU7iIjQfARg' : HoloName, live_tag, holo_tag  = '大神ミオ', '#ミオかわいい', '🌲'
    elif ID == 'UC1uv2Oq6kNxgATlCiez59hw' : HoloName, live_tag, holo_tag  = '常闇トワ', '#トワイライブ', '👾'
    elif ID == 'UCqm3BQLlJfvkTsX_hvm0UmA' : HoloName, live_tag, holo_tag  = '角巻わため', '#ドドドライブ', '🐏'
    elif ID == 'UCFKOVgVbGmX65RxO3EtH3iw' : HoloName, live_tag, holo_tag  = '雪花ラミィ', '#らみらいぶ', '☃️'
    elif ID == 'UCAWSyEs_Io8MtpY3m-zqILA' : HoloName, live_tag, holo_tag  = '桃鈴ねね', '#ねねいろらいぶ', '🥟'
    elif ID == 'UCUKD-uaobj9jiqB-VXt71mA' : HoloName, live_tag, holo_tag  = '獅白ぼたん', '#ぐうたらいぶ', '👅'
    elif ID == 'UCK9V2B22uJYu3N7eR_BT9QA' : HoloName, live_tag, holo_tag  = '尾丸ポルカ', '#ポルカ公演中', '🎪'
    # elif ID == 'UCgZuwn-O7Szh9cAgHqJ6vjw' : HoloName = '魔乃アロエ'
    # イノナカミュージック
    elif ID == 'UC0TXe_LYZ4scaW2XMyi5_kw' : HoloName, live_tag, holo_tag  = 'AZKi', '#AZKi', '⚒️'
    #ホロライブ　EN
    elif ID == 'UCL_qhgtOy0dy1Agp8vkySQg' : HoloName, live_tag, holo_tag  = '森美声', '#calliolive', '💀'
    elif ID == 'UCHsx4Hqa-1ORjQTh9TYDhww' : HoloName, live_tag, holo_tag  = '小鳥遊キアラ', '#キアライブ', '🐔'
    elif ID == 'UCMwGHR0BTZuLsmjY_NT5Pwg' : HoloName, live_tag, holo_tag  = '一伊那尓栖', '#TAKOTIME', '🐙'
    elif ID == 'UCoSrY_IQQVpmIRZ9Xf-y93g' : HoloName, live_tag, holo_tag  = 'がうる・ぐら', '#gawrgura', '🔱'
    elif ID == 'UCyl1z3jo3XHR1riLFKG5UAg' : HoloName, live_tag, holo_tag  = 'ワトソン・アメリア', '#amelive', '🔎'
    #ホロライブ ID
    elif ID == 'UCOyYb1c43VlX9rc_lT6NKQw' : HoloName, live_tag, holo_tag  = 'アユンダ・リス', '#Risu_Live', '🐿'
    elif ID == 'UCP0BspO_AMEe3aQqqpo89Dg' : HoloName, live_tag, holo_tag  = 'ムーナ・ホシノヴァ', '#MoonA_Live', '🔮'
    elif ID == 'UCAoy6rzhSf4ydcYjJw3WoVg' : HoloName, live_tag, holo_tag  =  'アイラニ・イオフィフティーン', '#ioLYFE', '🎨'
    elif ID == 'UCYz_5n-uDuChHtLo7My1HnQ' : HoloName, live_tag, holo_tag  =  'クレイジー・オリー', '#Kureiji_Ollie', '🧟‍♀️'
    elif ID == 'UC727SQYUvx5pDDGQpTICNWg' : HoloName, live_tag, holo_tag  =  'アーニャ・メルフィッサ', '#Anya_Melfissa', '🍂'
    elif ID == 'UChgTyjG-pdNvxxhdsXfHQ5Q' : HoloName, live_tag, holo_tag  =  'パヴォリア・レイネ', '#Pavolive', '🦚'
    # 運営
    elif ID == 'UCJFZiqLMntJufDCHc6bQixg' : HoloName, live_tag, holo_tag  = 'Hololive','#Hololive', '▶️'
    # 絵師
    elif ID == 'UCt30jJgChL8qeT9VPadidSw' : HoloName, live_tag, holo_tag  = 'しぐれうい', '#ういなま', '🌂'
    # のりプロ
    elif ID == 'UC8NZiqKx6fsDT3AVcMiVFyA' : HoloName, live_tag, holo_tag  = '犬山たまき', '#犬山たまき', '🐶'
    elif ID == 'UCC0i9nECi4Gz7TU63xZwodg' : HoloName, live_tag, holo_tag  = '白雪みしろ', '#白雪みしろ', '❄️'
    elif ID == 'UCJCzy0Fyrm0UhIrGQ7tHpjg' : HoloName, live_tag, holo_tag  = '愛宮みるく', '#愛宮みくる', '🍼'
    elif ID == 'UCle1cz6rcyH0a-xoMYwLlAg' : HoloName, live_tag, holo_tag  = '姫咲ゆずる', '姫咲ゆずる', '🐰'
    elif ID == 'UCLyTXfCZtl7dyhta9Jg3pZg' : HoloName, live_tag, holo_tag  = '鬼灯わらべ', '#鬼灯わらべ', '👹'
    elif ID == 'UCH11P1Hq4PXdznyw1Hhr3qw' : HoloName, live_tag, holo_tag  = '夢乃リリス', '#夢乃リリス', '🏩'
    elif ID == 'UCxrmkJf_X1Yhte_a4devFzA' : HoloName, live_tag, holo_tag  = '胡桃澤もも', '#胡桃澤もも', '🎀'
    elif ID == 'UCBAeKqEIugv69Q2GIgcH7oA' : HoloName, live_tag, holo_tag  = '逢魔きらら', '#逢魔きらら', '👿'
    elif ID == 'UCIRzELGzTVUOARi3Gwf1-yg' : HoloName, live_tag, holo_tag  = '看谷にぃあ', '#看谷にぃあ', '🌙❤️'
    return live_tag, holo_tag 


# 毎時0分に実行
# schedule.every().hour.at(":01").do(reMind)
# schedule.every().hour.at(":30").do(artTweet)
# schedule.every().hour.at(":15").do(holoNews)
# schedule.every().hour.at(":45").do(holoNews)

# schedule.every().hour.at(":21").do(main)
# schedule.every().hour.at(":09").do(searchSubscriber)

# PM00:05 AM12:05にjob実行
schedule.every().day.at("07:00").do(reMind)
schedule.every().day.at("12:00").do(reMind)
schedule.every().day.at("18:00").do(reMind)
# schedule.every().day.at("01:15").do(reMind)
schedule.every().day.at("23:15").do(tomorrowRemind)

while True:
    schedule.run_pending()
    time.sleep(1)