#!/usr/bin/env python
# coding: utf-8

# # Product_URL

# In[1]:


# import requests
# from bs4 import BeautifulSoup
# import time
# import urllib.request
# from selenium.webdriver import Chrome
# from selenium import webdriver
# import re     
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# import datetime as dt
# import pandas as pd


# In[20]:


def getNike(url):
    browser = webdriver.Chrome("C:/Users/kjh96/OneDrive/Desktop/Github/duck9967/ETC/chromedriver.exe") 
    url = url

    browser.get(url)  
    browser.maximize_window()
    browser.implicitly_wait(1)

    # 페이지 스크롤 - 스크롤 내려서 전체 동영상 목록 가져오기(예시 20번)
    body = browser.find_element_by_tag_name('body') # 스크롤하기 위해 소스 추출
    num_of_pagedowns = 30

    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        browser.implicitly_wait(1)
        num_of_pagedowns -= 1

    # html로 파싱
    url = browser.page_source
    html = BeautifulSoup(url,'html.parser')
    link = html.find_all('a',{'class':'a-product-image-link'})
    # print(link[0].find('img')['alt'])
    # print(link[0]["href"])
    # print(len(link))

    link_list = []
    title_list =  []
    for i in range(len(link)) :
        tltle = link[i].find('img')['alt']
        url= link[i]["href"]

        link_list.append(url)
        title_list.append(tltle)
        
    df = pd.DataFrame({"title" : title_list, "url" : link_list})
    print(df.shape)


# In[ ]:


# getNike("https://www.nike.com/kr/ko_kr/w/men/fw")


# In[ ]:


# get_ipython().system('jupyter nbconvert --to script Nike_crawl2.ipynb')

