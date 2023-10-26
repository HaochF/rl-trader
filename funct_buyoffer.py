import os
import sys
import pandas as pd
import requests

import csv
import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import re

def get_buy_offers(item, morethan):

    want = item
    want.replace(' ', '%20')
    output = []


    has = "credits" # DONT CHANGE

    url = f'https://www.rl-trades.com/#h0=' + has +  '&w0=' + want
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    delay = 3 # seconds


    htmlL = driver.page_source

    #myElem = WebDriverWait(browser, delay)

    #the_html = driver---somehow----.get_attribute('innerHTML')
    #bs = BeautifulSoup(the_html, 'html.parser')
    #browser = webdriver.Firefox()
    #browser.get("url")
    #delay = 3 # seconds
    #try:
    #   myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
    #    print "Page is ready!"
    #except TimeoutException:
    #    print "Loading took too much time!"


    r = requests.get(f'https://www.rl-trades.com/#h0=' + has +  '&w0=' + want)
    path = 'html.html'
    #time.sleep(5)
    # empty list
    data = []

    # for getting the header from
    # the HTML file
    list_header = []
    soup = BeautifulSoup(htmlL, 'html.parser')#r.text, 'html.parser')#open(path),'html.parser')
    header = soup.find_all("table")[0].find("tr")

    for items in header:
        try:
            list_header.append(items.get_text())
        except:
            continue

    # for getting the data
    HTML_data = soup.find_all("table")[0].find_all("tr")[1:]
    a_href = ""
    for element in HTML_data:
        #print(element)
        sub_data = []

        serch = re.search("(?P<url>https?://[^\s]+)", str(element))#.group("url")#soup.find("a",{"class":"hl"})#.get("href")
        if serch is None:
            a_href = a_href
        else:
            a_href = serch.group("url")
        #if len(a_href) != 0:
        #    sub_data.append(a_href)
        #else:
        #    sub_data.append()
        #print(a_href)
        #sub_data.append(str(a_href)) #doesnt work here for some reason (probably interferring with num tag or sum) mveo 2 bottom
        for sub_element in element:
            try:
                #print(type(sub_element.get_text()))
                sub_data.append(sub_element.get_text())
            except:
                continue
        sub_data.append(str(a_href))
        data.append(sub_data)

    # Storing the data into Pandas
    # DataFrame
    dataFrame = pd.DataFrame(data = data, columns = ['1', '2', '3', '4', '5', '6'])#, '6'])#list_header)

    # Converting Pandas DataFrame
    # into CSV file
    dataFrame.to_csv('data.csv')

    print(want.replace("%20", " "))

    with open('data.csv', mode ='r', encoding="utf8")as file:

        # reading the CSV file
        csvFile = csv.reader(file)

    # displaying the contents of the CSV file

        for line in csvFile:
                #line[1 is websitesmtimes but sometimes not]
                try:
                    if line[1].__eq__('R-L.COM') and has.replace("%20", " ") in line[2] and want.replace("%20", " ") in line[4]:
                        serch1 = re.search(r'\d+', line[2])
                        serch2 = re.search(r'\d+', line[4])
                        if serch1 is not None:
                            crednum = int(serch1.group())
                        else:
                            crednum = 0
                        if serch2 is not None:
                            itemnum = int(serch2.group())
                        else:
                            itemnum = 1
                        if (crednum/itemnum >= morethan or crednum == 0):
                            out = line
                            out[0] = crednum/itemnum
                            output.append(out)
                        #.append(crednum/itemnum)

                    #print(line)
                except Exception:
                    continue

    driver.close()
    return output


