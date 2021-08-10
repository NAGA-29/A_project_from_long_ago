import pandas as pd
from apiclient.discovery import build
from apiclient.errors import HttpError
from pprint import pprint
import os
from os.path import join, dirname
from dotenv import load_dotenv
# import holo_sql

import time


class Youtube_API:
    """
        エラー処理
    """
    def error_catch(error):
        print("NG ", error)


    """
        チャンネルの内容を返す
        @param youtubeObject 
        @param CHANNEL_ID
        @return dict
    """
    def channelInfo(youtubeObject,CHANNEL_ID):
        return  youtubeObject.channels().list(part = 'snippet,statistics',id = CHANNEL_ID).execute()   


    """
        特定チャンネル内の動画一覧を取得(一度に最高500件まで)
        @param youtubeObject 
        @param video_ID
        @return dict
    """
    def videoInfo(youtubeObject,CHANNEL_ID,NextPageToken):
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


    """
        動画の内容を返す
        @param youtubeObject 
        @param video_ID
        @return dict
    """
    def videoInfo(youtubeObject,video_ID):
        return youtubeObject.videos().list(
                part = 'snippet,statistics,liveStreamingDetails',    #snippetがデフォ,liveStreamingDetailsにするとライブ開始予定時間が取得できる
                id = video_ID
                ).execute()


    """
        動画IDからライブ開始時間または投稿時間を取得
        liveStreamingDetails.actualStartTime　（ライブ開始時間）
        liveStreamingDetails.scheduledStartTime　（ライブ開始予定時間）
        liveStreamingDetails.actualEndTime　（ライブ終了時間）
        liveStreamingDetails.concurrentViewers　（リアルタイム視聴者数）
        liveStreamingDetails.activeLiveChatId　（チャット取得用ID）
    """
    def getLiveStartTime_JT(youtubeObject,video_id:str):
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