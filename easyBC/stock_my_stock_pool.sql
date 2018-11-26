
DROP TABLE IF EXISTS my_stock_pool;
CREATE TABLE my_stock_pool (
   stock_code varchar(50) NOT NULL,
   buy_price decimal(20,2) DEFAULT NULL,
   hold_vol int(11) DEFAULT NULL,
   hold_days int(11) DEFAULT '1',
   PRIMARY KEY (stock_code))
