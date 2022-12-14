# -*- coding: utf-8 -*-
import datetime as dt
import os
SAVE_DIR = '/data/'

import csv
def csvwrite(data):
    today = dt.date.today()  #出力：datetime.date(2020, 3, 22)
    yyyymm = '{0:%Y%m}'.format(today) # 202003
    yyyymmdd = '{0:%Y%m%d}'.format(today) # 20200322
    os.makedirs(SAVE_DIR + yyyymm, exist_ok=True)

    csv_file = open(SAVE_DIR + yyyymm + '/' + yyyymmdd + '.csv', 'wt', newline = '', encoding = 'utf-8')
    csv_write = csv.writer(csv_file)
    for d in data:
        csv_write.writerow(d)

def csvwrite_invoice(data):
    today = dt.date.today()  #出力：datetime.date(2020, 3, 22)
    yyyymm = '{0:%Y%m}'.format(today) # 202003
    yyyymmdd = '{0:%Y%m%d}'.format(today) # 20200322
    os.makedirs(SAVE_DIR + yyyymm, exist_ok=True)

    csv_file = open(SAVE_DIR + yyyymm + '/' + yyyymmdd + '_inv.csv', 'wt', newline = '', encoding = 'utf-8')
    csv_write = csv.writer(csv_file)
    for d in data:
        csv_write.writerow(d)

# if __name__ == "__main__":
#     data = [['取得年月日', '使用量合計(kWh)', '昼時間使用量(kWh)', '夜時間使用量(kWh)'], ['2022/12/31', '-', '-', '-'], ['2022/12/30', '-', '-', '-'], ['2022/12/29', '-', '-', '-'], ['2022/12/28', '-', '-', '-'], ['2022/12/27', '-', '-', '-'], ['2022/12/26', '-', '-', '-'], ['2022/12/25', '-', '-', '-'], ['2022/12/24', '-', '-', '-'], ['2022/12/23', '-', '-', '-'], ['2022/12/22', '-', '-', '-'], ['2022/12/21', '-', '-', '-'], ['2022/12/20', '-', '-', '-'], ['2022/12/19', '-', '-', '-'], ['2022/12/18', '-', '-', '-'], ['2022/12/17', '-', '-', '-'], ['2022/12/16', '-', '-', '-'], ['2022/12/15', '-', '-', '-'], ['2022/12/14', '-', '-', '-'], ['2022/12/13', '-', '-', '-'], ['2022/12/12', '-', '-', '-'], ['2022/12/11', '-', '-', '-'], ['2022/12/10', '-', '-', '-'], ['2022/12/09', '-', '-', '-'], ['2022/12/08', '-', '-', '-'], ['2022/12/07', '-', '-', '-'], ['2022/12/06', '-', '-', '-'], ['2022/12/05', '6', '3', '2'], ['2022/12/04', '8', '6', '2'], ['2022/12/03', '6', '3', '3'], ['2022/12/02', '6', '2', '4'], ['2022/12/01', '6', '4', '2']]
#     csvwrite(data)
