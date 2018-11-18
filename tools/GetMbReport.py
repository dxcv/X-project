#coding=GBK
import queue
import urllib.request
import urllib.parse
import http.cookiejar
import urllib.error
import pandas as pd
from bs4 import *
from tools.toMysql import MySQLAlchemy
import time
import arrow
import threading
import re
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String

class report(Base):
    """定义数据库表基类"""
    __tablename__ = 'report'
    __table_args__ = {
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50))
    name_sec = Column(String(50))
    sec_num = Column(String(50))
    title = Column(String(200))
    date = Column(String(50))
    classes = Column(String(50))
    author = Column(String(50))
    score = Column(String(50))
    pages = Column(Integer)

class industrial(Base):
    """定义数据库表基类"""
    __tablename__ = 'industrial'
    __table_args__ = {
        "mysql_charset": "utf8"
    }

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(50))
    industrial = Column(String(50))
    title = Column(String(200))
    date = Column(String(50))
    classes = Column(String(50))
    author = Column(String(50))
    score = Column(String(50))
    pages = Column(Integer)



class ThreadUrl2(threading.Thread):
    def __init__(self, pages,Base, lastdate):
        threading.Thread.__init__(self)
        self.lastdate = lastdate
        self.thread = threading.Thread(target=self.run, name="Engine")

        self.pages = pages
        self.con = MySQLAlchemy(Base,report, "stock")
        self.headers = {
            'Connection': ' keep-alive',
            'Upgrade-Insecure-Requests': ' 1',
            'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        }

    def conn(self):

        dlurl = 'http://www.hibor.com.cn/toplogin.asp?action=login'
        datapost = {"name": "xuzhipeng8", "pwd": 'xuzhipeng8261426', 'tijiao.x': '12', 'tijiao.y': '2',
                    'checkbox': 'on'}
        postdata = urllib.parse.urlencode(datapost).encode("utf-8")
        req = urllib.request.Request(dlurl, postdata, headers=self.headers)
        cjar1 = http.cookiejar.CookieJar()
        try:

            proxy = urllib.request.ProxyHandler({'https': '127.0.0.1:4973'})

            self.opener = urllib.request.build_opener(proxy,urllib.request.HTTPHandler,urllib.request.HTTPCookieProcessor(cjar1))

            urllib.request.install_opener(self.opener)
            file = self.opener.open(req)
            data = file.read()
            file = open("pages.html", "wb")
            file.write(data)
            file.close()

        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                print(e.code)

            if hasattr(e,"reason"):
                print(e.reason)
            time.sleep(5)

        except Exception as e:
            print("exception:" +str(e))
            time.sleep(1)


    def run(self):
        file = open('errorlog.txt', "a+")
        while True:
            url = self.pages.get()
            print("爬取", url)
            get_request = urllib.request.Request(url, headers=self.headers)
            try:
                data2 = self.opener.open(get_request).read()
            except:
                print("等待5秒")
                time.sleep(5)
                try:
                    data2 = self.opener.open(get_request).read()
                except:
                    file.write(url)
                    file.write("/n")
                    continue

            soup_all = BeautifulSoup(data2, "html5lib")
            soup = soup_all.findAll('td', {"class": "td_spantxt"})
            soup_title = soup_all.findAll('span', {"class": "tab_lta"})

            pddata = pd.DataFrame([], columns=["券商","行业名称" ,"标题", "日期", "类别", "作者", "评级", "页数"])
            for i in range(len(soup)):
                if re.search("\w+行业", soup_title[i].text) == None:
                    continue

                pddata.loc[i] = [
                    re.search("\w+-", soup_title[i].text).group()[0:4],
                    re.search("\w+行业", soup_title[i].text).group(),
                    soup_title[i].text,
                    soup[i].find_all("span")[0].text,
                    "行业分析",
                    soup[i].find_all("span")[2].text[3:],
                    soup[i].find_all("span")[3].text[3:],
                    soup[i].find_all("span")[4].text[3:][:-1]
                    ]
                #print(soup2[i])
                #error_data = str(soup2[i])
                #error = open(".\error_data.txt", "r")
                #error.write(error_data)
                #error.write("\n")
                #error.close()
            deltatime = arrow.get(pddata["日期"].max(), "YYYY-MM-DD") - arrow.get(self.lastdate, "YYYY-MM-DD")
            print("爬取至日期", pddata["日期"].max(), "目标日期", self.lastdate)

            reports = [industrial(name=pddata["券商"][j], industrial=pddata["行业名称"][j],title=pddata["标题"][j], date=pddata["日期"][j], \
                             classes=pddata["类别"][j], author=pddata["作者"][j], score=pddata["评级"][j],\
                             pages=int(pddata["页数"][j])) for j in pddata.index.tolist()]
            self.con.insert(reports, 2)

            if deltatime.days < 0:
                file.close()
                break
            if self.pages.empty():
                file.close()
                break


class ThreadUrl3(threading.Thread):
    def __init__(self, pages,Base,lastdate):
        threading.Thread.__init__(self)
        self.lastdate = lastdate
        self.thread = threading.Thread(target=self.run, name="Engine")

        self.pages = pages
        self.con = MySQLAlchemy(Base,report,"stock")
        self.headers = {
            'Connection': ' keep-alive',
            'Upgrade-Insecure-Requests': ' 1',
            'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        }
        dlurl = 'http://www.hibor.com.cn/toplogin.asp?action=login'
        datapost = {"name": "xuzhipeng8", "pwd": 'xuzhipeng8261426', 'tijiao.x': '12', 'tijiao.y': '2',
                    'checkbox': 'on'}
        postdata = urllib.parse.urlencode(datapost).encode("utf-8")
        req = urllib.request.Request(dlurl, postdata, headers=self.headers)
        cjar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
        urllib.request.install_opener(self.opener)
        file=self.opener.open(req)
        data = file.read()
        file = open("pages.html", "wb")
        file.write(data)
        file.close()

    def run(self):
        file = open('errorlog.txt',"a+")
        while True:
            url = self.pages.get()
            print("爬取",url)
            get_request = urllib.request.Request(url, headers=self.headers)
            try:
                data2 = self.opener.open(get_request).read()
            except:
                print("等待5秒")
                time.sleep(5)
                try:
                    data2 = self.opener.open(get_request).read()
                except:
                    file.write(url)
                    file.write("/n")
                    continue



            soup_all = BeautifulSoup(data2, "html5lib")
            soup = soup_all.findAll('td', {"class": "td_spantxt"})
            soup_title = soup_all.findAll('span', {"class": "tab_lta"})

            pddata = pd.DataFrame([], columns=["券商","公司名称" ,"公司代码", "标题", "日期", "类别", "作者", "评级", "页数"])
            for i in range(len(soup)):

                pddata.loc[i] = [
                    re.search("\w+-", soup_title[i].text).group()[0:4],
                    re.search("-\w+-", soup_title[i].text).group()[1:-1],
                    re.search("-\d+-", soup_title[i].text).group()[1:-1],
                    soup_title[i].text,
                    soup[i].find_all("span")[0].text,
                    "个股调研",
                    soup[i].find_all("span")[2].text[3:],
                    soup[i].find_all("span")[3].text[3:],
                    soup[i].find_all("span")[4].text[3:][:-1]
                    ]
                #print(soup2[i])
                #error_data = str(soup2[i])
                #error = open(".\error_data.txt", "r")
                #error.write(error_data)
                #error.write("\n")
                #error.close()
            deltatime = arrow.get(pddata["日期"].max(), "YYYY-MM-DD") - arrow.get(self.lastdate, "YYYY-MM-DD")
            print("爬取至日期", pddata["日期"].max(),"目标日期", self.lastdate)

            reports = [report(name=pddata["券商"][j],  name_sec = pddata["公司名称"][j],sec_num = pddata["公司代码"][j],title=pddata["标题"][j], date=pddata["日期"][j], \
                             classes=pddata["类别"][j], author=pddata["作者"][j], score=pddata["评级"][j],\
                             pages=int(pddata["页数"][j])) for j in pddata.index.tolist()]
            self.con.insert(reports, 2)

            if deltatime.days<0:
                file.close()
                break
            if self.pages.empty():
                file.close()
                break




def main_indus():
    oriUrl2 = 'http://www.hibor.com.cn/microns_2_'  ###行业报告
    oriUrl3 = 'http://www.hibor.com.cn/microns_1_'  ###个股报告
    pages = queue.Queue()

    for i in range(1, 1000):
        pages.put(oriUrl2 + str(i)+".html")
    t = ThreadUrl2(pages,Base,"2018-11-13")
    t.conn()
    t.thread.start()

def main_stock():
    oriUrl3 = 'http://www.hibor.com.cn/microns_1_'  ###个股报告
    pages = queue.Queue()

    for i in range(1, 5):
        pages.put(oriUrl3 + str(i)+".html")
    t = ThreadUrl2(pages,Base,"2018-11-13")
    t.thread.start()


if __name__ == '__main__':
    main_indus()





