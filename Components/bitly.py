import requests

import os
from os.path import join, dirname
from dotenv import load_dotenv
from pprint import pprint

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#bitly本番アカウント
ACCESS_TOKEN = os.environ.get('BITLY_ACCESS_TOKEN')
# 予備
# ACCESS_TOKEN = os.environ.get('SECOND_BITLY_ACCESS_TOKEN')


'''
Bitly(url短縮サービス)_
'''
def get_shortenURL(longUrl:str):

    url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {"Authorization":'Bearer {}'.format(ACCESS_TOKEN),
                "Host": "api-ssl.bitly.com",
                "Accept":"application/json",
                "Content-Type": "application/json"
                }
    query = {
            "long_url":longUrl,
            "group_guid": 'Bj2abspuUWA',
            "domain": "bit.ly"
            }

    r = requests.post(url, json= query, headers= headers)
    return r.json()['link']


'''
Youtube専用 短縮URL
'''
def make_yURL(l_URL:str):
    if type(l_URL) is bytes:
        l_URL = l_URL.decode('utf-8')
<<<<<<< HEAD
=======
        pprint(l_URL)
>>>>>>> 821c066f681c233ddc947df98390e4a9d1f391f3
    _list = l_URL.split('=')
    return 'https://youtu.be/' + _list[1]
