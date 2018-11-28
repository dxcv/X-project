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
            sql_select = 'select * from my_capital a order by seq desc limit 1'
            cursor.execute(sql_select)
            done_set = cursor.fetchall()

            self.cur_capital = 0.00 # 初始化的时候会用到
            self.cur_money_rest = 0.00 # 初始化的时候会用到
            self.cur_hold = 0.00  #每次调用会重新计算仓位市值
            if len(done_set) > 0:
                self.cur_capital = float(done_set[0][0])
                self.cur_money_rest = float(done_set[0][2])
            sql_select2 = 'select * from my_stock_pool'
            cursor.execute(sql_select2)
            done_set2 = cursor.fetchall()
            self.stock_pool = []
            self.stock_all = []
            self.stock_map1 = []
            self.stock_map2 = []
            self.stock_map3 = []
            self.ban_list = []       ##禁止买入池
            if len(done_set2) > 0:
                self.stock_pool = [x[0] for x in done_set2 if x[2] > 0]
                self.stock_all = [x[0] for x in done_set2]
                self.stock_map1 = {x[0]: float(x[1]) for x in done_set2}  #买入价格
                self.stock_map2 = {x[0]: int(x[2]) for x in done_set2}    #持仓数量
                self.stock_map3 = {x[0]: int(x[3]) for x in done_set2}    #持仓天数
            for i in range(len(done_set2)):
                sql = "select * from stock_info a where a.stock_code = '%s' and a.state_dt = '%s'"%(done_set2[i][0],state_dt)
                cursor.execute(sql)
                done_temp = cursor.fetchall()
                db.commit()
                self.cur_hold += float(done_temp[0][3]) * float(done_set2[i][2])
            # sql_select3 = 'select * from ban_list'
            # cursor.execute(sql_select3)
            # done_set3 = cursor.fetchall()
            # if len(done_set3) > 0:
            #     self.ban_list = [x[0] for x in done_set3]


        except Exception as excp:
            #db.rollback()
            print(excp)

        db.close()
