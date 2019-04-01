'''
This is code is used to scrape AUM values of all MF schemes for all the MFHs.
This  data further needs to be processed
'''
# coding: utf-8

# In[53]:


from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get('https://www.amfiindia.com/research-information/aum-data/average-aum')

select_box = driver.find_element_by_xpath("//div[@id='divAumType']/span/input")
select_box.send_keys("Schemewise")
select_box = driver.find_element_by_xpath("//div[@id='divAumCategoryType']/span/input")
select_box.send_keys("Typewise")

MFH = ['Aditya Birla Sun Life Mutual Fund', 'HDFC Mutual Fund', 'ICICI Prudential Mutual Fund', 'Reliance Mutual Fund',
       'SBI Mutual Fund', 'Sundaram Mutual Fund', 'Tata Mutual Fund', 'UTI Mutual Fund']
Date = {'April 2012 - March 2013':['January - March 2013'],
        'April 2013 - March 2014':['April - June 2013', 'July - September 2013','October - December 2013','January - March 2014'],
        'April 2014 - March 2015':['April - June 2014', 'July - September 2014','October - December 2014','January - March 2015'],
        'April 2015 - March 2016':['April - June 2015', 'July - September 2015','October - December 2015','January - March 2016'],
        'April 2016 - March 2017':['April - June 2016', 'July - September 2016','October - December 2016','January - March 2017'],
        'April 2017 - March 2018':['April - June 2017', 'July - September 2017','October - December 2017']}


# In[54]:


for mf in MFH:
    select_box = driver.find_element_by_xpath("//div[@id='divAumMFName']/span/input")
    select_box.clear()
    select_box.send_keys(mf)
    select_box.send_keys(Keys.DOWN)
#     select_box.send_keys(Keys.DOWN)
    select_box.send_keys(Keys.RETURN)
    sleep(3)
    for fYear in Date.keys():
        select_box = driver.find_element_by_xpath("//div[@id='divAumYear']/span/input")
        select_box.clear()
        select_box.send_keys(fYear)
        select_box.send_keys(Keys.DOWN)
#         select_box.send_keys(Keys.DOWN)
        select_box.send_keys(Keys.RETURN)
        sleep(3)
        for fQuarter in Date[fYear]:
            select_box = driver.find_element_by_xpath("//div[@id='divAumQuarter']/span/input")
            select_box.clear()
            select_box.send_keys(fQuarter)
            select_box.send_keys(Keys.DOWN)
#             select_box.send_keys(Keys.DOWN)
            select_box.send_keys(Keys.RETURN)
            sleep(3)
            go = driver.find_element_by_xpath("//a[@id='hrfGo']")
            go.click()
            sleep(3)
            dl = driver.find_element_by_xpath("//input[@title='Excel']")
            dl.click()
            sleep(1)
sleep(10)
driver.close()

