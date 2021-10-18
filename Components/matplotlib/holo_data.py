import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import ScalarFormatter,NullFormatter
import pandas as pd
import datetime
from datetime import timedelta
from pprint import pprint

import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv

'''
original
'''
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
# from sqlalchemy import func
from model import HoloData
from model.setting import session as Session
from config import app

_SAVE_DIR_PATH = app.HOLO_DATA_IMG_DIR + 'holo_data.png'

def make_holo_data_graph():
    print('create starting')
    plt.style.use('seaborn')
    plt.rcParams['font.family'] = "MS Gothic"
    end = datetime.date.today()   #今日の日付
    start = end - timedelta(days=7) #1週間計算
    end = end + timedelta(days=1)
    # pprint(start.strftime('%Y-%m-%d %H:%M:%S'))

    # DBからidを検索
    x_axis = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    # columns = ['総登録者','総動画数','総再生数']
    # weeks = session.query(HoloData).filter(func.date(HoloData.updated_at) == (datetime.date.today() - datetime.timedelta(days=7)) ).all()
    
    Session.commit()
    # Session.refresh(session)
    weeks = Session.query(HoloData).filter(HoloData.updated_at.between(start, end)).all()
    for week in weeks:
        x_axis.append(week.updated_at - timedelta(days=1))
        y1.append(week.all_youtube_subscriber)
        y2.append(week.all_youtube_videoCount)
        y3.append(week.all_youtube_viewCount)

    # x = pd.date_range(start.strftime('%Y-%m-%d'), periods=7, freq='d')

    df = pd.DataFrame(data={'総登録者':y1, '総動画数':y2, '総再生数':y3,}, index= x_axis,)
    diff = df.diff() #前日差
    del x_axis[0]
    del y1[0]
    del y2[0]
    del y3[0]
    y1_min, y1_max = min(y1), max(y1)
    y2_min, y2_max = min(y2), max(y2)
    y3_min, y3_max = min(y3), max(y3)
    # pprint(list(diff['総登録者']))
    # pprint(list(diff['総動画数']))
    # pprint(list(diff['総再生数']))
    # pprint(df.loc[:,'総登録者'])

    y4 = list(diff['総登録者'])
    y5 = list(diff['総動画数'])
    y6 = list(diff['総再生数'])
    del y4[0]
    del y5[0]
    del y6[0]

    # fig = plt.figure()
    fig = plt.figure(figsize=(16,9))

    ax_youtube_subscriber = fig.add_subplot(3, 1, 1,)
    ax_youtube_videoCount = fig.add_subplot(3, 1, 2)
    ax_youtube_viewCount = fig.add_subplot(3, 1, 3)

    # グラフ種類の設定
    # 棒グラフ
    ax_youtube_subscriber.bar(x_axis, y1, color='xkcd:sky blue', align="center", width=0.5, label='登録者数')
    ax_youtube_videoCount.bar(x_axis, y2, color='xkcd:turquoise', align="center", width=0.5, label='apapap')
    ax_youtube_viewCount.bar(x_axis, y3, color='xkcd:grey blue', align="center", width=0.5, label='suisei')
    # 折れ線グラフ
    ax_youtube_subscriber2 = ax_youtube_subscriber.twinx()
    ax_youtube_subscriber2.grid(False)
    ax_youtube_subscriber2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax_youtube_subscriber2.plot(x_axis, y4, linewidth = 0.7, marker='.', linestyle='dashed', color='red', label='前日差')

    ax_youtube_videoCount2 = ax_youtube_videoCount.twinx()
    ax_youtube_videoCount2.grid(False)
    ax_youtube_videoCount2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax_youtube_videoCount2.plot(x_axis, y5, linewidth = 0.7, marker='.', linestyle='dashed', color='red', label='前日差')

    ax_youtube_viewCount2 = ax_youtube_viewCount.twinx()
    ax_youtube_viewCount2.grid(False)
    ax_youtube_viewCount2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax_youtube_viewCount2.plot(x_axis, y6, linewidth = 0.7, marker='.', linestyle='dashed', color='red', label='前日差')

    # x軸のフォーマット変更
    # ax_youtube_subscriber.xaxis.set_visible(False)
    ax_youtube_subscriber.xaxis.set_major_formatter(NullFormatter())
    ax_youtube_videoCount.xaxis.set_major_formatter(NullFormatter())
    ax_youtube_viewCount.xaxis.set_major_formatter(DateFormatter('%m/%d'))

    # y軸のフォーマット変更
    ax_youtube_subscriber.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax_youtube_subscriber.set_ylim(y1_min-(y1_min * 0.01), y1_max+(y1_max * 0.01) )
    ax_youtube_videoCount.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax_youtube_videoCount.set_ylim(y2_min-(y2_min * 0.01), y2_max+(y2_max * 0.01) )
    ax_youtube_viewCount.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax_youtube_viewCount.set_ylim(y3_min-(y3_min * 0.01), y3_max+(y3_max * 0.01) )
    # ax_youtube_subscriber.set_yscale("log")
    # ax_youtube_viewCount.set_yscale("log")

    # 注釈
    # ax_youtube_subscriber.annotate(s='text', xy=(100,100), xytext=(100,100), ha='center',fontsize=9)
    # ax_youtube_videoCount.annotate(s='text', xy=(100,100), xytext=(100,100), ha='center',fontsize=9)
    # ax_youtube_viewCount.annotate(s='text', xy=(100,100), xytext=(100,100), ha='center',fontsize=9)

    # 棒グラフ内に数値を書く
    for x1, y in zip(x_axis, y1):
        ax_youtube_subscriber.text(x1, y, y, ha='center', va='bottom')
    # 棒グラフ内に数値を書く
    for x2, y in zip(x_axis, y2):
        ax_youtube_videoCount.text(x2, y, y, ha='center', va='bottom')
    # 棒グラフ内に数値を書く
    for x3, y in zip(x_axis, y3):
        ax_youtube_viewCount.text(x3, y, y, ha='center', va='bottom')

    # titleの設定
    ax_youtube_subscriber.set_title('総登録者(人)')
    ax_youtube_videoCount.set_title('総動画本数(本)')
    ax_youtube_viewCount.set_title('総再生回数(回)')

    #凡例
    ax_youtube_subscriber2.legend(loc = 'upper left') 
    ax_youtube_videoCount2.legend(loc = 'upper left')
    ax_youtube_viewCount2.legend(loc = 'upper left')

    # 余白
    fig.subplots_adjust(left=0.49, right=0.51, bottom=0.49, top=0.51)
    ax_youtube_subscriber.margins(y=0.2)
    ax_youtube_videoCount.margins(y=0.2)
    ax_youtube_viewCount.margins(y=0.2)
    # x軸のラベル回転
    # plt.xticks(rotation=45) 

    plt.tight_layout()
    fig.savefig(_SAVE_DIR_PATH)
    # plt.show()
    print('Done!')

if __name__ == '__main__':
    make_holo_data_graph()