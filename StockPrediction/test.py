import os
import tushare as ts
import datetime as dt
today = dt.datetime.today().strftime('%Y-%m-%d')
print(today)
yes = '2018-05-20'
print(ts.is_holiday(yes))
print(ts.is_holiday(today))
def a():
    print(1)