import pandas as pd
import requests
from retrying import retry

import time

'''
Google SDK
'''
from apiclient.discovery import build
from apiclient.errors import HttpError

import os
from os.path import join, dirname
from dotenv import load_dotenv

from pprint import pprint

'''
Original Modules
'''
from Components.lines import lines


class Youtube_API:

    def __init__(self):
        pass


    """
    エラー処理s
    """
    def error_catch(self, error):
        print("NG ", error)


    @retry(stop_max_attempt_number=5, wait_fixed=5000)
    def channelInfo(self, youtubeObject, CHANNEL_ID):
        """
        チャンネルの内容を返す
        @param youtubeObject 
        @param CHANNEL_ID
        @return dict
        """
        return  youtubeObject.channels().list(part = 'snippet,statistics',id = CHANNEL_ID).execute() 
        # try:
        #     return  youtubeObject.channels().list(part = 'snippet,statistics',id = CHANNEL_ID).execute() 
        # except ConnectionResetError as err:
        #     pprint(err)
        #     print('channelInfoエラー')
        #     time.sleep(10)
        #     pass


    def getVideoList(self, youtubeObject, CHANNEL_ID, NextPageToken):
        """
        特定チャンネル内の動画一覧を取得(一度に最高500件まで)
        @param youtubeObject 
        @param video_ID
        @return dict
        """
        # チャンネル内の動画をリサーチメソッド
        return youtubeObject.search().list(
                part = "snippet",
                channelId = CHANNEL_ID,
                type = 'video',
                # eventType = 'completed',    # 'completed':完了したブロードキャストのみ　'live':アクティブなブロードキャストのみ  'upcoming':今後配信予定のブロードキャスト、live中を取得可能
                maxResults = 50,
                order = "date", #日付順にソート
                pageToken = NextPageToken #再帰的に指定
                ).execute()  


    @retry(stop_max_attempt_number=5, wait_fixed=5000)
    def videoInfo(self, youtubeObject, video_ID):
        """
        動画の内容を返す
        @param youtubeObject 
        @param video_ID
        @return youtubeObject.videos().list() video情報
        """
        return youtubeObject.videos().list(
                part = 'snippet,statistics,liveStreamingDetails',    #snippetがデフォ,liveStreamingDetailsにするとライブ開始予定時間が取得できる
                id = video_ID
                ).execute()
        # try:
        #     return youtubeObject.videos().list(
        #             part = 'snippet,statistics,liveStreamingDetails',    #snippetがデフォ,liveStreamingDetailsにするとライブ開始予定時間が取得できる
        #             id = video_ID
        #             ).execute()
        # except TimeoutError as time_err:
        #     print('videoInfoエラー')
        #     pprint(time_err)
        # except HttpError as err:
        #     print ("videoInfoエラー An HTTP error {} occurred: {}").format(err.resp.status, err.content)
        # except ConnectionResetError as connect_err:
        #     print('videoInfoエラー')
        #     pprint(connect_err)


    def getLiveStartTime_JT(youtubeObject, video_id:str):
        """
        動画IDからライブ開始時間または投稿時間を取得
        liveStreamingDetails.actualStartTime　（ライブ開始時間）
        liveStreamingDetails.scheduledStartTime　（ライブ開始予定時間）
        liveStreamingDetails.actualEndTime　（ライブ終了時間）
        liveStreamingDetails.concurrentViewers　（リアルタイム視聴者数）
        liveStreamingDetails.activeLiveChatId　（チャット取得用ID）
        """
        video_time_datas = {}
        #　動画内容をリサーチメソッド
        video_response = youtubeObject.videos().list(
            part = 'snippet,statistics,liveStreamingDetails',    #snippetがデフォ,liveStreamingDetailsにするとライブ開始予定時間が取得できる
            id = video_id
            ).execute()

        video_result = video_response.get("items", [])
        if video_result[0]["kind"] == "youtube#video":
            if video_result[0].get('liveStreamingDetails',False):
                video_time_datas['scheduledStartTime'] = video_result[0]['liveStreamingDetails'].get('scheduledStartTime',None), #ライブ開始予定時間
                video_time_datas['actualStartTime'] = video_result[0]['liveStreamingDetails'].get('liveStreamingDetails',None), #ライブ開始時間
                video_time_datas['actualEndTime'] = video_result[0]['liveStreamingDetails'].get('actualEndTime',None), #ライブ終了時間
                video_time_datas['concurrentViewers'] = video_result[0]['liveStreamingDetails'].get('concurrentViewers',None), #リアルタイム視聴者数
                return video_time_datas
            else:
                video_time_datas['publishedAt'] = video_result[0]['snippet']['publishedAt']   #投稿の場合はこちら,投稿された時間を取得
                return  video_time_datas
        else:
            pprint('エラー発生')
            return  video_time_datas


    @retry(stop_max_attempt_number=5, wait_fixed=500)
    def get_chat(youtubeObject, CHAT_ID:str, PAGE_TOKEN):
        """
        チャット内容を取得する
        """
        try:
            if type(PAGE_TOKEN) == str:
                return youtubeObject.liveChatMessages().list(
                        liveChatId=CHAT_ID,
                        pageToken=PAGE_TOKEN,
                        maxResults=2000,
                        part='id,snippet,authorDetails'
                        ).execute()
        except HttpError as err:
            pprint(err)
            pprint('liveが取得できません。LIVEは終了しているようです')
            return False

        # try:                                                                                                                                                                                                                                                                                                                                                                                                     
        #     for item in data['items']:
        #         channelId = item['snippet']['authorChannelId']
        #         msg       = item['snippet']['displayMessage']
        #         usr       = item['authorDetails']['displayName']
        #         supChat   = item['snippet'].get('superChatDetails', 'supChat:none')
        #         supStic   = item['snippet'].get('superStickerDetails', 'supStic:none')
        #         log_text  = '[{} : by {} https://www.youtube.com/channel/{}]\n{} [{},{}]'.format(chat_time, usr, channelId, msg, supChat,supStic)
        #         with open(log_file, 'a') as f:
        #             print(log_text, file=f)
        #             print(log_text)
        #     print('start : ', data['items'][0]['snippet']['publishedAt'])
        #     print('end   : ', data['items'][-1]['snippet']['publishedAt'])

        # except Exception as err:
        #     print(err)

        # return data['nextPageToken']