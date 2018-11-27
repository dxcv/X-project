
DROP TABLE IF EXISTS model_ev_mid;

CREATE TABLE model_ev_mid (
  state_dt varchar(50) NOT NULL,
  stock_code varchar(45) NOT NULL,
  resu_predict decimal(20,2) DEFAULT NULL,
  resu_real decimal(20,2) DEFAULT NULL
)