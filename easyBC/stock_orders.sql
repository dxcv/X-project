
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
  stock_code varchar(45) NOT NULL,
  order_time varchar(45) NOT NULL,
  trade_side varchar(45) NOT NULL,
  volume decimal(20,2) DEFAULT NULL,
  price decimal(20,2) DEFAULT NULL,
  amount decimal(20,2) DEFAULT NULL,
  err_msg varchar(45) DEFAULT NULL,
  PRIMARY KEY (order_time,stock_code))