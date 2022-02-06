# 参考 https://develop.blue/2020/02/python-use-logging/
# https://srbrnote.work/archives/1656
# https://ahyt910.hateblo.jp/entry/2019/04/16/170339
# https://github.com/pistatium/about_python_logging

# from bot.config import twitter_stream, SCREEN_NAME 
from logging import getLogger, StreamHandler, FileHandler, Formatter, \
                                    DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

_LOG_FORMAT = '%(asctime)s- %(name)s - %(levelname)s - %(pathname)s - %(lineno)d - %(message)s'
# _LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s'
# _LOG_FILE = './logs/test.log' 

def get_module_logger(modname, filename, level=DEBUG):
    logger = getLogger(modname)
    if not logger.hasHandlers():
        stream_handler = StreamHandler()
        # file_handler = FileHandler(filename=filename, mode='a')
        file_handler = RotatingFileHandler(filename=filename,  mode='a', maxBytes=3000000, backupCount=5)
        formatter = Formatter(_LOG_FORMAT)
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        logger.setLevel(level)
    return logger