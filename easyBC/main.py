import pymysql
from easyBC import Model_Evaluate as ev
from easyBC import orders
from easyBC import Portfolio as pf
from pylab import *
import tushare as ts
from easyBC import statistics
from tools.to_mysql import ToMysql

class main(object):
    def __init__(self):
        self.securities = ['603912.SH', '300666.SZ', '300618.SZ', '002049.SZ', '300672.SZ']     #回测标的
        self.capital = 100000000    # 初始本金
        self.start_date = '2018-03-01' #回测开始时间
        self.end_date = '2018-04-01' #回测结束时间
        self.period = 'd' #策略运行周期, 'd' 代表日, 'm'代表分钟  现在还没有m

    ###########################################准备工作#################################################
    # 建立数据库连接,设置tushare的token,定义一些初始化参数

    def initialize(self):
        ts.set_token('502bcbdbac29edf1c42ed84d5f9bd24d63af6631919820366f53e5d4')
        pro = ts.pro_api()
        db = ToMysql()
        # 先清空之前的测试记录,并创建中间表
        sql_wash1 = 'delete from my_capital'
        db.execute(sql_wash1)
        sql_wash3 = 'truncate table my_stock_pool'
        db.execute(sql_wash3)
        sql_setCash ="INSERT INTO my_capital VALUES (%s,%s,0,0,%s)"%(repr(self.start_date),self.capital,self.capital)
        db.execute(sql_setCash)
        db.close()
        # 建回测时间序列
        back_test_date_start = (datetime.datetime.strptime(self.start_date, '%Y-%m-%d')).strftime('%Y%m%d')
        back_test_date_end = (datetime.datetime.strptime(self.end_date, "%Y-%m-%d")).strftime('%Y%m%d')
        df = pro.trade_cal(exchange_id='', is_open=1, start_date=back_test_date_start, end_date=back_test_date_end)
        self.date_temp = list(df.iloc[:, 1])
        self.date_seq = [(datetime.datetime.strptime(x, "%Y%m%d")).strftime('%Y-%m-%d') for x in self.date_temp]

    def get_bars(self, trdate):
        db = ToMysql()
        # 清空行情源表，并插入新的相关股票的行情数据。该操作是为了提高回测计算速度而剔除行情表(stock_all)中的冗余数据。
        sql_wash4 = 'truncate table stock_info'
        db.execute(sql_wash4)
        in_str = '('
        for x in range(len(self.securities)):
            if x != len(self.securities) - 1:
                in_str += str('\'') + str(self.securities[x]) + str('\',')
            else:
                in_str += str('\'') + str(self.securities[x]) + str('\')')

        sql_insert = "insert into stock_info(select * from stock_all a where a.stock_code in %s and a.state_dt = '%s')"%(in_str,trdate)
        db.execute(sql_insert)
        db.close()

    def go(self):
        # 开始模拟交易
        index = 1
        day_index = 0
        for i in range(1, len(self.date_seq)):
            print(i)
            day_index += 1
            ####选择品种  这里示例采用的是机器学习模块，可以替换为其他模块  #######
            self.get_bars(self.date_seq[i])

            self.handle_data(self.date_seq[i],self.securities)

            ###### 每5个交易日运行一次自定义交易函数，这里是更新一次配仓比例 ()
            if divmod(day_index + 5, 5)[1] == 0:
                self.schedule(self.date_seq[i],self.securities)

            self.cap_update_daily(self.date_seq[i])  # 更新估值表
            print('Runnig to Date :  ' + str(self.date_seq[i]))
        print('ALL FINISHED!!')



    def handle_data(self,trdate, context):
        for stock in self.securities:
            try:
                ans2 = ev.model_eva(stock, trdate, 90, 365)
                ##这里其实没啥用，懒得写了，仅仅用作示例，后续换成其他的就好了
                # print('Date : ' + str(date_seq[i]) + ' Update : ' + str(stock))
                pass
            except Exception as ex:
                print(ex)

    def schedule(self,trdate, context):
        portfolio_pool = context
        pf_src = pf.get_portfolio(portfolio_pool, trdate, 250)
        # 取最佳收益方向的资产组合
        risk = pf_src[1][0]
        weight = pf_src[1][1]
        orders.change_to(portfolio_pool, trdate, weight)



    def change_securities(self,code_list):
        self.securities = code_list

    def cap_update_daily(self,state_dt):
        para_norisk = (1.0 + 0.04 / 365)
        db = pymysql.connect(host="localhost", user='root', passwd='8261426', db='stock', charset='utf8')
        cursor = db.cursor()
        sql_pool = "select * from my_stock_pool"
        cursor.execute(sql_pool)
        done_set = cursor.fetchall()
        db.commit()
        new_lock_cap = 0.00
        for i in range(len(done_set)):
            stock_code = str(done_set[i][0])
            stock_vol = float(done_set[i][2])
            sql = "select * from stock_info a where a.stock_code = '%s' and a.state_dt <= '%s' order by a.state_dt desc limit 1" % (
            stock_code, state_dt)
            cursor.execute(sql)
            done_temp = cursor.fetchall()
            db.commit()
            if len(done_temp) > 0:
                cur_close_price = float(done_temp[0][3])
                new_lock_cap += cur_close_price * stock_vol
            else:
                print('Cap_Update_daily Err!!')
                raise Exception
        sql_cap = "select * from my_capital order by seq asc"
        cursor.execute(sql_cap)
        done_cap = cursor.fetchall()
        db.commit()
        new_cash_cap = float(done_cap[-1][2]) * para_norisk
        new_total_cap = new_cash_cap + new_lock_cap
        sql_insert = "insert into my_capital(capital,money_lock,money_rest,bz,state_dt)values('%.2f','%.2f','%.2f','%s','%s')" % (
        new_total_cap, new_lock_cap, new_cash_cap, str('Daily_Update'), state_dt)
        cursor.execute(sql_insert)
        db.commit()
        return 1

    def afterbc(self):
        db = ToMysql()
        sharp, c_std = statistics.get_sharp_rate()
        print('Sharp Rate : ' + str(sharp))
        print('Risk Factor : ' + str(c_std))

        sql_show_btc = "select * from stock_index a where a.stock_code = '000001.SH' and a.state_dt >= '%s' and a.state_dt <= '%s' order by state_dt asc" % (
        self.start_date, self.end_date)
        done_set_show_btc = db.select(sql_show_btc)
        # btc_x = [x[0] for x in done_set_show_btc]
        btc_x = list(range(len(done_set_show_btc)))
        btc_y = [x[3] / done_set_show_btc[0][3] for x in done_set_show_btc]
        dict_anti_x = {}
        dict_x = {}
        for a in range(len(btc_x)):
            dict_anti_x[btc_x[a]] = done_set_show_btc[a][0]
            dict_x[done_set_show_btc[a][0]] = btc_x[a]

        # sql_show_profit = "select * from my_capital order by state_dt asc"
        sql_show_profit = "select max(a.capital),a.state_dt from my_capital a where a.state_dt is not null group by a.state_dt order by a.state_dt asc"
        done_set_show_profit = db.select(sql_show_profit)
        profit_x = [dict_x[x[1]] for x in done_set_show_profit]
        profit_y = [x[0] / done_set_show_profit[0][0] for x in done_set_show_profit]

        # 绘制收益率曲线（含大盘基准收益曲线）
        def c_fnx(val, poz):
            if val in dict_anti_x.keys():
                return dict_anti_x[val]
            else:
                return ''

        fig = plt.figure(figsize=(20, 12))
        ax = fig.add_subplot(111)
        ax.xaxis.set_major_formatter(FuncFormatter(c_fnx))

        plt.plot(btc_x, btc_y, color='blue')
        plt.plot(profit_x, profit_y, color='red')
        plt.show()
        db.close()

if __name__ == '__main__':
    a=main()
    a.initialize()
    a.go()






