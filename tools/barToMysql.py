import pymysql


class ToMysql(object):
    def __init__(self):
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_pass = "8261426"
        self.db_name = "stock"
        # 打开数据库连接
        self.db = pymysql.connect(self.db_host, self.db_user, self.db_pass,self.db_name
                                  , use_unicode=True, charset="utf8")
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

    def creat(self, table_name):
        self.cursor.execute("DROP TABLE IF EXISTS %s" % table_name)
        sql = """CREATE TABLE %s (
         date  DATE ,
         code  CHARACTER,
         open  DOUBLE,
         high  DOUBLE,  
         low   DOUBLE,
         close DOUBLE,
         volume  DOUBLE,
         pct_chg  DOUBLE,
         trade_status varchar(20) character set utf8,
         PRIMARY KEY (date,code)   
                       )""" %table_name
        self.cursor.execute(sql)
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        self.db.commit()

    def insert(self, table_name, data):
        for i in range(len(data)):
            data_date = data["time"][i]
            data_code =data["thscode"][i]
            data_open = data["ths_open_price_stock"][i]
            data_high = data["ths_high_price_stock"][i]
            data_low = data["ths_low_stock"][i]
            data_close = data["ths_close_price_stock"][i]
            data_volume = data["ths_amt_stock"][i]
            data_pct_chg = data["ths_chg_ratio_stock"][i]
            data_trade_status = data["ths_trading_status_stock"][i]
            sql = """INSERT INTO %s(date,open, high, low, close,volume,pct_chg,trade_status)
            VALUES (%s,%s,%f,%f,%f,%f,%f,%f,%s)""" % (table_name, repr(data_date),data_code, data_open, data_high, data_low\
                                                 ,data_close, data_volume, data_pct_chg, repr(data_trade_status))
            self.cursor.execute(sql)
            self.db.commit()

    def get_data(self):
        pass

    def close(self):
        self.db.close()

    def update(self):
        pass