import requests
from bs4 import BeautifulSoup
import feedparser

import base64
import re

import time
import datetime
import dateutil.parser
from pytz import timezone
from datetime import timedelta

from pprint import pprint 

class NicoNico_Wrapper:
    _end_point = 'https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search'
    
    def __init__(self) -> None:
        pass

    def parse_time(self, published_parsed:list)->str:
        year = published_parsed[0]
        month = published_parsed[1]
        day = published_parsed[2]
        hour = published_parsed[3]
        minutes = published_parsed[4]
        second = published_parsed[5]
        origin_time = f'{year}/{month}/{day} {hour}:{minutes}'
        return origin_time

    def search_thumbnail(self, video_id:str):
        url = 'https://www.nicovideo.jp/watch/' + video_id
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        print (url)

        elems = soup.select('meta[property="og:image"]')
        img = re.findall('content="(.*?)"', str(elems[0]))
        if 'r1280x720l' in img[0]:
            print('サムネ取得成功')
            return img[0]
        else:
            print('サムネ検出失敗')
            return None

    def nico_convertToJST(self, time):
        '''
        日本時間に変換
        '''
        try:
            jst_timestamp = dateutil.parser.parse(time).astimezone(timezone('Asia/Tokyo'))
            jst_timestamp += timedelta(hours=9)
            updateJST = jst_timestamp.strftime('%Y/%m/%d %H:%M')
            return updateJST
        except Exception as err:
            pprint(err)
            return None

# if __name__ == '__main__':
#     nico = NicoNico_Wrapper()
#     url = 'https://ch.nicovideo.jp/hololive/video?rss=2.0'
#     rss = feedparser.parse(url).entries

#     videos = []
#     if rss:
#         for i in rss:
#             if i['nicoch_ispremium'] == 'true':
#                 videos.append(i)
#             else:
#                 continue

#     for vi in videos:
#         link = vi['link']
#         published = vi['published']
#         published_parsed = vi['published_parsed']
#         title = vi['title']

#         video_id = link.split('/')[-1]
#         img = nico.search_thumbnail(video_id) 

#         jpt_str = nico.parse_time(published_parsed)
#         print(title)
#         print(img)
#         print(nico.nico_convertToJST(jpt_str))

# t = 'https://img.cdn.nimg.jp/s/nicovideo/thumbnails/38697444/38697444.87274044.original/r1280x720l?key=2377d3045f0a68a887246eabcc2ec5228df770a5268fb56789d112c60fd35aa9'
# print(t.split('/')[6])