

DROP TABLE IF EXISTS my_capital;

CREATE TABLE my_capital (
  capital decimal(30,2) NOT NULL,
  money_lock decimal(30,2) DEFAULT NULL,
  money_rest decimal(30,2) DEFAULT NULL,
  deal_action varchar(45) DEFAULT NULL,
  stock_code varchar(45) DEFAULT NULL,
  deal_price decimal(30,2) DEFAULT NULL,
  stock_vol int(20) DEFAULT NULL,
  profit decimal(30,2) DEFAULT NULL,
  profit_rate decimal(20,2) DEFAULT NULL,
  bz varchar(45) DEFAULT NULL,
  state_dt varchar(45) DEFAULT NULL,
  seq int(11) NOT NULL AUTO_INCREMENT,
  score decimal(20,6) DEFAULT NULL,
  PRIMARY KEY (seq)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=gbk;



INSERT INTO `my_capital` VALUES (1000000.00,0.00,1000000.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL);

