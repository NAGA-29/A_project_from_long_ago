import time
import datetime
from datetime import datetime as dt
import dateutil.parser
from pytz import timezone

from pprint import pprint

class HoloDate:

    def __init__(self):
        pass


    def convertToJST(self,time):
        '''
        日本時間に変換
        '''
        try:
            # JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
            # jst_timestamp = dateutil.parser.parse(time).astimezone(JST)
            jst_timestamp = dateutil.parser.parse(time).astimezone(timezone('Asia/Tokyo'))
            updateJST = jst_timestamp.strftime('%Y/%m/%d %H:%M')
            return updateJST
        except Exception as err:
            return None

    def convert_To_CST(self, time):
        '''
        台湾時間に変換
        '''
        try:
            # CST = datetime.timezone(datetime.timedelta(hours=+8), 'CST')
            jst_timestamp = dateutil.parser.parse(time).astimezone(timezone('Asia/Taipei'))
            updateJST = jst_timestamp.strftime('%Y/%m/%d %H:%M')
            return updateJST
        except Exception as err:
            # pprint(err)
            return None

    def convert_To_NY(self, time):
        '''
        NY時間に変換
        '''
        try:
            # NY = datetime.timezone(datetime.timedelta(hours=-4), 'NY')
            jst_timestamp = dateutil.parser.parse(time).astimezone(timezone('America/New_York'))
            updateJST = jst_timestamp.strftime('%Y/%m/%d %H:%M')
            return updateJST
        except Exception as err:
            # pprint(err)
            return None

    def convert_To_LON(self, time):
        '''
        GMT標準時間(ロンドン)時間に変換
        '''
        try:
            # LON = datetime.timezone(datetime.timedelta(hours=0), 'LON')
            jst_timestamp = dateutil.parser.parse(time).astimezone(timezone('Europe/Belfast'))
            updateJST = jst_timestamp.strftime('%Y/%m/%d %H:%M')
            return updateJST
        except Exception as err:
            # pprint(err)
            return None

    def convert_To_ID(self, time):
        '''
        🇮インドネシア標準時間に変換
        '''
        try:
            # LON = datetime.timezone(datetime.timedelta(hours=0), 'LON')
            jst_timestamp = dateutil.parser.parse(time).astimezone(timezone('Asia/Jakarta'))
            updateJST = jst_timestamp.strftime('%Y/%m/%d %H:%M')
            return updateJST
        except Exception as err:
            # pprint(err)
            return None