from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml

class BooksUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('www\.books\.com\.tw\/web\/.+', url)
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        
        #user_agent = utility.gen_random_useragent()
        #headers = utility.gen_spider_headers(user_agent, referer='https://www.google.com/')
        #res = requests.get(url, headers=headers, timeout=100)
        pure_html = res.text
        soup = BeautifulSoup(pure_html,features="lxml")

        # ---- 取下整頁的urls ----
        #prd_urls = [u['href'] for u in soup.select('div.item div.msg h4 a')]
        prd_urls = []
        for item in soup.select('div.main_wrap div[class*="item"]'):
            u=item.select_one('div.msg h4 a')
            ptext=item.select_one('div.price_box').text.replace(',','')
            match=re.findall(r"[^\d]*(\d+)?元", ptext)
            p=''
            if match:
                p = match[-1]
            prd_urls.append({'url': u['href'], 
                           'price':int(p)})
        
        # ---- 檢查有無下一頁，有則回填url ----
        elem = soup.select_one('div.page a.nxt')
        if elem:
            self._next_pg_url = elem['href']
        else:
            self._next_pg_url = None
        return prd_urls
        
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    