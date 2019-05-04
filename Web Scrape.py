
from selenium import webdriver
import urllib.request
import time
from bs4 import BeautifulSoup



#Connect to the 
driver = webdriver.Chrome()
driver.get('http://disclosures.house.gov/ld/ldsearch.aspx')
driver.find_element_by_xpath('//*[@id="DropDownList1"]').send_keys('Lobbyist Covered')
driver.find_element_by_xpath('//*[@id="DropDownList10"]').send_keys('True')
driver.find_element_by_xpath('//*[@id="DropDownList4"]').send_keys('Filing Year')
driver.find_element_by_xpath('//*[@id="DropDownList40"]').send_keys('2018')
driver.find_element_by_xpath('//*[@id="DropDownList2"]').send_keys('Filing Type')
driver.find_element_by_xpath('//*[@id="DropDownList20"]').send_keys('Registration')
driver.find_element_by_xpath('//*[@id="DropDownList5"]').send_keys('Issue Data')
driver.find_element_by_xpath('//*[@id="DropDownList3"]').send_keys('Lobbyist Covered Position')
submit_button = driver.find_element_by_xpath('//*[@id="cmdSearch"]')
submit_button.click()

element = driver.find_element_by_id("lblPageCounter")

current_page = int(element.text.split()[1])
last_page = int(element.text.split()[3])


counter = 0
for x in range(last_page):
    next_page_button = driver.find_element_by_xpath('//*[@id="btnNext"]')
    soup=BeautifulSoup(driver.page_source,'html.parser')
    url_list = []
    for i in range(len(soup.findAll('a'))): #'a' tags are for links
        one_a_tag = soup.findAll('a')[i]
        l = one_a_tag['href']
        if 'pdfform' in l:
            link = l
            file=link[-9:]
            url = 'http://disclosures.house.gov/ld/ldxmlrelease/2018/RR/'+ file + ".xml"
            result=urllib.request.urlretrieve(url,'./'+file[file.find(file)+1:])
            time.sleep(5)
    next_page_button.click()
    counter += 1
    print(counter)
    
