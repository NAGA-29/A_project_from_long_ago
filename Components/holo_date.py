import time
import datetime
from datetime import datetime as dt
import dateutil.parser

from pprint import pprint

class HoloDate:

    def __init__(self):
        pass

    '''
    日本時間に変換
    '''
    def convertToJST(self,time):
        try:
            JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
            jst_timestamp = dateutil.parser.parse(time).astimezone(JST)
            updateJST = jst_timestamp.strftime('%Y/%m/%d %H:%M:%S')
            return updateJST
        except Exception as err:
            # pprint(err)
            return None