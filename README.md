# 项目文档

## 文件内容说明
一下内容将采用与项目目录相同的结构进行说明
- StockPrediction/
    - migrations/
        此文件夹由Django框架创建，用于创建与修改数据库。不用动
    - static/ 服务器存储静态文件时使用，例如js或css文件。前端文件，写算法时不需要考虑。
    - __init__.py Django框架创建，__勿动__
    - admin.py Django框架创建，__勿动__
    - apps.py Django框架创建，__勿动__
    - cacl_pred.py 对预测结果进行进行计算，判断这些股票在15天过后最大涨幅是否超过8%。对应结果分析中的折线图以及饼图。__已弃用__，使用下面的cacl_pred_macdh.py
    - cacl_pred_macdh.py 上面的优化版。 加快了计算效率。
    - classfier_test.py 神经网络模型，预测是否为强势反弹股票。尚未启用，启用时需要修改test_daily.py并把数据库连接由down改为prediction
    - models.py 由Django框架创建，定义各个数据库表。
    - price_data_migration.py 每日获取股票行情数据。
    - stock-data.py 第一次运行时需要初始化股票列表。记录都有什么股票代码，用于后续遍历股票操作。
    - test.py 用于尝试某段代码是否能够正确实现，项目中没有实际意义，可随意修改。
    - test_daily.py 每日运行一次，调用了行情计算、指标计算的脚本。开启神经网络只需取消第59行的注释（classfier_test.test_classfier())
    - test_daily_local.py 删了一些代码，功能与test_daily.py 相同，用上面的就可以。
    - test_feature.py 计算每个股票的指标特征
    - test_get_price.py 获取价格，__已弃用__
    - test_is_Down.py 判断是否满足前三天下跌，已经整合到test_feature.py中，__已弃用__
    - test_rate.py 训练模型之前的预处理，判断每个股票最高涨幅，模型训练时可能会用到，在使用模型时不会用到。
    - views.py 由Django框架创建，用于连接url与html，并做一些数据展示的操作。
- StockTools/ Django框架创建，包括url配置，服务器配置等。
- templates/ 网页前端展示所需的html文件
- tmp/ 可删，之前为了引用一个模板，暂时存放在这里。