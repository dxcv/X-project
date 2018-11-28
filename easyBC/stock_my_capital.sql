

DROP TABLE IF EXISTS my_capital;

CREATE TABLE my_capital (
  date varchar(45) NOT NULL,
  available_fund decimal(30,2) NOT NULL,
  holding_value decimal(30,2) DEFAULT NULL,
  margin decimal(30,2) DEFAULT NULL,
  total_asset decimal(30,2) DEFAULT NULL,
  PRIMARY KEY (date)
)


