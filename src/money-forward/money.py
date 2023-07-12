# -*- coding: utf-8 -*-
import time
import datetime as dt
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SAVE_DIR = "/data/"


def login(driver):
    url = "https://id.moneyforward.com/sign_in/email"
    driver.get(url)

    login_id = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div[2]/div/div/div[1]/section/form/div[2]/div/input",
    )
    login_id.send_keys(os.getenv("id"))

    email_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div[2]/div/div/div[1]/section/form/div[2]/div/div[3]/button",
    )
    email_button.click()

    password_form = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div[2]/div/div/div[1]/section/form/div[2]/div/div[2]/input",
    )
    password_form.send_keys(os.getenv("pass"))

    login_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div[2]/div/div/div[1]/section/form/div[2]/div/div[3]/button",
    )
    login_button.click()

    # ---
    # login money forward ME
    url = "https://moneyforward.com/sign_in/"
    driver.get(url)

    # choose account button
    choose_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div[2]/div/div/div[1]/section/form/div[2]/div/div[2]/button",
    )
    choose_button.click()

    html = driver.page_source.encode("utf-8")
    return html


def get_from_url(driver, url):
    wait = WebDriverWait(driver=driver, timeout=30)

    print("fetch url: " + url)
    driver.get(url)
    wait.until(EC.presence_of_all_elements_located)
    html = driver.page_source.encode("utf-8")
    return html


def get_from_url_cf_lastmonth(driver):
    # cf ページの last_month を取得して書き出す関数
    wait = WebDriverWait(driver=driver, timeout=30)

    url = "https://moneyforward.com/cf"
    print("fetch url: " + url)
    driver.get(url)
    wait.until(EC.presence_of_all_elements_located)

    # lastmonth_button button
    lastmonth_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/div[3]/div/div/section/div[2]/button[1]",
    )
    lastmonth_button.click()
    time.sleep(15)
    html = driver.page_source.encode("utf-8")
    write_html(html, url + "_lastmonth")
    return


def write_html(html, url):
    today = dt.date.today()  # 出力：datetime.date(2020, 3, 22)
    yyyymmdd = "{0:%Y%m%d}".format(today)  # 20200322
    os.makedirs(SAVE_DIR + yyyymmdd, exist_ok=True)
    path_w = SAVE_DIR + yyyymmdd + "/" + os.path.basename(url)
    with open(path_w, mode="w") as f:
        f.write(html.decode("utf-8"))
    print("write ok")
    return
