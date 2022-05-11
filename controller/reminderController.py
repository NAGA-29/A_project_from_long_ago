import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv

import time 
import datetime
import schedule

'''
Original Modules
'''
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import holo_sql
from Components.tweet import tweet_components
from Components.vtuber.hololive import Hololive
from Components.vtuber.noripro import NoriPro
from Components import logging as log
from config import app

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

# twitter本番アカウント My_Hololive_Art_project
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

# twitter本番アカウント My_NoriPro_project
CONSUMER_KEY_NORI = os.environ.get('CONSUMER_KEY_B')
CONSUMER_SECRET_NORI = os.environ.get('CONSUMER_SECRET_B')
ACCESS_TOKEN_NORI = os.environ.get('ACCESS_TOKEN_B')
ACCESS_TOKEN_SECRET_NORI = os.environ.get('ACCESS_TOKEN_SECRET_B')

# テストアカウント 
CONSUMER_KEY_TEST = os.environ.get('CONSUMER_KEY_TEST')
CONSUMER_SECRET_TEST = os.environ.get('CONSUMER_SECRET_TEST')
ACCESS_TOKEN_TEST = os.environ.get('ACCESS_TOKEN_TEST')
ACCESS_TOKEN_SECRET_TEST = os.environ.get('ACCESS_TOKEN_SECRET_TEST')

# IMG_TRIM_DIR = os.environ.get('IMG_TRIM_DIR')
# IMG_TRIM_DIR = '../src/Trim_Images/'
# print(app.IMG_TRIM_DIR)
# トリム加工済み画像の保存先
IMG_TRIM_DIR = app.IMG_TRIM_DIR

# logging
file = os.path.splitext(os.path.basename(__file__))[0]
_FILE_NAME = f'../storage/logs/{file}.log'


def reMinder(target:str):
    next_id = None
    hSql = holo_sql.holo_sql()
    today_live = hSql.selectTodayKeepWatchTable(target)

    if(target == 'hololive'):
        tw = tweet_components(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    elif(target == 'noripro'):
        tw = tweet_components(CONSUMER_KEY_NORI, CONSUMER_SECRET_NORI, ACCESS_TOKEN_NORI, ACCESS_TOKEN_SECRET_NORI)

    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    FILE_NAME = []
    message = '本日[ {}/{} ]のLive予定はコチラ!🌟\n'.format(month, day)
    if today_live:
        live_count = len(today_live)
        # 回した回数
        loop = 1
        count = 0
        print(live_count)
        if live_count <= 4:
            for live in today_live:
                if live['scheduled_start_time_at'].date() == today :
                    live_tag, holo_tag = Hololive.getLiveTag(live['channel_id'])
                    # message += '{}{}({}) : {}~\n'.format(holo_tag, live['holo_name'], live_tag, live['scheduled_start_time_at'].time().strftime('%H:%M'))
                    message += '{}{} : {}~\n'.format(holo_tag, live['holo_name'], live['scheduled_start_time_at'].time().strftime('%H:%M'))
                # ↓添付したい画像のファイル名
                FILE_NAME.append(IMG_TRIM_DIR + live['video_id'] +'.jpg')
            print(message) #ツイート
            # tw.remind_tweetWithIMG(message, FILE_NAME)
            tw.remind_tweetWithIMG_test(message, FILE_NAME)
        else:
            for live in today_live:
                if loop <=4:
                    if live['scheduled_start_time_at'].date() == today :
                        live_tag, holo_tag  = Hololive.getLiveTag(live['channel_id'])
                        # message += '{}{}({}) : {}~\n'.format(holo_tag, live['holo_name'], live_tag, live['scheduled_start_time_at'].time().strftime('%H:%M'))
                        message += '{}{} : {}~\n'.format(holo_tag, live['holo_name'], live['scheduled_start_time_at'].time().strftime('%H:%M'))
                        # ↓添付したい画像のファイル名
                        FILE_NAME.append(IMG_TRIM_DIR + live['video_id'] +'.jpg')
                        loop += 1
                        count += 1
                        if loop >= 5 or live_count == count :
                            print(message) #ツイート
                            # tw.remind_tweetWithIMG(message, FILE_NAME)
                            result = tw.remind_tweetWithIMG_test(message, FILE_NAME, next_id)
                            next_id = result.id
                            FILE_NAME = []
                            message = '本日[ {}/{} ]のLive予定はコチラ!🌟\n'.format(month, day)
                            loop = 1
                            time.sleep(1)
    else:
        message = '現在予定はありません。'
    hSql.dbClose()
    hSql = None
    pass


def tomorrowReminder(target):
    next_id = None
    hSql = holo_sql.holo_sql()
    tomorrow_live = hSql.selectTomorrow_KeepWatch(target)

    if(target == 'hololive'):
        tw = tweet_components(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    elif(target == 'noripro'):
        tw = tweet_components(CONSUMER_KEY_NORI, CONSUMER_SECRET_NORI, ACCESS_TOKEN_NORI, ACCESS_TOKEN_SECRET_NORI)

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    year = tomorrow.year
    month = tomorrow.month
    day = tomorrow.day
    FILE_NAME = []
    message = '明日[ {}/{} ]のLive予定はコチラ!🌟\n\n'.format(month, day)
    if tomorrow_live:
        live_count = len(tomorrow_live)
        # 回した回数
        loop = 1
        count = 0
        print(live_count)
        if live_count <= 4:
            for live in tomorrow_live:
                if live['scheduled_start_time_at'].date() == tomorrow :
                    live_tag, holo_tag = Hololive.getLiveTag(live['channel_id'])
                    # message += '{}{}({}) : {}~\n'.format(holo_tag, live['holo_name'], live_tag, live['scheduled_start_time_at'].time().strftime('%H:%M'))
                    message += '{}{} : {}~\n'.format(holo_tag, live['holo_name'], live['scheduled_start_time_at'].time().strftime('%H:%M'))
                # ↓添付したい画像のファイル名
                FILE_NAME.append(IMG_TRIM_DIR + live['video_id'] +'.jpg')
            print(message) #ツイート
            # tw.remind_tweetWithIMG(message, FILE_NAME)
            tw.remind_tweetWithIMG_test(message, FILE_NAME)
        else:
            for live in tomorrow_live:
                if loop <= 4:
                    if live['scheduled_start_time_at'].date() == tomorrow :
                        live_tag, holo_tag  = Hololive.getLiveTag(live['channel_id'])
                        # message += '{}{}({}) : {}~\n'.format(holo_tag, live['holo_name'], live_tag, live['scheduled_start_time_at'].time().strftime('%H:%M'))
                        message += '{}{} : {}~\n'.format(holo_tag, live['holo_name'], live['scheduled_start_time_at'].time().strftime('%H:%M'))
                        # ↓添付したい画像のファイル名
                        # print(FILE_NAME)
                        FILE_NAME.append(IMG_TRIM_DIR + live['video_id'] +'.jpg')
                        loop += 1
                        count += 1
                        if loop >= 5 or live_count == count :
                            print(message) #ツイート
                            # tw.remind_tweetWithIMG(message, FILE_NAME)
                            result = tw.remind_tweetWithIMG_test(message, FILE_NAME, next_id)
                            next_id = result.id
                            FILE_NAME = []
                            message = '明日[ {}/{} ]のLive予定はコチラ!🌟\n\n'.format(month, day)
                            loop = 1
                            time.sleep(1)
    else:
        message = '現在予定はありません。'
    hSql.dbClose()
    hSql = None
    tw = None
    pass

def main():
    logger = log.get_module_logger(__name__, _FILE_NAME)
    logger.info('Start main')
    reMinder('hololive')
    reMinder('noripro')
    logger.info('End main')
    logger = None

def main_tommorrow():
    logger = log.get_module_logger(__name__, _FILE_NAME)
    logger.info('Start main_tommorrow')
    tomorrowReminder('hololive')
    tomorrowReminder('noripro')
    logger.info('End main_tommorrow')
    logger = None


# 毎時0分に実行
# schedule.every().hour.at(":01").do(reMind)
# schedule.every().hour.at(":30").do(artTweet)
# schedule.every().hour.at(":15").do(holoNews)
# schedule.every().hour.at(":45").do(holoNews)

# schedule.every().hour.at(":21").do(main)
# schedule.every().hour.at(":09").do(searchSubscriber)

schedule.every().day.at("06:00").do(main)
schedule.every().day.at("12:10").do(main)
schedule.every().day.at("18:00").do(main)
# schedule.every().day.at("07:00").do(reMind)

schedule.every().day.at("23:00").do(main_tommorrow)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)