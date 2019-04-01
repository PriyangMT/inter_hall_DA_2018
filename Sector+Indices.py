'''
This code is used to scrape data of NIFTY index.
'''
# coding: utf-8

# In[87]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import wget
import pandas as pd
from bs4 import BeautifulSoup

#capa = DesiredCapabilities.FIREFOX
#capa["pageLoadStrategy"] = "none"

driver = webdriver.Chrome()

indices = ["NIFTY Auto", "NIFTY Bank", "NIFTY Financial Services", "NIFTY FMCG", "NIFTY IT", "NIFTY Media",
           "NIFTY Metal", "NIFTY Pharma", "NIFTY Private Bank", "NIFTY PSU Bank", "NIFTY Realty"]


# In[88]:


driver.get("https://www.nseindia.com/products/content/equities/indices/historical_index_data.htm")


# In[89]:


for index in indices:
    select_box = driver.find_element_by_name("indexType")
    for option in select_box.find_elements_by_tag_name('option'):
        if (option.text == index):
            option.click()
            break
    for i in range(3,6):
        select_box = driver.find_element_by_id("fromDate")
        select_box.clear()
        select_box.send_keys("01-01-201" + str(i))
        select_box = driver.find_element_by_id("toDate")
        select_box.clear()
        select_box.send_keys("31-12-201" + str(i))

        get = driver.find_element_by_id("get")
        get.click()
        sleep(2)
        dl_link = driver.find_element_by_xpath("//span[@class='download-data-link']/a")
        sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.5)
        dl_link.click()
#        wget.download(dl_link.get_attribute("href"))
        sleep(5)
    for i in range(6,7):
        select_box = driver.find_element_by_id("fromDate")
        select_box.clear()
        select_box.send_keys("01-01-201" + str(i))
        select_box = driver.find_element_by_id("toDate")
        select_box.clear()
        select_box.send_keys("30-12-201" + str(i))

        get = driver.find_element_by_id("get")
        get.click()
        sleep(2)
        dl_link = driver.find_element_by_xpath("//span[@class='download-data-link']/a")
        sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.5)
        dl_link.click()
#        wget.download(dl_link.get_attribute("href"))
        sleep(5)
    for i in range(7,8):
        select_box = driver.find_element_by_id("fromDate")
        select_box.clear()
        select_box.send_keys("01-01-201" + str(i))
        select_box = driver.find_element_by_id("toDate")
        select_box.clear()
        select_box.send_keys("31-12-201" + str(i))

        get = driver.find_element_by_id("get")
        get.click()
        sleep(2)
        dl_link = driver.find_element_by_xpath("//span[@class='download-data-link']/a")
        sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.5)
        dl_link.click()
#        wget.download(dl_link.get_attribute("href"))
        sleep(5)

