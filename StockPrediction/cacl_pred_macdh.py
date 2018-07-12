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

d1 = dt.datetime.now()

engine = sa.create_engine('mysql://root:root@localhost/stocktool?charset=utf8')


# stock_df = pd.read_sql_query("select DISTINCT code from stockprediction_stock_pred;", engine)
# stock_s = pd.Series(stock_df['code']).sort_values()
# stock_list = stock_s.tolist()
counter = 0
# print(counter)
# for i in stock_list:
#     print(i)
calc_pred_df = pd.DataFrame(columns=['code','stockname','hopeopen','buydate','hopesale','high','highdate'])
counter += 1
sql_price = "select * from stockprediction_stock_pred where date> '2018-04-24' and date <='2018-05-03' and (macdh > 0.6 or macdh< -1.2) and down = 1;"
tmp_data = pd.read_sql(sql_price,engine)
row_num = tmp_data.shape[0]
for j in range(0,row_num):
    tmp_code = tmp_data.iloc[j].code
    tmp_date = tmp_data.iloc[j].date
    # print(type(tmp_date))

    sql_str = "select * from stockprediction_stock_pred where code = "+str(tmp_code)+" and date > '"+tmp_date.strftime("%Y-%m-%d")+"' order by date";
    price_data = pd.read_sql(sql_str,engine)
    # print(price_data)
# price_data = pd.read_sql(sql_price,engine)
# row_number = price_data.shape[0]
# for j in range(0,row_number):
#     if j+16>row_number:
#         break;
#     else:
    sub_df = price_data.iloc[0:16]
        # print(sub_df.date)
        # if(sub_df.iloc[0].down == 1 and sub_df.iloc[0].macdh is not None and(sub_df.iloc[0].macdh > 0.6 or sub_df.iloc[0].macdh<-1.2)):
        #     print(sub_df)
    tmp_high = sub_df.iloc[1:16].high.max()
    # print(sub_df[sub_df.high == tmp_high].iloc[0])
    calc_pred_df.loc[calc_pred_df.shape[0]+1] = {'code':tmp_code,
                                                 'stockname':sub_df.iloc[0].stockname,
                                                 'hopeopen':sub_df.iloc[1].open,
                                                 'buydate':sub_df.iloc[1].date,
                                                 'hopesale':sub_df.iloc[1].open*1.08,
                                                 'high':tmp_high,
                                                 'highdate':sub_df[sub_df.high == tmp_high].iloc[0].date}
# print(calc_pred_df)
    # print(calc_pred_df)
calc_pred_df.to_sql('stockprediction_pred_anal_macdh',engine,if_exists='append',index=False)
    # iD = pd.DataFrame(np.zeros((price_data.shape[0], 1)), columns=['down'])

""" 
for j in range(0,row_number):
    if(j<2):
        continue
    elif(price_data.iloc[j-2].high*0.95>price_data.iloc[j].open):
        iD.iloc[j].down = True
    else:
        continue
    price_data.insert(price_data.shape[1],'down',iD)
"""


    # price_data[price_data.date>=dt.datetime.strptime(date_after,'%Y-%m-%d').date()].to_sql('stockprediction_stock_pred',engine,if_exists='append',index=False)
    # print(counter)
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