# -*- coding: utf-8 -*-
import csv
import time
import os
import sys
from venv import create
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import money


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=ja-JP")
    options.add_argument("--disable-dev-shm-usage")
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    options.add_argument("--user-agent=" + UA)
    chrome_service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=chrome_service, options=options)
    return driver


def main():
    print("fetcher start")
    print("Get driver")
    driver = get_driver()
    driver.implicitly_wait(5)

    html = money.login(driver)
    print("login ok")

    urls = os.getenv("urls").split(',')

    for url in urls:
        html = money.get_from_url(driver, url)
        money.write_html(html, url)


if __name__ == "__main__":
    main()