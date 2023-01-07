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
