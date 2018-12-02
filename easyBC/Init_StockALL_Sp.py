import datetime
import tushare as ts
from tools.to_mysql import TsBarToMysql
import time
if __name__ == '__main__':

    # 设置tushare pro的token并获取连接
    ts.set_token('502bcbdbac29edf1c42ed84d5f9bd24d63af6631919820366f53e5d4')
    pro = ts.pro_api()
    # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
    start_dt = '20100406'
    end_dt = "20181130"
    df = pro.trade_cal(exchange_id='', is_open=1, start_date=start_dt, end_date=end_dt)
    date_temp = list(df.iloc[:, 1])
    date_seq = [x for x in date_temp]
    # 建立数据库连接,剔除已入库的部分
    Bars = TsBarToMysql()
    for i in range(int(len(date_seq)/30)-1):
        s_dt = date_seq[i*30]
        e_dt = date_seq[(i+1)*30]

        con_list = pro.index_weight(index_code='000906.Sh', start_date=s_dt, end_date=e_dt)

        # 设定需要获取数据的股票池
        stock_pool = con_list.con_code.tolist()
        total = len(stock_pool)
        # 循环获取单个股票的日线行情
        for i in range(len(stock_pool)):
            try:
                df = pro.daily(ts_code=stock_pool[i], start_date=s_dt, end_date=e_dt)
                time.sleep(0.3)
                print('Seq: ' + "start_date: "+ str(s_dt)+"end_date: "+str(e_dt) + ' of ' + str(date_seq[-1]) + '   Code: ' + str(stock_pool[i]))
                c_len = df.shape[0]
            except Exception as aa:
                print(aa)
                print('No DATA Code: ' + str(i))
                continue
            for j in range(c_len):
                resu0 = list(df.iloc[c_len - 1 - j])
                resu = []
                for k in range(len(resu0)):
                    if str(resu0[k]) == 'nan':
                        resu.append(-1)
                    else:
                        resu.append(resu0[k])
                state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
                try:
                    sql_insert = "INSERT INTO stock_all(state_dt,stock_code,open,close,high,low,vol,amount,pre_close,amt_change,pct_change) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f','%.2f','%.2f')" % (
                    state_dt, str(resu[0]), float(resu[2]), float(resu[5]), float(resu[3]), float(resu[4]),
                    float(resu[9]), float(resu[10]), float(resu[6]), float(resu[7]), float(resu[8]))
                    Bars.insert(sql_insert)
                except Exception as err:
                    continue
    Bars.close()
    print('All Finished!')
