
from WindPy import *
from datetime import *
import pandas as pd
w.start()
from patsy import dmatrices
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


from visual_k import get_visual

get_visual("000906.sh","2010-9-1","2014-1-1")

class factor_test(object):
    def __init__(self,factor, sector, start_date, end_date):
        self.sector = sector
        self.start_date = start_date
        self.end_date = end_date
        self.factor=factor
        self.list =w.wset("sectorconstituent","date="+start_date+";sectorid="+sector).Data[1]
    def get_data(self):
        data = w.wss(self.list, "pct_chg_per,"+self.factor+",industry_sw,ev",
                     "industryType=1;startDate=" + self.start_date + ";endDate=" + self.end_date + ";tradeDate=" + self.start_date)
        df = pd.DataFrame(list(map(list, (zip(*data.Data)))), index=list(data.Codes), columns=data.Fields)
        self.data=df
        return df

    def singal_factor_test(self,data):
        ##数据清洗
        data = data.dropna()
        data = data[data[factor.upper()] < data[factor.upper()].quantile(.95)]
        data = data[data["PCT_CHG_PER"] < data["PCT_CHG_PER"].quantile(.98)]
        data = data[data[factor.upper()] > data[factor.upper()].quantile(.05)]
        data = data[data["PCT_CHG_PER"] > data["PCT_CHG_PER"].quantile(.02)]
        data = data[data["PCT_CHG_PER"] != 0]
        a = data[factor.upper()].map(
            lambda x: x / (data[factor.upper()].max() - data[factor.upper()].min())).values
        data["%s_1" % factor.upper()] = a

        data["%s_2" % factor.upper()] = list(data[factor.upper()].map(lambda x: log(x)))

        ##总览
        ## data.plot.scatter(y='PCT_CHG_PER', x="%s_2" %factor.upper())
        ## from pandas.plotting import scatter_matrix
        ## scatter_matrix(data.iloc[:, 0:3], alpha=0.2, figsize=(6, 6), diagonal='kde')
        ## bp = data.groupby('INDUSTRY_SW')["PCT_CHG_PER"]

        ##因子分组
        def cla(n, lim):
            return '[%.f ,%.f)' % (lim * (n // lim), lim * (n // lim) + lim)

        b = data[factor.upper()].apply(cla, args=(20,)).values
        data["%s_3" % factor.upper()] = b
        ##data.hist(by="%s_3" % factor.upper(), column="PCT_CHG_PER")
        group_industry = data.groupby('INDUSTRY_SW')
        #group_PE = data.groupby(['INDUSTRY_SW', 'VAL_PE_DEDUCTED_TTM_2', ])
        #group_industry.boxplot(column="PCT_CHG_PER")
        ##WLS拟合
        data = data.dropna()
        industrys = data['INDUSTRY_SW']
        x2 = np.array(list(industrys), dtype=np.str)
        dummy = sm.categorical(x2, drop=True)  # 得到申万一级行业虚拟变量

        x1 = np.array(list(data["%s_1" % factor.upper()]))
        x = np.column_stack((x1, dummy))  # 合并回归所需自变量
        y = np.array(list(data["PCT_CHG_PER"]))  # 得到回归所需的因变量
        results = sm.WLS(y, x, weights=list(data.values.T[3])).fit()
        return results,data



sector="a001010f00000000"
factor="val_lnfloatmv"

date=w.tdays("2007-06-26", "2018-07-26", "Period=Q")
returns={}

for i in range(len(date.Data[0])-4):
    print("时间段%s--%s" %(date.Data[0][4 * i].strftime("%Y%m%d"), date.Data[0][4 * i + 4].strftime("%Y%m%d")))
    pe=factor_test(factor,sector,date.Data[0][4 * i].strftime("%Y%m%d"),
                                 date.Data[0][4 * i + 4].strftime("%Y%m%d"))
    data=pe.get_data()
    returns[date.Data[0][4 * i].strftime("%Y%m%d")] = pe.singal_factor_test(data)

from collections import OrderedDict #保持Key的顺序

A_stocks =w.wset("sectorconstituent","date="+"2018-08-20"+";sectorid="+"a001030208000000")
list=pd.DataFrame(A_stocks.Data, columns=A_stocks.Codes, index=A_stocks.Fields).T
A_stocks=w.wss(list["wind_code"].tolist(),"trade_status,maxupordown，ipo_listdays","tradeDate=20180820")
A_stocks=A_stocks[A_stocks["IPO_LISTDAYS"]>900]


trDate="2018-08-20"
quanters = w.tdays("2008-07-01", trDate, "Period=Q").Data[0]
factor = OrderedDict()
for i in range(3):
    time = quanters[-2-4*i].strftime('%Y-%m-%d')
    data = w.wss(A_stocks.index.tolist(), "fa_orgr_ttm,fa_nagr,fa_gpmgr_ttm,fa_npgr_ttm,fa_tagr,fa_ncgr_ttm,fa_oigr_ttm",\
                 "tradeDate=" + time)
    data = pd.DataFrame(data.Data, columns=data.Codes, index=data.Fields).T
    factor["%s" %time] = data
key=[]
for k in factor:
    key.append(k)
factor_ave=(factor[key[0]]+factor[key[1]]+factor[key[2]])/3
factor_ave
factor_grow=factor_ave.mean(axis=1)



