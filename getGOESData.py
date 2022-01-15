# -*- coding: utf-8 -*-
"""
A Basic webscraping script to get a list of GOES satellite data csv files from the website
years = ['1974','2020','1981'] can be used to get only spesific years or if the list is empty all csv files are listed
No error handling is implemented as this is a one time use script. All errors were handled manually.
List of files is written into a csv file named results='???'
"""

from bs4 import BeautifulSoup
import requests
import csv

toppage = 'https://satdat.ngdc.noaa.gov/sem/goes/data/full/'
years =[]
results='listoffiles.csv'

csvfiles = []
   
def grabSubPage(linkUrl):
    i = 0
    source = requests.get(linkUrl).text
    subpage = BeautifulSoup(source, 'lxml')
    rows = subpage.find_all('tr')
    for row in rows:
        if row.td:
            if row.td.a:
                clink = row.td.a.get('href')
                if clink[-1]=='/' and clink[0:4]!='/sem' and clink[0:4]!='http':
                    print("Now getting "+linkUrl+clink)
                    grabSubPage(linkUrl+clink)
                elif clink[-4:]=='.csv':
                    #print('CSV File :'+linkUrl+clink)
                    i += 1
                    csvfiles.append([i, linkUrl+clink, clink])

source = requests.get(toppage).text
soup = BeautifulSoup (source,'lxml')

rows = soup.find_all('tr')
for row in rows:
    if row.td:
        if row.td.a:
            if row.td.a.text[0:4] in years or len(years)==0:
                link = row.td.a.get('href')
                linkUrl = toppage + link
                print("Now getting " + linkUrl)
                grabSubPage(linkUrl)
                
with open (results,'w',newline='') as f:
    write = csv.writer(f)
    write.writerows(csvfiles)