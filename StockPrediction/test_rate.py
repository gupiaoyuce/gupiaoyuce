import http.client, urllib
import os
import sqlalchemy as sa
import pandas as pd
import datetime as dt
import numpy as np
d1 = dt.datetime.now()
engine = sa.create_engine('mysql://kevin:@127.0.0.1/Stock?charset=utf8') # 123.206.69.99 server
stock_df = pd.read_sql_query("select code from stock_list;",engine)
stock_s = pd.Series(stock_df['code']).sort_values()
stock_list = stock_s.tolist()
counter = 0
for i in stock_list:
    print(i)
    list = []
    list2= []
    sql = "SELECT * FROM stock_price_test_allfeature WHERE stockname = "+i+" ORDER BY date;"
    stock_price_df = pd.read_sql_query(sql,engine)
    # stock_price_UD = pd.DataFrame(np.zeros((stock_price_df.shape[0],1)),columns=['UpOrDown'])
    # stock_price_UD['UpOrDown']=False
    # print(stock_price_df)
    stock_price_df.pop('level_0')
    stock_price_df.pop('index')
    stock_price_df['rate']=-1
    row_number = stock_price_df.shape[0]
    for j in range(0, row_number):
        if j + 16> row_number:
            # print(j)
            break
        else:
            sub_df = stock_price_df.iloc[j:j+16]
            if(sub_df.iloc[0].high*0.95 > sub_df.iloc[2].open):
                stock_price_df.rate.iloc[j+2]=sub_df.iloc[4:16].high.max()/sub_df.iloc[3].low
                # if((1.15*sub_df.iloc[3].low) < sub_df.iloc[4:16].high.max()):
                #     list2.append(j+2)
                    # counter +
    # stock_price_UD['UpOrDown'].loc[list2]=True
    # print(stock_price_UD.loc[list2])
    # list.append(j)

    # else:
    #     counter += 1
    #     list.append(j+2)
    # print('1')
    # print(stock_price_UD.loc[list2])
    # stock_price_df.insert(stock_price_df.shape[1],'UpOrDown',stock_price_UD)
    # print(stock_price_df)
    # print(stock_price_UD[stock_price_UD['UpOrDown']==True])
    stock_price_df.to_sql('stock_label_3d_openrate',engine,if_exists='append')
    # stock_price_df.iloc[list].to_sql('stock_label_3d',engine,if_exists='append')



print("total number: ")
print(counter)
d2 = dt.datetime.now()
print("time used: ")
print(d2-d1)
print_str = "total number: "+str(counter)+"\ntime used: "+str(d2-d1)

conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": "a22vgia8q7vszh4zromzgd2jgikxeh",
    "user": "u6xu8s5vtjz982g9btzrfzm1r6e2q8",
    "message": "done ！\n"+print_str,
    "title":os.path.basename(__file__),
  }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()
