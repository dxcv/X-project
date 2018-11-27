
DROP TABLE IF EXISTS model_ev_resu;

CREATE TABLE model_ev_resu (
  state_dt varchar(50) NOT NULL DEFAULT '',
  stock_code varchar(45) NOT NULL DEFAULT '',
  acc decimal(20,4) DEFAULT NULL,
  recall decimal(20,4) DEFAULT NULL,
  f1 decimal(20,4) DEFAULT NULL,
  acc_neg decimal(20,4) DEFAULT NULL,
  bz varchar(45) DEFAULT NULL,
  predict varchar(45) DEFAULT NULL,
  PRIMARY KEY (state_dt,stock_code)
)