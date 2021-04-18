from PIL import Image
import tweepy

from pprint import pprint

import os
from os.path import join, dirname
from dotenv import load_dotenv


load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#twitter本番アカウント
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(auth)



def tweetWithIMG()->bool:
    """
    ツイートメソッド 画像付き url分解機能
    """
    #ツイート内容
    TWEET_TEXT = '画像変更っス！テストっス！！！'
    try :
        # ↓添付したい画像のファイル名
        FILE_NAME = 'renketu_test.jpg'
        tweet_status = API.update_with_media(filename=FILE_NAME, status=TWEET_TEXT)
        if tweet_status == 200: #成功
            pprint("Succeed!")
            result = True
        else:
            result = False
    except Exception as e:
            pprint(e)
            result = False
    return result




im1 = Image.open('./Trim_Images/IMG_6D3F3ABB2313-1.jpg')
im2 = Image.open('./Trim_Images/VW6SVPIiIvU.jpg')

# def get_concat_h(im1, im2):
#     dst = Image.new('RGB', (im1.width + im2.width, im1.height))
#     dst.paste(im1, (0, 0))
#     dst.paste(im2, (im1.width, 0))
#     return dst

# def get_concat_v(im1, im2):
#     dst = Image.new('RGB', (im1.width, im1.height + im2.height))
#     dst.paste(im1, (0, 0))
#     dst.paste(im2, (0, im1.height))
#     return dst


def get_concat_v(oldImg, newImg):
    im1 = Image.open(oldImg)
    im2 = Image.open(newImg)
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

# get_concat_h(im1, im2).save('renketu_test.jpg')
get_concat_v(im1, im2).save('renketu_test.jpg')
tweetWithIMG()