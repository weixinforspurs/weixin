#!/usr/bin/python
#coding:utf-8
from selenium import webdriver
from time import sleep,time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from json import dumps
import sys
import selenium
import cPickle as p
from time import strftime,localtime
import re
from simsimi import simsimi
def pm25(city):
	city=city.encode("utf-8")
	f=file('./stats_weather/pm25.txt','r')
	dic_pm25=p.load(f)
	f.close
	hour=strftime("%H",localtime())
	if city in dic_pm25.keys():
		if dic_pm25[city]<50:
			level='优'
		elif dic_pm25[city]<101:
			level='良'
		elif dic_pm25[city]<151:
			level='轻度污染'
		elif dic_pm25[city]<201:
			level='中度污染'
		elif dic_pm25[city]<301:
			level='重度污染'
		else:
			level='严重污染'
		return "%s<br>PM2.5:    %s<br>空气质量:%s<br>发布时间:%s:00"%(city,dic_pm25[city],level,hour)
	else:
		return "input error"
def stats_nba(name):
	'''dict.dat example
	   key		code
	'托尼帕克':'tony_parkey'
	'''
	f=file('./stats_nba/dict.dat','r')
	dict_nba=p.load(f)
	f.close
	str_stats=''
	cnt=0
	for key in dict_nba:
		if (len(re.findall(name,key))!=0) & (cnt<5):
			cnt=cnt+1
			print cnt
			code=dict_nba[key]
			ff='./stats_nba/stats_%s.dat'%(code)	
			f_stats=file(ff,'r')
			stats=p.load(f_stats)	#stats is dict 
			f_stats.close()
	#http://china.nba.com/static/data/player/stats_kawhi_leonard.json
			ast=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['assistsPg']
			blk=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['blocksPg']
			point=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['pointsPg']
			games=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['games']
			gamesStarted=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['gamesStarted']
			minsPg=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['minsPg']
			offRebsPg=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['offRebsPg']
			defRebsPg=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['defRebsPg']
			rebsPg=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['rebsPg']
			stealsPg=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['stealsPg']
			turnoversPg=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['turnoversPg']
			tppct=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['tppct']
			ftpct=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['ftpct']
			fgpct=stats['payload']['player']['stats']['currentSeasonTypeStat']['currentSeasonTypePlayerTeamStats'][0]['statAverage']['fgpct']
			str_stats=str_stats+'%s<br>出场:%s<br>首发:%s<br>时间:%s<br>得分:%s<br>篮板:%s<br>助攻:%s<br>抢断:%s<br>盖帽:%s<br>投篮命中率:%s%%<br>罚篮命中率:%s%%<br>三分命中率:%s%%<br>失误:%s<br>'%(code,games,gamesStarted,minsPg,point,rebsPg,ast,stealsPg,blk,fgpct,ftpct,tppct,turnoversPg)
	return str_stats

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

'''=============Login==========='''
print '=======open webdirver'
br=webdriver.Remote(desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS)
#br=webdriver.Chrome()
br.get("https://mp.weixin.qq.com")
#account=raw_input('Plese input account:')
#br.find_element_by_name('account').send_keys(account)
br.find_element_by_name('account').send_keys('weixinforspurs@126.com')
#password=raw_input('Plese input account:')
#br.find_element_by_name('password').send_keys(password)
br.find_element_by_name('password').send_keys('cpu2.55305')
br.find_element_by_id('loginBt').click()
print '=======login success!'
sleep(1)
br.find_element_by_xpath('//a[@data-id=10012]').click()
sleep(1)
while 1:
	try:
		br.find_element_by_xpath('//li[@class="message_item "]/div/a[2]').click()
		msg=br.find_element_by_xpath('//li[@class="message_item  replying"]/div[@class="message_content text"]').text
		print msg
		'''=======reply======='''
		msg_pm25=pm25(msg)
		msg_nba=stats_nba(msg)
		if msg_pm25!='input error':
			msg_out=msg_pm25
		elif len(msg_nba)!=0: 
			msg_out=msg_nba
		else:
			#msg_out='input error'
			msg_out=simsimi(msg)
		br.execute_script('document.getElementsByClassName("edit_area js_editorArea")[1].click()')
		br.execute_script('document.getElementsByClassName("edit_area js_editorArea")[1].innerHTML='+dumps(msg_out))
		br.find_element_by_xpath('//div[@class="emotion_editor"]/div[2]').send_keys(Keys.LEFT)
		br.find_element_by_xpath('//div[@class="emotion_editor"]/div[2]').send_keys(Keys.LEFT)
		br.find_element_by_xpath('//div[@class="emotion_editor"]/div[2]').send_keys(Keys.ENTER)
	except selenium.common.exceptions.NoSuchElementException:
		print "new msg is 0",time()
	sleep(0.3)
	br.refresh()	
