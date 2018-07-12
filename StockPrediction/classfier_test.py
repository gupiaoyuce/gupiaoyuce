import http.client, urllib
import os
import datetime as dt
import tensorflow as tf
import sqlalchemy as sa
import pandas as pd
import numpy as np
# import matplotlib.pyplot    as plt


def test_classfier(date_after, bar, count, train_times):
    d1 = dt.datetime.now()

    train_count = train_times # 训练次数
    train_grad  = 0.1 #梯度下降
    train_grad2  = 0.01 #梯度下降
    layer1_num  = 3 #1层神经元数量
    layer2_num  = 10 #2层神经元数量 使用
    layer3_num  = 5 #3层神经元数量 使用
    input_num   = 7 #输入单元数量
    output_num  = 2 #输出单元数量
    #绘图初始化
    fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    bx = fig.add_subplot(1,1,1)



    # 数据获取
    engine = sa.create_engine('mysql://root:root@localhost/stocktool?charset=utf8')
    # sql_train_true      = "SELECT open,close,high,low FROM stock_label_true WHERE date >= '2016-01-01' AND date < '2017-01-01';"
    # sql_train_false     = "SELECT open,close,high,low FROM stock_label_false WHERE date >='2016-01-01' AND date < '2017-01-01';"
    # sql_varify_true     = "SELECT open,close,high,low FROM stock_label_true WHERE date >='2017-01-01';"
    # sql_varify_false    = "SELECT open,close,high,low FROM stock_label_false WHERE date>='2017-01-01';"
    #
    # sql_train_true      = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi FROM stock_label_3d_rate WHERE DATE >= '2016-01-01' AND date < '2017-01-0-1' AND macd IS NOT NULL AND (rate>1.08) AND (macdh > 1 or macdh < -1);"
    # sql_train_false     = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi FROM stock_label_3d_rate WHERE DATE >= '2016-01-01' AND date < '2017-01-0-1' AND macd IS NOT NULL AND (rate < 1.08 AND rate != -1) AND (macdh > 1 or macdh < -1);"
    # sql_varify_true     = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi FROM stock_label_3d_rate WHERE DATE >= '2017-01-01' AND macd IS NOT NULL AND (rate>1.08) AND (macdh > 1 or macdh < -1) ;"
    # sql_varify_false    = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi FROM stock_label_3d_rate WHERE DATE >= '2017-01-01' AND macd IS NOT NULL AND (rate < 1.08 AND rate != -1)  AND (macdh > 1 or macdh < -1) ;"

    # sql_train_true = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi FROM stock_label_3d_rate WHERE DATE >= '2016-01-01' AND date < '2017-01-0-1' AND macd IS NOT NULL AND (rate>1.08) ;"
    # sql_train_false = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi FROM stock_label_3d_rate WHERE DATE >= '2016-01-01' AND date < '2017-01-0-1' AND macd IS NOT NULL AND (rate < 1.08 AND rate != -1);"
    # sql_varify_true = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi FROM stock_label_3d_rate WHERE DATE >= '2018-01-01' AND macd IS NOT NULL AND (rate>1.08) ;"
    # sql_varify_false = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi FROM stock_label_3d_rate WHERE DATE >= '2018-01-01' AND macd IS NOT NULL AND (rate < 1.08 AND rate != -1) ;"
    # sql_varify_true     = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi FROM stock_label_3d_rate WHERE DATE >= '2017-01-01' AND macd IS NOT NULL AND (rate>1.08) AND (macdh > 1 or macdh < -1);"
    # sql_varify_false    = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi FROM stock_label_3d_rate WHERE DATE >= '2017-01-01' AND macd IS NOT NULL AND (rate < 1.08 AND rate != -1) AND (macdh > 1 or macdh < -1);"



    sql_train_true      = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi FROM stock_label_3d_rate WHERE date < '2018-01-01' AND (macdh<-1.2 or macdh>0.6) AND rate>1.08 AND rate != -1;"
    sql_train_false     = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi FROM stock_label_3d_rate WHERE date < '2018-01-01' AND (macdh<-1.2 or macdh>0.6) AND rate<=1.08 AND rate != -1;"
    sql_test            = "SELECT macdh,stoK,stoD,rsi,willR,ultosc,mfi,code,date FROM stock_price_test_down WHERE date>='"+date_after+"' AND (macdh<-1.2 or macdh>0.6) AND isDown = 1;"
    print(sql_test)
    x_train_true        = pd.read_sql_query(sql_train_true, engine)
    x_train_false       = pd.read_sql_query(sql_train_false,engine)
    x_test              = pd.read_sql_query(sql_test,engine)

    x_train_false.macdh  = x_train_false.macdh.astype('float32')
    x_train_true.macdh  = x_train_true.macdh.astype('float32')
    x_test.macdh = x_test.macdh.astype('float32')

    x_train_false.stoK  = x_train_false.stoK.astype('float32')
    x_train_true.stoK  = x_train_true.stoK.astype('float32')
    x_test.stoK = x_test.stoK.astype('float32')

    x_train_false.stoD  = x_train_false.stoD.astype('float32')
    x_train_true.stoD  = x_train_true.stoD.astype('float32')
    x_test.stoD = x_test.stoD.astype('float32')

    x_train_false.rsi  = x_train_false.rsi.astype('float32')
    x_train_true.rsi  = x_train_true.rsi.astype('float32')
    x_test.rsi = x_test.rsi.astype('float32')

    x_train_false.willR  = x_train_false.willR.astype('float32')
    x_train_true.willR  = x_train_true.willR.astype('float32')
    x_test.willR = x_test.willR.astype('float32')

    x_train_false.ultosc  = x_train_false.ultosc.astype('float32')
    x_train_true.ultosc  = x_train_true.ultosc.astype('float32')
    x_test.ultosc = x_test.ultosc.astype('float32')

    x_train_false.mfi  = x_train_false.mfi.astype('float32')
    x_train_true.mfi  = x_train_true.mfi.astype('float32')
    x_test.mfi = x_test.mfi.astype('float32')
    x_train_true['j']   = 1
    x_train_false['j']  = 0
    x_train_false = x_train_false.sample(frac=1)
    # x_train_true = x_train_true.sample(frac=1)
    x_train_false=x_train_false[0:x_train_true.shape[0]]# 正负标签等量
    x_train = x_train_true.append(x_train_false,ignore_index=True)
    x_train = x_train.sample(frac=1)
    x_train.macdh=x_train.macdh/100

    x_train.stoK=x_train.stoK/100

    x_train.stoD=x_train.stoD/100

    x_train.rsi=x_train.rsi/100

    x_train.willR=x_train.willR/100

    x_train.ultosc=x_train.ultosc/100

    x_train.mfi=x_train.mfi/100

    # x_varify_false=x_varify_false[0:x_varify_true.shape[0]]# 正负标签等量
    x_test          =x_test.sample(frac=1)
    x_test.macdh    =x_test.macdh/100
    x_test.stoK     =x_test.stoK/100
    x_test.stoD     =x_test.stoD/100
    x_test.rsi      =x_test.rsi/100
    x_test.willR    =x_test.willR/100
    x_test.ultosc   =x_test.ultosc/100
    x_test.mfi      =x_test.mfi/100
    y_train_d = pd.DataFrame(np.zeros((x_train.shape[0],2)))
    y_train_d = y_train_d.astype('int32')
    # print(x_test)
    for i in range(0,y_train_d.shape[0]):
        if(x_train.j.iloc[i]):
            y_train_d.iloc[i:i+1,1]=1
        else:
            y_train_d.iloc[i:i+1,0]=1
    # 调试
    # print(x_train)
    # print(x_varify)
    # print("y_train_d")
    # print(y_train_d)
    # print(x_train_true.shape[1])

    xs = tf.placeholder(tf.float32,[None,7])
    ys = tf.placeholder(tf.float32,[None,2])

    l1 = tf.layers.dense(xs,layer1_num,name="l1")
    # l2 = tf.layers.dense(l1,layer2_num,activation=tf.nn.softmax,name="l2")
    # l3 = tf.layers.dense(l2,layer3_num,activation=tf.nn.softmax,name="l3")
    prediction = tf.layers.dense(l1,output_num,activation=tf.nn.softmax,name="prediction")
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys-prediction), reduction_indices=[1]))
    train_step = tf.train.GradientDescentOptimizer(train_grad).minimize(loss)
    train_step2 = tf.train.GradientDescentOptimizer(train_grad2).minimize(loss)


    # def judge_accuracy():
    #     ans = sess.run(prediction, feed_dict={xs: x_varify.iloc[:, 0:input_num]})
    #     ans2 = tf.argmax(ans, 1)
    #     accuracy_prediction = tf.equal(ans2, x_varify_j)
    #     accuracy = sess.run(tf.reduce_mean(tf.cast(accuracy_prediction, tf.float64)))
    #     print("result: "+str(accuracy))
    #     bx.scatter(i,accuracy)

    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)

    #训练
    for i in range(train_count):
        if(i<400):
            sess.run(train_step,feed_dict={xs:x_train.iloc[:,0:input_num],ys:y_train_d.iloc[:,:]})
        else:
            sess.run(train_step2,feed_dict={xs:x_train.iloc[:,0:input_num],ys:y_train_d.iloc[:,:]})
        bar.update(i+count+1)
        # if i%10==0:
        #     print(i)
            # judge_accuracy()

    #训练2
    # for i in range(train_count):
    #     print(x_train.iloc[i*500:(i+1)*500,0:input_num])
    #     print(y_train_d.iloc[i*500:(i+1)*500,:])
    #     if(i<400):
    #         sess.run(train_step,feed_dict={xs:x_train.iloc[i*500:(i+1)*500,0:input_num],ys:y_train_d.iloc[i*500:(i+1)*500,:]})
    #     else:
    #         sess.run(train_step2,feed_dict={xs:x_train.iloc[i*500:(i+1)*500,0:input_num],ys:y_train_d.iloc[i*500:(i+1)*500,:]})
    #
    plt.ion()
    plt.show()

    ans = sess.run(prediction,feed_dict={xs:x_test.iloc[:,0:7]})

    # print(ans_pd)

    # print(ans)
    ans2 = sess.run(tf.argmax(ans,1))
    print('ans2')
    print(type(ans2))
    x_test['ans'] = pd.DataFrame(ans2)
    x_test.to_csv(date_after+'.csv',encoding='utf-8')
    bar.update(train_count+count+1)
    # accuracy_prediction = tf.equal(ans2, x_varify_j)
    # accuracy = tf.reduce_mean(tf.cast(accuracy_prediction, tf.float64))
    # tp_op = tf.reduce_sum(tf.cast(tf.logical_and(tf.equal(x_varify_j,tf.ones_like(  x_varify_j)),tf.equal(ans2,tf.ones_like(    ans2))),'int32'))
    # tn_op = tf.reduce_sum(tf.cast(tf.logical_and(tf.equal(x_varify_j,tf.zeros_like( x_varify_j)),tf.equal(ans2,tf.zeros_like(   ans2))),'int32'))
    # fp_op = tf.reduce_sum(tf.cast(tf.logical_and(tf.equal(x_varify_j,tf.zeros_like( x_varify_j)),tf.equal(ans2,tf.ones_like(    ans2))),'int32'))
    # fn_op = tf.reduce_sum(tf.cast(tf.logical_and(tf.equal(x_varify_j,tf.ones_like(  x_varify_j)),tf.equal(ans2,tf.zeros_like(    ans2))),'int32'))
    # tp = sess.run(tp_op)
    # tn = sess.run(tn_op)
    # fp = sess.run(fp_op)
    # fn = sess.run(fn_op)
    # print(ans2)
    # print(tp)
    # print(tn)
    # print(fp)
    # print(fn)
    # result = sess.run(accuracy)
    # print("acc")
    # print(result)
    # recall = float(tp)/(float(tp)+float(fn))
    # precision = float(tp)/(float(tp)+float(fp))
    # print('recall')
    # print(recall)
    # print('precision')
    # print(precision)
    # print(x_test[(x_test.date>'2018-04-01')&(x_test.date<'2018-04-10')])

    sess.close()
    # 最终手机提示d
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

    return train_count+1