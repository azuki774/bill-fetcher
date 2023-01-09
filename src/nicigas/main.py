# -*- coding: utf-8 -*-
import csv
import time
import os
import sys
import driver
from venv import create
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import nicigas
import writer

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    options.add_argument('--user-agent=' + UA)
    chrome_service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=chrome_service, options=options)
    return driver

if __name__ == "__main__":
    print("fetcher start")
    args = sys.argv

    options = webdriver.ChromeOptions()

    driver = get_driver()
    driver.implicitly_wait(10)

    print("Get driver")

    nicigas.login(driver)
    data = nicigas.fetch_invoice(driver)
    print("fetcher complete")
    
    print("writer start")
    writer.csvwrite_invoice(data)
    print("writer end")
    print("the program end")

