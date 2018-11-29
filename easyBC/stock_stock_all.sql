
DROP TABLE IF EXISTS stock_all;

CREATE TABLE stock_all (
  state_dt varchar(45) NOT NULL,
  stock_code varchar(45) NOT NULL,
  open decimal(20,2) DEFAULT NULL,
  close decimal(20,2) DEFAULT NULL,
  high decimal(20,2) DEFAULT NULL,
  low decimal(20,2) DEFAULT NULL,
  vol int(20) DEFAULT NULL,
  amount decimal(30,2) DEFAULT NULL,
  pre_close decimal(20,2) DEFAULT NULL,
  amt_change decimal(20,2) DEFAULT NULL,
  pct_change decimal(20,2) DEFAULT NULL,
  big_order_cntro decimal(20,2) DEFAULT NULL,
  big_order_delt decimal(20,2) DEFAULT NULL,
  PRIMARY KEY (state_dt,stock_code)
) 