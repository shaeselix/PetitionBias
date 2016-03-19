from selenium import webdriver
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
import re
import collections
import pandas as pd
import numpy as np

class ChangeScraper(object):
    
    def __init__(self):
        
        self.driver = webdriver.Chrome()
        self.driver.get('https://change.org/')
        self.df = pd.DataFrame(columns = ['ID',
                                          'Link',
                                          'Title',
                                          'Sponsor',
                                          'Description',
                                          'Petitioning',
                                         'Letter',
                                         'Signatures',
                                         'Victory'])
        self.dflen = 0
        
    def Search(self, query, auto = False):
        
        qurl = 'https://www.change.org/search?q=' + quote_plus(query)
        self.driver.get(qurl)
        resultstext = self.driver.find_element_by_xpath(
            '//div[@class="search-results"]/strong[@class="mhxs"]').text
        print('"%s": %s' % (query, resultstext))
        if resultstext == 'No results found':
            return
        if not auto:
            cont = input('Continue? (y/n): ')
            if cont != 'y':
                return
        nresults = int(resultstext[:-8])
        for pg in range(0,nresults,10):
            
            self.driver.get(qurl + '&offset=' + str(pg))
            
            results = self.driver.find_elements_by_xpath('//div[@class="search-result"]/a')
            
            for e in results:
                
                self.df.loc[self.dflen] = self.Parse(e.get_attribute('href'))
                self.dflen += 1
                if self.dflen % 100 == 0:
                    print('%s done out of %s' % (self.dflen, nresults))
                
        self.driver.close()
                               
    def Parse(self, link):
        
        r = requests.get(link)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        title = soup.find("h1").string
        
        cidre = re.search('[0-9]+',str(soup.find("div", "emergency_banner")))
        
        if cidre:
            ID = int(cidre.group(0))
            
        else:
            ID = np.nan
            
        sponsor = soup.find('strong', 'link-subtle').string
        
        description = soup.find('div', 'rte js-description-content').get_text(' ')
        
        petitioning = soup.find('span', 'link-stealth link').string
        
        lsoup = soup.find('div', "modal-dialog animate animate-zoom-in modal-medium")
        
        if lsoup:
            letter = lsoup.find('p').get_text(' ')
        else:
            letter = ''
        
        signatures = np.nan
        
        victory = 0

        sigtext = soup.find('div', 'js-sign-and-share-components').get_text()
        
        if sigtext:
            if sigtext[0:7] == 'Victory':
                victory = 1
            sigre = re.search('[0-9,]+',sigtext)
            if sigre:
                signatures = int(sigre.group(0).replace(',',''))
            
        return([ID, link, title, sponsor, description, petitioning, letter, signatures, victory])
        
        
            