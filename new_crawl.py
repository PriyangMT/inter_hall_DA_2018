"""Scraping the sectoral allocation and top 5 holdings of each mutual fund
"""
from bs4 import BeautifulSoup
import urllib2
import sys
import os
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import getpass
import re


driver = webdriver.Firefox()

def crawl(url):
	# page=urllib2.urlopen(url)
	soup=BeautifulSoup(url,'lxml')
	data=pd.read_csv('crawled_data.csv',delimiter=',')
	# print soup
	name=(unicode(soup.findChildren(['h1'])[0].string)).encode('utf-8')
	
	data['Fund Name']=name
	tables=soup.findChildren(['table'])
	strdata=[]
	table=tables[4]
	rows=table.findChildren(['tr'])
	for row in rows:
		for string in row.stripped_strings:
			strdata.append((unicode(string)).encode('utf-8'))
			# print string
	flag=7
	for i,string in enumerate(strdata):
		if(string=='Fund Returns'):
			flag=i
			data['Fund Returns']=strdata[i+flag]
		if(string=='Category avg'):
			data['Category avg']=strdata[i+flag]
		if(string=='Difference of Fund returns and Category returns'):
			data['Difference of Fund returns and Category returns']=strdata[i+flag]
		if(string=='Best of category'):
			data['Best of category']=strdata[i+flag]
		if(string=='Worst of category'):
			data['Worst of category']=strdata[i+flag]
		if('Benchmark returns' in string and 'Difference' not in string):
			data['Benchmark returns']=strdata[i+flag]
		if(string=='Difference of Fund returns and Benchmark returns'):
			data['Difference of Fund returns and Benchmark returns']=strdata[i+flag]

	strdata=[]
	table=tables[5]
	rows=table.findChildren(['tr'])
	for row in rows:
		for string in row.stripped_strings:
			strdata.append((unicode(string)).encode('utf-8'))
			# print string
	for i,string in enumerate(strdata):
		if(string=='Fund Type'):
			data['Fund Type']=strdata[i+1]
		if(string=='Minimum Investment'):
			data['Minimum Investment']=strdata[i+1]
		if('Benchmark' in string):
			if('Asset' not in strdata[i+1]):
				data['Benchmark']=strdata[i+1]
		if('Launch date' in string):
			data['Launch Date']=strdata[i+1]
		if(string=='Investment Plan'):
			data['Investment Plan']=strdata[i+1]
	# print data

	strdata=[]
	table=tables[10]
	rows=table.findChildren(['tr'])
	for row in rows:
		for string in row.stripped_strings:
			strdata.append((unicode(string)).encode('utf-8'))
			# print string
	for i,string in enumerate(strdata):
		if('Automotive' in string):
			data['Automotive']=strdata[i+1]
		if('Banking/Finance' in string):
			data['Banking/Finance']=strdata[i+1]
		if('Pharmaceuticals' in string):
			data['Pharmaceuticals']=strdata[i+1]
		if('Cons NonDurable' in string):
			data['Cons NonDurable']=strdata[i+1]
		if('Miscellaneous' in string):
			data['Miscellaneous']=strdata[i+1]
		if('Telecom' in string):
			data['Telecom']=strdata[i+1]
		if('Cement' in string):
			data['Cement']=strdata[i+1]
		if('Real Estate' in string):
			data['Real Estate']=strdata[i+1]
		if('Engineering' in string):
			data['Engineering']=strdata[i+1]
		if('Oil & Gas' in string):
			data['Oil & Gas']=strdata[i+1]
		if('Utilities' in string):
			data['Utilities']=strdata[i+1]
		if('Manufacturing' in string):
			data['Manufacturing']=strdata[i+1]
		if('Technology' in string):
			data['Technology']=strdata[i+1]
		if('Conglomerates' in string):
			data['Conglomerates']=strdata[i+1]
		if('Chemicals' in string):
			data['Chemicals']=strdata[i+1]
		if('Food & Beverage' in string):
			data['Food & Beverage']=strdata[i+1]
		if('Tobacco' in string):
			data['Tobacco']=strdata[i+1]
		if('Media' in string):
			data['Media']=strdata[i+1]
		if('Services' in string):
			data['Services']=strdata[i+1]
		if('Metals & Mining' in string):
			data['Metals & Mining']=strdata[i+1]
		if('Cons Durable' in string):
			data['Cons Durable']=strdata[i+1]

	strdata=[]
	table=tables[11]
	rows=table.findChildren(['tr'])
	for row in rows:
		for string in row.stripped_strings:
			strdata.append((unicode(string)).encode('utf-8'))
			# print string		
	for i,string in enumerate(strdata):
		if('Equity' in string):
			data['Equity']=strdata[i+1]
		if('Debt' in string):
			data['Debt']=strdata[i+1]

	if(len(tables)>=13):
		strdata=[]
		table=tables[12]
		rows=table.findChildren(['tr'])
		for row in rows:
			for string in row.stripped_strings:
				strdata.append((unicode(string)).encode('utf-8'))
				# print string

		if(strdata[0]=='Holdings'):
			for i,string in enumerate(strdata):
				if('Top 5' in string):
					data['Top 5 Holdings']=strdata[i+1]
				if('Top 10' in string):
					data['Top 10 Holdings']=strdata[i+1]
		if(strdata[0]=='Sector'):
			for i,string in enumerate(strdata):
				if('Top 3' in string):
					data['Top 3 Sector']=strdata[i+1]

	# try:
	if(len(tables)>=14):
		strdata=[]
		table=tables[13]
		# print table
		rows=table.findChildren(['tr'])
		for row in rows:
			for string in row.stripped_strings:
				strdata.append((unicode(string)).encode('utf-8'))
				# print string

		if(strdata[0]=='Holdings'):
			for i,string in enumerate(strdata):
				if('Top 5' in string):
					data['Top 5 Holdings']=strdata[i+1]
				if('Top 10' in string):
					data['Top 10 Holdings']=strdata[i+1]
		if(strdata[0]=='Sector'):
			for i,string in enumerate(strdata):
				# print string
				if('Top 3' in string):
					data['Top 3 Sector']=strdata[i+1]
	return data


# crawl('http://www.moneycontrol.com/mutual-funds/nav/tata-fixed-income-portfolio-fund-scheme-a2-regular-plan/MTA266')
for file in os.listdir('scheme code mutual fund'):
	dataframe=pd.DataFrame()
	if('.~' in file):
		continue
	df=pd.read_csv('scheme code mutual fund/'+file)
	for counter,sch_name in enumerate(list(df['Scheme Name'])):
		if(sch_name=='NaN'):
			print 'continue'
			continue

		try:
			sch_name+'str'
		except:
			continue
		print sch_name
		driver.get("https://google.co.in")
		search_bar = driver.find_element_by_id("lst-ib")
		search_bar.send_keys(sch_name+' moneycontrol')
		search = driver.find_element_by_xpath("//input[@value='Google Search']")
		search.click()
		i=0
		while(1):
			try:
				link = driver.find_elements_by_xpath("//h3[@class='r']/a")[i]
				i+=1
				if("http://www.moneycontrol.com/mutual-funds/nav/" in link.get_attribute('href')):
					link.click()
					sleep(5)
					try:
						df2=crawl(driver.page_source)
						df2['Scheme Code']=df.iloc[counter,0]
						df2['Scheme Name']=sch_name
						dataframe=dataframe.append(df2)
						print "Counter : ",counter
						break
					except Exception as inst:
						if('list index' not in str(inst)):
							print 'first except : ',inst
							break
						# sp=BeautifulSoup(driver.page_source,'lxml')
						# snapshot=sp.find(id='a_0')			
						snapshot=driver.find_element_by_xpath("//h2[@id='h2_0']")
						snapshot.click()
						sleep(4)
						df2=crawl(driver.page_source)
						df2['Scheme Code']=df.iloc[counter,0]
						df2['Scheme Name']=sch_name
						dataframe=dataframe.append(df2)
						print "Counter : ",counter
						break
						
			except Exception as e:
				print 'second except : ',e
				break
	dataframe.to_csv('final/'+file+'_data.csv',index=False)
