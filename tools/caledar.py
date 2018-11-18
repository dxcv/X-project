import tushare as ts
ts.set_token('502bcbdbac29edf1c42ed84d5f9bd24d63af6631919820366f53e5d4')
from datetime import *





class calendar(object):
    """日历函数"""
    def __init__(self):
        pro = ts.pro_api()
        date = pro.trade_cal(exchange='', start_date='20180101', end_date='20181231')
        self.year =
        self.da

        