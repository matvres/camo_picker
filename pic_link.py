import requests  
from bs4 import BeautifulSoup 
import time
import random
from selenium import webdriver


user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'

headers = { 'User-Agent': user_agent_desktop}


def getdata(url):
    l = "https://www.camopedia.org"
    driver = webdriver.PhantomJS()
    driver.get(l + url)
    #print(driver.page_source)
    #p_element = driver.find_element_by_id(id_='intro-text')
    #print(p_element.text)
    #r = requests.get(l + url, headers=headers)  
    return driver.page_source
    
    
file = open("links.txt", "r")
lines = file.readlines()
file.close()



for line in lines:
    htmldata = getdata(line)  
    soup = BeautifulSoup(htmldata, 'html.parser')
    #print(soup)
    country = line.split("=")
    ll = country[1]
    fileimg = open(ll + ".txt", "w+")
    for item in soup.find_all('img'): 
        fileimg.write(item.get('src') + "\n")
        print(item.get('src'))
        time.sleep(1+random.randint(2,6))

    fileimg.close()


    

