CREATE TABLE `factor_mon` (
  `state_dt` varchar(45) NOT NULL,
  `stock_code` varchar(45) NOT NULL,
  PRIMARY KEY (`state_dt`,`stock_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `month` (
  `state_dt` varchar(45) NOT NULL,
  PRIMARY KEY (`state_dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

