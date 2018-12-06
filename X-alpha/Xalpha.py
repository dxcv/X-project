from WindPy import *
from datetime import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.matplotlib_fname()
w.start()
import tushare as ts

# 解决中文乱码问题
#sans-serif就是无衬线字体，是一种通用字体族。
#常见的无衬线字体有 Trebuchet MS, Tahoma, Verdana, Arial, Helvetica, 中文的幼圆、隶书等等。
mpl.rcParams['font.sans-serif']=['SimHei'] #指定默认字体 SimHei为黑体
mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.style.use('ggplot')
from tools import get_wind_data
from tools.to_mysql import ToMysql
from tools.toMysql import MySQLAlchemy

# factor 表的索引
context = {
    "state_dt":0,
    "stock_code":1,
    "val_floatmv":2,
    "industry_sw":3
}
#####常用因子######

##价值类##
##fa_roicebit_ttm                 投入资本回报率ROIC
##fa_ocftoor_ttm                  经营活动产生的现金流量净额/营业收入
##fa_debttoasset                  资产负债率
##fa_npgr_ttm                     净利润增长率
##fa_orgr_ttm                     营业收入增长率
##pe_ttm                          市盈率
##val_mvtoebitda_ttm              市值/EBITDA
##pb_lf                           市净率


##风险类##
##beta_24m                        BETA近24个月
##annualstdevr_24m                年化波动率近24个月

##量价类##
##tech_price1y                   当前股价/过去一年均价-1

class Xalpha(object):
    def __init__(self,start_date,end_date,trdate,period ="M"):
        self.start_date = start_date
        self.end_date = end_date
        self.trdate = trdate
        self.period = period

    def prepare_raw_data(self,stock_code, ind_codes):
        ind_cod = ""
        for i in ind_codes:
            ind_cod += "," + i
        ind_cod = ind_cod[1:]
        in_str = '('
        for x in range(len(stock_code)):
            if x != len(stock_code) - 1:
                in_str += str('\'') + str(stock_code[x]) + str('\',')
            else:
                in_str += str('\'') + str(stock_code[x]) + str('\')')
        db = ToMysql()
        sql_select = "select state_dt,stock_code,"+\
                     ind_cod+" from factor_mon where stock_code in %s and state_dt = '%s'" %(in_str,self.trdate)
        done_select = db.select(sql_select)
        state_dt =  [x[0] for x in done_select]
        stock_code = [x[1] for x in done_select]
        data = []
        for code in range(len(ind_codes)):
            indata =[x[code+2] for x in done_select]
            data.append(indata)
        tuples = list(zip(*[state_dt,stock_code]))
        index = pd.MultiIndex.from_tuples(tuples, names=['state_dt', 'stock_code'])
        raw_data = pd.DataFrame(data= data, columns=ind_codes,index= index)
        return raw_data

    def put_winddata_tosql(self,stock, ind_codes):
        db = ToMysql()
        data = self.get_winddata(stock,ind_codes)
        for code in ind_codes:
            if data[code.upper()].dtypes == object:
                for i in range(len(data)):
                    sql = "insert into factor_mon (state_dt,stock_code, %s) " \
                          "VALUES ('%s','%s','%s') on  DUPLICATE key update  %s = '%s'"\
                          %(code,self.trdate, data.index[i], data[code.upper()][i],code,data[code.upper()][i])
                    db.execute(sql)
            else:
                for i in range(len(data)):
                    sql = "insert into factor_mon (state_dt,stock_code, %s) " \
                          "VALUES ('%s','%s',%f) on  DUPLICATE key update  %s = %f" \
                          % (code, self.trdate, data.index[i], data[code.upper()][i], code, data[code.upper()][i])
                    db.execute(sql)

    def get_winddata(self,stock, ind_codes):

        data = get_wind_data.wss(stock,self.trdate,ind_codes).get_data()
        return data


if __name__ == '__main__':

    ts.set_token('502bcbdbac29edf1c42ed84d5f9bd24d63af6631919820366f53e5d4')
    pro = ts.pro_api()
    list_500 = 
    x =  Xalpha("2018-01-22","2018-12-31","2018-01-22")
    d = x.prepare_raw_data(["600008.SH","600010.SH"],["val_floatmv","industry_sw"])
    print(d)
