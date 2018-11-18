
# encoding=utf8
import pymysql


class barToMysql(object):
    """储存行情数据到本地数据库中"""
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
         date  CHAR(16),
         code  CHAR(16),
         open  DOUBLE,
         high  DOUBLE,  
         low   DOUBLE,
         close DOUBLE,
         pct_chg  DOUBLE,
         volume  DOUBLE,
         totalShares DOUBLE,
         totalCapital DOUBLE,
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
            data_code = data["thscode"][i]
            data_open = data["open"][i]
            data_high = data["high"][i]
            data_low = data["low"][i]
            data_close = data["close"][i]
            data_volume = data["amount"][i]
            data_pct_chg = data["changeRatio"][i]
            data_shares = data["totalShares"][i]
            data_capital = data["totalCapital"][i]
            sql = """INSERT INTO %s(date,code,open, high, low, close,pct_chg,volume,totalShares,totalCapital)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" % (table_name,repr(data_date),repr(data_code), data_open, data_high, data_low, data_close,data_pct_chg, data_volume,data_shares,data_capital)
            sql=sql.replace('None', 'NULL')
            self.cursor.execute(sql)
            self.db.commit()


    def delete(self,table_name,date):
        sql="""delete from %s where date=%s""" %(table_name,repr(date))
        self.cursor.execute(sql)
        self.db.commit()


    def get_data(self):
        pass

    def close(self):
        self.db.close()

    def update(self):
        pass


class factorToMysql(object):
    ##储存因子数据到本地数据库中
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
       
                       )""" %table_name
        self.cursor.execute(sql)
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        self.db.commit()

    def insert(self, table_name, data):
        for i in range(len(data)):
            data_date = data["time"][i]
            data_code = data["thscode"][i]
            data_open = data["open"][i]
            data_high = data["high"][i]
            data_low = data["low"][i]
            data_close = data["close"][i]
            data_volume = data["amount"][i]
            data_pct_chg = data["changeRatio"][i]
            data_shares = data["totalShares"][i]
            data_capital = data["totalCapital"][i]
            sql = """INSERT INTO %s(date,code,open, high, low, close,pct_chg,volume,totalShares,totalCapital)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""" % (table_name,repr(data_date),repr(data_code), data_open, data_high, data_low, data_close,data_pct_chg, data_volume,data_shares,data_capital)
            sql=sql.replace('None', 'NULL')
            self.cursor.execute(sql)
            self.db.commit()


    def delete(self,table_name,date):
        sql="""delete from %s where date=%s""" %(table_name,repr(date))
        self.cursor.execute(sql)
        self.db.commit()


    def get_data(self):
        pass

    def close(self):
        self.db.close()

    def update(self):
        pass


class UrlTomysql(object):
    ##储存网址数据到本地数据库中

    def __init__(self):
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_pass = "8261426"
        self.db_name = "stock"
        # 打开数据库连接
        self.db = pymysql.connect(self.db_host, self.db_user, self.db_pass, self.db_name
                                  , use_unicode=True, charset="utf8")
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

    def creat(self, table_name):
        self.cursor.execute("DROP TABLE IF EXISTS %s" % table_name)
        sql = """CREATE TABLE %s (
        id  integer(8),
        url  varchar(255),
        PRIMARY KEY (id)  
                       )""" % table_name
        self.cursor.execute(sql)
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        self.db.commit()

    def insert(self, table_name, data):
        for i in range(len(data)):
            data_url = data["url"][i]
            sql = """INSERT INTO %s (url)
            VALUES (%s)""" % (table_name,repr(data_url))
            sql = sql.replace('None', 'NULL')
            self.cursor.execute(sql)
            self.db.commit()

    def delete(self, table_name, date):
        sql = """delete from %s where date=%s""" % (table_name, repr(date))
        self.cursor.execute(sql)
        self.db.commit()

    def get_data(self):
        pass

    def close(self):
        self.db.close()

    def update(self):
        pass