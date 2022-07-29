import urllib.request
import http.client
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import bs4
import cfscrape
# use selenium to get pages
driver=webdriver.Chrome()
def get_thesaurus(str):
    if ' ' in str:
        driver.get('https://www.collinsdictionary.com/zh/dictionary/english-thesaurus/')
        driver.find_element(By.NAME,'q').send_keys(str)
        driver.find_element(By.NAME,'q').send_keys('\n')
        #driver.get(driver.current_url)
        # get the html of the page
        html=driver.page_source
    else:
        scraper = cfscrape.create_scraper()
        html = scraper.get('https://www.collinsdictionary.com/zh/dictionary/english-thesaurus/'+str).content
    #print(html)
    # use bs4 to parse the html
    soup=bs4.BeautifulSoup(html,'html.parser')
    # get the div with class 'definition'
    words=soup.find_all('span',{"class":"orth"})
    # get the text of the div
    answer=''
    for i in range(0,min(len(words),15)):
        answer=answer+words[i].text+','
    # print the text
    # print(answer)
    # close the browser
    return answer

#print(get_thesaurus("Related to"))