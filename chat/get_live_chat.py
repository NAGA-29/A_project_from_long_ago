'''
https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list
youtube chat取得
'''
import csv
import requests
import json
from apiclient.discovery import build
from apiclient.errors import HttpError

import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv

import time
from datetime import datetime as dt

from pprint import pprint

# original
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import holo_sql
from YoutubeAPI.YoutubeAPI import Youtube_API as yApi

# Initial Setting
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

_API_KEY = 'YOUTUBE_API_KEY_dev4'
_api_number = 1

API_KEY = os.environ.get(_API_KEY)
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtubeObject = build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
    )




# def get_chat_id(yt_url):
#     '''
#     https://developers.google.com/youtube/v3/docs/videos/list?hl=ja
#     '''
#     video_id = yt_url.replace('https://www.youtube.com/watch?v=', '')
#     print('video_id : ', video_id)

#     url    = 'https://www.googleapis.com/youtube/v3/videos'
#     params = {'key': YT_API_KEY, 'id': video_id, 'part': 'liveStreamingDetails'}
#     data   = requests.get(url, params=params).json()

#     liveStreamingDetails = data['items'][0]['liveStreamingDetails']
#     if 'activeLiveChatId' in liveStreamingDetails.keys():
#         chat_id = liveStreamingDetails['activeLiveChatId']
#         print('get_chat_id done!')
#     else:
#         chat_id = None
#         print('NOT live')

#     return chat_id




def get_chat(chat_id, pageToken, log_file):
    '''
    https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list
    '''
    YT_API_KEY = 'AIzaSyByQJU3eIImAtHdHr6W9_xd9fO7K-Qn9to'
    url    = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
    params = {'key': YT_API_KEY, 'liveChatId': chat_id, 'part': 'id,snippet,authorDetails'}
    if type(pageToken) == str:
        params['pageToken'] = pageToken

    data   = requests.get(url, params=params).json()

    try:                                                                                                                                                                                                                                                                                                                                                                                                     
        for item in data['items']:
            chat_time = item['snippet']['publishedAt']
            channelId = item['snippet']['authorChannelId']
            msg       = item['snippet']['displayMessage']
            usr       = item['authorDetails']['displayName']
            supChat   = item['snippet'].get('superChatDetails', 'none')
            supStic   = item['snippet'].get('superStickerDetails', 'none')
            log_text  = '[{} : by {} https://www.youtube.com/channel/{}]\n{} [{},{}]'.format(chat_time, usr, channelId, msg, supChat,supStic)
            with open(log_file, 'a') as f:
                print(log_text, file=f)
                print(log_text)
        print('start : ', data['items'][0]['snippet']['publishedAt'])
        print('end   : ', data['items'][-1]['snippet']['publishedAt'])

    except Exception as err:
        print(err)

    return data['nextPageToken']




# def main(yt_url):
#     slp_time        = 10 #sec
#     iter_times      = 90 #回
#     take_time       = slp_time / 60 * iter_times
#     print('{}分後　終了予定'.format(take_time))
#     print('work on {}'.format(yt_url))

#     log_file = yt_url.replace('https://www.youtube.com/watch?v=', '') + '.txt'
#     with open(log_file, 'a') as f:
#         print('{} のチャット欄を記録します。'.format(yt_url), file=f)
#     chat_id  = get_chat_id(yt_url)

#     nextPageToken = None
#     for ii in range(iter_times):
#         #for jj in [0]:
#         try:
#             print('\n')
#             nextPageToken = get_chat(chat_id, nextPageToken, log_file)
#             time.sleep(slp_time)
#         except:
#             break




if __name__ == '__main__':
    # yt_url = input('Input YouTube URL > ')
    # main(yt_url)

    nextPageToken = ''

    while True:
        # chat_idは　@TODO dbから取得
        # hsql = holo_sql.holo_sql()
        """本番用"""
        # live_info = hsql.selectAllLiveTable()
        # file_name = live_info[4] + '.csv'
        """テスト"""
        video_id = 'LAVJjIu03mA'
        file_name = './chat_csv/' + video_id  + '.csv'

        CHAT_ID = 'Cg0KC0xBVkpqSXUwM21BKicKGFVDaEFucWNfQVk1X0kzUHg1ZGlnM1gxURILTEFWSmpJdTAzbUE'
        messages = yApi.get_chat(youtubeObject, CHAT_ID, nextPageToken)

        if messages:
            for message in messages['items']:
                chat_time = message['snippet']['publishedAt']
                user_id = message['snippet']['authorChannelId']
                msg       = message['snippet']['displayMessage']
                usr       = message['authorDetails']['displayName']

                super_Chat = ''
                super_Chat_currency = ''
                super_Chat_comment = ''
                super_Stic = ''
                super_Stic_currency = ''
                super_Stic_comment = ''

                if message['snippet'].get('superChatDetails', None):
                    """ス-パ-チャット"""
                    super_Chat = message['snippet']['superChatDetails']['amountMicros']
                    super_Chat_currency = message['snippet']['superChatDetails']['currency']
                    super_Chat_comment = message['snippet']['superChatDetails'].get('userComment', '') # コメントなし対策

                if message['snippet'].get('superStickerDetails', None):
                    """ス-パ-ティッカー"""
                    supStic = message['snippet']['superStickerDetails']['amountMicros']
                    supStic_currency = message['snippet']['superStickerDetails']['currency']
                    supStic_comment = message['snippet']['superStickerDetails'].get('userComment', '') # コメントなし対策

                with open (file_name, 'a', encoding='utf-8') as ff:
                    fields = [
                        'chat_time', 
                        'user', 'user_id', 'msg', 
                        'super_Chat', 'super_Chat_currency', 'super_Chat_comment',
                        'super_Stic', 'super_Stic_currency', 'super_Stic_comment',
                        ]
                    writer = csv.DictWriter(ff, fieldnames = fields)
                    writer.writerow({
                        'chat_time': chat_time, 
                        'user': usr, 
                        'user_id': user_id, 
                        'msg': msg,
                        'super_Chat': super_Chat,
                        'super_Chat_currency': super_Chat_currency,
                        'super_Chat_comment': super_Chat_comment,
                        'super_Stic': supStic,
                        'super_Stic_currency':  supStic_currency,
                        'super_Stic_comment': supStic_comment,
                        })
            nextPageToken = messages['nextPageToken']
            try:
                pprint('start : ' + messages['items'][0]['snippet']['publishedAt'])
                pprint('end   : ' + messages['items'][-1]['snippet']['publishedAt'])
            except IndexError as err:
                pprint('チャットは閉じられました')
                break
            pprint(nextPageToken)
            pprint('一時停止')

            hSql = holo_sql.holo_sql()
            live_now = hSql.select(video_id)
            if live_now:
                if live_now[0][9] <= 20000:
                    print('sleep 15sec')
                    time.sleep(15)
                elif 40000 > live_now[0][9] >= 20001:
                    print('sleep 10sec')
                    time.sleep(10)
                else:
                    print('sleep 5sec')
                    time.sleep(5)
            else:
                pprint('DBに動画が存在しません')
            hSql.dbClose()
            hSql = None
            # time.sleep(30)
        else:
            break
