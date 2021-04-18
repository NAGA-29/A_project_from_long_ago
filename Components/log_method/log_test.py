from logging import config, getLogger
from json import load

with open("./config/logging.json", "r", encoding="utf-8") as f:
    config.dictConfig(load(f))
logger = getLogger(__name__)

logger.info("オハペコ〜〜")