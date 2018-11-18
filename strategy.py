

from EventEngine import *

# coding: utf-8
import time
from WindPy import w
from EventEngine import *
from ClockEngine import *

w.start()
from threading import Thread

from EventEngine import Event


class StrategyEngine:
    """策略引擎基类"""
    from WindPy import w

    w.start()
    EventType = 'Market'
    PushInterval = 1
    tradedate = w.tdays("2018-01-01", "2018-04-07", "").Data[0]
    clocks = ClockEvent("clock", tradedate)
    def __init__(self, event_engine):

        self.event_engine = event_engine
        self.clock_engine = ClockEngine(event_engine,clocks)
        self.context = {}
        self.is_active = True
        self.quotation_thread = Thread(target=self.push_quotation, name="%s" % self.EventType)

    def start(self):
        self.quotation_thread.start()

    def stop(self):
        self.is_active = False

    def push_quotation(self):
        while self.is_active:
            try:
                clock_data = self.fetch_clock()
            except:
                self.wait()
                continue
            feed_data=self.clockhandel(clock_data)
            event = Event(event_type=self.EventType, data=feed_data)
            self.event_engine.put(event)
            self.wait()

    def fetch_clock(self):
        self.clock_engine.event_engine.queue.get(block=True, timeout=1)


        # return your quotation

        return None

    def init(self):
        # do something init
        pass

    def wait(self):
        # for receive quit signal
        for _ in range(int(self.PushInterval) + 1):
            time.sleep(1)

    def clockhandel(self,Event):
        date = Event.data.strftime("%Y-%m-%d")
        bar = tusharebar(date).getOneBar("600008.SH")
        event = Event(event_type=self.EventType, data=bar)
        print("传递bar")
        print(bar)
        self.event_engine.put(event)


    def handle_data(self,bar_datetime, context, bar_data):
        pass

    def my_schedule(self,bar_datetime, context, bar_data):
        pass


class strategy(Event):
    def __init__(self,market,context,bar_data):
        self.data=market
        self.context=context
        Event.__init__(self)






    def handle_data(self,bar_datetime, context, bar_data):
        pass

    def my_schedule(self,bar_datetime, context, bar_data):
        pass



