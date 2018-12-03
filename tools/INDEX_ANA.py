from WindPy import *
from datetime import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
# 解决中文乱码问题
#sans-serif就是无衬线字体，是一种通用字体族。
#常见的无衬线字体有 Trebuchet MS, Tahoma, Verdana, Arial, Helvetica, 中文的幼圆、隶书等等。
mpl.rcParams['font.sans-serif']=['SimHei'] #指定默认字体 SimHei为黑体
mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.style.use('ggplot')

import matplotlib
matplotlib.matplotlib_fname()
w.start()
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String,Float
from tools.toMysql import MySQLAlchemy

class factor(Base):
    """定义数据库表基类"""
    __tablename__ = 'factor'
    __table_args__ = {
        "mysql_charset": "utf8"
    }

    code = Column(String(50), primary_key=True)
    date = Column(String(50), primary_key=True)
    name = Column(String(50))
    i_weight = Column(String(50))
    PCT_CHG_PER = Column(Float)
    INDUSTRY_CSRC12 = Column(String(200))
    FA_ROICEBIT_TTM = Column(Float)
    FA_OCFTOOR_TTM = Column(Float)
    FA_DEBTTOASSET = Column(Float)
    FA_NPGR_TTM = Column(Float)
    FA_ORGR_TTM = Column(Float)
    TECH_PRICE1Y = Column(Float)
    VAL_MVTOEBITDA_TTM = Column(Float)
    PB_LF = Column(Float)
    BETA_24M = Column(Float)
    ANNUALSTDEVR_24M = Column(Float)
    TURN_ND = Column(Float)
    PCT_CHG_10D = Column(Float)
    PCT_CHG_1M = Column(Float)


class index(object):
    """指数截面表现"""
    def __init__(self, tradate,indexCode ,benchmark):
        self.indexCode = indexCode
        self.tradate = tradate
        self.benchmark = benchmark
        self.factor = None
        self.data = None
        self.indextimeseries = None
        codelist = w.wset('indexconstituent', "date=" + self.tradate + ";windcode=" + self.indexCode)
        self.codelist = pd.DataFrame(codelist.Data, columns=codelist.Codes, index=codelist.Fields,dtype=float).T
        self.list = pd.DataFrame(codelist.Data, columns=codelist.Codes, index=codelist.Fields,dtype=float).T["wind_code"].tolist()

        self.tradedate2 = datetime.strptime(self.tradate, '%Y-%m-%d').strftime('%Y%m%d')
        self.startdate = w.tdaysoffset(-1, self.tradate, "Period=M").Data[0][0].strftime('%Y%m%d')
        self.enddate = w.tdaysoffset(1, self.tradate, "Period=M").Data[0][0].strftime('%Y%m%d')
        self.con = MySQLAlchemy(Base,factor, "stock")
    def get_code_list(self):
        """获取指数成分"""        
        return self.codelist

    def get_factor_fromwind(self):
        """获取指数截面因子"""

        year = datetime.strptime(self.tradate, '%Y-%m-%d').year
        ind ="pct_chg_per,industry_CSRC12,fa_roicebit_ttm,fa_ocftoor_ttm,fa_debttoasset,fa_npgr_ttm,fa_orgr_ttm,tech_price1y,val_mvtoebitda_ttm,pb_lf,beta_24m,annualstdevr_24m,turn_nd,pct_chg_10d,pct_chg_1m" 
        #####因子列表####
        factor =w.wss(self.list, ind,"startDate=%s;endDate=%s;industryType=1;tradeDate=%s;days=-20"%(self.tradedate2,self.enddate,self.tradedate2))
        self.factor = pd.DataFrame(factor.Data, columns=factor.Codes, index=factor.Fields,dtype=float).T
        return self.factor

    def get_factor_fromsql(self):
        pass

    def get_factorfromcsv(self):
        pass

    def saveDataTosql(self):
        data = self.get_data()
        factor_data = [factor(code = data.index[j],
             date = self.tradate,
             name = data["sec_name"][j],
             i_weight = data["i_weight"][j],
             PCT_CHG_PER = data["PCT_CHG_PER"][j] ,
             INDUSTRY_CSRC12 =data["INDUSTRY_CSRC12"][j] ,
             FA_ROICEBIT_TTM = data["FA_ROICEBIT_TTM"][j],
             FA_OCFTOOR_TTM =data["FA_OCFTOOR_TTM"][j] ,
             FA_DEBTTOASSET = data["FA_DEBTTOASSET"][j],
             FA_NPGR_TTM =data["FA_NPGR_TTM"][j] ,
             FA_ORGR_TTM = data["FA_ORGR_TTM"][j],
             TECH_PRICE1Y = data["TECH_PRICE1Y"][j],
             VAL_MVTOEBITDA_TTM = data["VAL_MVTOEBITDA_TTM"][j],
             PB_LF = data["PB_LF"][j],
             BETA_24M = data["BETA_24M"][j],
             ANNUALSTDEVR_24M = data["ANNUALSTDEVR_24M"][j],
             TURN_ND = data["TURN_ND"][j],
             PCT_CHG_10D = data["PCT_CHG_10D"][j],\
             PCT_CHG_1M = data["PCT_CHG_1M"][j]) for j in range(len(data))]
        self.con.insert(factor_data, 2)
             
        

    def get_data(self):
        codelist = self.get_code_list()
        codelist.set_index(['wind_code'], inplace = True)

        factor = self.get_factor_fromwind()
        self.data = pd.concat([codelist,factor], axis=1, join_axes=[factor.index])
        return self.data

    def get_indextimeseries(self):
        data = w.wsd(self.indexCode,"close,pct_chg", "ED-5Y",self.tradate, "")
        self.indextimeseries = pd.DataFrame(data.Data, columns=data.Times, index=data.Fields,dtype=float).T
        self.indextimeseries["PCT_CHG_1"] = self.indextimeseries["PCT_CHG"].map(lambda x: x / 100 + 1)
        self.indextimeseries["nav"] = self.indextimeseries["PCT_CHG_1"].cumprod()

   


    

##因子分组函数
def cla(n, lim):
    return '[%.f ,%.f)' % (lim * ((n-0.01 )// lim), lim * ((n-0.01 ) // lim) + lim)

  ##  b = data["VAL_FLOATMV"].apply(cla, args=(100,)).values
  ##  data["%s_3" % factor.upper()] = b

def visual(data,title, x=None, y=None):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()

def replace1(x,mean,std):
    if x == None:
        x= None
    elif x > mean+3*std:
        x= None
    elif x <=mean+3*std and x >=mean-3*std:
        x=x
    else:
        x=None
    return x

def replace2(x,mean,std):
    if x == None:
        x= None
    elif x > mean+3*std:
        x= None
    elif x <=mean+3*std and x >0:
        x=x
    else:
        x=None
    return x

def DataCleaning(data,cloumn,model):
    """1:正态分布变量，2左边截＞0，右边3西格玛"""
    if model ==1:
        data[cloumn] = data[cloumn].map(
            lambda x: replace1(x, data[cloumn].median(), data[cloumn].std()))
    if model == 2:
        data[cloumn] = data[cloumn].map(
            lambda x: replace2(x, data[cloumn].median(), data[cloumn].std()))



if __name__ == '__main__':
    ####准备数据
    zz500=index("2018-9-26", "000905.SH", "000905.SH")
    zz500.get_code_list()
    zz500.get_factor()
    zz500.get_indextimeseries()
    timeseries = zz500.indextimeseries
    data = zz500.get_data()
    ##data.to_csv("E:\\github\\X\\data.csv",encoding="gbk")
    data= pd.read_csv("E:\\github\\X\\data.csv",encoding="gbk", na_values=["None"])
    ##净值走势图
    aa=plt.figure()
    timeseries["nav"].plot()
    plt.savefig("E:\\github\\X\\2.jpg")

    ##PE分位数
    pe =w.wses("a001030208000000", "sec_pettm_media_chn", "2007-01-19", "2018-10-17", "excludeRule=2;Period=W;DynamicTime=0").Data[0]
    pe_l = []
    for i in range(len(pe)-1):
        i=i+1
        re = sum(pd.Series(pe[0:i]).map(lambda x: 1 if x < pe[0:i][-1] else 0))/len(pe[0:i])
        pe_l.append(re)

    fig, axs = plt.subplots()
    axs.plot(pe_l)



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


    ###因子权重分析
    factor = ['i_weight', 'PCT_CHG_PER','FA_ROICEBIT_TTM', 'FA_OCFTOOR_TTM', 'FA_DEBTTOASSET', 'FA_NPGR_TTM','FA_ORGR_TTM', 'TECH_PRICE1Y', 'PE_TTM', 'VAL_MVTOEBITDA_TTM', 'PB_LF','BETA_24M', 'ANNUALSTDEVR_24M']
    factor_i = ['FA_DEBTTOASSET', 'PE_TTM', 'VAL_MVTOEBITDA_TTM', 'PB_LF','BETA_24M', 'ANNUALSTDEVR_24M']
    factor_d = ['i_weight', 'PCT_CHG_PER','FA_ROICEBIT_TTM', 'FA_OCFTOOR_TTM','FA_NPGR_TTM','FA_ORGR_TTM', 'TECH_PRICE1Y','EP_TTM','BP_LF','EBITDAVAL_MVTO']
    data[factor] = data[factor].astype(float)
    ###估值数据数据变换
    data['EP_TTM'] = data['PE_TTM'].map(lambda x: 1/x if x else None)
    data[ 'BP_LF'] = data[ 'PB_LF'].map(lambda x: 1/x if x else None)
    data[ 'EBITDAVAL_MVTO'] = data[ 'VAL_MVTOEBITDA_TTM'].map(lambda x: 1/x if x else None)
    data.eval('equit_return = EP_TTM*PB_LF')
    data.apply(lambda x:x)

    jsyh = w.wsd("601939.SH", "close,pe_est_ftm,pb_lf,risk_variance20", "2007-10-01", "2018-10-17", "PriceAdj=F")
    jsyh2 = pd.DataFrame(jsyh.Data, columns=jsyh.Times, index=jsyh.Fields).T
    jsyh2["equit"] = jsyh2.apply(lambda x: 1/x.PE_EST_FTM*x.PB_LF,axis=1)
    ##数据清洗
    factor_a = ['FA_ROICEBIT_TTM', 'FA_OCFTOOR_TTM', 'FA_DEBTTOASSET', 'FA_NPGR_TTM','FA_ORGR_TTM', 'EP_TTM','BP_LF','EBITDAVAL_MVTO']
    for i in factor_a:
        DataCleaning(data,i, 1)

    ##缺失值分析
    data = data.dropna()
    data[ 'FA_OCFTOOR_TTM'].plot.box()

    ##数据标准化




    document.add_heading('因子权重分析')
      ###因子分组均分成5组
    for i in factor_d:
        data[i+"_group"] = data[i].rank(ascending=False).apply(cla, args=(50,)).values  #降序

    for i in factor_i:
        data[i+"_group"] = data[i].rank(ascending=True).apply(cla, args=(50,)).values  #升序

    from pandas.plotting import scatter_matrix
    scatter_matrix(data[factor_d], alpha=0.2, figsize=(6, 6), diagonal='kde')

    pie_data1 = data.groupby("INDUSTRY_CSRC12")["i_weight"].sum().sort_values()
    fig1, ax1 = plt.subplots()
    ax1.pie(pie_data1,labels=pie_data1.index.tolist(),shadow=True, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("因子权重")
    plt.show()
    plt.savefig("E:\\github\\X\\1.jpg")
    document.add_picture("E:\\github\\X\\1.jpg", width=Inches(4.0))

    fig, axs = plt.subplots(3, 2, figsize=(5, 5))
    for i in range(len(factor_i)):
        factor=factor_i[i]
        pie_data = data.groupby(factor + "_group")["i_weight"].sum().sort_values()
        a=i//2
        b=i%2
        axs[a, b].pie(pie_data, labels=pie_data.index.tolist(), shadow=True, autopct='%1.1f%%', startangle=90)
        axs[a, b].set_title(factor)
    plt.show()

    fig, axs = plt.subplots()
    axs.scatter(data['EP_TTM'],data['i_weight'])
##热力图
vegetables = data[factor_d].corr().round(2)
fig, ax = plt.subplots()
im = ax.imshow(vegetables)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

for i in range(len(vegetables)):
    for j in range(len(vegetables)):
        text = ax.text(j, i, vegetables.iloc[i, j],
                       ha="center", va="center", color="w")
fig.tight_layout()
plt.show()


    # 因子交叉分析
    dddata = data.groupby( ['VAL_PE_DEDUCTED_TTM_group','EST_PEG_group'])["i_weight"].sum()
    x= dddata.index.levels[1].tolist()
    y = dddata.index.levels[0].tolist()
    X,Y =np.meshgrid(x,y)
    def zz(x,y):
        return dddata[x][y]

    Z=dddata.map(zz)





    document.add_picture("E:\\github\\X\\3.jpg", width=Inches(4.0))

    ##分组

    ##writeTable(data.head(),document)


    ##因子相关性


    #####收益归因--分组收益统计####





