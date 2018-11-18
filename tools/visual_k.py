# -*- coding: utf-8 -*-
import matplotlib.pylab as plt
import pandas as pd
from WindPy import *
from matplotlib.dates import date2num
from matplotlib.finance import candlestick_ohlc
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
w.start()


def get_visual(code, date_start, date_end):
    dat = w.wsd(code, "open,high,low,close,volume,amt", date_start,
                date_end, "TradingCalendar=SZSE;Fill=Previous")
    fm = pd.DataFrame(dat.Data, index=dat.Fields, columns=dat.Times)  # pandas timeseries type
    fm = fm.T
    type(fm['OPEN'])
    ## 带成交量k线图
    fig = plt.figure()
    ax1 = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4)
    ohlc = zip(fm.index.map(date2num), fm['OPEN'], fm['HIGH'], fm['LOW'], fm['CLOSE'])
    candlestick_ohlc(ax1, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')
    plt.grid(True)

    ax2 = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)
    ax2.bar(fm.index.map(date2num), fm['VOLUME'], width=0.4, align='center')
    plt.grid(True)

    ax2.set_xticklabels(fm.index, rotation=30)
    plt.setp(ax1.get_xticklabels(), visible=True)
    plt.setp(ax1.yaxis.get_ticklabels()[0], visible=True)
    plt.show()

    ## 双y轴
    ax2 = ax1.twinx()
