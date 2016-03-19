from selenium import webdriver
from urllib.parse import quote_plus

class ChangeScraper(object):
    
    def __init__(self):
        
        self.driver = webdriver.Chrome()
        self.driver.get('https://change.org/')
        
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
                
                print(e.get_attribute('href'))