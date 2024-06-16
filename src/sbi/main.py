from curses import raw
import time
import datetime
import os
import driver
from venv import create
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import logging
from pythonjsonlogger import jsonlogger

lg = logging.getLogger(__name__)
lg.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s", json_ensure_ascii=False
)
h.setFormatter(json_fmt)
lg.addHandler(h)

SBI_USER = os.getenv("sbi_user")
SBI_PASS = os.getenv("sbi_pass")
SAVE_DIR = "/data/"
LOGIN_URL = "https://site1.sbisec.co.jp/ETGate/"
PORT_URL = "https://site1.sbisec.co.jp/ETGate/?_ControlID=WPLETpfR001Control&_PageID=DefaultPID&_DataStoreID=DSWPLETpfR001Control&_ActionID=DefaultAID&getFlg=on"


# HTMLテーブルデータからCSVを作成
def createCSV(table_data):
    outputCSV = ""
    m = []
    tbody = table_data.find("tbody")
    trs = tbody.find_all("tr")
    for tr in trs:
        r = []
        for td in tr.find_all("td"):
            td_text_without_comma = td.text.replace(",", "")
            r.append(td_text_without_comma)
        m.append(r)
    for r in m:
        outputCSV += ",".join(r)

    return outputCSV


# ディレクトリ作成とファイル名取得する
def get_file_path(index):
    today = datetime.date.today()  # 出力：datetime.date(2020, 3, 22)
    yyyymm = "{0:%Y%m}".format(today)  # 202003
    yyyymmdd = "{0:%Y%m%d}".format(today)  # 20200322
    os.makedirs(SAVE_DIR + yyyymm, exist_ok=True)

    filepath = SAVE_DIR + yyyymm + "/" + yyyymmdd + "_" + str(index) + ".csv"
    return filepath


# 作成した文字列データ(CSV)を指定場所に書き込み
def writeCSV(rawoutputCSV, index):
    filepath = get_file_path(index)
    outputCSV = reshapeCSV(rawoutputCSV)

    with open(filepath, mode="w") as f:
        f.write(outputCSV)

    print(outputCSV)


# 作成した文字列データから空行などを消してCSVフォーマットを整える
def reshapeCSV(rawoutputCSV):
    outputCSV = rawoutputCSV.replace(",\n", ",")
    return outputCSV


if __name__ == "__main__":
    lg.info("Program start")

    # ブラウザ起動
    driver = driver.get_driver()
    lg.info("Get driver")

    # ログインURLにアクセス
    driver.get(LOGIN_URL)
    element = driver.find_element(by=By.NAME, value="ACT_login")
    input_user_id = driver.find_element(by=By.NAME, value="user_id")
    input_user_id.send_keys(SBI_USER)
    input_user_password = driver.find_element(by=By.NAME, value="user_password")
    input_user_password.send_keys(SBI_PASS)

    # ログインボタンを押す
    driver.find_element(by=By.NAME, value="ACT_login").click()
    lg.info("Login")
    time.sleep(5)

    # ポートフォリオページに移動
    driver.get(PORT_URL)
    lg.info("Move portfolio page")
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # ポートフォリオのテーブルを取得
    table_data = soup.find_all(
        "table", bgcolor="#9fbf99", cellpadding="4", cellspacing="1", width="100%"
    )

    # 取得したテーブルを上から順に、#1, #2 をつけて YYYYMMDD_#x.csv として保存
    for i in range(len(table_data)):
        fetch_data = createCSV(table_data[i])
        lg.info("create CSV: #{}".format(i + 1))
        writeCSV(fetch_data, i + 1)
        lg.info("write CSV")

    # ブラウザを閉じる
    driver.quit()
