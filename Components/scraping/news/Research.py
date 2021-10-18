import feedparser
from bs4 import BeautifulSoup
import requests
from collections import OrderedDict
import random
import csv
import re

import os
from os.path import join, dirname
from dotenv import load_dotenv

import schedule
import time
import datetime

from newsapi import NewsApiClient

from pprint import pprint

# News API
NEWS_API_KEY = os.environ.get('NEWS_API')
# NEWS_API_KEY = 'c7ad8c43a0c34dd8ac105acdc61cad19'

#------------------------------------------GoogleNews スクレイピング------------------------------------------
def googleNewsResearch():
    '''
    Google News スクレイピング
    '''
    url = 'https://news.google.com/search?q=hololive&hl=ja&gl=JP&ceid=JP%3Aja'
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    elems = soup.select("h3")
    Titles_google = []
    Urls_google = []

    print('Log:GoogleNews , NOW Research...')
    for elem in elems:
        if elem.getText():
            for access in elem.select("a"):
                if access.get("href"):
                    Titles_google.append(elem.getText())
                    Urls_google.append(access.get("href"))
                else:
                    continue
        else:
            continue

    print ('search results... Title : ' + len(Titles_google))
    print ('search results... URL : ' + len(Urls_google))

    NEWS_LIST = dict(zip(Titles_google , Urls_google))
    pprint(NEWS_LIST)
    print ('LOG Google Research.py end:'+str(len(Urls_google)))
    return NEWS_LIST


#------------------------------------------GoogleNews RSS------------------------------------------
def googleNewsRSS(keyword='hololive'):
    '''
    Google News スクレイピング
    '''
    url = 'https://news.google.com/rss/search?q={}&hl=ja&gl=JP&ceid=JP:ja'.format(keyword)
    # res = requests.get(url)
    # res.raise_for_status()
    res = feedparser.parse(url)
    pprint(res)

    return res


# #---------------------------------------News API 専用------------------------------------------
def NewsAPIResearch_Top(keyword='ホロライブ'):
    """
    https://newsapi.org/
    """
    NewsList = []
    newsapi = NewsApiClient(NEWS_API_KEY)
    all_articles = newsapi.get_top_headlines(
                                            q=keyword,
                                            country='jp',)
    pprint(all_articles)
    for lists in all_articles['articles']:
        NewsList.append( {lists['title'] : lists['url']} )

    return NewsList


def NewsAPIResearch_Every(file_name, fromDay, toDay, keyword='ホロライブ'):
    """
    https://newsapi.org/
    """
    News = {}
    tweeted = {}
    
    newsapi = NewsApiClient(NEWS_API_KEY)
    # /v2/everything
    all_articles = newsapi.get_everything(
                                        q=keyword, 
                                        from_param=fromDay, 
                                        to=toDay, 
                                        sort_by='relevancy',)

    if all_articles['articles']:
        for lists in all_articles['articles']:
            if blackFilter(lists['url']):
                News[lists['url']] = [lists['title'], lists['publishedAt']]
        past_news = csvFileRead(file_name)
        for key in past_news.keys():
            try:
                del News[key]
            except KeyError as err:
                pprint(err)
        # os.remove(file_name)
        # past_news.update(News)
        url, val = random.choice(list(News.items()))
        tweeted[url] = val
        # csvFileWrite(file_name, tweeted)
        # pprint(past_news)
    return tweeted


def blackFilter(url:str)->bool:
    """
    ブラックリスト・フィルター
    """
    pattern = "https?://[^/]+/"
    res = re.match(pattern, url)
    # print(res.group())
    BLACK_LIST = ['http://yaraon-blog.com/','https://www.mdn.co.jp/','https://togetter.com/',
                    'http://onecall2ch.com/','http://alfalfalfa.com/','https://it.srad.jp/',
                    'http://jin115.com/','http://blog.esuteru.com/','https://anond.hatelabo.jp/',
                    'https://srad.jp/','https://www.moeyo.com/','https://yro.srad.jp/','http://himasoku.com/',
                    'http://majikichi.com/','http://www.scienceplus2ch.com/','https://vtubernews.jp','http://h-pon.doorblog.jp']
    for black in BLACK_LIST:
        if res is None:
            return True
        # pprint(res.group())
        # @TODO 修正必要
        if res.group() == black:
            return False
    return True


def csvFileRead(filename:str) :
    """
    csv読み取り
    """
    past_all = {}
    past_title= []
    past_url = []
    past_time = []

    with open(filename , "r", newline='') as i:
        reader = csv.reader(i)
        for rows in reader:
            try:
                val = [rows[1], rows[2]]
                past_all[rows[0]] = val
                # past_url.append(rows[1])
                # past_time.append(rows[2])
                # past_all.append( dict([rows[1],list(rows[0], rows[2])]) )
                return past_all

            except IndexError as err:
                print(err)
        # past_all = dict(zip(past_title, [past_url, past_time]))   
    return past_all


def csvFileWrite(file_name:str, lists:dict) :
    """
    csvに書き込み
    """
    field = ['url', 'title', 'time']
    try:
        for key, values in lists.items():
            with open (file_name, 'w', newline='') as ff:
                writer = csv.DictWriter(ff, fieldnames = field)
                writer.writerow({
                    'url': key,
                    'title': values[0], 
                    'time': values[1],
                    })
    except ImportError as err:
        pprint(err)


if __name__ == '__main__':
    # 日本時間 - 1日前
    base_toDay = datetime.date.today() - datetime.timedelta(days=1) 
    base_fromDay = base_toDay - datetime.timedelta(days=7)
    toDay =  base_toDay.strftime('%Y-%m-%d')
    fromDay =  base_fromDay.strftime('%Y-%m-%d')
    file = './src/news_file/news.csv'

    # NewsAPIResearch_Every(file, fromDay, toDay)
    pprint(NewsAPIResearch_Every(file, fromDay, toDay))
# pprint(blackFilter('https://www.mdn.co.jp/di/newstopics/78205/'))
# pprint(NewsAPIResearch_Every(fromDay,toDay))
# pprint(googleNewsRSS())

# schedule.every().hour.at(":58").do(googleNewsResearch)

# while True:
#     schedule.run_pending()
#     time.sleep(1)