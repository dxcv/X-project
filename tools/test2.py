
# coding: utf-8
from WindPy import w

from EventEngine import *


import time
w.start()

from tools.getTushareData import *
w.start()
tradedate=w.tdays("2018-01-01", "2018-04-07", "").Data[0]
date=w.tdays("2018-01-01", "2018-04-01", "Days=Alldays").Data[0]
clockevent=ClockEvent("Clock",tradedate)
clock=ClockEngine(EventEngine(),clockevent)

from tools.getTushareData import *

def clockhandel(Event):
    date=Event.data.strftime("%Y-%m-%d")
    bar=tusharebar(date).getOneBar("600008.SH")
    print("传递bar")
    print(bar)

Event=Event( 'clock_time',date[1])
clockhandel(aa)


clock.register(clockhandel)
clock.start()
clock.event_engine.start()
