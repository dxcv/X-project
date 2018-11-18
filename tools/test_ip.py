# -*- coding: utf-8 -*-

import requests
'''代理IP地址（高匿）'''
proxy = {
  'http': 'http://117.85.105.170:808',
  'https': 'https://117.85.105.170:808'
}
'''head 信息'''
head = {'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
       'Connection': 'keep-alive'}
'''http://icanhazip.com会返回当前的IP地址'''
p = requests.get('http://icanhazip.com', headers=head, proxies=proxy)
print(p.text)