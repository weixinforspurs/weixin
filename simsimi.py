#!/usr/bin/python
#!coding:utf-8
import requests
def simsimi(req):
	if type(req)==unicode:
		req=req.encode('utf-8')
	headers={'Content-Length':'8', 
	'Accept':'*/*',
	'Origin': 'http://www.niurenqushi.com',
	'X-Requested-With': 'XMLHttpRequest',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Referer': 'http://www.niurenqushi.com/app/simsimi/',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8'
	}
	data='txt=%s'%(req)
	p=requests.post("http://www.niurenqushi.com/app/simsimi/ajax.aspx",data=data,headers=headers)
	return p.text
if __name__ == '__main__':
	req=raw_input('Plese input:')
	print simsimi(req)
