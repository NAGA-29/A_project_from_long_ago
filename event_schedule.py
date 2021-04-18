'''
指定された日までのカウントダウンを行う
'''

import time
from datetime import datetime as dt
import dateutil.parser
import schedule

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

def Main():
    hSql = holo_sql.holo_sql()
    tw = tweet_components()
    hDate = HoloDate()
    message = ''

    dt_now = dt.now()
    all_schedules = hSql.selectEventSchedulesTable()
    for schedule in all_schedules:
        if schedule[4]:
            time_lag = schedule[4] - dt_now
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
                    message = '{}まで\nあと{}日と{}時間!!✨\n{}✨'.format(schedule[2],day,hours,schedule[5])
                    tw.event_tweetWithIMG(message,schedule[6])
                    pprint(message)
                else:
                    '''
                    hours == 1                 予定時間まで1時間以上時間がある場合
                    hours == 0 and min > 1     1時間以内かつ1分以上ある場合
                    その他                      1分未満かつ0秒以上ある場合(何もしない)
                    '''
                    if hours >= 1:
                        message = '{}まで\nあと「{}時間{}分」!!✨\n{}✨'.format(schedule[2],hours,min,schedule[5])
                        tw.event_tweetWithIMG(message,schedule[6])
                        pprint(message)
                    elif hours == 0 and min > 1:
                        message = '{}まで\nあと{}分!!✨\n{}✨'.format(schedule[2],min,schedule[5])
                        tw.event_tweetWithIMG(message,schedule[6])
                        pprint(message)
                    else:
                        hSql.updateStatus_SchedulesTable(schedule[4])
                        pass

            else:
                hSql.updateStatus_SchedulesTable(schedule[4])
                pprint('予定時間を過ぎています')
                # 予定まで24時間を切った場合

# 毎時0分に実行
# schedule.every().hour.at(":46").do(Main)
schedule.every().hour.at(":10").do(Main)

# # PM00:05 AM12:05にjob実行
# schedule.every().day.at("00:05").do(Main)
# schedule.every().day.at("12:05").do(Main)
# schedule.every().day.at("20:00").do(Main)
# schedule.every().day.at("08:00").do(Main)

while True:
    schedule.run_pending()
    time.sleep(1)