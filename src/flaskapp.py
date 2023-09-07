from flask import Flask
from pythonjsonlogger import jsonlogger
import logging
import sys
import driver
import moneyforward.money as money

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s",
    json_ensure_ascii=False,
)
h.setFormatter(json_fmt)
logger.addHandler(h)

app = Flask("flaskapp")
@app.route("/", methods=["GET"])
def index_get():
    return "OK"

drv = None

def main():
    ## Get Initial Browser setup
    global drv
    logger.info("api setup start")
    logger.info("get driver")
    drv = driver.get_driver()
    logger.info("money forward login")
    try:
        money.login(drv)
    except Exception as e:
        logger.error("failed to login. maybe changing xpath: %s", e)
        sys.exit(1)
    logger.info("money forward login sucessful")

main()
