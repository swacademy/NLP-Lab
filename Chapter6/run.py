#run.py
from bs4 import BeautifulSoup as bs
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import re
from Tour import TourInfo

#명시적 대기를 위해서
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import time

url = 'http://tour.interpark.com/'
keyword = '미국여행'
mylist = list()

driver = wd.Chrome(executable_path = 'chromedriver.exe')
driver.get(url)
driver.find_element_by_id('SearchGNBText').send_keys(keyword)
driver.find_element_by_css_selector('button.search-btn').click()
#명시적 대기 : 특정 element가 load될 때까지 대기
#암시적 대기 : 일정 시간 대기

try :
    WebDriverWait(driver, 10).until(
        #지정한 요소가 로딩되면 대기 종료
        #<div class = 'oTravelBox' ..>
        ec.presence_of_element_located((By.CLASS_NAME, 
                                                                'oTravelBox'))
    )
except Exception as e :
    print("Exception Occurrance, reason =", e.reason)

#암묵적 대기
driver.implicitly_wait(10)
#time.sleep(10)

driver.find_element_by_css_selector(
    '.oTravelBox > .boxList > .moreBtnWrap > .moreBtn').click()

for page in range(1, 2) :
    #상품명, comment, 가격, 평점, 이미지, 링크(상품상세정보), 기간1, 기간2
    #proTit, proSub, proPrice, proInfo, img, onClick의 주소, proInfo, boxItem
    #<li class="boxItem">
    time.sleep(2)
    boxItems = driver.find_elements_by_css_selector(
        '.oTravelBox > .boxList > .boxItem')

    for box in boxItems :
        price = box.find_element_by_css_selector('strong.proPrice').text
        price = re.sub(r',', '', price.split(' ')[0])
        price = int(price)
        point = box.find_elements_by_css_selector('p.proInfo')[2].text
        period1 = box.find_elements_by_css_selector('p.proInfo')[0].text
        period2 = box.find_elements_by_css_selector('p.proInfo')[1].text
        obj = TourInfo(
            box.find_element_by_css_selector('h5.proTit').text,
            price,
            box.find_element_by_css_selector('p.proSub').text,
            float(point.split(' ')[1]),
            period1.split(':')[1].strip(),
            period2.split(":")[1].strip()
        )    
        mylist.append(obj)

driver.close()

import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test
info = db['TourInfo']
try:
    for mytour in mylist:
        db.info.insert({
            'title' : mytour.title,
            'price' : mytour.price,
            'comment' : mytour.comment,
            'point' : mytour.point,
            'period1' : mytour.period1,
            'period2' : mytour.period2
        })
    print("Success.")
except Exception as e: 
    print('Exception 발생 = ', e)