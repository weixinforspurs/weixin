#!/usr/bin/python
#coding:utf-8
from urllib import urlopen
import re
import cPickle as p
from time import sleep
while 1:
	page=urlopen('http://www.pm25.com/rank.html')
	html=page.readlines()
	dic_pm25={}
	for i in html:
		if len(re.findall("a class=\"pjadt_location\"",i))!=0:
			key_city=re.findall(">(.+?)<",i)
		if len(re.findall("span class=\"pjadt_aqi\"",i))!=0:
			value_city=re.findall(">(.+?)<i",i)
			dic_pm25[key_city[0]]=eval(value_city[0])
	f=file('./stats_weather/pm25.txt','w')
	p.dump(dic_pm25,f)
	f.close()
	print 'finish pm25.txt'
	sleep(1800)
