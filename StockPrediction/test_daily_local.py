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

today = dt.datetime.today().strftime('%Y-%m-%d')
engine = create_engine('mysql+pymysql://root:root@127.0.0.1/stocktool?charset=utf8') #TODO:检查数据库配置是否符合字符串要求，root账号root密码 stocktool数据库名
price_max_date = pd.read_sql_query('select max(date) from stockprediction_stock_price;',engine).iloc[0,0]# 数据库中存储的最新行情日期
pred_max_date = pd.read_sql_query('select max(date) from stockprediction_stock_pred;',engine).iloc[0,0]# 最新的预测日期
anal_max_date = pd.read_sql_query('select max(buydate) from stockprediction_pred_anal_macdh;',engine).iloc[0,0]# 最新的结果分析信息


start_date = price_max_date+dt.timedelta(days=1)# 需要开始的日期
price_max_date = str(price_max_date)
pred_max_date = str(pred_max_date)
# start_date = str(start_date)
start_date = '2018-05-25'
print('行情数据记录最大日期:',price_max_date)
print('预测数据记录最大日期:',pred_max_date)
print('今日日期：',today)

#
if(price_max_date == today):
    print('今日已经预测过了')
    # return ;
else:
        price_num = 5000# 用来标识运算进度的，与prograssbar有关 不影响使用。
        feature_num = 5000
        down_num = 5000
        print("price_num: "+str(price_num))
        print("feature_num: "+str(feature_num))
        print("down_num: "+str(down_num))
        with progressbar.ProgressBar(max_value=price_num+feature_num+down_num+1+train_times,redirect_stdout=True) as bar:
            # price_data_migration.get_price(start_date,bar,count)#FIXME: 获取股票行情时执行

            print('get_price finished')
            # test_feature.test_feature(start_date,bar,count)#FIXME:获取股票特征及判断是否下跌时执行
            print('feature finished')
            # classfier_test.test_classfier(start_date,bar,count,train_times)#FIXME:使用神经网络时执行 可能不能正常运行，请小心使用

            print('prediction finished')
        #FIXME: pushover代码自行更该token以及user
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
          urllib.parse.urlencode({
            "token": "a22vgia8q7vszh4zromzgd2jgikxeh",
            "user": "u6xu8s5vtjz982g9btzrfzm1r6e2q8",
            "message": "done ！\ntotal_num: "+str(price_num+feature_num+down_num+train_times+1),
            "title":os.path.basename(__file__),
          }), { "Content-type": "application/x-www-form-urlencoded" })
        conn.getresponse()
