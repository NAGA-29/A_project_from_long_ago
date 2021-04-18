import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time

import os
from os.path import join, dirname
from dotenv import load_dotenv

from pprint import pprint

import tweepy

'''
Initial Setting
'''
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

_DRIVER_PATH = os.environ.get('DRIVER_PATH')
SCREENSHOT_FILE = './screenshot_image/'

#twitter本番アカウント
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(auth)


class ScreenShot:
    options = ''
    width = 1280
    height = 720

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
        self.options.add_argument(f'window-size={self.width}x{self.height}')
        self.options.add_argument('--force-device-scale-factor=1')
        if headless == False:
            pass
        elif headless == True:
            self.options.add_argument('--headless') # ※ヘッドレスモードを使用する場合、コメントアウトを外す


    def screenshot(self, url):
        # DRIVER_PATH = '/Users/nagaki/Documents/naga-sample-code/python/test/chromedriver'
        driver = selenium.webdriver.Chrome(executable_path=_DRIVER_PATH, chrome_options=self.options)
        driver.get(url)
        
        # driver.set_window_size(1024, 768)
        page_width = driver.execute_script('return document.body.scrollWidth')
        page_height = driver.execute_script('return document.body.scrollHeight')   
        print(page_width)
        print(page_height)
        driver.set_window_size(page_width, page_height + 100)
        # driver.set_window_size(1980, 1080)
        # driver.get('http://localhost/Hololive_Project/public/holo/live')


        # for i in range(5):
        #     # 一番下までスクロールする
        #     driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN) 
        #     # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(1)


        time.sleep(3)
        driver.save_screenshot(SCREENSHOT_FILE + 'screenshot.png')
        driver.quit()


    # def tweetWithIMG(self, message):
    #     #ツイート内容
    #     TWEET_TEXT = message
    #     try :
    #         FILE_NAME = SCREENSHOT_FILE + 'screenshot.png'
    #         tweet_status = API.update_with_media(filename=FILE_NAME, status=TWEET_TEXT)
    #         pprint(tweet_status)
    #         if tweet_status == 200: #成功
    #             pprint(tweet_status)
    #             result = True
    #         else:
    #             result = False
    #     except Exception as e:
    #             message = e
    #             pprint(e)
    #             result = False
    #     return result

# i = ScreenShot(headless=True)
# i.screenshot('http://localhost/Hololive_Project/public/holo/live_screenshot')
# i.tweetWithIMG('テスト!! 現在のLIVE中一覧だでな！!')