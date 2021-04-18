# 
#  Youtubeからゲームのタイトルと画像を抜き取る
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

from bs4 import BeautifulSoup
import requests

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

#
# Chromeドライバーの起動
# 
DRIVER_PATH = '/Users/nagaki/Documents/naga-sample-code/python/test/scraping/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)


#
# Googleにアクセスする
#
url = 'https://www.youtube.com/watch?v=zOBhKOFl-5Y'
driver.get(url)
time.sleep(3)
html = driver.page_source.encode('utf-8')
#------------------------------------------pageからゲームを取得------------------------------------------
soup = BeautifulSoup(html, "html.parser")

elems = soup.select("div#title")
elems_img = soup.select("img#img.style-scope.yt-img-shadow")
result_list_title = []
result_list_url = []

# pprint(elems)
# pprint(elems_img)

for elem in elems:
    result_list_title.append(elem.getText())
# pprint(result_list_title)
    # for access in elem.select("a"):
    #     href = access.get("href")
    #     result_list.append(href)
    #     time.sleep(1)
for elem in elems_img:
    result_list_url.append(elem.get("src"))


pprint(result_list_title[1])
pprint('https:' + result_list_url[1])

# 検索窓にSeleniumと入力する
# keyWord = '検索したいキーワード'
# selector = '#tsf > div:nth-child(2) > div.A8SBwf > div.RNNXgb > div > div.a4bIc > input'
# element = driver.find_element_by_css_selector(selector)
# element.send_keys(keyWord)


# 一番下までスクロールする
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")



# # 1位の記事のタイトルを取得する
# selector = '#zox-main-blog-wrap > div > div > a'
# element = driver.find_element_by_css_selector(selector)
# # enterキーを押す
# element.send_keys(Keys.ENTER)
# time.sleep(5)
# # page_title = element.text


# # 一番下までスクロールする
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# selector = '#zox-main-blog-wrap > div > div > a'
# element = driver.find_element_by_css_selector(selector)
# time.sleep(60)



# 1位の記事のURLを取得する
# selector = '#rso > div > div.rc > div > a'
# element = driver.find_element_by_css_selector(selector)
# page_url = element.get_attribute('href')

# ブラウザを終了する(全てのウィンドウを閉じる）
# Chromeのショートカットキー(Command+Q)と同じ動作
driver.quit()

# print(page_title, page_url)
# 10分で理解する Selenium - Qiita https://qiita.com/Chanmoro/items/9a3c86bb465c1cce738a
