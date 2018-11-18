
from WindPy import w
import numpy as np
import pandas as pd
from datetime import datetime


w.start()
class wsd(object):

    ##获取wind 里面的WSD数据，并转换为dataframe
    def __init__(self,code,startdate,enddate,variable="open,high,low,close,volume,pct_chg,trade_status",frequency="day"):
        self.code=code
        self.startdate=startdate
        self.enddate=enddate
        self.frequency=frequency
        self.variable=variable

    def get_data(self):
        if self.frequency=="day":
            indata = w.wsd(self.code,self.variable, datetime.strftime(self.startdate,'%Y-%m-%d'),
                           datetime.strftime(self.enddate,'%Y-%m-%d'), "")
            if indata.ErrorCode != 0:
                print('错误:' + str(indata.ErrorCode) + '\n')
            Fields = indata.Fields
            A = list(map(list, (zip(*indata.Data))))
            df = pd.DataFrame(A, index=list(indata.Times), columns=Fields)
            return df
        elif self.frequency=="min":
            indata=w.wsd(self.code, "open,high,low,close,volume,pct_chg",datetime.strftime(self.startdate,'%Y-%m-%d %H:%M:%S'),
                         datetime.strftime(self.enddate,'%Y-%m-%d %H:%M:%S'), "BarSize=5")
            if indata.ErrorCode != 0:
                    print('错误:' + str(indata.ErrorCode) + '\n')
            A = list(map(list, (zip(*indata.Data))))
            Fields = indata.Fields
            df = pd.DataFrame(A, index=list(indata.Times), columns=Fields)
            return df
        else:
            print("缺少频率变量")
class wss(object):
    ##获取多维数据
    w.start()
    def __init__(self,code,date,variable="close"):
        self.code=code
        self.date=datetime.strftime(date,'%Y%m%d')
        self.variable=variable

    def get_data(self):
        indata=w.wss(self.code,self.variable,"tradeDate="+self.date+";priceAdj=F;cycle=D")
        if indata.ErrorCode != 0:
            print('错误:' + str(indata.ErrorCode) + '\n')
            return ()
        A = list(map(list, (zip(*indata.Data))))
        Fields = indata.Fields
        df = pd.DataFrame(A, index=list(indata.Codes), columns=Fields)
        return df

class wsee(object):
    def __init__(self,code,variable,enddate,startdate=datetime.now(),mode=1):
        self.code=code
        self.variable=variable
        self.enddate=datetime.strftime(enddate,'%Y-%m-%d')
        self.year=str(enddate.year-1)
        self.startdate=datetime.strftime(startdate,'%Y-%m-%d')
        self.mode=mode

    def get_data(self):
        if self.mode==1:
            indata=w.wsee(self.code,self.variable,
                   "tradeDate="+self.enddate+";excludeRule=1;DynamicTime=1;unit=1;currencyType=;year="+self.year+";startDate="+self.startdate+";endDate="+self.enddate)
            if indata.ErrorCode != 0:
                print('错误:' + str(indata.ErrorCode) + '\n')

            A = list(map(list, (zip(*indata.Data))))
            Fields = indata.Fields
            df = pd.DataFrame(A, index=list(indata.Codes), columns=Fields)
            return df
        else:
            indata=w.wsee(self.code, self.variable,self.startdate,self,enddate,"year="+self.year+";DynamicTime=0")
            if indata.ErrorCode != 0:
                print('错误:' + str(indata.ErrorCode) + '\n')

            data = np.array(indata.Data)
            Fields = indata.Fields
            df = pd.DataFrame(data.transpose(), index=list(indata.Times), columns=indata.Codes)
            return df

class edb(object):
    def __init__(self,code,startdate,enddate,frequency="D"):
        self.code=code
        self.startdate=datetime.strftime(startdate,'%Y-%m-%d')
        self.enddate=datetime.strftime(enddate,'%Y-%m-%d')


    def get_data(self):
        indata=w.edb(self.code,self.startdate,self.enddate,"Fill=Previous")
        if indata.ErrorCode != 0:
            print('错误:' + str(indata.ErrorCode) + '\n')

        A = list(map(list, (zip(*indata.Data))))
        df = pd.DataFrame(A, index=list(indata.Times), columns=indata.Codes)
        return df
