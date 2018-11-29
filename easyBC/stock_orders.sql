
DROP TABLE IF EXISTS my_position;

CREATE TABLE my_position (
  trdate varchar(45) NOT NULL,
  code varchar(45) NOT NULL,
  cost_price decimal(30,2) NOT NULL,
  revenue decimal(30,2) DEFAULT NULL,
  volume decimal(30,2) DEFAULT NULL,
  amount decimal(30,2) DEFAULT NULL,
  margin decimal(30,2) DEFAULT NULL,
  side varchar(45) DEFAULT NULL,
  PRIMARY KEY (trdate,code)
)