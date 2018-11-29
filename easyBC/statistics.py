from pylab import *
import pandas as pd
from tools.to_mysql import ToMysql

def get_sharp_rate():
    db =ToMysql()

    sql_cap = "select * from my_capital a order by seq asc"
    done_exp = db.select(sql_cap)
    cap_list = [float(x[0]) for x in done_exp]
    return_list = []
    base_cap = float(done_exp[0][0])
    for i in range(len(cap_list)):
        if i == 0:
            return_list.append(float(1.00))
        else:
            ri = (float(done_exp[i][0]) - float(done_exp[0][0]))/float(done_exp[0][0])
            return_list.append(ri)
    std = float(np.array(return_list).std())
    exp_portfolio = (float(done_exp[-1][0]) - float(done_exp[0][0]))/float(done_exp[0][0])
    exp_norisk = 0.04*(5.0/12.0)
    sharp_rate = (exp_portfolio - exp_norisk)/(std)

    return sharp_rate,std


def r(nav_df):   #计算收益率,超额收益率，夏普比率，基准夏普比率，胜率，信息比率，最大回撤，基准最大回撤
    nav, benchmark = nav_df['nav'], nav_df['benchmark']
    r_year = (nav.iloc[-1]/nav.iloc[0]-1)*100
    r_benchmark_year = (benchmark.iloc[-1]/benchmark.iloc[0]-1)*100
    r_excess_year = r_year - r_benchmark_year
    r = (np.array(nav.iloc[1:])/np.array(nav.iloc[:-1]) -1)*100
    rb = (np.array(benchmark.iloc[1:])/np.array(benchmark.iloc[:-1]) - 1)*100
    r_excess = r - rb
    sharpe = (r.mean()*252 - 3.5)/(r.std()*np.sqrt(252))
    sharpe_benchmark = (rb.mean()*252 - 3.5)/(rb.std()*np.sqrt(252))    #这里无风险利率假定为3%
    win_rate = (r > rb).sum()/len(r)*100
    information_ratio = r_excess.mean()/(r_excess.std())*100
    Drawdown = []
    for j in range(1,len(nav)):
        drawdown = abs((np.array(nav.iloc[j]) - np.array(nav.iloc[:j]).max())/(np.array(nav.iloc[:j]).max()))*100
        Drawdown.append(drawdown)
    max_drawdown = np.array(Drawdown).max()
    Drawdown_benchmark = []
    for i in range(1,len(benchmark)):
        drawdown = abs((np.array(benchmark.iloc[j]) - np.array(benchmark.iloc[:j]).max())/(np.array(benchmark.iloc[:j]).max()))*100
        Drawdown_benchmark.append(drawdown)
    max_drawdown_benchmark = np.array(Drawdown_benchmark).max()
    return r_year,r_excess_year,sharpe,sharpe_benchmark,win_rate,information_ratio,max_drawdown,max_drawdown_benchmark


if __name__ == '__main__':
    nav_df = pd.read_csv(./data/300.csv)
    assessment_stg = pd.DataFrame([], columns=['年化收益率', '年化超额收益率', '夏普比率', '基准夏普比率', '胜率', '信息比率', '最大回撤', '基准最大回撤'])
    nav_df['year'] = [i[0:4] for i in nav_df['time']]
    re = nav_df[nav_df["year"] == "2010"]
    res = pd.DataFrame(nav_df.groupby('year').apply(r))
    for year in list(res.index):
        assessment_stg.loc[year] = res.loc[year, 0]
    print(assessment_stg)


