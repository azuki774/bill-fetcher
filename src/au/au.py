import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
from pythonjsonlogger import jsonlogger
import argparse
import pickle

lg = logging.getLogger(__name__)
lg.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(fmt='%(asctime)s %(levelname)s %(name)s %(message)s', json_ensure_ascii=False)
h.setFormatter(json_fmt)
lg.addHandler(h)

SECRET_2FA_FILE="/.2fa_secret"
COOKIES='/.cookies'

def load_cookies(driver):
    cookies = pickle.load(open(COOKIES, 'rb'))
    for cookie in cookies:
        driver.add_cookie(cookie)
    return

def save_cookies(driver):
    pickle.dump(driver.get_cookies(), open(COOKIES, 'wb'))
    return

def login(driver):
    lg.info("au login start")
    url = "https://connect.auone.jp/net/vwc/cca_lg_eu_nets/login?targeturl=https%3A%2F%2Fwww.au.com%2Fenergy%2Fdenki%2Flogin"
    driver.get(url)
    if os.path.isfile(COOKIES):
        lg.info("load cookies")
        try:
            load_cookies(driver)
            lg.info("load cookies success")
        except Exception as e:
            lg.warning('failed to load cookies. skipping. {0}'.format(e))
    else:
        lg.warning("cookie file not found")

    # After loading cookies
    url = "https://connect.auone.jp/net/vwc/cca_lg_eu_nets/login?targeturl=https%3A%2F%2Fwww.au.com%2Fenergy%2Fdenki%2Flogin"
    driver.get(url)

    telno_field = driver.find_element(
        by=By.XPATH,
        value="/html/body/div[2]/div/div[1]/div[2]/div/div/form/input[24]",
    )
    telno_field.send_keys(os.getenv("telno"))

    next_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/div[2]/div/div[1]/div[2]/div/div/form/button[1]",
    )
    next_button.click()
    time.sleep(10)
    html = driver.page_source.encode("utf-8").decode("utf-8")
    print(html)

    pass_field = driver.find_element(
        by=By.XPATH,
        value="/html/body/div[3]/div/div[1]/div[2]/div/div/form/input[25]",
    )
    pass_field.send_keys(os.getenv("pass"))

    login_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/div[3]/div/div[1]/div[2]/div/div/form/button[4]",
    )
    login_button.click()

    lg.info("user/pass login ok")
    time.sleep(10)
    html = driver.page_source.encode("utf-8").decode("utf-8")
    print(html)

def login_2fa(driver):
    login(driver)
    _login_2fa_proc(driver)
    return

def _login_2fa_proc(driver):
    # 前提: https://connect.auone.jp/net/vwc/cca_lg_eu_nets/cca で止まっている状態
    # 2段階認証のためのログイン操作をする
    # /.2fa_secret に 2段階認証コードを書くことで認証を進める
    lg.info("try 2FA login")
    lg.info("please set {0} written 2FA code".format(SECRET_2FA_FILE))
    lg.info("docker exec -it <pod_name> /bin/bash")
    lg.info("echo '<pass>' > {0}".format(SECRET_2FA_FILE))

    while True:
        # ファイルが存在するようになるまで待つ
        if os.path.isfile(SECRET_2FA_FILE):
            break
        time.sleep(10)

    with open(SECRET_2FA_FILE, encoding='utf-8') as f:
        lines = f.read()
        secret_2fa_code = str(lines)

    pass_field = driver.find_element(
        by=By.XPATH,
        value="/html/body/div[2]/div/form/input[7]",
    )
    pass_field.send_keys(os.getenv("pass"))

    login_button = driver.find_element(
        by=By.XPATH,
        value="/html/body/div[2]/div/form/button",
    )
    login_button.click()
    lg.info("2FA login information send")

def get_from_url(driver, url):
    wait = WebDriverWait(driver=driver, timeout=30)
    driver.get(url)
    time.sleep(10)
    wait.until(EC.presence_of_all_elements_located)
    html = driver.page_source.encode("utf-8").decode("utf-8")
    print(html)
    return html
