from tools.getTushareData import *

def clockhandel(Event):
    date = Event.data.strftime("%Y-%m-%d")
    bar = tusharebar(date).getOneBar("600008.SH")
    print("传递bar")
    print(bar)


