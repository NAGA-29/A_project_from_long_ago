import tweepy
import csv
import sys 
import time
import datetime
from datetime import datetime as dt
import pytz
import pandas as pd
import schedule

import os
from os.path import join, dirname
from dotenv import load_dotenv

from pprint import pprint


# original modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from Components.vtuber.hololive import Hololive
from Components.vtuber.noripro import NoriPro
import holo_sql
from Components.tweet import tweet_components


load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../../../.env')
load_dotenv(dotenv_path)

##twitterテストアカウント----------------
# CONSUMER_KEY = os.environ.get('CONSUMER_KEY_TEST')
# CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET_TEST')
# ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN_TEST')
# ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET_TEST')
##twitterアカウント----------------
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
# MyNoriP　アカウント用
CONSUMER_KEY_B = os.environ.get('CONSUMER_KEY_B')
CONSUMER_SECRET_B = os.environ.get('CONSUMER_SECRET_B')
ACCESS_TOKEN_B = os.environ.get('ACCESS_TOKEN_B')
ACCESS_TOKEN_SECRET_B = os.environ.get('ACCESS_TOKEN_SECRET_B')
# ------------------------------------
auth = tweepy.OAuthHandler(CONSUMER_KEY , CONSUMER_SECRET )
auth.set_access_token(ACCESS_TOKEN , ACCESS_TOKEN_SECRET)
tw = tweepy.API(auth)


#th_val人刻みでツイートするための条件設定。th_val = 10000 なら10000人刻み
def subJudge(tw_subscriber, value, belongs)->bool:
    sub_val = 0
    if belongs == 'hololive':
        sub_val = 50000
    elif belongs == 'noripro':
        sub_val = 10000

    if (tw_subscriber // sub_val)  > (value[0]['twitter_subscriber'] // sub_val):
        return True
    else:
        return False

def twitter_subscriber(belongs):
    hSql = holo_sql.holo_sql()
    Holo_twitter = Hololive.get_twitter_ids()
    Nori_twitter = NoriPro.get_twitter_ids()

    Holo_JP, Holo_OSea = Hololive.get_video_ids()
    Nori_Pro = NoriPro.get_video_ids()
    Twitter_Account_Holo = [Holo_JP, Holo_OSea,]
    Twitter_Account_Nori = [Nori_Pro]

    if belongs == 'hololive':
        for Account in Twitter_Account_Holo:
            for Name, channel_ID in Account.items():
                # =======================
                followers_count = ''
                profile = None
                message = ''
                # =======================
                try:
                    user_info = tw.get_user(Holo_twitter[Name])
                except KeyError as err:
                    pprint(err)
                    continue
                except tweepy.TweepError as err:
                    pprint(err)
                    continue
                followers_count = user_info.followers_count  # follower数の取得

                if Account == Holo_JP:  # Hololive
                    profile = hSql.selectHolo(channel_ID)
                    if subJudge(followers_count, profile, belongs):
                        tweet = tweet_components(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

                        message = '速報！\n{}✨\n{}\n\n<twitter>フォロワー数が\n【{}万人】到達!🔥\n\nおめでとうございます！\n\nデビュー日:{}\n誕生日:{}\n{}'.format(
                            Name, profile[0]['live_tag'], (int(followers_count)//10000), 
                            profile[0]['debut'].strftime('%Y/%m/%d'),
                            profile[0]['birthday'].strftime('%m/%d'),
                            'twitter.com/'+Holo_twitter[Name],)
                        
                        tweet.sub_tweetWithIMG(message, profile[0]['image1'])
                        pprint(message)
                        hSql.insert_HoloJP_ProfileTable_tw(channel_ID, followers_count)

                elif Account == Holo_OSea:  # Hololive 海外
                    profile = hSql.selectOSHolo(channel_ID)
                    if subJudge(followers_count, profile, belongs):
                        tweet = tweet_components(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

                        message = '速報！\n{}✨\n{}\n\n<twitter>フォロワー数が\n【{}万人】到達!🔥\nおめでとうございます！\n\nデビュー日:{}\n誕生日:{}\n{}'.format(
                            Name, profile[0]['live_tag'], (int(followers_count)//10000),
                            profile[0]['debut'].strftime('%Y/%m/%d'),
                            profile[0]['birthday'].strftime('%m/%d'),
                            'twitter.com/'+Holo_twitter[Name],)

                        tweet.sub_tweetWithIMG(message, profile[0]['image1'])
                        pprint(message)
                        hSql.insert_HoloOS_ProfileTable_tw(channel_ID, followers_count)

    elif belongs == 'noripro':
        for Account in Twitter_Account_Nori:
            for Name, channel_ID in Account.items():
                # =======================
                followers_count = ''
                profile = None
                message = ''
                # =======================
                try: 
                    user_info = tw.get_user(Nori_twitter[Name])
                except KeyError as err:
                    pprint(err)
                    continue
                followers_count = user_info.followers_count  # follower数の取得

                profile = hSql.selectFriendsHolo(channel_ID)
                if subJudge(followers_count, profile, belongs):
                    tweet = tweet_components(CONSUMER_KEY_B, CONSUMER_SECRET_B, ACCESS_TOKEN_B, ACCESS_TOKEN_SECRET_B)

                    message = '速報！\n{}✨\n{}\n\n<twitter>フォロワー数が\n【{}万人】到達!🔥\nおめでとうございます！\n{}'.format(
                        Name, profile[0]['live_tag'], (int(followers_count)//10000),
                        'twitter.com/'+Nori_twitter[Name],)

                    tweet.sub_tweetWithIMG(message, profile[0]['image1'])
                    pprint(message)
                    hSql.insert_HoloFri_ProfileTable_tw(channel_ID, followers_count)

def main():
    twitter_subscriber('hololive')
    twitter_subscriber('noripro')


# # schedule.every().day.at("15:17").do(main)
# schedule.every().hour.at(":00").do(main)
# schedule.every().hour.at(":15").do(main)
# schedule.every().hour.at(":30").do(main)
# schedule.every().hour.at(":45").do(main)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
