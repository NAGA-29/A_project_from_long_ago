'''
指定された日までのカウントダウンを行う
'''

from re import DEBUG
import time
from datetime import datetime as dt
import datetime
from datetime import date
import dateutil.parser
import schedule
import random

from pprint import pprint

import os
from os.path import join, dirname
from dotenv import load_dotenv

'''
Original Modules
'''
import holo_sql
from Components.tweet import tweet_components
from Components.holo_date import HoloDate

def test():
    hSql = holo_sql.holo_sql()
    tw = tweet_components()
    hDate = HoloDate()

    message = ''

    dt_now = dt.now()
    all_schedules = hSql.selectEventSchedulesTable()
    for schedule in all_schedules:
        if schedule['scheduled_start_time_at']:
            time_lag = schedule['scheduled_start_time_at'] - dt_now
            # pprint(time_lag)
            '''
            time_lag.days >= 0 予定時前
            time_lag.days < 0  予定時間より過ぎている
            '''
            if time_lag.days >= 0:
                # 予定まで1日以上ある場合
                day = time_lag.days
                min, sec = divmod(time_lag.seconds, 60)
                hours, min= divmod(min, 60)
                if day > 0:
                    message = '{}まで\nあと{}日と{}時間!!✨\n{}✨'.format(schedule['title'],day,hours,schedule['message'])
                    tw.event_tweetWithIMG(message,schedule['image'])
                    pprint(message)
                else:
                    '''
                    hours == 1                 予定時間まで1時間以上時間がある場合
                    hours == 0 and min > 1     1時間以内かつ1分以上ある場合
                    その他                      1分未満かつ0秒以上ある場合(何もしない)
                    '''
                    if hours >= 1:
                        message = '{}まで\n\nあと「{}時間{}分」!!✨\n\n{}✨'.format(schedule['title'],hours,min,schedule['message'])
                        tw.event_tweetWithIMG(message,schedule['image'])
                        pprint(message)
                    elif hours == 0 and min > 1:
                        message = '{}まで\n\nあと{}分!!✨\n\n{}✨'.format(schedule['title'],min,schedule['message'])
                        tw.event_tweetWithIMG(message,schedule['image'])
                        pprint(message)
                    else:
                        hSql.updateStatus_SchedulesTable(schedule['scheduled_start_time_at'])
                        pass

            else:
                hSql.updateStatus_SchedulesTable(schedule['scheduled_start_time_at'])
                pprint('予定時間を過ぎています')
                # 予定まで24時間を切った場合

def main():
    hSql = holo_sql.holo_sql()
    today = dt.now()
    one_year_ago = today - datetime.timedelta(days=365)
    pprint(today.month)
    pprint(one_year_ago)
    histories = hSql.one_year_ago_TubeTable()
    # pprint(history)
    history = random.choice(histories)
    pprint(history['title'])


# 毎時0分に実行
# schedule.every().hour.at(":46").do(Main)
# schedule.every().hour.at(":15").do(Main)

# # PM00:05 AM12:05にjob実行
schedule.every().day.at("15:00").do(main)
schedule.every().day.at("12:00").do(main)
schedule.every().day.at("17:30").do(main)
schedule.every().day.at("08:00").do(main)
schedule.every().day.at("00:20").do(main)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
    
    # pprint(d)


    # SELECT * FROM Tube WHERE acutual_start_at = %s(one_years_ago) ????
    # 今日の日付の一年前を計算
    # DBから検索
    # ランダム選択
    # video_idを取得,画像url取得ダウンロード
    # message作成
    # アウトプット

    # 問題:
    # SQLでdatetimeの絞り込みできるのか？？？->remind.pyでのコードを参考に