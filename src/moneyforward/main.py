# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import money
import logging
from pythonjsonlogger import jsonlogger

ROOTPAGE_URL = "https://moneyforward.com"

lg = logging.getLogger(__name__)
lg.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s", json_ensure_ascii=False
)
h.setFormatter(json_fmt)
lg.addHandler(h)


def get_driver():
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions(),
    )
    return driver


def main():
    lg.info("fetcher start")
    lg.info("wait sleep for starting server")
    time.sleep(int(os.getenv("START_SLEEP", default="0")))
    lg.info("Get driver")
    driver = get_driver()
    lg.info("Get driver ok")
    driver.implicitly_wait(10)

    # login
    try:
        html = money.login(driver)
    except Exception as e:
        lg.error("failed to login. maybe changing xpath: %s", e)
        driver.quit()
        sys.exit(1)
    lg.info("login ok")

    urls = os.getenv("urls").split(",")

    # Refresh Button
    money.move_page(driver, ROOTPAGE_URL)
    refresh_xpaths = os.getenv("refresh_xpaths").split(",")
    for xpath in refresh_xpaths:
        try:
            money.press_from_xpath(driver, xpath)
            lg.info("press update button: %s", xpath)
            time.sleep(30)  # 反映されるように30sec待っておく
        except Exception as e:
            lg.warn("failed to press update button: %s", e)
            driver.quit()

    # download HTML
    for url in urls:
        try:
            html = money.get_from_url(driver, url)
            money.write_html(html, url)
            if url == "https://moneyforward.com/cf":  # このページは先月分のデータも取っておく
                html = money.get_from_url_cf_lastmonth(driver)
                money.write_html(html, url + "_lastmonth")
        except Exception as e:
            lg.error("failed to get HTML: %s", e)
            driver.quit()
            sys.exit(1)

    driver.quit()


if __name__ == "__main__":
    main()
