# coding: utf-8
from iFinDPy import *
from datetime import *
import pandas as pd
import numpy as np
from collections import OrderedDict #保持Key的顺序

THS_DateSerial(",".join(A_stocks_list[0:10]),'ths_trading_status_stock;ths_listed_days_stock',';','Days:Tradedays,Fill:Previous,Interval:D','2018-07-15','2018-08-15')


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



def get_stocks(trDate):
    #股票-股票市场类-全部A股(非ST):001005150
    A_stocks= THS_DataPool('block',trDate+";001045011006004",'date:Y,thscode:Y,security_name:Y')  #提取非ST，非PT的全部A股
    A_stocks_list=list(THS_Trans2DataFrame(A_stocks)["THSCODE"])
    status= THS_DateSerial(",".join(A_stocks_list),'ths_trading_status_stock;ths_listed_days_stock',';','Days:Tradedays,Fill:Previous,Interval:D',trDate,trDate)
    #提取股票的交易状态和首发上市日期
    status_pd=THS_Trans2DataFrame(status)
    trade_codes=list(status_pd[(status_pd['ths_trading_status_stock']=='交易')&(status_pd['ths_listed_days_stock']>=900)]["thscode"])  #选取交易且上市时间超过12月的股票,并将index转换成list格式
    return trade_codes

def get_trade_date(start_date, end_date, period='M'):
    data=THS_DateQuery('SSE', 'dateType:0,period:'+period+',dateFormat:0', start_date, end_date)
    return data["tables"]["time"]


#获取因子测试时间段
start_date='20160101'
end_date='20180630'
dates=get_trade_date(start_date, end_date, period='M')

class factor:
    def __init__(self,dates,codeList):
        self.dates=dates
        self.codeList=codeList

    #################估值因子######################
    ##    EP_TTM	净利润TTM/总市值
    ##    EP_LYR	净利润（最新年报）/总市值
    ##    BP_LF	净资产TTM/总市值
    ##    BP_LYR	净资产（最新年报）/总市值
    ##    NCF_TTM	净现金流TTM/总市值
    ##    OCF_TTM	经营性现金流TTM/总市值
    ##    SP_TTM	营业收入TTM/总市值
    ##    SP_LYR	营业收入（最新年报）/总市值
    ##    FCFP_LYR	自由现金流TTM/总市值
    ##    PEG	市盈率/净利润同比增长率 * 100
    ##    EV/EBITDA	企业价值倍数
    ##    DYR	近12个月股息率

    ###############################################

    #############################质量因子##########
    ##      ROE_TTM	净资产收益率
    ##      ROA_TTM	资产回报率
    ##      GORSS_PROFIT_MARGIN_TTM	销售毛利率
    ##      ROC_TTM	资本报酬率
    ##      NET_PROFIT_MARGIN_TTM	销售净利率
    ##      TOTAL_ASSETS_TURNOVER_TTM	总资产周转率
    ##      FIXED_ASSETS_TURNOVER_TTM	固定资产周转率
    ##      CURRENT_SAAENTS_TURNOVER_TTM	流动资产周转率
    ################################################

    def get_values_factor(self,codeList):
        dict_df = OrderedDict()
        factors_value = THS_DateSerial(",".join(codeList), 'ths_or_yoy_stock', '',
                       'Days:Tradedays,Fill:Previous,Interval:D', self.dates, self.dates)
            # 估值因子value_factor
        factors_value = THS_Trans2DataFrame(factors_value)

        dict_df[date] = factors_value

        factors_values = pd.concat(dict_df.values(), keys=dict_df.keys())
        return factors_values

    ################################################
    ##            规模因子
    # 获取规模因子：对数总市值、对数流通市值

    ################################################
    def get_size_factor(self,codeList):
        dict_df = OrderedDict()
        for i in range(len(self.dates) - 1):
            date = self.dates[i]
            A_stocks = get_stocks(date)  # 获取当前时点满足条件的全部A股
            size_factors = w.wss(A_stocks, "val_lnmv,val_lnfloatmv", "tradeDate=" + date)
            factors_names = ['LN_MV', 'LN_FLOAT_MV']
            size_factors = pd.DataFrame(size_factors.Data, index=factors_names, columns=size_factors.Codes).T
            dict_df[date] = size_factors.iloc[:, :]
            # print(dict_df.values())
            # print(dict_df.keys())
        size_factors = pd.concat(dict_df.values(), keys=dict_df.keys())
        return size_factors

    #########################成长因子###########################
    ##       sales_gr_TTM	             营业收入增长率_TTM同比
    ##       net_asset_gr_TTM          	 净资产增长率_TTM同比
    ##       gross_margin_gr_TTM	     毛利率增长率_TTM同比
    ##       net_profit_gr_TTM	         净利润增长率_TTM同比
    ##       total_asset_gr_TTM	         总资产增长率_TTM同比
    ##       net_cash_flow_gr_TTM	     净现金流增长率_TTM同比
    ##       invest_cash_flow_gr_TTM	 资活动产生的现金流量净额增长率_TTM同比
    ##       inance_cash_folw_gr_TTM	 资活动产生的现金流量净额增长率_TTM同比
    ##       operate_cash_flow_gr_TTM	 营活动产生的现金流量净额增长率_TTM同比
    ##       operete_profit_gr_TTM	     营业利润增长率_TTM同比
    ############################################################

    # 获取成长因子
    def get_growth_factors(self):
        dict_df = OrderedDict()
        for i in range(len(self.dates) - 1):
            date = self.dates[i]
            A_stocks = get_stocks(date)  # 获取当前时点满足条件的全部A股
            factors_codes = "fa_orgr_ttm,fa_nagr,fa_gpmgr_ttm,fa_npgr_ttm,fa_tagr,fa_ncgr_ttm,fa_cfigr_ttm,fa_cffgr_ttm,fa_cfogr_ttm,fa_oigr_ttm"
            factors_names = ['sales_gr_TTM', 'net_asset_gr_TTM', 'gross_margin_gr_TTM', 'net_profit_gr_TTM',
                             'total_asset_gr_TTM', 'net_cash_flow_gr_TTM', 'invest_cash_flow_gr_TTM',
                             'finance_cash_folw_gr_TTM', 'operate_cash_flow_gr_TTM', 'operete_profit_gr_TTM']
            growth_factors = w.wss(A_stocks, factors_codes, "tradeDate=" + date)
            growth_factors = pd.DataFrame(growth_factors.Data, index=factors_names, columns=growth_factors.Codes).T
            # growth_factors['eps_growth_TTM']=w.wss(A_stocks, "yoyeps_basic","rptDate="+date+";N=1").Data[0]  #基本每股收益同比增长率
            # growth_factors['roe_growth_TTM']=w.wss(A_stocks, "growth_roe","rptDate="+date+";N=1").Data[0]  #净资产收益率N年同比增长率
            dict_df[date] = growth_factors
        growth_factors = pd.concat(dict_df.values(), keys=dict_df.keys())
        return growth_factors

    # 估值因子
    def get_values_factor(dates, stocks):
        dict_df = OrderedDict()
        for i in range(len(dates) - 1):
            date = dates[i]

            # 估值因子value_factor
            factors_codes = "pe_ttm,pe_lyr,pb_lf,pb_lyr,pcf_ncf_ttm,pcf_ocf_ttm,ps_ttm,ps_lyr,val_mvtofcff"
            factors_names = ['EP_TTM', 'EP_LYR', 'BP_LF', 'BP_LYR', 'NCF_TTM', 'OCF_TTM', 'SP_TTM', 'SP_LYR',
                             'FCFP_LYR']
            factors_value = w.wss(stocks, factors_codes, "tradeDate=" + date)
            factors_value = pd.DataFrame(factors_value.Data, index=factors_names, columns=factors_value.Codes).T
            factors_value = 1 / factors_value

            # 获取PEG=市盈率/净利润同比增长率*100
            PE = np.array(w.wss(stocks, "pe_ttm", "tradeDate=" + date).Data[0])  # 获取市盈率
            profit = np.array(w.wss(stocks, "fa_npgr_ttm", "tradeDate=" + date).Data[0])  # 净利润同期增长率*100
            factors_value['PEG_TTM'] = PE / profit

            # 获取企业价值倍数
            factors_value['EV/EBITDA'] = w.wss(stocks, "ev2_to_ebitda", "tradeDate=" + date).Data[0]

            # 获取股息率
            factors_value['DYR'] = w.wss(stocks, "dividendyield2", "tradeDate=" + date).Data[0]

            dict_df[date] = factors_value
        factors_values = pd.concat(dict_df.values(), keys=dict_df.keys())
        return factors_values

    # 规模因子
    def get_size_factor(dates, stocks):
        dict_df = OrderedDict()
        for i in range(len(dates) - 1):
            date = dates[i]
            size_factors = w.wss(stocks, "val_lnmv,val_lnfloatmv,val_lntotassets", "tradeDate=" + date)
            factors_names = ['LN_MV', 'LN_FLOAT_MV', 'LN_TOTAL_ASSETS']
            size_factors = pd.DataFrame(size_factors.Data, index=factors_names, columns=size_factors.Codes).T
            dict_df[date] = size_factors.iloc[:, :]
            # print(dict_df.values())
            # print(dict_df.keys())
        size_factors = pd.concat(dict_df.values(), keys=dict_df.keys())
        return size_factors

    # 杠杆因子
    def get_leverage_factors(dates, stocks, factors_codes, factors_names):
        dict_df = OrderedDict()
        for i in range(len(dates) - 1):
            date = dates[i]
            leverage_factors = w.wss(stocks, factors_codes, "tradeDate=" + date)
            leverage_factors = pd.DataFrame(leverage_factors.Data, index=factors_names,
                                            columns=leverage_factors.Codes).T
            dict_df[date] = leverage_factors
        leverage_factors = pd.concat(dict_df.values(), keys=dict_df.keys())
        return leverage_factors

    # 技术因子
    def get_Technical_factors(dates, stocks):
        dict_df = OrderedDict()
        for i in range(len(dates) - 1):
            date = dates[i]
            factors_codes = "tech_rvi,tech_rstr12,tech_cyf,tech_cry,tech_cr20"
            factors_names = ['RVI', 'RSTR12', 'CYF', 'CRY', 'CR20']
            Technical_factors = w.wss(stocks, factors_codes, "tradeDate=" + date)
            Technical_factors = pd.DataFrame(Technical_factors.Data, index=factors_names,
                                             columns=Technical_factors.Codes).T
            # 获取RSI指标
            Technical_factors['RSI'] = w.wss(stocks, "RSI", "tradeDate=" + date + ";RSI_N=6;priceAdj=F;cycle=D").Data[0]
            # 获取DEA异同平均数指标
            Technical_factors['DEA'] = w.wss(stocks, "MACD",
                                             "tradeDate=" + date + ";MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=2;priceAdj=F;cycle=D").Data[
                0]
            # 获取MACD指标
            Technical_factors['MACD'] = w.wss(stocks, "MACD",
                                              "tradeDate=" + date + ";MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=3;priceAdj=F;cycle=D").Data[
                0]
            # 获取K\D\J
            Technical_factors['K'] = \
            w.wss(stocks, "KDJ", "tradeDate=" + date + ";KDJ_N=9;KDJ_M1=3;KDJ_M2=3;KDJ_IO=1;priceAdj=F;cycle=D").Data[0]
            Technical_factors['D'] = \
            w.wss(stocks, "KDJ", "tradeDate=" + date + ";KDJ_N=9;KDJ_M1=3;KDJ_M2=3;KDJ_IO=2;priceAdj=F;cycle=D").Data[0]
            Technical_factors['J'] = \
            w.wss(stocks, "KDJ", "tradeDate=" + date + ";KDJ_N=9;KDJ_M1=3;KDJ_M2=3;KDJ_IO=3;priceAdj=F;cycle=D").Data[0]

            dict_df[date] = Technical_factors
        Liquidation_factors = pd.concat(dict_df.values(), keys=dict_df.keys())
        return Liquidation_factors

    # 动量因子
    def get_Momentum_factors(dates, stocks):
        dict_df = OrderedDict()
        for i in range(len(dates) - 1):
            date = dates[i]
            factors_codes = "tech_revs5,tech_revs10,tech_revs60,tech_revs120,tech_revs250,tech_revs750,tech_revs1mmax,tech_lnhighlow20d"
            factors_names = ['REV_5D', 'REV_10D', 'REV_3M', 'REV_6M', 'REV_1Y', 'REV_3Y', 'REV_LAST1M_MAX',
                             'LN_HIGH-LOW']
            Momentum_factors = w.wss(stocks, factors_codes, "tradeDate=" + date)
            Momentum_factors = pd.DataFrame(Momentum_factors.Data, index=factors_names,
                                            columns=Momentum_factors.Codes).T
            dict_df[date] = Momentum_factors
        Momentum_factors = pd.concat(dict_df.values(), keys=dict_df.keys())
        return Momentum_factors

    # 获取成长因子
    def get_growth_factors(dates, stocks):
        dict_df = OrderedDict()
        for i in range(len(dates) - 1):
            date = dates[i]
            factors_codes = "fa_orgr_ttm,fa_nagr,fa_gpmgr_ttm,fa_npgr_ttm,fa_tagr,fa_ncgr_ttm,fa_cfigr_ttm,fa_cffgr_ttm,fa_cfogr_ttm,fa_oigr_ttm"
            factors_names = ['sales_gr_TTM', 'net_asset_gr_TTM', 'gross_margin_gr_TTM', 'net_profit_gr_TTM',
                             'total_asset_gr_TTM', 'net_cash_flow_gr_TTM', 'invest_cash_flow_gr_TTM',
                             'finance_cash_folw_gr_TTM', 'operate_cash_flow_gr_TTM', 'operete_profit_gr_TTM']
            growth_factors = w.wss(stocks, factors_codes, "tradeDate=" + date)
            growth_factors = pd.DataFrame(growth_factors.Data, index=factors_names, columns=growth_factors.Codes).T
            # growth_factors['eps_growth_TTM']=w.wss(A_stocks, "yoyeps_basic","rptDate="+date+";N=1").Data[0]  #基本每股收益同比增长率
            # growth_factors['roe_growth_TTM']=w.wss(A_stocks, "growth_roe","rptDate="+date+";N=1").Data[0]  #净资产收益率N年同比增长率
            dict_df[date] = growth_factors
            growth_factors = pd.concat(dict_df.values(), keys=dict_df.keys())
        return growth_factors

    # 市值因子
    def get_assisted_factors(dates, stocks):
        dict_df = OrderedDict()
        for i in range(len(dates) - 1):
            date = dates[i]
            assisted_factors = w.wss(stocks, "industry_sw,mkt_cap_ashare",
                                     "tradeDate=" + date + ';industryType=1;unit=1')
            factors_names = ['INDUSTRY_SW', 'CAP']
            assisted_factors = pd.DataFrame(assisted_factors.Data, index=factors_names,
                                            columns=assisted_factors.Codes).T
            dict_df[date] = assisted_factors
        assisted_factors = pd.concat(dict_df.values(), keys=dict_df.keys())
        return assisted_factors

    def get_factor_grow(trDate, A_stocks):
        ###part1:因子去异常值，标准化
        factor = OrderedDict()
        quanters = w.tdays("2007-07-01", trDate, "Period=Q").Data[0]
        ###part2:计算得到成长因子
        ##       sales_gr_TTM	             营业收入增长率_TTM同比
        ##       net_asset_gr_TTM          	 净资产增长率_TTM同比
        ##       gross_margin_gr_TTM	     毛利率增长率_TTM同比
        ##       net_profit_gr_TTM	         净利润增长率_TTM同比
        ##       total_asset_gr_TTM	         总资产增长率_TTM同比
        ##       net_cash_flow_gr_TTM	     净现金流增长率_TTM同比
        ##       operete_profit_gr_TTM	     营业利润增长率_TTM同比
        for i in range(3):
            time = quanters[-2 - 4 * i].strftime('%Y%m%d')
            data = w.wss(A_stocks,
                         "fa_orgr_ttm,fa_ncgr_ttm,fa_tpgr_ttm,fa_oigr_ttm,fa_npgr_ttm,fa_cfogr_ttm,fa_cffgr_ttm,fa_cfigr_ttm,fa_gpmgr_ttm,fa_tagr,fa_nagr",
                         "tradeDate=" + time)
            data = pd.DataFrame(data.Data, columns=data.Codes, index=data.Fields).T
            factor["%s" % time] = data
        key = []
        for k in factor:
            key.append(k)
        factor_grow = (factor[key[0]] + factor[key[1]] + factor[key[2]]) / 3

        ###part3:计算估值因子DPRO

        data2 = w.wss(A_stocks, "fa_nppcgr_ttm,pe_ttm", "tradeDate=" + trDate)
        data2 = pd.DataFrame(data2.Data, columns=data2.Codes, index=data2.Fields).T  # 提取最近可得单季净利润数据

        market_value = w.wss(A_stocks, "mkt_cap_ard", "unit=1;tradeDate=" + trDate)
        market_value = pd.DataFrame(market_value.Data, columns=market_value.Codes).T
        data2['ln_market_value'] = np.log(market_value)  # 提取总市值并取对数

        industrys = w.wss(A_stocks, "industry_citic", "tradeDate=" + trDate + ";industryType=1")
        industrys = pd.DataFrame(industrys.Data, columns=industrys.Codes).T
        data2['industrys'] = industrys  # 提取个股所属中信一级行业情况
        data = pd.concat([factor_grow, data2], axis=1)  # 数据合并
        data = data[data['pe_ttm'.upper()] > 0]

        # 开始进行截面回归计算估值因子
        industrys = data['industrys']
        x2 = np.array(industrys.tolist(), dtype=np.str)
        dummy = sm.categorical(x2, drop=True)  # 得到中信一级行业虚拟变量

        x1 = np.array(data['pe_ttm'.upper()].tolist())
        x = np.column_stack((x1, dummy))  # 合并回归所需自变量

        y = data['fa_nppcgr_ttm'.upper()].tolist()  # 得到回归所需的因变量

        result = sm.OLS(y, x).fit()
        result.summary()
        DPRO = result.resid  # 得到回归的残差作为估值因子
        data['PE/g'] = DPRO.data
        return data, factor_grow

    def get_factor_value(trDate, A_stocks):
        ###part1:因子去异常值，标准化
        factor = OrderedDict()
        quanters = w.tdays("2008-07-01", trDate, "Period=Q").Data[0]
        ###part2:计算得到价值因子

        for i in range(3):
            time = quanters[-2 - 4 * i].strftime('%Y%m%d')
            data = w.wss(A_stocks, "fa_roenp_ttm", "tradeDate=" + time)
            data = pd.DataFrame(data.Data, columns=data.Codes, index=data.Fields).T
            factor["%s" % time] = data
        key = []
        for k in factor:
            key.append(k)
        factor_value = (factor[key[0]] + factor[key[1]] + factor[key[2]]) / 3

        ###part3:计算估值因子DPRO

        data2 = w.wss(A_stocks, "val_pbindu_sw", "tradeDate=" + trDate)
        data2 = pd.DataFrame(data2.Data, columns=data2.Codes, index=data2.Fields).T  # 提取最近可得单季净利润数据

        market_value = w.wss(A_stocks, "mkt_cap_ard", "unit=1;tradeDate=" + trDate)
        market_value = pd.DataFrame(market_value.Data, columns=market_value.Codes).T
        data2['ln_market_value'] = np.log(market_value)  # 提取总市值并取对数

        industrys = w.wss(A_stocks, "industry_citic", "tradeDate=" + trDate + ";industryType=1")
        industrys = pd.DataFrame(industrys.Data, columns=industrys.Codes).T
        data2['industrys'] = industrys  # 提取个股所属中信一级行业情况
        data = pd.concat([factor_value, data2], axis=1)  # 数据合并
        data = data.dropna()
        data = data[data['fa_roenp_ttm'.upper()] > 10]
        # 开始进行截面回归计算估值因子
        industrys = data['industrys']
        x2 = np.array(industrys.tolist(), dtype=np.str)
        dummy = sm.categorical(x2, drop=True)  # 得到中信一级行业虚拟变量

        x1 = np.array(data['fa_roenp_ttm'.upper()].tolist())
        x = np.column_stack((x1, dummy))  # 合并回归所需自变量

        y = data["val_pbindu_sw".upper()].tolist()  # 得到回归所需的因变量

        result = sm.OLS(y, x).fit()
        result.summary()
        DPRO = result.resid  # 得到回归的残差作为估值因子
        data['roe/pb'] = DPRO.data
        return data, factor_value
