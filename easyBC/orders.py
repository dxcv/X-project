# encoding: UTF-8
from easyBC import Deal
from easyBC import order
from tools.to_mysql import TsBarToMysql
from WindPy import *
w.start()
import pandas as pd
###批量下单函数


def change_to(stock_new, state_dt,**poz):
    # 建立数据库连接
    db = TsBarToMysql()
    deal = Deal.Deal(state_dt)
    old_stocklist = deal.stock_pool
    if old_stocklist == None:
        old_stocklist = []


    data = w.wss(stock_new, "mkt_freeshares,pre_close", "unit=1;tradeDate=" + state_dt + ";priceAdj=U;cycle=D")
    target_po = pd.DataFrame(data.Data, columns=data.Codes, index=data.Fields).T
    sumvl = target_po["MKT_FREESHARES"].sum()
    now_position = deal.stock_amount
    ##计算停牌股
    if deal.stock_pool == []:
        tingpai_list = []
        vll = 0

    else:
        data2 = w.wss(stock_new, "trade_status", "tradeDate=" + state_dt)
        tingpai = pd.DataFrame(data2.Data, columns=data2.Codes, index=data2.Fields).T
        jiaoyi_list = tingpai[tingpai['TRADE_STATUS'] == "交易"].index.tolist()
        tingpai_list = list(set(stock_new) - set(jiaoyi_list))
        vll = 0          # 停牌市值
        for i in now_position.keys():
            if i in tingpai_list:
                vll = vll + now_position[i]
            else:
                pass

    vl = (deal.cur_total_asset - vll)
    if poz == {}:
        target_po["weight"] = [i / sumvl for i in target_po["MKT_FREESHARES"].tolist()]
    else:
        target_po["weight"] = poz["poz"]


    target_po["target_vl"] = [i * vl for i in target_po["weight"].tolist()]

    hold = list(set(old_stocklist) & set(stock_new))
    sell1 = list(set(old_stocklist) - set(hold))
    sell = list(set(sell1) - set(tingpai_list))
    buy1 = list(set(stock_new) - set(hold))
    #sell1.remove("cash")
    #sell.remove("cash")
    #buy1.remove("cash")
    list_order = list(set(hold + sell + buy1))
    #list_order.remove("cash")
    buy_order = {}
    sell_order = {}
    sell_order1 = {}

    for i in list_order:
        if i in hold:
            if now_position[i] - target_po["target_vl"].loc[i] < 0:
                buy_order[i] = abs(now_position[i] - target_po["target_vl"].loc[i])

            else:
                sell_order[i] = abs(now_position[i] - target_po["target_vl"].loc[i])


        elif i in buy1:

            buy_order[i] = target_po["target_vl"].loc[i]

        elif i in sell:

            sell_order1[i] = now_position[i]

        else:
            print("股票不在列表中")

    for i in sell_order1:
        order.sell(i,state_dt , sell_order1[i], "sell")
        print("卖出%s  %s股" %(i,sell_order1[i]))


    for i in sell_order:
        order.sell(i,state_dt , sell_order[i], "sell")
        print("卖出%s  %s元" %(i,sell_order[i]))
        # print(err["err_code"])
        # print(err["err_msg"])
    for i in buy_order:
        order.buy(i, state_dt, buy_order[i], "buy")
        print("买入%s  %s元" %(i,buy_order[i]))
        # print(err["err_code"])
        # print(err["err_msg"])
    db.close()
