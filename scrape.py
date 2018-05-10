'''
A script that scrapes the html files and stores them in 'data' directory.

author:-Shradha Nayak,Ankita Sawant,Vandna Yadav
'''
import urllib2,os,sys,time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys

#making a directory function
def makeDirec(loc):
    if not os.path.exists(loc):os.mkdir(loc)
def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None
def scrapePage():
    #making a directory data for all raw data
    makeDirec('data')
    #scrape the page with all users
    url='https://www.goodreads.com/user/best_reviewers'
    #open the browser and visit the url
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    html=driver.page_source
    time.sleep(2)
    cssPath='a.gr-button.gr-button--dark'
    page=1
    try:
        button=driver.find_element_by_css_selector(cssPath)
    except:
        error_type, error_obj, error_info = sys.exc_info()
        print 'STOPPING - COULD NOT FIND THE LINK TO PAGE: ', page
        print error_type, 'Line:', error_info.tb_lineno

    time.sleep(2)
    button.click()
    html1=driver.page_source
    #############################################
    #passing login details since the source was unable to retrieve in chrome web-driver
    wait = ui.WebDriverWait(driver, 3)
    wait.until(page_is_loaded)
    email_field = driver.find_element_by_id("user_email")
    email_field.send_keys("anki.sawant@gmail.com")
    password_field = driver.find_element_by_id("user_password")
    password_field.send_keys("shardavijay")
    password_field.submit()
    time.sleep(2)
    #############################################
    html2=driver.page_source
    html3=html2.encode('utf-8')
    #writing the file
    fwriter=open('data/user_list.html','w')
    fwriter.write(html3)
    fwriter.close()
    time.sleep(2)
scrapePage()



