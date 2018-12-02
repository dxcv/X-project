import pymysql.cursors
from easyBC import Deal
from tools.to_mysql import ToMysql

# 单独的交易函数
def buy(stock_code,opdate,buy_money,trade_side):
    # 建立数据库连接
    db1 = ToMysql()
    db = pymysql.connect(host="localhost", user='root', passwd='8261426', db='stock', charset='utf8')
    cursor = db.cursor()
    deal_buy = Deal.Deal(opdate)

    if deal_buy.cur_available_fund >= buy_money: # 现金要充足
        sql_buy = "select * from stock_info a where a.state_dt = '%s' and a.stock_code = '%s'" % (opdate, stock_code)
        cursor.execute(sql_buy)
        done_set_buy = cursor.fetchall()
        if len(done_set_buy) == 0:
            new_err_msg = "缺少买入股票当日行情数据"
        buy_price = float(done_set_buy[0][3])
        if buy_price <= 0:
            new_err_msg ="买入价格异常"
        vol, rest = divmod(min(deal_buy.cur_available_fund, buy_money), buy_price * 100)
        vol = vol * 100
        if vol == 0:
            new_err_msg ="买入数量为0"
        # 更新账户表my_capital
        new_capital = deal_buy.cur_total_asset - vol * buy_price * 0.0005  # 手续费为万5，直接减少净资产
        new_available_fund = deal_buy.cur_available_fund - vol * buy_price * 1.0005     # 减少相应的现金。
        new_holding_value = deal_buy.cur_holding_value + vol * buy_price # 增加持仓市值
        new_margin = 0 # 先不填这个坑
        sql_buyorder_update ="UPDATE my_capital SET available_fund = %.2f," \
                             "holding_value = %.2f," \
                             "margin = %.2f," \
                             "total_asset = %.2f  " \
                             "WHERE date = '%s'  " % (new_available_fund, new_holding_value, new_margin, new_capital,opdate)
        cursor.execute(sql_buyorder_update)
        db.commit()

        # 更新orders表
        new_stock_code = stock_code
        new_order_time = opdate
        new_trade_side = trade_side
        new_volume = vol
        new_price = buy_price
        new_amount = vol * buy_price
        new_err_msg = 1

        sql_order_update = "insert into my_orders(stock_code,order_time,trade_side,volume,price,amount,err_msg) " \
                           "VALUES ('%s','%s','%s',%.2f,,%.2f,%.2f,'%s')" \
                           % (new_stock_code,new_order_time,new_trade_side,new_volume,new_price,new_amount,new_err_msg
                              )
        cursor.execute(sql_order_update)
        db.commit()

        # 更新position表
        #判断是不是在持仓里面
        if stock_code in deal_buy.stock_pool:
            new_code = stock_code
            new_amount = deal_buy.stock_amount["stock_code"] + vol * buy_price
            new_revenue = deal_buy.stock_revenue["stock_code"]
            new_cost_price = (new_amount-new_revenue)/buy_price
            new_volume = new_amount/buy_price
            new_margin = 0
            new_side = "buy"
            sql_position_update ="UPDATE my_position SET code = '%s'," \
                             "cost_price = %.2f,revenue = %.2f," \
                             "volume = %.2f,amount = %.2f,margin= %.2f,side=,'%s'"\
                             "WHERE code = '%s' " % (new_code, new_cost_price,new_revenue,new_volume,new_amount,new_margin,new_side,new_code)
            cursor.execute(sql_position_update)
            db.commit()
        else:
            new_code = stock_code
            new_amount = vol * buy_price
            new_revenue = 0
            new_cost_price = buy_price
            new_volume = vol
            new_margin = 0
            new_side = 1

            sql_position_insert = "insert into my_position(code,cost_price,revenue,volume,amount,margin,side) " \
                                  "VALUES ('%s',%.2f,%.2f,%.2f,%.2f,%.2f,'%s')" \
                                  % (new_code, new_cost_price,new_revenue,new_volume,new_amount,new_margin,new_side
                                     )
            cursor.execute(sql_position_insert)
            db.commit()
        db.close()
        return 1
    else:
        print("现金余额不足")
    db.close()
    return 0



def sell(stock_code,opdate,sell_money,trade_side):
    # 建立数据库连接
    db = pymysql.connect(host="localhost", user='root', passwd='8261426', db='stock', charset='utf8')
    cursor = db.cursor()

    deal_sell = Deal.Deal(opdate)

    sql_sell_select = "select * from stock_info a where a.state_dt = '%s' and a.stock_code = '%s'" % (opdate, stock_code)
    cursor.execute(sql_sell_select)
    done_set_sell_select = cursor.fetchall()
    if len(done_set_sell_select) == 0:
        return "缺少股票""+stock_code+opdate+行情数据"
    sell_price = float(done_set_sell_select[0][3])
    vol = sell_money/sell_price
    ###更新账户表my_capital######
    new_capital = deal_sell.cur_total_asset  #卖出净资产不变
    new_available_fund = deal_sell.cur_available_fund + sell_money  # 增加相应的现金。
    new_holding_value = deal_sell.cur_holding_value - sell_money  # 减少持仓市值
    new_margin = 0  # 先不填这个坑
    sql_sellorder_update = "UPDATE my_capital SET available_fund = %.2f," \
                          "holding_value = %.2f," \
                          "margin = %.2f," \
                          "total_asset = %.2f  " \
                          "WHERE date = '%s'  " % (
                          new_available_fund, new_holding_value, new_margin, new_capital, opdate)
    cursor.execute(sql_sellorder_update)
    db.commit()
    ###更新orders表###
    new_stock_code = stock_code
    new_order_time = opdate
    new_trade_side = trade_side
    new_volume = vol
    new_price = sell_price
    new_amount = vol * sell_price
    new_err_msg = 1

    sql_order_update = "insert into my_orders(stock_code,order_time,trade_side,volume,price,amount,err_msg) " \
                       "VALUES ('%s','%s','%s',%.2f,,%.2f,%.2f,'%s')" \
                       % (
                       new_stock_code, new_order_time, new_trade_side, new_volume, new_price, new_amount, new_err_msg
                       )
    cursor.execute(sql_order_update)
    db.commit()

    ###更新position表#####
    new_code = stock_code
    new_amount = vol * buy_price
    new_revenue = 0
    new_cost_price = buy_price
    new_volume = vol
    new_margin = 0
    new_side = 1

    sql_position_insert = "insert into my_position(code,cost_price,revenue,volume,amount,margin,side) " \
                          "VALUES ('%s',%.2f,%.2f,%.2f,%.2f,%.2f,'%s')" \
                          % (new_code, new_cost_price, new_revenue, new_volume, new_amount, new_margin, new_side
                             )
    cursor.execute(sql_position_insert)
    db.commit()




    db.close()
    return 0

