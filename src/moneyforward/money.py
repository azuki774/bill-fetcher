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
import logging
from pythonjsonlogger import jsonlogger

lg = logging.getLogger(__name__)
lg.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(fmt='%(asctime)s %(levelname)s %(name)s %(message)s', json_ensure_ascii=False)
h.setFormatter(json_fmt)
lg.addHandler(h)

SAVE_DIR = "/data/"


def login(driver):
    url = "https://id.moneyforward.com/sign_in/email"
    driver.get(url)

    login_id = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div/div[2]/div/section/div/form/div/div/input",
    )
    login_id.send_keys(os.getenv("id"))

    email_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div/div[2]/div/section/div/form/div/button",
    )
    email_button.click()

    password_form = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div/div[2]/div/section/div/form/div/div[2]/input",
    )
    password_form.send_keys(os.getenv("pass"))

    login_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div/div[2]/div/section/div/form/div/button",
    )
    login_button.click()

    # ---
    # login money forward ME
    url = "https://moneyforward.com/sign_in/"
    driver.get(url)

    # choose account button
    choose_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div/div[2]/div/section/div/form/div/button",
    )
    choose_button.click()

    html = driver.page_source.encode("utf-8")
    return html


def get_from_url(driver, url):
    wait = WebDriverWait(driver=driver, timeout=30)

    lg.info("fetch url: " + url)
    driver.get(url)
    wait.until(EC.presence_of_all_elements_located)
    html = driver.page_source.encode("utf-8")
    return html


def get_from_url_cf_lastmonth(driver):
    # cf ページの last_month を取得して書き出す関数
    wait = WebDriverWait(driver=driver, timeout=30)

    url = "https://moneyforward.com/cf"
    lg.info("fetch url: " + url)
    driver.get(url)
    wait.until(EC.presence_of_all_elements_located)

    # lastmonth_button button
    lastmonth_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/div[1]/div[3]/div/div/section/div[2]/button[1]",
    )
    lastmonth_button.click()
    time.sleep(2)
    html = driver.page_source.encode("utf-8")
    return html


def move_page(driver, url):
    wait = WebDriverWait(driver=driver, timeout=30)
    lg.info("move page url: " + url)
    driver.get(url)
    return

def press_from_xpath(driver, xpath):
    """
    指定したxpathのリンクを押す
    ページはすでに遷移済にしておくこと
    """
    xpath_link = driver.find_element(
        by=By.XPATH,
        value=xpath,
    )
    xpath_link.click()
    return


def write_html(html, url):
    today = dt.date.today()  # 出力：datetime.date(2020, 3, 22)
    yyyymmdd = "{0:%Y%m%d}".format(today)  # 20200322
    os.makedirs(SAVE_DIR + yyyymmdd, exist_ok=True)
    path_w = SAVE_DIR + yyyymmdd + "/" + os.path.basename(url)
    with open(path_w, mode="w") as f:
        f.write(html.decode("utf-8"))
    lg.info("write ok")
    return
