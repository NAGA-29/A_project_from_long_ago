'''
１つのテーブルからのりプロのデータのみ抽出し,
その元のテーブルからはのりプロのデータを削除しつつ、、別のテーブルに保存する
'''

import requests
from pyasn1.type.univ import Boolean, Null
import urllib.request, urllib.error
from pprint import pprint

import holo_sql

dir = './Images/'

"""
画像のダウンロード
"""
def ImgDownload(img_url:str, dir_path:str) ->Boolean:
    path = dir_path + img_url.split('/')[-1]
    try:
        response = urllib.request.urlopen(url=img_url)
        with open(path, "wb") as f:
            f.write(response.read())
        print('Image Download OK ' + img_url)
    except Exception as err:
        pprint(err)
        return False
    else:
        return True


headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAC0tJQEAAAAA2zX9L%2FOo8fNjrnisbeAe%2F4X8pcw%3DP55lBKu76Hn88gz0Y0OQp5l4yTFH2sx7M1q0NwawuuH5Uv7ZpE',
}

params = {
    'expansions': 'attachments.media_keys,author_id,entities.mentions.username',
    'media.fields': 'type,url,preview_image_url',
    #  'media.fields': 'url,type,duration_ms,public_metrics',
    'tweet.fields': 'public_metrics',
    'user.fields': 'id,name,url,username',
}

hSql = holo_sql.holo_sql()
# for j in range(6,1894):
for j in range(1600,1894):
    result = hSql.selectArtTable(j)
    url = 'https://api.twitter.com/2/tweets/' + str(result[0][3])
    response = requests.get(url, headers=headers, params=params)
    # response = requests.get('https://api.twitter.com/2/tweets/1302103770826862593', headers=headers, params=params)
    pprint(response.json())
    data = response.json()
    # pprint(data['includes']['media'][0]['url'])
    data_list = [None,None,None,None]
    creator_url = ''
    try: 
        creator_url = 'https://twitter.com/' + data['includes']['users'][0]['username']
        for i in range(4):
            media_url = data['includes']['media'][i]['url']
            path = media_url.split('/')[-1]
            data_list[i] = path

            ImgDownload(media_url, dir)

    except Exception as err:
        pprint(err)
    if data_list[0]:
        hSql.updateArts(result[0][0],creator_url,data_list)

hSql.dbClose()
hSql = None