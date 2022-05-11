from datetime import datetime
import logging
from hypothesis import target
import tweepy
from datetime import datetime
from dotenv import load_dotenv
import os
from os.path import join, dirname
import pickle
import re
import sys
from logging import getLogger, StreamHandler, FileHandler, Formatter, \
                                DEBUG, INFO, WARNING, ERROR, CRITICAL
from pprint import pprint

'''
original module
'''
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from config import app 
from Components.tweet import tweet_components
from model import KeepWatch, NowLiveKeepWatch
from model.setting import session

class TrendWatcher:
    def __init__(self, twitter_api, lineAPI=None, logger=None, trend_save_file:str=None):
        self.TWITTER_API        = twitter_api
        self.SCREEN_NAME        = app.TWITTER_SCREEN_NAME # @usernameの自分のusername
        self.WOEID_DICT         = app.WOEID_DICT
        self.DEFAULT_CHECK_LIST = app.DEFAULT_CHECK_LIST
        self.CHECK_LIST         = app.CHECK_LIST
        self._NOTIFICATION_SEC = 3600   # 通知基準 60分
        self.TREND_SAVE_FILE    = '/Users/nagaki/Documents/naga-sample-code/python/MyHololiveProject_stg/My_Hololive_Project/config/trend_log_JP.pkl'
        if trend_save_file != None:
            self.TREND_SAVE_FILE = trend_save_file
        self.logger = logger


    """ 
    ツイートメソッド
    """
    def tweet(self, twitter_api:tweepy, message:str)->bool:
        #ツイート内容
        try :
            message += '\n' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tweet_status = twitter_api.update_status(message)
            if tweet_status == 200: #成功
                return True
            else:
                return False
        except TimeoutError as err:
                return False
        except tweepy.TweepError as err:
                return False


    '''
    タイトルからハッシュタグを抽出
    '''
    def hashtag_extract(self)->list:
        tags = ''
        hashtags = []
        # keep_watch_db = session.query(KeepWatch).all()
        now_live_keep_watch_db = session.query(NowLiveKeepWatch).filter(NowLiveKeepWatch.belongs == 'hololive').all()
        for data in now_live_keep_watch_db:
            tags = re.findall(r"([#＃][^#\s]*?)[\/\／\【\】\(\)\[\]　 \「\」]", data.title)
            for tag in tags:
                hashtags.append(re.sub('＃', '#', tag))
        return hashtags

    '''
    '''
    def check_notice_time(self, last_notice_time:str, sec:int)->bool:
        if (datetime.now() - last_notice_time).seconds >= sec:
            return True
        else:
            return False


    '''
    param defalt bool デフォルトのハッシュタグが含まれているか判定する
    '''
    def main(self, default=False):
        Read_Trend_log = {}
        Write_Trend_log = {}
        New_Trend = {}
        target_trend = self.hashtag_extract()
        
        if not target_trend and not default:
            return

        if default:
            target_trend = target_trend + self.DEFAULT_CHECK_LIST
        print(target_trend)

        try:
            with open(self.TREND_SAVE_FILE, 'rb') as f:
                Read_Trend_log = pickle.load(f)
                pprint(Read_Trend_log)
        except EOFError as err:
            # print(f'EOFError on load pickle file: {err}')
            self.logger.error(f'EOFError on load pickle file: {err}')
            
        for place, woeid in self.WOEID_DICT.items():
            trends = self.TWITTER_API.trends_place(woeid)

        rank = 0
        Reset_flag = True
        for tr in trends[0]['trends']:
            # pprint(tr)
            rank += 1
            # トレンドにキーワ-ドが出現した場合
            if tr['name'] in target_trend:
                tr['rank'] = rank
                tr['place'] = place
                name = tr['name']
                New_Trend[name] = tr #トレンドを追加
                print(f'{name}がトレンドにランクインしました')
                # self.logger.info(f'{name}がトレンドにランクインしました')
                Reset_flag = False

        if Reset_flag:
            # キーワ-ドが出現しなかったらリセット
            Read_Trend_log = []

        try:
            if Read_Trend_log: #前回のトレンドがある場合
                for key, value in Read_Trend_log.items():
                    message = f'Hololive Trend (β ver)\n\n'
                    message += f'{key}\n\n'

                    # 順位が1位になったか判定
                    if value['rank'] == 1:
                        Write_Trend_log[key] = New_Trend[key]
                        message += f'twitterトレンドランキング1位獲得!\n'
                        if self.check_notice_time(tr['last_notice_time'], self._NOTIFICATION_SEC):
                            # FIXME:
                            Write_Trend_log[key]['last_notice_time'] = datetime.now()
                            self.tweet(self.TWITTER_API, message)
                        continue

                    # 新規
                    if key not in New_Trend:
                        message += '新着トレンド入りです!\n'
                        Write_Trend_log[key] = New_Trend[key]
                        self.tweet(self.TWITTER_API, message)
                        print(f'{key}が新着トレンド入り')
                        continue

                    # 前回より順位上昇しているか判定
                    if value['rank'] > New_Trend[key]['rank']:
                        message += f'ランキング上昇!\n'
                        if self.check_notice_time(tr['last_notice_time'], 0):
                            # FIXME:
                            Write_Trend_log[key]['last_notice_time'] = datetime.now()
                            Write_Trend_log[key] = New_Trend[key]
                            self.tweet(self.TWITTER_API, message)
                            print(f'{key}がランキング上昇中!')
                        continue

                    # 前回より順位が急上昇しているか判定
                    if value['rank'] > New_Trend[key]['rank'] \
                            and value['rank'] - New_Trend[key]['rank'] >= 9:
                        message += f'ランキング急上昇中!\n'
                        Write_Trend_log[key] = New_Trend[key]
                        self.tweet(self.TWITTER_API, message)
                        print(f'{key}がランキング上昇中!')

            else: #前回のトレンドがない場合
                for key, value in New_Trend.items():
                    message = f'Hololive Trend (β ver)\n\n'
                    message += f'{key}\n\n'

                    # 順位が1位
                    if value['rank'] == 1:
                        Write_Trend_log[key] = New_Trend[key]
                        message += '新着トレンド入りです!\n'
                        message += f'twitterトレンドランキング1位獲得!\n'
                        # FIXME:
                        tr['last_notice_time'] = datetime.now()
                        self.tweet(self.TWITTER_API, message)
                        continue

                    # 新規
                    Write_Trend_log[key] = New_Trend[key]
                    message += '新着トレンド入りです!\n'
                    message += f'ランキング{value["rank"]}位獲得!\n'
                    self.tweet(self.TWITTER_API, message)

        # try:
            # pklファイルに保存
            pprint('pklファイルに保存')
            with open(self.TREND_SAVE_FILE, 'wb') as f:
                pickle.dump(Write_Trend_log, f)
        except Exception as err:
            print(f'ERROR on save pickle file: {err}')
            # self.logger.error(f'ERROR on save pickle file: {err}')


# # 本番アカウント
# # ###############################################################################
# CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
# CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
# ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
# ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

# auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# TWITTER_API = tweepy.API(auth)
# # ###############################################################################

# # 開発用アカウント
# # ###############################################################################
# CONSUMER_KEY_DEV = os.environ.get('CONSUMER_KEY_dev')
# CONSUMER_SECRET_DEV = os.environ.get('CONSUMER_SECRET_dev')
# ACCESS_TOKEN_DEV = os.environ.get('ACCESS_TOKEN_dev')
# ACCESS_TOKEN_SECRET_DEV = os.environ.get('ACCESS_TOKEN_SECRET_dev')

# auth = tweepy.OAuthHandler(CONSUMER_KEY_DEV, CONSUMER_SECRET_DEV)
# auth.set_access_token(ACCESS_TOKEN_DEV, ACCESS_TOKEN_SECRET_DEV)
# TWITTER_API_DEV = tweepy.API(auth)
# # ###############################################################################

# #ツイートしない
# @sched.scheduled_job('cron', minute='5,10,20,25,35,40,50,55', hour='*')
# def main_wo_tw():
#     try:
#         tw_switch = 0
#         tweet.twitter_trend_notification(tw_switch)
#     except Exception as e:
#         print('ERROR on twitter_trend_notification')
#         print(e)


# #ツイートする
# @sched.scheduled_job('cron', minute='0,15,30,45', hour='*')
# def main_w_tw():
#     try:
#         tw_switch = 1
#         tweet.twitter_trend_notification(tw_switch)
#     except Exception as e:
#         print('ERROR on twitter_trend_notification')
#         print(e)

# if __name__ == '__main__':
    # load_dotenv(verbose=True)
    # dotenv_path = join(dirname(__file__), '../../../.env')
    # load_dotenv(dotenv_path)
    # # ###############################################################################
    # CONSUMER_KEY_DEV = os.environ.get('CONSUMER_KEY_TEST')
    # CONSUMER_SECRET_DEV = os.environ.get('CONSUMER_SECRET_TEST')
    # ACCESS_TOKEN_DEV = os.environ.get('ACCESS_TOKEN_TEST')
    # ACCESS_TOKEN_SECRET_DEV = os.environ.get('ACCESS_TOKEN_SECRET_TEST')

    # auth = tweepy.OAuthHandler(CONSUMER_KEY_DEV, CONSUMER_SECRET_DEV)
    # auth.set_access_token(ACCESS_TOKEN_DEV, ACCESS_TOKEN_SECRET_DEV)
    # TWITTER_API_DEV = tweepy.API(auth)
    # ###############################################################################
    # TrendWatcher(TWITTER_API_DEV).main()