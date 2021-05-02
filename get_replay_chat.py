'''
https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list
youtube archive　chat取得
'''
from bs4 import BeautifulSoup
import requests
import json
import csv
from retrying import retry

import os
from os.path import join, dirname
from dotenv import load_dotenv

import time
from datetime import datetime as dt

from pprint import pprint

'''
Google SDK
'''
from apiclient.discovery import build
from apiclient.errors import HttpError

'''
Original
'''
import holo_sql
from YoutubeAPI.YoutubeAPI import Youtube_API as yApi


'''
Initial Setting
'''
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


# target_url = youtube_url

class ContinuationURLNotFound(Exception):
    '''
    chat取得用のURLが取得出来なくなった場合使用
    '''
    pass

class LiveChatReplayDisabled(Exception):
    '''
    チャットのリプレイが出来ない場合に使用
    '''
    pass

class RestrictedFromYoutube(Exception):
    pass


def csvfileExists(holo_name:str, video_id:str)->bool:
    '''
    ファイルの存在をチェック
    '''
    file_path = './chat_csv/' + holo_name  + '/' + video_id + '.csv'
    return os.path.exists(file_path)

# def purseVideoInfo():
#     video_info_details = yApi.videoInfo(youtubeObject,video_ID).get("items", [])

if __name__ == '__main__':
    video_info_details = yApi.videoInfo(youtubeObject,'YDwzDiyXa-8')
    pprint(video_info_details)

# if not csvfileExists():

# def get_chat(chat_id, pageToken, log_file):
#     '''
#     https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list
#     '''
#     YT_API_KEY = 'AIzaSyByQJU3eIImAtHdHr6W9_xd9fO7K-Qn9to'
#     url    = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
#     params = {'key': YT_API_KEY, 'liveChatId': chat_id, 'part': 'id,snippet,authorDetails'}
#     if type(pageToken) == str:
#         params['pageToken'] = pageToken

#     data   = requests.get(url, params=params).json()

#     try:                                                                                                                                                                                                                                                                                                                                                                                                     
#         for item in data['items']:
#             chat_time = item['snippet']['publishedAt']
#             channelId = item['snippet']['authorChannelId']
#             msg       = item['snippet']['displayMessage']
#             usr       = item['authorDetails']['displayName']
#             supChat   = item['snippet'].get('superChatDetails', 'none')
#             supStic   = item['snippet'].get('superStickerDetails', 'none')
#             log_text  = '[{} : by {} https://www.youtube.com/channel/{}]\n{} [{},{}]'.format(chat_time, usr, channelId, msg, supChat,supStic)
#             with open(log_file, 'a') as f:
#                 print(log_text, file=f)
#                 print(log_text)
#         print('start : ', data['items'][0]['snippet']['publishedAt'])
#         print('end   : ', data['items'][-1]['snippet']['publishedAt'])

#     except Exception as err:
#         print(err)

#     return data['nextPageToken']




# # def main(yt_url):
# #     slp_time        = 10 #sec
# #     iter_times      = 90 #回
# #     take_time       = slp_time / 60 * iter_times
# #     print('{}分後　終了予定'.format(take_time))
# #     print('work on {}'.format(yt_url))

# #     log_file = yt_url.replace('https://www.youtube.com/watch?v=', '') + '.txt'
# #     with open(log_file, 'a') as f:
# #         print('{} のチャット欄を記録します。'.format(yt_url), file=f)
# #     chat_id  = get_chat_id(yt_url)

# #     nextPageToken = None
# #     for ii in range(iter_times):
# #         #for jj in [0]:
# #         try:
# #             print('\n')
# #             nextPageToken = get_chat(chat_id, nextPageToken, log_file)
# #             time.sleep(slp_time)
# #         except:
# #             break




# if __name__ == '__main__':
#     # yt_url = input('Input YouTube URL > ')
#     # main(yt_url)

#     nextPageToken = ''

#     while True:
#         # chat_idは　@TODO dbから取得
#         # hsql = holo_sql.holo_sql()
#         """本番用"""
#         # live_info = hsql.selectAllLiveTable()
#         # file_name = live_info[4] + '.csv'
#         """テスト"""
#         video_id = 'GG1auNklXsk'
#         file_name = './chat_csv/' + video_id  + '.csv'

#         CHAT_ID = 'Cg0KC0dHMWF1TmtsWHNrKicKGFVDLWhNNllKdU5ZVkFtVVd4ZUlyOUZlQRILR0cxYXVOa2xYc2s'
#         messages = yApi.get_chat(youtubeObject, CHAT_ID, nextPageToken)

#         if messages:
#             for message in messages['items']:
#                 chat_time = message['snippet']['publishedAt']
#                 channelId = message['snippet']['authorChannelId']
#                 msg       = message['snippet']['displayMessage']
#                 usr       = message['authorDetails']['displayName']

#                 supChat = ''
#                 supChat_currency = ''
#                 supChat_comment = ''
#                 supStic = ''
#                 supStic_currency = ''
#                 supStic_comment = ''

#                 if message['snippet'].get('superChatDetails', None):
#                     """ス-パ-チャット"""
#                     supChat = message['snippet']['superChatDetails']['amountMicros']
#                     supChat_currency = message['snippet']['superChatDetails']['currency']
#                     supChat_comment = message['snippet']['superChatDetails'].get('userComment', '') # コメントなし対策

#                 if message['snippet'].get('superStickerDetails', None):
#                     """ス-パ-ティッカー"""
#                     supStic = message['snippet']['superStickerDetails']['amountMicros']
#                     supStic_currency = message['snippet']['superStickerDetails']['currency']
#                     supStic_comment = message['snippet']['superStickerDetails'].get('userComment', '') # コメントなし対策

#                 with open (file_name,'a') as ff:
#                     fiels = [
#                         'chat_time', 'usr', 
#                         'channelId', 'msg', 
#                         'supChat', 'supChat_currency', 'supChat_comment',
#                         'supStic', 'supStic_currency', 'supStic_comment',
#                         ]
#                     writer = csv.DictWriter(ff, fieldnames = fiels)
#                     writer.writerow({
#                         'chat_time': chat_time, 
#                         'usr': usr, 
#                         'channelId': channelId, 
#                         'msg': msg,
#                         'supChat': supChat,
#                         'supChat_currency': supChat_currency,
#                         'supChat_comment': supChat_comment,
#                         'supStic': supStic,
#                         'supStic_currency':  supStic_currency,
#                         'supStic_comment': supStic_comment,
#                         })
#             nextPageToken = messages['nextPageToken']
#             try:
#                 pprint('start : ' + messages['items'][0]['snippet']['publishedAt'])
#                 pprint('end   : ' + messages['items'][-1]['snippet']['publishedAt'])
#             except IndexError as err:
#                 pprint('チャットは閉じられました')
#                 break
#             pprint(nextPageToken)
#             pprint('一時停止')

#             hSql = holo_sql.holo_sql()
#             live_now = hSql.select(video_id)
#             if live_now:
#                 if live_now[0][9] <= 20000:
#                     print('sleep 15sec')
#                     time.sleep(15)
#                 elif 40000 > live_now[0][9] >= 20001:
#                     print('sleep 10sec')
#                     time.sleep(10)
#                 else:
#                     print('sleep 5sec')
#                     time.sleep(5)
#             else:
#                 pprint('DBに動画が存在しません')
#             hSql.dbClose()
#             hSql = None
#             # time.sleep(30)
#         else:
#             break
