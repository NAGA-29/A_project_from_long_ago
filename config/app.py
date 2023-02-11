import sys 
import os
from os.path import join, dirname
from dotenv import load_dotenv

from pprint import pprint

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../env')
load_dotenv(dotenv_path)


''' 
ディレクトリ リスト
'''
# サムネフォルダ
live_tmb_img_dir = os.path.join(os.path.dirname(__file__), '../src/live_thumbnail_image/')
LIVE_TMB_IMG_DIR = os.path.normpath(live_tmb_img_dir) + '/'


# テンポラリーフォルダ
live_tmb_tmp_dir = os.path.join(os.path.dirname(__file__), '../src/live_temporary_image/')
LIVE_TMB_TMP_DIR = os.path.normpath(live_tmb_tmp_dir) + '/'


# のりプロサムネフォルダ 
noripro_live_tmb_tmp_dir = os.path.join(os.path.dirname(__file__), '../src/live_temporary_image_NoriP/')
NORIPRO_LIVE_TMB_TMP_DIR = os.path.normpath(noripro_live_tmb_tmp_dir) + '/'


# その他テンポラリーフォルダ
other_tmb_tmp_dir = os.path.join(os.path.dirname(__file__), '../src/other_temporary_image/')
OTHER_TMB_TMP_DIR = os.path.normpath(other_tmb_tmp_dir) + '/'


# トリム画像フォルダ
img_trim_dir = os.path.join(os.getcwd(), '../src/Trim_Images/')
IMG_TRIM_DIR = os.path.normpath(img_trim_dir) + '/'


# プロフィール画像フォルダ
profile_img_dir= os.path.join(os.getcwd(), '../src/Profile_Images/')
PROFILE_IMG_DIR = os.path.normpath(profile_img_dir) + '/'


# イベント画像フォルダ
event_img_dir = os.path.join(os.path.dirname(__file__), '../src/Event_Images/')
EVENT_IMG_DIR = os.path.normpath(event_img_dir) + '/'


# スクリーンショット画像フォルダ
screenshot_dir = os.path.join(os.path.dirname(__file__), '../storage/screenshot_image/')
SCREENSHOT_DIR = os.path.normpath(screenshot_dir) + '/'


# コンビネーション画像フォルダ
combine_img_dir = os.path.join(os.path.dirname(__file__), '../src/Combine_Image/')
COMBINE_IMG_DIR = os.path.normpath(combine_img_dir) + '/'

# holo data解析画像フォルダ
holo_data_img_dir = os.path.join(os.path.dirname(__file__), '../storage/holo_data_image/')
HOLO_DATA_IMG_DIR = os.path.normpath(holo_data_img_dir) + '/'

'''
chrome driver
''' 
# google_driver = os.path.join(os.path.dirname(__file__), '../'+ os.environ.get('DRIVER_PATH'))
google_driver = os.path.join(os.path.dirname(__file__), '../chromedriver')
GOOGLE_DRIVER = os.path.normpath(google_driver)

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
TWITTER_SCREEN_NAME = os.environ.get('TWITTER_SCREEN_NAME')

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


'''
地域番号
'''
WOEID_DICT = {'日本': 23424856,}

# WOEID_DICT = {'世界': 1, '日本': 23424856,
#             '東京': 1118370, '京都': 15015372, '大阪': 15015370,
#             '札幌': 1118108, '仙台': 1118129, '名古屋': 1117817, 
#             '神戸': 1117545, '広島': 1117227, '福岡': 1117099,
#             '埼玉': 1116753, '千葉': 1117034, '横浜': 1118550,
#             '川崎': 1117502, '相模原': 1118072, '北九州': 1110809,
#             '岡山': 90036018, '新潟': 1117881, '高松': 1118285,
#             '浜松': 1117155, '熊本': 1117605, '沖縄': 2345896
#             }

'''
トレンド検索で常に監視するワード
'''
DEFAULT_CHECK_LIST = ['#hololive','#ホロ鯖夏祭り']
CHECK_LIST = ['#hololive']