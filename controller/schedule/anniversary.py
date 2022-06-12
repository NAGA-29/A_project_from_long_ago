'''
指定された日までのカウントダウンを行う
'''
from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv
import os
from os.path import join, dirname
from pprint import pprint
import sys
import schedule
from typing import List, Dict, Union

'''
Original Modules
'''
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from Components.tweet import tweet_components
from Components.holo_date import HoloDate
from sqlalchemy import func, extract
from model.setting import session
from model import HoloOverSeaProfile, HoloProfile
# from model import 

'''
誕生日判定

@param target: 指定日数 datetime
@param MODEL: モデル object
@return: 誕生日のメンバーリスト list
'''
def birthday(target:datetime, MODEL)->list:
    d = session.query(MODEL).filter(func.date_format(MODEL.birthday, '%m-%d') == target.strftime('%m-%d')).all()
    return d

'''
デビュー判定

@param target: 指定日数 object
@param MODEL: モデル object
@return: デビュー日のメンバーリスト list
'''
def debut(target:datetime, MODEL):
    d = session.query(MODEL).filter(func.date_format(MODEL.debut, '%m-%d') == target.strftime('%m-%d')).all()
    return d

'''
数字から日付へ変換

@param target: 日付を表す数字 int
@return: datetime object
'''
def convert_challenge(target:int)->datetime:
    if target == 0:
        return datetime.today()
    else:
        return datetime.today() + timedelta(days=target)

'''
記念日通知

@param target_days: 日付リスト list[int]
@param tweet: tweet_components インスタンス
@param *args: モデルクラス tuple
@return: None
'''
def anniversary(target_days:List[int], tweet:tweet_components, *args)->None:
    for MODEL in args:
        for target in target_days:
            date = convert_challenge(target)
            message = f'Hololive Anniversary テスト中\n\n'

            members = birthday(date, MODEL) # 誕生日
            if members :
                for mem in members:
                    if target is 0:
                        message += f'本日は{mem.holo_name}さんの誕生日です!\n\n'
                    else:
                        message += f'{target}日後は{mem.holo_name}ちゃんの誕生日です!\n\n'
                    tweet.tweet(message)

            member = debut(date, MODEL) # デビュー
            if member:
                for mem in members:
                    if target is 0:
                        message += f'本日は{mem.holo_name}さんのデビュー日です!\n\n'
                    else:
                        message += f'{target}日後は{mem.holo_name}ちゃんのデビュー日です!\n\n'
                    tweet.tweet(message)



if __name__ == '__main__':
    # # # PM00:05 AM12:05にjob実行
    # schedule.every().day.at("15:00").do(anniversary)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    target_list = [0, 5] #0日後(今日), 7日後
    tw = tweet_components()
    anniversary(target_list, tw, HoloProfile, HoloOverSeaProfile)
