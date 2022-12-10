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
import remix
import writer

if __name__ == "__main__":
    print("fetcher start")
    args = sys.argv

    remix_fetch_data = []
    driver = driver.get_driver()
    driver.implicitly_wait(10)

    print("Get driver")

    remix.login(driver)
    if len(args) >= 2 and args[1] == 'invoice':
        data = remix.fetch_invoice(driver)
        print("fetcher complete")
        print("writer start")
        writer.csvwrite_invoice(data)
    else:
        data = remix.fetch_consume_month(driver)
        print("fetcher complete")
        print("writer start")
        writer.csvwrite(data)
    
    print("writer end")
    print("the program end")
