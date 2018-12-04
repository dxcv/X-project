# encoding: UTF-8
import tushare as ts
from easyBC import Deal
from tools.to_mysql import ToMysql
from datetime import datetime
# 单独的交易函数
def buy(stock_code,opdate,buy_money,trade_side):
    # 建立数据库连接
    db = ToMysql()
    deal_buy = Deal.Deal(opdate)
    ts.set_token('502bcbdbac29edf1c42ed84d5f9bd24d63af6631919820366f53e5d4')
    pro = ts.pro_api()
    if deal_buy.cur_available_fund+1 >= buy_money: # 现金要充足
        sql_buy = "select * from stock_info a where a.state_dt = '%s' and a.stock_code = '%s'" % (opdate, stock_code)
        done_set_buy = db.select(sql_buy)
        if len(done_set_buy) == 0:
            print("缺少买入股票当日行情数据" + str(stock_code) + str(opdate))
            opdate2 = (datetime.strptime(opdate, "%Y-%m-%d")).strftime('%Y%m%d')
            resu = pro.daily(ts_code = stock_code, trade_date = opdate2)
            if len(resu) !=0:
                print("已经从互联网获取数据"+ str(stock_code) + str(opdate))
            buy_price = resu["pre_close"][0]

            sql_insert = "INSERT INTO stock_all(state_dt,stock_code,open,close,high,low,vol,amount,pre_close,amt_change,pct_change) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f','%.2f','%.2f')" % (
                        opdate, str(resu.iloc[0][0]), float(resu.iloc[0][2]), float(resu.iloc[0][5]), float(resu.iloc[0][3]), float(resu.iloc[0][4]),
                        float(resu.iloc[0][9]), float(resu.iloc[0][10]), float(resu.iloc[0][6]), float(resu.iloc[0][7]), float(resu.iloc[0][8]))
            db.execute(sql_insert)
        else:
            buy_price = float(done_set_buy[0][8])
        if buy_price <= 0:
            print("买入价格异常"+ str(stock_code) + str(opdate))
        vol, rest = divmod(min(deal_buy.cur_available_fund, buy_money), buy_price * 100)
        vol = vol * 100
        if vol == 0:
            print("买入数量为0"+ str(stock_code) + str(opdate))
        # 更新账户表my_capital
        new_capital = deal_buy.cur_total_asset - vol * buy_price * 0.0005  # 手续费为万5，直接减少净资产
        new_available_fund = deal_buy.cur_available_fund - vol * buy_price * 1.0005     # 减少相应的现金。
        new_holding_value = deal_buy.cur_holding_value + vol * buy_price   # 增加持仓市值
        new_margin = 0  # 先不填这个坑
        sql_buyorder_update = "UPDATE my_capital SET available_fund = %.2f," \
                             "holding_value = %.2f," \
                             "margin = %.2f," \
                             "total_asset = %.2f  " \
                             "WHERE date = '%s'  " % (new_available_fund, new_holding_value, new_margin, new_capital,opdate)
        db.execute(sql_buyorder_update)
        # 更新position cash
        sql_position_cash = "UPDATE my_position SET code = '%s',cost_price = %.2f,revenue = %.2f," \
                              "volume = %.2f,amount = %.2f,margin= %.2f,side='%s'  WHERE code = '%s' AND  trdate = '%s' " \
                              % ('cash', 1, 0, float(new_available_fund),float(new_available_fund), 0, 'buy','cash', opdate)
        db.execute(sql_position_cash)

        # 更新orders表
        new_stock_code = stock_code
        new_order_time = opdate
        new_trade_side = trade_side
        new_volume = vol
        new_price = buy_price
        new_amount = vol * buy_price
        new_err_msg = 1

        sql_order_update = "insert into orders(stock_code,order_time,trade_side,volume,price,amount,err_msg) " \
                           "VALUES ('%s','%s','%s',%.2f,%.2f,%.2f,'%s')" \
                           % (new_stock_code,new_order_time,new_trade_side,new_volume,new_price,new_amount,new_err_msg
                              )
        db.execute(sql_order_update)

        # 更新position表
        #判断是不是在持仓里面
        if stock_code in deal_buy.stock_pool:
            new_code = stock_code
            new_amount = deal_buy.stock_amount[stock_code] + vol * buy_price
            new_revenue = deal_buy.stock_revenue[stock_code]
            new_volume = new_amount / buy_price
            new_cost_price = (new_amount-new_revenue)/new_volume
            new_margin = 0
            new_side = "buy"
            sql_position_update = "UPDATE my_position SET code = '%s'," \
                             "cost_price = %.2f,revenue = %.2f," \
                             "volume = %.2f,amount = %.2f,margin= %.2f,side='%s' WHERE code = '%s' AND trdate = '%s' "\
                                  % (new_code, new_cost_price,new_revenue,new_volume,new_amount,new_margin,new_side,new_code,opdate)
            db.execute(sql_position_update)
        else:
            new_code = stock_code
            new_amount = vol * buy_price
            new_revenue = 0
            new_cost_price = buy_price
            new_volume = vol
            new_margin = 0
            new_side = "buy"

            sql_position_insert = "insert into my_position(trdate,code,cost_price,revenue,volume,amount,margin,side) " \
                                  "VALUES ('%s','%s',%.2f,%.2f,%.2f,%.2f,%.2f,'%s')" \
                                  % (opdate,new_code, new_cost_price, new_revenue, new_volume, new_amount, new_margin, new_side
                                     )
            db.execute(sql_position_insert)
        return 1
    else:
        print("现金余额不足"+ str(stock_code) + str(opdate))
    db.close()
    return 0


def sell(stock_code, opdate, sell_money, trade_side):
    # 建立数据库连接
    db = ToMysql()
    ts.set_token('502bcbdbac29edf1c42ed84d5f9bd24d63af6631919820366f53e5d4')
    pro = ts.pro_api()
    deal_sell = Deal.Deal(opdate)
    sql_sell_select = "select * from stock_info a where a.state_dt = '%s' and a.stock_code = '%s'" \
                      % (opdate, stock_code)
    done_set_sell_select = db.select(sql_sell_select)
    if len(done_set_sell_select) == 0:
        print("缺少卖出股票当日行情数据"+ str(stock_code) + "   "+ str(opdate))
        opdate2 = (datetime.strptime(opdate, "%Y-%m-%d")).strftime('%Y%m%d')
        resu = pro.daily(ts_code = stock_code, trade_date = opdate2)
        if len(resu) != 0:
            print("已经从互联网获取数据"+ str(stock_code) + "   "+str(opdate))
            sell_price = resu["pre_close"][0]

        else:
            print(str(stock_code)+ "  停牌无法卖出"+ str(stock_code) +"   "+ str(opdate))
            return

        sql_insert = "INSERT INTO stock_all(state_dt,stock_code,open,close,high,low,vol,amount,pre_close,amt_change,pct_change) VALUES ('%s', '%s', '%.2f', '%.2f','%.2f','%.2f','%i','%.2f','%.2f','%.2f','%.2f')" % (
            opdate, str(resu.iloc[0][0]), float(resu.iloc[0][2]), float(resu.iloc[0][5]), float(resu.iloc[0][3]), float(resu.iloc[0][4]),
                        float(resu.iloc[0][9]), float(resu.iloc[0][10]), float(resu.iloc[0][6]), float(resu.iloc[0][7]), float(resu.iloc[0][8]))
        db.execute(sql_insert)

    else:
        sell_price = float(done_set_sell_select[0][8])


    if sell_money < deal_sell.stock_amount[stock_code]:
        vol = sell_money / sell_price
        # 更新账户表my_capital######
        new_capital = deal_sell.cur_total_asset  # 卖出净资产不变
        new_available_fund = deal_sell.cur_available_fund + sell_money  # 增加相应的现金。
        new_holding_value = deal_sell.cur_holding_value - sell_money  # 减少持仓市值
        new_margin = 0  # 先不填这个坑
        sql_sellorder_update = "UPDATE my_capital SET available_fund = %.2f," \
                               "holding_value = %.2f," \
                               "margin = %.2f," \
                               "total_asset = %.2f  " \
                               "WHERE date = '%s'  " % (
                                   new_available_fund, new_holding_value, new_margin, new_capital, opdate)
        db.execute(sql_sellorder_update)
        # 更新position cash
        sql_position_cash = "UPDATE my_position SET code = '%s'," \
                            "cost_price = %.2f,revenue = %.2f," \
                            "volume = %.2f,amount = %.2f,margin= %.2f,side='%s' WHERE code = '%s' AND trdate = '%s' " \
                            % ("cash", 1, 0, float(new_available_fund),float(new_available_fund), 0, "buy",
                               "cash", opdate)
        db.execute(sql_position_cash)
        # 更新orders表###
        new_stock_code = stock_code
        new_order_time = opdate
        new_trade_side = trade_side
        new_volume = vol
        new_price = sell_price
        new_amount = vol * sell_price
        new_err_msg = 1
        sql_order_insert = "insert into orders(stock_code,order_time,trade_side,volume,price,amount,err_msg) " \
                           "VALUES ('%s','%s','%s',%.2f,%.2f,%.2f,'%s')" \
                           % (
                               new_stock_code, new_order_time, new_trade_side, new_volume, new_price, new_amount, new_err_msg
                           )
        db.execute(sql_order_insert)
        # 更新position表
        new_code = stock_code
        new_amount = deal_sell.stock_amount[stock_code] - vol * sell_price
        new_revenue = deal_sell.stock_revenue[stock_code]
        new_volume = new_amount / sell_price
        new_cost_price = (new_amount - new_revenue) / new_volume
        new_margin = 0
        new_side = "buy"
        if new_amount == 0:
            sql_position_delete = "DELETE FROM my_position" \
                                 "WHERE code = '%s' AND trdate = '%s'" %(stock_code,opdate)
            db.execute(sql_position_delete)
        else:
            sql_position_update = "UPDATE my_position SET code = '%s'," \
                                  "cost_price = %.2f,revenue = %.2f," \
                                  "volume = %.2f,amount = %.2f,margin= %.2f,side='%s'" \
                                  "WHERE code = '%s' AND trdate = '%s'" \
                                  % (new_code, new_cost_price, new_revenue, new_volume, new_amount, new_margin,
                                      new_side,new_code,opdate)
            db.execute(sql_position_update)
    else:
        print("卖出金额超限"+ str(stock_code) +"   "+ str(opdate))
    db.close()
    return 0
