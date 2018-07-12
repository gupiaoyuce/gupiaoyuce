import http.client, urllib
import os
from sqlalchemy import create_engine
import tushare as ts
import datetime as dt
# df = ts.get_tick_data('600848', date='2014-12-22')
d1 = dt.datetime.now()
engine = create_engine('mysql+pymysql://root:root@127.0.0.1/stocktool?charset=utf8') # 123.206.69.99 server

sba = ts.get_stock_basics()
sba.to_sql('stock_list',engine,if_exists='append')
d2 = dt.datetime.now()

print("time used: ")
print(d2 - d1)
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
