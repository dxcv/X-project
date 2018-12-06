from WindPy import *
w.start()
from tools.to_mysql import ToMysql

def mon():
    month = w.tdays("2007-01-01", "2018-12-06", "Period=M").Data[0]
    mon = [datetime.strftime(x, '%Y-%m-%d') for x in month]
    db = ToMysql()
    for i in mon:
        sql = "INSERT IGNORE INTO month (state_dt) VALUES ('%s')" % (i)
        db.execute(sql)
    return mon

def day():
    d = w.tdays("2007-01-01", "2018-12-06", "Period=D").Data[0]
    days = [datetime.strftime(x, '%Y-%m-%d') for x in d]
    db = ToMysql()
    for i in days:
        sql = "INSERT IGNORE INTO day (state_dt) VALUES ('%s')" % (i)
        db.execute(sql)
    return days


if __name__ == '__main__':
    mon()
    day()