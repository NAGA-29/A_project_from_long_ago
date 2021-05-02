# 
#  特定のチャンネルの動画を全て取得する
# 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import datetime
from datetime import datetime as dt

from bs4 import BeautifulSoup
import requests

import pandas as pd
import numpy as np

from pprint import pprint

#
# Seleniumをあらゆる環境で起動させるオプション
#
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--start-maximized')
# options.add_argument('--headless') # ※ヘッドレスモードを使用する場合、コメントアウトを外す
options.add_argument('--kiosk')

# Channel = {
#     # ホロライブ
#     'KORONE_ch' :'UChAnqc_AY5_I3Px5dig3X1Q',    #戌神ころね
#     'MIKO_ch' : 'UC-hM6YJuNYVAmUWxeIr9FeA',     #さくらみこ
#     'FUBUKI_ch' : 'UCdn5BQ06XqgXoAxIhbqw5Rg',   #白上フブキ
#     'AQUA_ch' : 'UC1opHUrw8rvnsadT-iGp7Cg',     #湊あくあ
#     'PEKORA_ch' : 'UC1DCedRgGHBdm81E1llLhOQ',   #兎田ぺこら
#     'AKIROSE_ch' : 'UCFTLzh12_nrtzqBPsTCqenA',   #アキ・ローゼンタール
#     'SORA_ch' : 'UCp6993wxpyDPHUpavwDFqgg',     #ときのそら
#     'SUBARU_ch' : 'UCvzGlP9oQwU--Y0r9id_jnA',   #大空スバル
#     'ROBOCO_ch' : 'UCDqI2jOz0weumE8s7paEk6g',   #ロボ子さん
#     'SHION_ch' : 'UCXTpFs_3PqI41qX2d9tL2Rw',    #紫咲シオン
#     'FLARE_ch' : 'UCvInZx9h3jC2JzsIzoOebWg',    #不知火フレア
#     'MEL_ch' : 'UCD8HOxPs4Xvsm8H0ZxXGiBw',      #夜空メル
#     'CHOCO_ch' : 'UCp3tgHXw_HI0QMk1K8qh3gQ',    #癒月ちょこ サブ
#     'CHOCO_Main_ch' : 'UC1suqwovbL1kzsoaZgFZLKg', #癒月ちょこ メイン
#     'HAATO_ch' : 'UC1CfXB_kRs3C-zaeTG3oGyg',    #赤井はあと
#     'OKAYU_ch' : 'UCvaTdHTWBGv3MKj3KVqJVCw',    #猫又おかゆ
#     'LUNA_ch' : 'UCa9Y57gfeY0Zro_noHRVrnw',     #姫森ルーナ
#     'SUISEI_ch' : 'UC5CwaMl1eIgY8h02uZw7u8A',   #星街すいせい
#     'MATSURI_ch' : 'UCQ0UDLQCjY0rmuxCDE38FGg',  #夏色まつり
#     'MARINE_ch' : 'UCCzUftO8KOVkV4wQG1vkUvg',   #宝鐘マリン
#     'NAKIRI_ch' : 'UC7fk0CB07ly8oSl0aqKkqFg',   #百鬼あやめ
#     'NOEL_ch' : 'UCdyqAaZDKHXg4Ahi7VENThQ',     #白銀ノエル
#     'RUSHIA_ch' : 'UCl_gCybOJRIgOXw6Qb4qJzQ',   #潤羽るしあ
#     'COCO_ch' : 'UCS9uQI-jC3DE0L4IpXyvr6w',     #桐生ココ
#     'KANATA_ch' : 'UCZlDXzGoo7d44bwdNObFacg',   #天音かなた
#     'MIO_ch' : 'UCp-5t9SrOQwXMU7iIjQfARg',      #大神ミオ
#     'TOWA_ch' : 'UC1uv2Oq6kNxgATlCiez59hw',     #常闇トワ
#     'WATAME_ch' : 'UCqm3BQLlJfvkTsX_hvm0UmA',   #角巻わため
#     'LAMY_ch' : 'UCFKOVgVbGmX65RxO3EtH3iw',      #雪花ラミィ
#     'NENE_ch' : 'UCAWSyEs_Io8MtpY3m-zqILA',     #桃鈴ねね
#     'BOTAN_ch' : 'UCUKD-uaobj9jiqB-VXt71mA',      #獅白ぼたん
#     'ALOE_ch' : 'UCgZuwn-O7Szh9cAgHqJ6vjw',      #魔乃アロエ
#     'POLKA_ch' : 'UCK9V2B22uJYu3N7eR_BT9QA' ,      #尾丸ポルカ

#     # イノナカミュージック
#     'AZKI_ch' : 'UC0TXe_LYZ4scaW2XMyi5_kw',     #AZKi

#     #ホロライブ　EN
#     'CALLIOPE_ch' : 'UCL_qhgtOy0dy1Agp8vkySQg',    #森美声 モリ・カリオペ
#     'KIARA_ch' : 'UCHsx4Hqa-1ORjQTh9TYDhww',    #小鳥遊キアラ
#     'INANIS_ch' : 'UCMwGHR0BTZuLsmjY_NT5Pwg',    #一伊那尓栖 にのまえいなにす
#     'GawrGura_ch' : 'UCoSrY_IQQVpmIRZ9Xf-y93g',    #がうる・くら
#     'AMELIA_ch' : 'UCyl1z3jo3XHR1riLFKG5UAg',  #ワトソン・アメリア

#     #ホロライブ　ID
#     'IOFIFTEEN_ch' : 'UCAoy6rzhSf4ydcYjJw3WoVg',    #Airani Iofifteen / アイラニ・イオフィフティーン
#     'MOONA_ch' : 'UCP0BspO_AMEe3aQqqpo89Dg',    #Moona Hoshinova / ムーナ・ホシノヴァ
#     'RISU_ch' : 'UCOyYb1c43VlX9rc_lT6NKQw',    #Ayunda Risu / アユンダ・リス

#     # 運営
#     'HOLOLIVE_ch' : 'UCJFZiqLMntJufDCHc6bQixg',   #Hololive

#     # 絵師他
#     'SHIGURE_UI_ch' : 'UCt30jJgChL8qeT9VPadidSw', #しぐれうい
#     'TAMAKI_ch' : 'UC8NZiqKx6fsDT3AVcMiVFyA',     #佃煮のりお
#     'SHIRAYUKI_ch' : 'UCC0i9nECi4Gz7TU63xZwodg',  #白雪みしろ
#     'MILK_ch' : 'UCJCzy0Fyrm0UhIrGQ7tHpjg',       #愛宮みるく
#     'YUZURU' : 'UCle1cz6rcyH0a-xoMYwLlAg'  #姫咲ゆずる
# }




for name,channel_id in Channel.items():

    #
    # Chromeドライバーの起動
    # 
    DRIVER_PATH = '/Users/nagaki/Documents/naga-sample-code/python/scraping/chromedriver'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    #
    # Youtubeにアクセスする
    #
    url = 'https://www.youtube.com/channel/' + channel_id + '/videos'
    driver.get(url)
    time.sleep(3)

    for i in range(60):
        # # # 一番下までスクロールする
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN) 
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    #------------------------------------------pageからvideoを取得------------------------------------------
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    elems = soup.select('#thumbnail')
    result_video_list = []
    filename = './Holo_menber_video_list/{}.csv'.format(name)

    # pprint(elems)

    for elem in elems:
        try:
            result_video_list.append('https://www.youtube.com' + elem.get("href"))
        except:
            continue

    # ブラウザを終了する(全てのウィンドウを閉じる）
    # Chromeのショートカットキー(Command+Q)と同じ動作
    driver.quit()


    # CSV登録
    lives_report = pd.DataFrame(result_video_list)
    lives_report.to_csv(filename, header=False, index=False, mode='w')

    # print(page_title, page_url)
    # 10分で理解する Selenium - Qiita https://qiita.com/Chanmoro/items/9a3c86bb465c1cce738a
