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
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def login(driver):
    driver.get("https://my.nichigas.co.jp/entry")
    html = driver.page_source.encode('utf-8')

    # 事業者選択
    selector = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div/div/div/div/div[4]/div/select')
    select = Select(selector)
    select.select_by_value('00005')

    login_button = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div/div/div/div/div[5]/div')
    login_button.click()
    
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    # ログインページ操作
    login_id = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div/div/div/div/div/div[2]/input[1]')
    login_id.send_keys(os.getenv("nicigas_id"))

    password_form = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div/div/div/div/div/div[2]/input[2]')
    password_form.send_keys(os.getenv("nicigas_pass"))

    login_button = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div/div/div/div/div/div[2]/div[4]')
    login_button.click()
    time.sleep(5)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return

def fetch_invoice(driver):
    driver.get("https://my.nichigas.co.jp/dashboard/gas")
    time.sleep(5)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    # soup = BeautifulSoup(open('/src/testtext.htm'), 'html.parser')
    label_fields = soup.find_all(class_="card-title")
    labels = []

    price_fields = soup.find_all(class_="list-item--text idx-i0")
    prices = []

    use_amount_fields = soup.find_all(class_="list-item--text idx-i1")
    amounts = []

    billing_done_field = soup.find_all(class_="list-item--text idx-i2")
    billing_done = []
    
    # 20xx年yy月分総合料金詳細 取得
    i = 0
    for l in label_fields:
        labels.append(trim_text(l.get_text()))
        i = i + 1
        if i == 12: # 13レコード目以降は重複しているので skip
            break

    # 料金 取得
    i = 0
    for l in price_fields:
        prices.append(trim_text(l.get_text()))
        i = i + 1
        if i == 12: # 13レコード目以降は重複しているので skip
            break

    # 使用量 取得
    i = 0
    for l in use_amount_fields:
        amounts.append(trim_text(l.get_text()))
        i = i + 1
        if i == 12: # 13レコード目以降は重複しているので skip
            break


    # 支払い状態 取得
    i = 0
    for l in billing_done_field:
        billing_done.append(trim_text(l.get_text()))
        i = i + 1
        if i == 12: # 13レコード目以降は重複しているので skip
            break

    records = []
    for i in range(12):
        records.append([labels[i], prices[i], amounts[i], billing_done[i]])
    
    print(records)
    return records


def trim_text(text):
    text = text.replace("\n", "")
    text = text.replace(" ", "")
    text = text.replace('\u3000', '')
    return text


def testfetch_invoice():
    soup = BeautifulSoup(open('/src/testtext.htm'), 'html.parser')
    label_fields = soup.find_all(class_="card-title")
    labels = []

    price_fields = soup.find_all(class_="list-item--text idx-i0")
    prices = []

    billing_done_field = soup.find_all(class_="list-item--text idx-i2")
    billing_done = []
    
    # 20xx年yy月分総合料金詳細 取得
    i = 0
    for l in label_fields:
        labels.append(trim_text(l.get_text()))
        i = i + 1
        if i == 12: # 13レコード目以降は重複しているので skip
            break

    # 料金 取得
    i = 0
    for l in price_fields:
        prices.append(trim_text(l.get_text()))
        i = i + 1
        if i == 12: # 13レコード目以降は重複しているので skip
            break

    # 支払い状態 取得
    i = 0
    for l in billing_done_field:
        billing_done.append(trim_text(l.get_text()))
        i = i + 1
        if i == 12: # 13レコード目以降は重複しているので skip
            break

    records = []
    for i in range(12):
        records.append([labels[i], prices[i], billing_done[i]])
    
    print(records)
    return records
