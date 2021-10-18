'''
指定された日までのカウントダウンを行う
'''

import time
from datetime import datetime as dt
import dateutil.parser
import schedule

from pprint import pprint

import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv

'''
Original Modules
'''
# import holo_sql
# from Components.tweet import tweet_components
# from Components.holo_date import HoloDate
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from sqlalchemy import func, extract
from model import HoloProfile
from model.setting import session


def Main():
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

def birthday(date_time: dt):
    # DBからidを検索
    print(date_time.month)
    return session.query(HoloProfile).filter(func.month(HoloProfile.birthday) == date_time.month).all()

if __name__ == '__main__':

    # 毎時0分に実行
    # schedule.every().hour.at(":46").do(Main)
    # schedule.every().hour.at(":15").do(Main)

    # # # PM00:05 AM12:05にjob実行
    # schedule.every().day.at("15:00").do(Main)
    # schedule.every().day.at("12:00").do(Main)
    # schedule.every().day.at("17:30").do(Main)
    # schedule.every().day.at("08:00").do(Main)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    w = birthday(dt.now())
    pprint(w)
    pprint('what')