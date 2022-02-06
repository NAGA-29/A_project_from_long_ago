# from bot.config import twitter_stream, SCREEN_NAME 
from logging import getLogger, StreamHandler, FileHandler, Formatter, \
                                    DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

def get_module_logger(modname, filename, level=DEBUG):
    logger = getLogger(modname)

    stream_handler = StreamHandler()
    # file_handler = FileHandler(filename=filename, mode='a')
    file_handler = RotatingFileHandler(filename=filename,  mode='a', maxBytes=100000, backupCount=10)
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.setLevel(level)
    return logger