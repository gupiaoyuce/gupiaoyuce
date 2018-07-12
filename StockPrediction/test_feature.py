import http.client, urllib
import os
import datetime as dt
import time
import sqlalchemy as sa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib as ta
Notifi = True
result = None

def test_feature(date_after,bar,count):
    d1 = dt.datetime.now()

    engine = sa.create_engine('mysql+pymysql://root:root@localhost/stocktool?charset=utf8')
    stock_df = pd.read_sql_query("select DISTINCT code from stockprediction_stock_price;",engine)
    stock_s = pd.Series(stock_df['code']).sort_values()
    stock_list = stock_s.tolist()
    counter = 0

    for i in stock_list:
        counter += 1
        sql_price = "SELECT * FROM stockprediction_stock_price WHERE code = "+i+" and date > '2018-04-01' ORDER BY date;"# 4月1日只是为了缩短预测时获取的数据量，应该是随着时间增加而增加的
        price_data = pd.read_sql(sql_price,engine)
        if(price_data.empty):
            print(i)
        else:
            macd,macds,price_data['macdh']                                  =ta.MACD(price_data['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
            price_data['stoK'],price_data['stoD']                           =ta.STOCH(price_data['high'].values,price_data['low'].values,price_data['close'].values)
            price_data['rsi']                                               =ta.RSI(price_data['close'].values)
            price_data['willR']                                             =ta.WILLR(price_data['high'].values,price_data['low'].values,price_data['close'].values)
            price_data['ultosc']                                            =ta.ULTOSC(price_data['high'].values,price_data['low'].values,price_data['close'].values)
            price_data['mfi']                                               =ta.MFI(price_data['high'].values,price_data['low'].values,price_data['close'].values,price_data['volume'].values)
            price_data.pop('id')# pandas算出结果后会多出一列 存入数据库会报错就pop掉
            """ 判断是否下跌"""
            iD = pd.DataFrame(np.zeros((price_data.shape[0], 1)), columns=['down'])
            iD['down'] = False
            row_number = price_data.shape[0]
            for j in range(0,row_number):
                if(j<2):
                    continue
                elif(price_data.iloc[j-2].high*0.95>price_data.iloc[j].open):#FIXME:两天前的最高价*0.95>预测日的开盘价
                    iD.iloc[j].down = True
                else:
                    continue
            price_data.insert(price_data.shape[1],'down',iD)

            price_data[price_data.date>=dt.datetime.strptime(date_after,'%Y-%m-%d').date()].to_sql('stockprediction_stock_pred',engine,if_exists='append',index=False)
            bar.update(count+counter)

    # 最终手机提示
    if(Notifi):
        d2 = dt.datetime.now()
        print("time used: ")
        print(d2 - d1)
        print_str = "\ntime used: " + str(d2 - d1)
        if(result is not None):
            msg = "done ！\n" + print_str+"\nresult: "+str(result)
        else:
            msg = "done ！\n" + print_str
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                     urllib.parse.urlencode({
                         "token": "a22vgia8q7vszh4zromzgd2jgikxeh",
                         "user": "u6xu8s5vtjz982g9btzrfzm1r6e2q8",
                         "message": msg,
                         "title": os.path.basename(__file__),
                     }), {"Content-type": "application/x-www-form-urlencoded"})
        conn.getresponse()
    return len(stock_list)
