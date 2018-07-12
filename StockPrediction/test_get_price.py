from sqlalchemy import create_engine
import tushare as ts
import datetime as dt
import pandas as pd
import http.client, urllib
import os

def get_price(date_start,date_end,bar,count):
    d1 = dt.datetime.now()
    engine = create_engine('mysql://root:root@127.0.0.1/stocktool?charset=utf8') # 123.206.69.99 server
 # 获取股价 已经使用完毕 禁止更改


    stock_df = pd.read_sql_query("select code from stock_list;",engine)
    stock_s = pd.Series(stock_df['code']).sort_values()
    stock_list = stock_s.tolist()
    counter = 0
    for i in stock_list:
        counter += 1
        # print(i)
        # df = ts.get_k_data(i, ktype='D',start=date_start,end=date_end)
        df = ts.get_k_data(i, ktype='D')
        if(df is None):# 异常情况数据为空
            print("name: "+i)
        else:
            df['stockname'] = i
            df.to_sql('stock_price_test',engine,if_exists='append')
        bar.update(count+counter)

    d2 = dt.datetime.now()
    print("time used: ")
    print(d2-d1)


    print_str = "\ntime used: " + str(d2 - d1)

    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": "a22vgia8q7vszh4zromzgd2jgikxeh",
                     "user": "u6xu8s5vtjz982g9btzrfzm1r6e2q8",
                     "message": "done ！\n" + print_str,
                     "title": os.path.basename(__file__),
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()
    return counter