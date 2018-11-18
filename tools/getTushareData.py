
import tushare as ts
class tusharebar(object):
    def __init__(self,date):
        self.date=date

    def getOneBar(self,code):
        tscode=code[0:6]
        bar_1=ts.get_hist_data(tscode,self.date,self.date)
        bar={"date":bar_1.index[0],
             "open": bar_1["open"][0],
             "high": bar_1["high"][0],
             "low": bar_1["low"][0],
             "close": bar_1["close"][0],
             "volume": bar_1["volume"][0],
             "p_change": bar_1["p_change"][0]
             }
        return bar

    def getBars(self,code_list):
        bars={}
        for code in code_list:
            tscode = code[0:6]
            bars[code]=self.getOneBar(tscode)
        return bars




