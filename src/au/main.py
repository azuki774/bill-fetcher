from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging
import driver
from pythonjsonlogger import jsonlogger
import argparse
import sys
import au
import os
import time

lg = logging.getLogger(__name__)
lg.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(fmt='%(asctime)s %(levelname)s %(name)s %(message)s', json_ensure_ascii=False)
h.setFormatter(json_fmt)
lg.addHandler(h)

COOKIES='/.cookies'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--login-2fa', action='store_true') # default false
    args = parser.parse_args()
    lg.info("au start")

    lg.info("get driver")
    driver = driver.get_driver()

    if args.login_2fa:
        # login mode
        lg.info("au page login mode")
        au.login_2fa(driver)
        lg.info("save cookies")
        au.save_cookies(driver)
        time.sleep(3600)
        sys.exit(0)

    au.login(driver)

    lg.info("save cookies")
    au.save_cookies(driver)

    lg.info("fetch url: " + "https://mieru.auone.jp/#/results/daily")
    au.get_from_url(driver, "https://mieru.auone.jp/#/results/daily")

    lg.info("auelect end")
