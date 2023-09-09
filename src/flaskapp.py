from flask import Flask, Response
from pythonjsonlogger import jsonlogger
import logging
import os
import sys
import asyncio
import time
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
drv_locked = False # driver を同時に操作しないためのロック関数

app = Flask("flaskapp")
@app.route("/", methods=["GET"])
def index_get():
    return "OK"

@app.route("/moneyforward/cf", methods=["GET"])
def moneyforward_get():
    global drv_locked
    if drv_locked:
        return Response(status=503)
    drv_locked = True
    html = money.get_from_url(drv, "https://moneyforward.com/cf")

    drv_locked = False
    return str(html.decode("utf-8"))

@app.route("/moneyforward/cf/lastmonth", methods=["GET"])
def moneyforward_lastmonth_get():
    global drv_locked
    if drv_locked:
        return Response(status=503)
    drv_locked = True
    html = money.get_from_url_cf_lastmonth(drv)

    drv_locked = False
    return str(html.decode("utf-8"))

@app.route("/moneyforward/status", methods=["GET"])
def moneyforward_status():
    global drv_locked
    if drv_locked:
        return Response(status=503)
    drv_locked = True
    xpaths = os.getenv("refresh_xpaths").split(",")
    ret_f_json = money.get_status(drv, xpaths)

    drv_locked = False
    return ret_f_json

@app.route("/moneyforward/status", methods=["PUT"])
def moneyforward_status_update():
    global drv_locked
    if drv_locked:
        return Response(status=503)
    drv_locked = True

    money.move_page(drv, "https://moneyforward.com")
    # Async update button
    asyncio.new_event_loop().run_in_executor(None, _async_update_button, drv)

    # async で driver を使っているので drv_locked を解除しない
    return "Received"

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

def _async_update_button(driver):
    global drv_locked
    refresh_xpaths = os.getenv("refresh_xpaths").split(",")
    for xpath in refresh_xpaths:
        try:
            money.press_from_xpath(driver, xpath)
            logger.info("press update button: %s", xpath)
            time.sleep(5) # 同時押し負荷対策
        except Exception as e:
            logger.warn('failed to press update button: %s', e)
        finally:
            drv_locked = False

main()
