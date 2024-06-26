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
import alert
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


def get_driver_standalone():
    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=webdriver.ChromeOptions(),
    )
    return driver


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    options.add_argument("--user-agent=" + UA)
    chrome_service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=chrome_service, options=options)
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
            # update ボタンが押せなくとも終了しない

    # download HTML
    for url in urls:
        try:
            html = money.get_from_url(driver, url)
            money.write_html(html, url)
            if (
                url == "https://moneyforward.com/cf"
            ):  # このページは先月分のデータも取っておく
                html = money.get_from_url_cf_lastmonth(driver)
                money.write_html(html, url + "_lastmonth")
        except Exception as e:
            lg.error("failed to get HTML: %s", e)
            driver.quit()

            # alert
            alert.send_alert_main(str(e))
            sys.exit(1)

    driver.quit()


if __name__ == "__main__":
    main()
