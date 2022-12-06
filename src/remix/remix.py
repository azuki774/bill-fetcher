from curses import raw
# -*- coding: utf-8 -*-
import csv
import re
import time
import json
import datetime
import os
import driver
from venv import create
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import datetime

def login(driver):
    driver.get("https://portal.remix-denki.com/index.php")

    login_id = driver.find_element(by=By.XPATH, value='/html/body/form/div/div/div/div/div[2]/div[1]/input')

    login_id.send_keys(os.getenv("remix_id"))

    password_form = driver.find_element(by=By.XPATH, value='/html/body/form/div/div/div/div/div[2]/div[2]/input')
    password_form.send_keys(os.getenv("remix_pass"))

    login_button = driver.find_element(by=By.XPATH, value='/html/body/form/div/div/div/div/div[2]/a')
    login_button.click()
    driver.implicitly_wait(10)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return

def remove_return(text):
    return text.replace("\n", "")

def fetch_consume_month(driver):
    # [取得年月日, 使用量合計(kWh), 昼時間使用量(kWh), 夜時間使用量(kWh)]
    driver.get("https://portal.remix-denki.com/consumption.php")
    detail_button = driver.find_element(
        by=By.XPATH, value='//*[@id="page-wrapper"]/div[2]/div/div/div[2]/div/table/tbody/tr/td[5]/a'
    )
    detail_button.click()

    day_button = driver.find_element(
        by=By.XPATH, value='//*[@id="page-wrapper"]/div[3]/div/ul/li[2]/a'
    )
    day_button.click()
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    result_data = []
    # セレクタ(タグ：table、クラス：test)
    table = soup.find(id="graph_list")

    trs = table.findAll("tr")

    result_data = []
    for tr in trs:
        row_data = []
        for cell in tr.findAll(['td', 'th']):
            row_data.append(remove_return(cell.get_text()))
        result_data.append(row_data)

    print(result_data)
    return result_data
