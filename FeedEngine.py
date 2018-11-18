# coding: utf-8
import time
from WindPy import w
from EventEngine import *
from ClockEngine import *

w.start()
from threading import Thread

from EventEngine import Event
from tools.getTushareData import *

class MarketEngine:
    """行情推送引擎基类"""
    

    EventType = 'Market'
    PushInterval = 1

    def __init__(self,event_engine,clock_engine):

        self.event_engine = event_engine
        self.clock_engine = clock_engine
        self.context = {}

        self.is_active = True
        self.quotation_thread = Thread(target=self.push_quotation, name="%s" % self.EventType)

    def start(self):
        self.is_active = True
        self.quotation_thread.start()

    def stop(self):
        self.is_active = False

    def push_quotation(self):
        while self.is_active:
            clock_data = self.fetch_clock()
            date = clock_data.data.strftime("%Y-%m-%d")
            bar = tusharebar(date).getOneBar("600008.SH")
            event = Event(event_type=self.EventType, data=bar)
            print("传递bar")
            print(bar)
            self.event_engine.put(event)


    def fetch_clock(self):
        self.clock_engine.event_engine.queue.get(block=True, timeout=1)


        # return your quotation

    def init(self):
        # do something init
        pass

    def wait(self):
        # for receive quit signal
        for _ in range(int(self.PushInterval) + 1):
            time.sleep(1)





if __name__ == '__main__':
    from WindPy import w
    from EventEngine import Event, EventEngine,ClockEvent
    from ClockEngine import ClockEngine
    from FeedEngine import MarketEngine
    w.start()
    tradedate = w.tdays("2018-01-01", "2018-04-07", "").Data[0]
    clocks = ClockEvent("clock", tradedate)
    def clockhandel(Event):
        date = Event.data.strftime("%Y-%m-%d")
        bar = tusharebar(date).getOneBar("600008.SH")
        print("传递bar")
        print(bar)

    M=MarketEngine(EventEngine(),ClockEngine(EventEngine(),clocks))
    import queue

    events = queue.Queue()
    class test:
        def __init__(self):
            pass

        def aa(self):
            events.put(1)





