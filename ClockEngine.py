
# coding: utf-8
from threading import Thread

from EventEngine import Event,EventEngine,ClockEvent

def IsTradeDate(date):
    if date in tradedate:
        return 1
    else:
        return 0


class ClockEngine():
    """
    时间推送引擎
    1. 提供bar序列.
    """
    def __init__(self, EventEngine, ClockEvent):
        """
        :param clockEvent:
        :return:
        """
        self.event_engine = EventEngine
        self.clock_engine_thread = Thread(target=self.clocktick, name="ClockEngine")
        self.sleep_time = 1
        self.is_active = True
        self.data = ClockEvent.data
        self.EventType = ClockEvent.event_type

    def start(self):
        self.clock_engine_thread.start()

    def clocktick(self):
        for i in self.data:
            self.push_clock_event(i)
            print("传递时间%s" %i)

    def push_clock_event(self,data):
        event = Event(event_type=self.EventType,data=data)
        self.event_engine.put(event)

    def stop(self):
        self.is_active = False

    def register(self,handle):
        self.event_engine.register(self.EventType,handle)


if __name__ == '__main__':
    from WindPy import w
    from EventEngine import *
    from ClockEngine import *
    w.start()
    tradedate = w.tdays("2018-01-01", "2018-04-07", "").Data[0]
    clocks = ClockEvent("clock", tradedate)
    clock = ClockEngine(EventEngine(), clocks)


    def clockhandel(Event):
        date = Event.data.strftime("%Y-%m-%d")
        bar = tusharebar(date).getOneBar("600008.SH")
        print("传递bar")
        print(bar)



    from tools.getTushareData import *

    clock.register(clockhandel)
    clock.start()
    clock.event_engine.start()




