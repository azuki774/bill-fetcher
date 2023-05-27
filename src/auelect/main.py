from pythonjsonlogger import jsonlogger
import logging
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(fmt='%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s', json_ensure_ascii=False)
h.setFormatter(json_fmt)
logger.addHandler(h)

if __name__ == "__main__":
    logger.info("auelect start")

    logger.info("writer start")

    logger.info("writer end")
    logger.info("auelect end")
