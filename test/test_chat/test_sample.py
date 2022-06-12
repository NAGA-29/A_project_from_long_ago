# 単体テスト
import unittest
import sys, os
# sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from chat import get_live_chat as ch
# .accumulate_diff_data

class TestGetLiveChat(unittest.TestCase):

    def setUp(self):
        """各テストメソッドが実行される直前に呼び出される"""
        print('setUp called.')

    def tearDown(self):
        """各テストメソッドが実行された直後に呼び出される"""
        print('tearDown called.')

    def test_get_chat(self):
        video_id = '9onljeWo24'
        file_name = './chat_csv/' + video_id  + '.csv'
        result = ch.get_chat()
        self.assertTrue(result)
        # pass

if __name__ == '__main__':
    unittest.main()