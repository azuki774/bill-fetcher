from flask import Flask
from pythonjsonlogger import jsonlogger
import logging
import os
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
drv = None

app = Flask("flaskapp")
@app.route("/", methods=["GET"])
def index_get():
    return "OK"

@app.route("/moneyforward/cf", methods=["GET"])
def moneyforward_get():
    html = money.get_from_url(drv, "https://moneyforward.com/cf")
    return str(html.decode("utf-8"))

@app.route("/moneyforward/cf/lastmonth", methods=["GET"])
def moneyforward_lastmonth_get():
    html = money.get_from_url_cf_lastmonth(drv)
    return str(html.decode("utf-8"))

@app.route("/moneyforward/status", methods=["GET"])
def moneyforward_status():
    xpaths = os.getenv("refresh_xpaths").split(",")
    ret_f_json = money.get_status(drv, xpaths)
    return ret_f_json

def main():
    ## Get Initial Browser setup & login
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
    logger.info("money forward login successful")

main()
