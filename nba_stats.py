#!/usr/bin/python
#coding:utf-8
from urllib import urlopen
import json
import re
import urllib
import cPickle as p
from time import sleep
import sys
while 1:
	'''=========get the code of players========'''
	page_playerlist=urllib.urlopen('http://china.nba.com/static/data/league/playerlist.json').read()
	playerlist_json=json.loads(page_playerlist)
	playerlist=[]
	playerdic={}	#displayname is key,code is value
	for player in playerlist_json['payload']['players']:
		playerlist.append(player['playerProfile']['code'])
		playerdic[player['playerProfile']['displayName']]=player['playerProfile']['code']
	f_dic=file('./stats_nba/dict.dat','w')
	p.dump(playerdic,f_dic)
	f_dic.close
	'''=========get the stats of players according to the code========'''
	for code in playerlist:
		print 'get the stats of %s'%(code)
		stats_url='http://china.nba.com/static/data/player/stats_%s.json'%(code)
		page_stats=urllib.urlopen(stats_url).read()
		stats_json=json.loads(page_stats)
		file_name='./stats_nba/stats_%s.dat'%(code)
		f=file(file_name,'w')
		p.dump(stats_json,f)
		f.close
	print 'finish stats_nba.dat'
	sys.exit()
	sleep(3600)
