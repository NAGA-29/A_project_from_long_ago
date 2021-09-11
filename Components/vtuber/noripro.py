import time
import datetime
from datetime import datetime as dt
import dateutil.parser
from pytz import timezone

from pprint import pprint

class NoriPro:

    def __init__(self):
        pass

    @staticmethod
    def get_twitter_ids():
        return  {
            # のりプロ , 絵師
            'しぐれうい' : 'ui_shig',        #'しぐれうい' 
            '犬山たまき' : 'norioo_',        #'犬山たまき' 
            '白雪みしろ' : 'mishiro_seiso',     #'白雪みしろ'
            '愛宮みるく' : 'Enomiya_MILK',      #'愛宮みるく'
            '姫咲ゆずる' : 'Himesaki_yuzuru',    #'姫咲ゆずる' 
            '熊谷タクマ' : 'KUMAgaya_taKUMA',     #熊谷タクマ
            '鬼灯わらべ' : 'hoozukiwarabe',    #鬼灯わらべ
            '夢乃リリス' : 'yumenolilith',     #夢乃リリス
            '胡桃澤もも' : 'kurumizawamomo', #胡桃澤もも
            '逢魔きらら' : 'omakirara',     #逢魔きらら
            '看谷にぃあ' : 'mirutani_nia',   #看谷にぃあ
        }

    @staticmethod
    def get_video_ids():
        return  {
            # のりプロ他
            'しぐれうい' : 'UCt30jJgChL8qeT9VPadidSw',       #時雨うい
            '熊谷タクマ' : 'UCCXME7oZmXB2VFHJbz5496A',     #熊谷タクマ
            '犬山たまき' : 'UC8NZiqKx6fsDT3AVcMiVFyA',     #佃煮のりお
            '白雪みしろ' : 'UCC0i9nECi4Gz7TU63xZwodg',     #白雪みしろ
            '愛宮みるく' : 'UCJCzy0Fyrm0UhIrGQ7tHpjg',     #愛宮みるく
            '姫咲ゆずる' : 'UCle1cz6rcyH0a-xoMYwLlAg',     #姫咲ゆずる
            '鬼灯わらべ' : 'UCLyTXfCZtl7dyhta9Jg3pZg',     #鬼灯わらべ
            '夢乃リリス' : 'UCH11P1Hq4PXdznyw1Hhr3qw',     #夢乃リリス
            '胡桃澤もも' : 'UCxrmkJf_X1Yhte_a4devFzA',     #胡桃澤もも
            '逢魔きらら' : 'UCBAeKqEIugv69Q2GIgcH7oA',     #逢魔きらら
            '看谷にぃあ' : 'UCIRzELGzTVUOARi3Gwf1-yg',     #看谷にぃあ
        }

    @staticmethod
    def get_name_tag(ID):
        # 絵師V
        if ID == 'UCt30jJgChL8qeT9VPadidSw' : HoloName,live_tag = 'しぐれうい', '#ういなま'
        # のりプロ
        elif ID == 'UC8NZiqKx6fsDT3AVcMiVFyA' : HoloName,live_tag = '犬山たまき', '#犬山たまき'
        elif ID == 'UCCXME7oZmXB2VFHJbz5496A' : HoloName,live_tag = '熊谷タクマ', '#熊谷タクマ'
        elif ID == 'UCC0i9nECi4Gz7TU63xZwodg' : HoloName,live_tag = '白雪みしろ', '#白雪みしろ'
        elif ID == 'UCJCzy0Fyrm0UhIrGQ7tHpjg' : HoloName,live_tag = '愛宮みるく', '#愛宮みるく'
        elif ID == 'UCle1cz6rcyH0a-xoMYwLlAg' : HoloName,live_tag = '姫咲ゆずる', '#姫咲ゆずる'
        elif ID == 'UCLyTXfCZtl7dyhta9Jg3pZg' : HoloName,live_tag = '鬼灯わらべ', '#鬼灯わらべ'
        elif ID == 'UCH11P1Hq4PXdznyw1Hhr3qw' : HoloName,live_tag = '夢乃リリス', '#夢乃リリス'
        elif ID == 'UCxrmkJf_X1Yhte_a4devFzA' : HoloName,live_tag = '胡桃澤もも', '#胡桃澤もも'
        elif ID == 'UCBAeKqEIugv69Q2GIgcH7oA' : HoloName,live_tag = '逢魔きらら', '#逢魔きらら'
        elif ID == 'UCIRzELGzTVUOARi3Gwf1-yg' : HoloName,live_tag = '看谷にぃあ', '#看谷にぃあ'
        return HoloName, live_tag
