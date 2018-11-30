

DROP TABLE IF EXISTS my_position;

CREATE TABLE my_capital (
  trdate varchar(45) NOT NULL,
  code varchar(45) NOT NULL,
  cost_price decimal(30,2) NOT NULL,
  revenue decimal(30,2) NOT NULL,
  volume decimal(30,2) NOT NULL,
  amount decimal(30,2) NOT NULL,
  margin decimal(30,2) NOT NULL,
  side varchar(45) NOT NULL,
  PRIMARY KEY (trdate,code)
)