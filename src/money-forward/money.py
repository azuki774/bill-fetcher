# -*- coding: utf-8 -*-
import time
import datetime as dt
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

SAVE_DIR = "/data/"


def login(driver):
    url = "https://id.moneyforward.com/sign_in/email"
    driver.get(url)

    login_id = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div/div/div[1]/div[1]/section/form/div[2]/div/input",
    )
    login_id.send_keys(os.getenv("id"))

    email_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div/div/div[1]/div[1]/section/form/div[2]/div/div[3]/input",
    )
    email_button.click()

    password_form = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/input[2]",
    )
    password_form.send_keys(os.getenv("pass"))

    login_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[3]/input",
    )
    login_button.click()

    # ---
    # login money forward ME
    url = "https://moneyforward.com/sign_in/"
    driver.get(url)

    # choose account button
    choose_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[2]/input",
    )
    choose_button.click()

    html = driver.page_source.encode("utf-8")
    return html


def get_from_url(driver, url):
    print("fetch url: " + url)
    driver.get(url)
    html = driver.page_source.encode("utf-8")
    return html


def write_html(html, url):
    today = dt.date.today()  # 出力：datetime.date(2020, 3, 22)
    yyyymmdd = "{0:%Y%m%d}".format(today)  # 20200322
    os.makedirs(SAVE_DIR + yyyymmdd, exist_ok=True)
    path_w = SAVE_DIR + yyyymmdd + "/" + os.path.basename(url)
    with open(path_w, mode="w") as f:
        f.write(html.decode("utf-8"))
    print("write ok")
    return
