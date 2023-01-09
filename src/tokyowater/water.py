from curses import raw
# -*- coding: utf-8 -*-
import time
import os
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
    driver.get("https://www.suidoapp.waterworks.metro.tokyo.lg.jp/#/login")

    login_id = driver.find_element(by=By.XPATH, value='//*[@id="login-mail"]')

    login_id.send_keys(os.getenv("water_id"))
    print(os.getenv("water_id"))
    password_form = driver.find_element(by=By.XPATH, value='//*[@id="login-pass"]')
    password_form.send_keys(os.getenv("water_pass"))

    login_button = driver.find_element(by=By.XPATH, value='//*[@id="Content"]/div/div/div/div[1]/div/div[2]/form/button')
    login_button.click()

    time.sleep(5)
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    return

def extract_bill(driver):
    driver.get("https://www.suidoapp.waterworks.metro.tokyo.lg.jp/#/portal")
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(5)

    # 請求期間
    billing_date_field = driver.find_element(by=By.XPATH, value='//*[@id="Content"]/div/div/div/div[2]/div[1]/div[1]/div/p')
    print(billing_date_field.get_attribute("textContent"))
    # 使用量
    value_field = driver.find_element(by=By.XPATH, value='//*[@id="Content"]/div/div/div/div[2]/div[1]/div[1]/div/div[1]/p[2]/span[1]')
    print(value_field.get_attribute("textContent"))
    # 利用期間
    usage_term_field = driver.find_element(by=By.XPATH, value='//*[@id="Content"]/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/p[2]/span')
    print(usage_term_field.get_attribute("textContent"))
    # 利用量
    usage_amount_field = driver.find_element(by=By.XPATH, value='//*[@id="Content"]/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/p[2]/span[1]')
    print(usage_amount_field.get_attribute("textContent"))
    # 内訳（水道）
    detail_waterprice_field = driver.find_element(by=By.XPATH, value='//*[@id="Content"]/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div[3]/p[2]/span[1]')
    print(detail_waterprice_field.get_attribute("textContent"))
    # 内訳（下水道）
    detail_sewerprice_field = driver.find_element(by=By.XPATH, value='//*[@id="Content"]/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div[4]/p[2]/span[1]')
    print(detail_sewerprice_field.get_attribute("textContent"))
    # 現状では1ヶ月分
    ret = [[
        billing_date_field.get_attribute("textContent"), 
        value_field.get_attribute("textContent"), 
        usage_term_field.get_attribute("textContent"), 
        usage_amount_field.get_attribute("textContent"), 
        detail_waterprice_field.get_attribute("textContent"), 
        detail_sewerprice_field.get_attribute("textContent")
    ]]
    print(ret)

    return ret
