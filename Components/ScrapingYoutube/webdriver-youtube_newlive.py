# 
#  特定のチャンネルの動画を全て取得する
#  10分で理解する Selenium - Qiita https://qiita.com/Chanmoro/items/9a3c86bb465c1cce738a


"""
youtubeで新着検知をしようとしたのだが、セレクターが深く、また、live中のURLと混同して取得してしまう。
一時的には使用できるが、サイトの構造が変わる度に対応するのは手間がかかるので中止

APIを使用する方法か、ホロライブのスケジュールを直接検知した方が楽
構造もシンプルなので対応も楽そう
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import SessionNotCreatedException

from webdriver_manager.chrome import ChromeDriverManager

import time
import datetime
from datetime import datetime as dt

import os

from bs4 import BeautifulSoup
import requests

import pandas as pd
import numpy as np

from pprint import pprint


class YoutubeChannelMonitor:

    def __init__(self, headless=False):
        self.options = Options()
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--hide-scrollbars')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--proxy-server="direct://"')
        self.options.add_argument('--proxy-bypass-list=*')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--kiosk')
        self.options.add_argument('--start-maximized') 
        # self.options.add_argument(f'window-size={self.width}x{self.height}')
        self.options.add_argument('--force-device-scale-factor=1')
        if headless == False:
            pass
        elif headless == True:
            self.options.add_argument('--headless') # ※ヘッドレスモードを使用する場合、コメントアウトを外す

        self.Channel = {
            # ホロライブ
            # 'KORONE_ch' :'UChAnqc_AY5_I3Px5dig3X1Q',    #戌神ころね
            # 'MIKO_ch' : 'UC-hM6YJuNYVAmUWxeIr9FeA',     #さくらみこ
            # 'FUBUKI_ch' : 'UCdn5BQ06XqgXoAxIhbqw5Rg',   #白上フブキ
            # 'AQUA_ch' : 'UC1opHUrw8rvnsadT-iGp7Cg',     #湊あくあ
            'PEKORA_ch' : 'UC1DCedRgGHBdm81E1llLhOQ',   #兎田ぺこら
            # 'AKIROSE_ch' : 'UCFTLzh12_nrtzqBPsTCqenA',   #アキ・ローゼンタール
            # 'SORA_ch' : 'UCp6993wxpyDPHUpavwDFqgg',     #ときのそら
            # 'SUBARU_ch' : 'UCvzGlP9oQwU--Y0r9id_jnA',   #大空スバル
            # 'ROBOCO_ch' : 'UCDqI2jOz0weumE8s7paEk6g',   #ロボ子さん
            # 'SHION_ch' : 'UCXTpFs_3PqI41qX2d9tL2Rw',    #紫咲シオン
            # 'FLARE_ch' : 'UCvInZx9h3jC2JzsIzoOebWg',    #不知火フレア
            # 'MEL_ch' : 'UCD8HOxPs4Xvsm8H0ZxXGiBw',      #夜空メル
            # 'CHOCO_ch' : 'UCp3tgHXw_HI0QMk1K8qh3gQ',    #癒月ちょこ サブ
            # 'CHOCO_Main_ch' : 'UC1suqwovbL1kzsoaZgFZLKg', #癒月ちょこ メイン
            # 'HAATO_ch' : 'UC1CfXB_kRs3C-zaeTG3oGyg',    #赤井はあと
            # 'OKAYU_ch' : 'UCvaTdHTWBGv3MKj3KVqJVCw',    #猫又おかゆ
            # 'LUNA_ch' : 'UCa9Y57gfeY0Zro_noHRVrnw',     #姫森ルーナ
            # 'SUISEI_ch' : 'UC5CwaMl1eIgY8h02uZw7u8A',   #星街すいせい
            # 'MATSURI_ch' : 'UCQ0UDLQCjY0rmuxCDE38FGg',  #夏色まつり
            # 'MARINE_ch' : 'UCCzUftO8KOVkV4wQG1vkUvg',   #宝鐘マリン
            # 'NAKIRI_ch' : 'UC7fk0CB07ly8oSl0aqKkqFg',   #百鬼あやめ
            # 'NOEL_ch' : 'UCdyqAaZDKHXg4Ahi7VENThQ',     #白銀ノエル
            # 'RUSHIA_ch' : 'UCl_gCybOJRIgOXw6Qb4qJzQ',   #潤羽るしあ
            # 'COCO_ch' : 'UCS9uQI-jC3DE0L4IpXyvr6w',     #桐生ココ
            # 'KANATA_ch' : 'UCZlDXzGoo7d44bwdNObFacg',   #天音かなた
            # 'MIO_ch' : 'UCp-5t9SrOQwXMU7iIjQfARg',      #大神ミオ
            # 'TOWA_ch' : 'UC1uv2Oq6kNxgATlCiez59hw',     #常闇トワ
            # 'WATAME_ch' : 'UCqm3BQLlJfvkTsX_hvm0UmA',   #角巻わため
            # 'LAMY_ch' : 'UCFKOVgVbGmX65RxO3EtH3iw',      #雪花ラミィ
            # 'NENE_ch' : 'UCAWSyEs_Io8MtpY3m-zqILA',     #桃鈴ねね
            # 'BOTAN_ch' : 'UCUKD-uaobj9jiqB-VXt71mA',      #獅白ぼたん
            # # 'ALOE_ch' : 'UCgZuwn-O7Szh9cAgHqJ6vjw',      #魔乃アロエ
            # 'POLKA_ch' : 'UCK9V2B22uJYu3N7eR_BT9QA' ,      #尾丸ポルカ

            # # イノナカミュージック
            # 'AZKI_ch' : 'UC0TXe_LYZ4scaW2XMyi5_kw',     #AZKi

            # #ホロライブ　EN
            # 'CALLIOPE_ch' : 'UCL_qhgtOy0dy1Agp8vkySQg',    #森美声 モリ・カリオペ
            # 'KIARA_ch' : 'UCHsx4Hqa-1ORjQTh9TYDhww',    #小鳥遊キアラ
            # 'INANIS_ch' : 'UCMwGHR0BTZuLsmjY_NT5Pwg',    #一伊那尓栖 にのまえいなにす
            # 'GawrGura_ch' : 'UCoSrY_IQQVpmIRZ9Xf-y93g',    #がうる・くら
            # 'AMELIA_ch' : 'UCyl1z3jo3XHR1riLFKG5UAg',  #ワトソン・アメリア

            # #ホロライブ　ID
            # 'IOFIFTEEN_ch' : 'UCAoy6rzhSf4ydcYjJw3WoVg',    #Airani Iofifteen / アイラニ・イオフィフティーン
            # 'MOONA_ch' : 'UCP0BspO_AMEe3aQqqpo89Dg',    #Moona Hoshinova / ムーナ・ホシノヴァ
            # 'RISU_ch' : 'UCOyYb1c43VlX9rc_lT6NKQw',    #Ayunda Risu / アユンダ・リス

            # # 運営
            # 'HOLOLIVE_ch' : 'UCJFZiqLMntJufDCHc6bQixg',   #Hololive
        }


    def main(self):
        for name,channel_id in self.Channel.items():
            try:
                _DRIVER_PATH = './chromedriver'
                driver = webdriver.Chrome(executable_path=_DRIVER_PATH, chrome_options=self.options)
            except SessionNotCreatedException:
                driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=self.options)

            url = 'https://www.youtube.com/channel/' + channel_id
            driver.get(url)
            #------------------------------------------pageからvideoを取得------------------------------------------
            # res.raise_for_status()
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, "html.parser")
            # elems = soup.select('body > ytd-app div#content > ytd-page-manager#page-manager > ytd-browse　div#dismissible')
            elems = soup.select('#dismissible div#contents > ytd-expanded-shelf-contents-renderer div#grid-container > ytd-video-renderer div#dismissible > ytd-thumbnail a#thumbnail')

            # filename = './Holo_menber_video_list/{}.csv'.format(name)
            pprint(elems)
            video_list = []

            while True :
                for elem in elems:
                    pprint(elem)
                    video_list.append(elem.get("href"))
                break

            driver.quit()
            pprint(video_list)
            # # CSV登録
            # lives_report = pd.DataFrame(result_video_list)
            # lives_report.to_csv(filename, header=False, index=False, mode='w')
            # time.sleep(5)

            # print(page_title, page_url)


if __name__ == '__main__':
    y_c_m = YoutubeChannelMonitor(True)
    y_c_m.main()
