import pymysql.cursors

class Deal(object):
    cur_capital = 0.00
    cur_hold = 0.00
    cur_money_rest = 0.00
    stock_pool = []
    stock_map1 = {}
    stock_map2 = {}
    stock_map3 = {}
    stock_all = []
    ban_list = []

    def __init__(self,state_dt):
        # 建立数据库连接
        db = pymysql.connect(host="localhost", user='root', passwd='8261426', db='stock', charset='utf8')
        cursor = db.cursor()
        try:
            sql_select = 'select * from my_capital a where a.date = %s' %repr(state_dt)
            cursor.execute(sql_select)
            done_set = cursor.fetchall()

           ##读取capital数据
            if len(done_set) > 0:
                self.cur_date =done_set[0][0]
                self.cur_available_fund = float(done_set[0][1])
                self.cur_holding_value = float(done_set[0][2])
                self.cur_margin = float(done_set[0][3])
                self.cur_total_asset = float(done_set[0][4])

            else:
                print("账户表初始化未成功")

            sql_select2 = 'select * from my_position a where a.date = %s' %repr(state_dt)
            cursor.execute(sql_select2)
            done_set2 = cursor.fetchall()
            self.stock_pool = []
            self.stock_all = []
            self.stock_map1 = []
            self.stock_map2 = []
            self.stock_map3 = []
            self.ban_list = []       ##禁止买入池
            if len(done_set2) > 0:
                self.stock_pool = [x[0] for x in done_set2]
                self.stock_cost_price = {x[0]: float(x[1]) for x in done_set2}  #买入价格
                self.stock_revenue = {x[0]: int(x[2]) for x in done_set2}    #利润
                self.stock_volume = {x[0]: int(x[3]) for x in done_set2}    #持仓数量
                self.stock_amount = {x[0]: int(x[4]) for x in done_set2}  # 持仓金额
                self.stock_margin = {x[0]: int(x[5]) for x in done_set2}  # 保证金
                self.stock_side = {x[0]: int(x[6]) for x in done_set2}  # 持仓方向

            # sql_select3 = 'select * from ban_list'
            # cursor.execute(sql_select3)
            # done_set3 = cursor.fetchall()
            # if len(done_set3) > 0:
            #     self.ban_list = [x[0] for x in done_set3]


        except Exception as excp:
            #db.rollback()
            print(excp)

        db.close()
