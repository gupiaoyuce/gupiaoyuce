import test_get_price
import test_feature
import test_is_Down
import classfier_test
import price_data_migration
import http.client, urllib
import os
import datetime as dt
import time
import progressbar
import pandas as pd
from sqlalchemy import create_engine
import tushare as ts
d1 = dt.datetime.now()
count = 0
train_times = 1200
"""

engine = create_engine('mysql://root:root@127.0.0.1/stocktool?charset=utf8') # 123.206.69.99 server
price_num_df = pd.read_sql_query("select count(distinct code) from stock_list;",engine)
feature_num_df = pd.read_sql_query("select count(DISTINCT code) from stock_price_test;",engine)
down_num_df = pd.read_sql_query("select count(distinct code) from stock_price_test_allfeature;",engine)
price_num = price_num_df.iloc[0,0]
feature_num = feature_num_df.iloc[0,0]
down_num = down_num_df.iloc[0,0]
"""
today = dt.datetime.today().strftime('%Y-%m-%d')
# today = '2018-05-17'

print(today)
if(ts.is_holiday(today)):
    # print('yes')
    pass
else:
    # print('no')
    price_num = 5000
    feature_num = 5000
    down_num = 5000
    start_date = '2018-05-17'
    print("price_num: "+str(price_num))
    print("feature_num: "+str(feature_num))
    print("down_num: "+str(down_num))

    # with progressbar.ProgressBar(max_value=price_num+feature_num+down_num+1,redirect_stdout=True) as bar:
    with progressbar.ProgressBar(max_value=price_num+feature_num+down_num+1+train_times,redirect_stdout=True) as bar:
        # test_get_price.get_price(start_date,end_date,bar,count)
        # price_data_migration.get_price(today,bar,count)

        print('get_price finished')
        # count = count+int(price_num)
        test_feature.test_feature(start_date,bar,count)

        print('feature finished')
        # count = count+int(feature_num)
        # test_is_Down.test_down(start_date,bar,count)

        print('down finished')
        # count = count+int(down_num)
        # classfier_test.test_classfier(start_date,bar,count,train_times)

        print('prediction finished')

    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": "a22vgia8q7vszh4zromzgd2jgikxeh",
        "user": "u6xu8s5vtjz982g9btzrfzm1r6e2q8",
        "message": "done ！\ntotal_num: "+str(price_num+feature_num+down_num+train_times+1),
        "title":os.path.basename(__file__),
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
