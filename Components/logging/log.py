from logging import config,getLogger,basicConfig,DEBUG, WARNING,Formatter, FileHandler, StreamHandler
from json import load
# import logging
# import logging.handlers


# 参考 https://develop.blue/2020/02/python-use-logging/
# https://srbrnote.work/archives/1656
# https://ahyt910.hateblo.jp/entry/2019/04/16/170339
# https://github.com/pistatium/about_python_logging

_LOG_FORMAT = '%(asctime)s- %(name)s - %(levelname)s - %(pathname)s - %(lineno)d - %(message)s'
_LOG_FILE = './logs/test.log' 

basicConfig(filename=_LOG_FILE, filemode='a', format=_LOG_FORMAT, level=WARNING)

# フォーマッタを生成する
fmt = Formatter(_LOG_FORMAT)

# ロガーを取得する
logger = getLogger(__name__)

logger.setLevel(DEBUG) # 出力レベルを設定

# コンソール出力

log_str = StreamHandler()
log_str.setFormatter(fmt)      # ハンドラーにフォーマッターを設定する
log_str.setLevel(DEBUG) # 出力レベルを設定
logger.addHandler(log_str)     # ロガーにハンドラーを設定する


# ファイル出力
log_file = FileHandler(filename=_LOG_FILE)
log_file.setFormatter(fmt)      # ハンドラーにフォーマッターを設定する
log_file.setLevel(DEBUG)    # 出力レベルを設定
logger.addHandler(log_file)     # ロガーにハンドラーを設定する

# ログ出力を行う
logger.info("ログを出力")
# logger.debug('変数の値を確認')
# logger.info('処理開始')
# logger.warning('変数の値が変かも！？')
# logger.error('エラーが発生！！')
# logger.critical('処理の続行がません！！')