import schedule

import os
from os.path import join, dirname
from dotenv import load_dotenv

from pprint import pprint

# 自作モジュール
from Components.tweet import tweet_components

# TODO
# DBに何件入っているか調べる
# その数からランダムで数字を選ぶ
# DBからIDを検索
# file_name1に値が入っているかチェック(現在値が入っていないものがあるー＞dbの修正が必要だが、消されたツイートもあるためこの処理が必要)
# 値が確認できなかった場合、もう一度ランダムに数字を選びDBに検索をかける->成功するまで繰り返す
# 値が確認できたら、指定のDirにファイルがあるかチェック->存在が確認できない場合