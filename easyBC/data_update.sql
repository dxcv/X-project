select * from stock_all a
where (a.state_dt,a.stock_code) in (select state_dt,stock_code from stock_all group by state_dt,stock_code having count(*) > 1)