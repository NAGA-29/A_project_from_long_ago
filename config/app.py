import sys 
import os
from os.path import join, dirname
from dotenv import load_dotenv

from pprint import pprint

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../env')
load_dotenv(dotenv_path)


''' 
フォルダ 
'''
# サムネフォルダ
live_tmb_img_dir = os.path.join(os.path.dirname(__file__), '../'+ os.environ.get('LIVE_TMB_IMG_DIR'))
LIVE_TMB_IMG_DIR = os.path.normpath(live_tmb_img_dir) + '/'


# テンポラリーフォルダ
live_tmb_tmp_dir = os.path.join(os.path.dirname(__file__), '../'+ os.environ.get('LIVE_TMB_TMP_DIR'))
LIVE_TMB_TMP_DIR = os.path.normpath(live_tmb_tmp_dir) + '/'


# のりプロサムネフォルダ 
noripro_live_tmb_tmp_dir = os.path.join(os.path.dirname(__file__), '../'+ os.environ.get('NoriP_LIVE_TMB_TMP_DIR'))
NORIPRO_LIVE_TMB_TMP_DIR = os.path.normpath(noripro_live_tmb_tmp_dir) + '/'


# その他テンポラリーフォルダ
other_tmb_tmp_dir = os.path.join(os.path.dirname(__file__), '../'+ os.environ.get('OTHER_TMB_TMP_DIR'))
OTHER_TMB_TMP_DIR = os.path.normpath(other_tmb_tmp_dir) + '/'


# トリム画像フォルダ
img_trim_dir = os.path.join(os.path.dirname(__file__), '../'+ os.environ.get('IMG_TRIM_DIR'))
IMG_TRIM_DIR = os.path.normpath(img_trim_dir) + '/'


# プロフィール画像フォルダ
profile_img_dir= os.path.join(os.path.dirname(__file__), os.environ.get('PROFILE_IMG_DIR'))
PROFILE_IMG_DIR = os.path.normpath(profile_img_dir) + '/'
# pprint(PROFILE_IMG_DIR)

# イベント画像フォルダ
event_img_dir = os.path.join(os.path.dirname(__file__), os.environ.get('EVENT_IMG_DIR'))
EVENT_IMG_DIR = os.path.normpath(event_img_dir) + '/'


# スクリーンショット画像フォルダ
screenshot_dir = os.path.join(os.path.dirname(__file__), '../'+ os.environ.get('SCREENSHOT_DIR'))
SCREENSHOT_DIR = os.path.normpath(screenshot_dir) + '/'


# コンビネーション画像フォルダ
combine_img_dir = os.path.join(os.path.dirname(__file__), '../'+ os.environ.get('COMBINE_IMG_DIR'))
COMBINE_IMG_DIR = os.path.normpath(combine_img_dir) + '/'



'''
google driver
''' 
google_driver = os.path.join(os.path.dirname(__file__), '../'+ os.environ.get('DRIVER_PATH'))
GOOGLE_DRIVER = os.path.normpath(google_driver) + '/'



'''
Twitch api

# Client
# Secret
''' 
TWITCH_CLIENT = os.environ.get('TWITCH_CLIENT')

TWITCH_SECRET = os.environ.get('TWITCH_SECRET')

'''
Discord api

# Token
''' 
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')


'''
Line api

# Token
''' 
LINE_NOTIFY_TOKEN = os.environ.get('LINE_NOTIFY_TOKEN')


'''
Twitter api

# Consumer Key
# Consumer Secret Key
# Access Token 
# Access Token Secret

1.test
2.My_Hololive_Project
3.My_HoloNoriArts_Project
4.NoriUi_Project
''' 
#twitterテスト
CONSUMER_KEY_TEST = os.environ.get('CONSUMER_KEY_TEST')
CONSUMER_SECRET_TEST = os.environ.get('CONSUMER_SECRET_TEST')
ACCESS_TOKEN_TEST = os.environ.get('ACCESS_TOKEN_TEST')
ACCESS_TOKEN_SECRET_TEST = os.environ.get('ACCESS_TOKEN_SECRET_TEST')
# My_Hololive_Project
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
# My_HoloNoriArts_Project
CONSUMER_KEY_A = os.environ.get('CONSUMER_KEY_A')
CONSUMER_SECRET_A = os.environ.get('CONSUMER_SECRET_A')
ACCESS_TOKEN_A = os.environ.get('ACCESS_TOKEN_A')
ACCESS_TOKEN_SECRET_A = os.environ.get('ACCESS_TOKEN_SECRET_A')
BEARER_TOKEN_A = os.environ.get('BEARER_TOKEN_A')
# NoriUi_Project
CONSUMER_KEY_B = os.environ.get('CONSUMER_KEY_B')
CONSUMER_SECRET_B = os.environ.get('CONSUMER_SECRET_B')
ACCESS_TOKEN_B = os.environ.get('ACCESS_TOKEN_B')
ACCESS_TOKEN_SECRET_B = os.environ.get('ACCESS_TOKEN_SECRET_B')
BEARER_TOKEN_B =  os.environ.get('BEARER_TOKEN_B')

'''
Youtube api

#Hololive-Project

# 開発用
# Hololive-project-videolist
#　Hololive-Project-Sub01
#　Hololive-Project-Sub02
#　Hololive-Project-Sub03
''' 
YOUTUBE_API_KEY01 =  os.environ.get('YOUTUBE_API_KEY01')

# 開発用
# Hololive-project-videolist
YOUTUBE_API_KEY_DEV1 =  os.environ.get('YOUTUBE_API_KEY_dev1')
#　Hololive-Project-Sub01
YOUTUBE_API_KEY_DEV2 =  os.environ.get('YOUTUBE_API_KEY_dev2')
#　Hololive-Project-Sub02
YOUTUBE_API_KEY_DEV3 =  os.environ.get('YOUTUBE_API_KEY_dev3')
#　Hololive-Project-Sub03
YOUTUBE_API_KEY_DEV4 =  os.environ.get('YOUTUBE_API_KEY_dev4')


'''
Bitly api

Access Token
''' 
BITLY_ACCESS_TOKEN =  os.environ.get('BITLY_ACCESS_TOKEN')


'''
News api
''' 
NEWS_API =  os.environ.get('NEWS_API')