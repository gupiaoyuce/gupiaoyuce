from sqlalchemy import create_engine
import tushare as ts
import datetime as dt
import pandas as pd
import http.client, urllib
import os
d1 = dt.datetime.now()
def get_price(start_date,bar,count): #FIXME:获取股价时 请不要多次运行，数据有可能会重复
    engine = create_engine('mysql://root:root@127.0.0.1/stocktool?charset=utf8') # 123.206.69.99 server

    stock_df = pd.read_sql_query("select code,name from stock_list;",engine)# stock_list是指股票列表 记录所有股票的代码以及名称，用于遍历股票代码
    stock_s = pd.Series(stock_df['code']).sort_values()
    stock_list = stock_s.tolist()
    # counter = 0
    for i in stock_list:

        df = ts.get_k_data(i, ktype='D',start=start_date)# 取start_date及以后的价格
        if(df.empty):# 异常情况数据为空，经常会有报错 可以忽略
            print("name: "+i)
        else:
            df['stockname'] =  stock_df[stock_df['code']==i].name.iloc[0]
            df[['date','open','high','close','low','code','stockname','volume']].to_sql('stockprediction_stock_price',engine,if_exists='append',index=False)#存储数据

    d2 = dt.datetime.now()#FIXME:记录用时，每个文件都有。
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
