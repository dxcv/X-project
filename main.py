#-------------------------------------------------------------------
# encoding: UTF-8
from EventEngine import *
from ClockEngine import ClockEngine
from FeedEngine import MarketEngine
from strategy import strategy
from queue import Queue, Empty
from portfolio import *

from WindPy import w

import tushare as ts
ts.get_hist_data('600848.sh'[0:6],"2018-6-10","2018-6-14")
w.start()
tradedate=w.tdays("2018-01-01", "2018-08-07", "").Data[0]

def FeedHandler():
    print("启动市场事件处理引擎")


def Strategy():
    print("启动策略事件处理引擎")

def Portfolio():
    print("启动组合事件处理引擎")

def ExecutionHandler():
    print("启动执行事件处理引擎")



class go(object):
    def __init__(self):
        self.event_engine=EventEngine()
        self.feed_list = []
        self.portfolio_list=[]
        self.strategy_list = []
        self.order_list=[]
        self.context={}
        self.dateList=[]
        self.clock = ClockEngine(EventEngine(), tradedate)
        self.Market = MarketEngine(EventEngine())
        self.strategy= strategy(EventEngine())

    def strategy_listen_event(self, strategy, _type="listen"):
        """
        所有策略要监听的事件都绑定到这里
        :param strategy: Strategy()
        :param _type: "listen" OR "unlisten"
        :return:
        """
        func = {
            "listen": self.event_engine.register,
            "unlisten": self.event_engine.unregister,
        }.get(_type)

        # 行情引擎的事件
        for quotation_engine in self.quotation_engines:
            func(quotation_engine.EventType, strategy.run)

        # 时钟事件
        func(ClockEngine.EventType, strategy.clock)

    def run(self):
        # run_once function
        self.initialization()
        # Declare the components with respective parameters

        self.event_engine.start()

        while True:
            eventengine.put(event)

        while True:
            try:

                event = self.event_engine.get(False)
            except queue.Empty:
                break

            else:
                if event.type is 'Market':
                    strategy.calculate_signals(event)
                    port.update_timeindex(event)

                elif event.type is 'Signal':
                    port.update_signal(event)

                elif event.type is 'Order':
                    broker.execute_order(event)

                elif event.type is 'Fill':
                    port.update_fill(event)

    def initialization(self):
        self.portfolio=portfolio()

    def setContext(self,context={}):

        ##__________________________________________

        context["capital"]    = 10000000  # 回测的初始资金
        context["securities"] = ['000001.SZ']  # 回测标的
        context["start_date"] = "2018-1-1"  # 回测开始时间
        context["end_date"]   = "2018-6-1"  # 回测结束时间
        context["period"]     = 'd'  # 'd' 代表日, 'm'代表分钟   表示行情数据的频率
        context["pos"]        = 1  # 这里可以传一些自己定义的变量  这个表示的是组合1
        context["benchmark"]  = '000906.SH'
        ##___________________________________________
        self.context=context


################### In Loop #######################
    def _check_pending_order(self):
        for f in self.feed_list:    # 判断属于哪个feed_list
            self.fill.check_trade_list(f)
            self.fill.check_order_list(f)


    def _pass_to_market(self,marketevent):
        """因为Strategy模块用到的是marketevent，所以通过marketevent传进去"""
        m = marketevent
        m.fill = self.fill
        self.portfolio.fill = self.fill
        self.broker.fill = self.fill
        m.target = self.target

    def _check_finish_backtest(self,feed_list):
        # if finish, sum(backtest) = 0 + 0 + 0 = 0 -> False
        backtest = [i.continue_backtest for i in feed_list]
        return not sum(backtest)





