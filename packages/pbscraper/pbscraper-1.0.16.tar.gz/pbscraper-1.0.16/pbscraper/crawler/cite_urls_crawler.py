from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml
import json
from requests.adapters import HTTPAdapter

class CiteUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('www\.cite\.com\.tw\/', url.lower())
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        '''# ---- 下載response回來 ----
        reqss = requests.Session()
        reqss.mount('https://', HTTPAdapter(max_retries=0))
        user_agent = utility.gen_random_useragent()
        headers = utility.gen_spider_headers(user_agent, referer='https://www.cite.com.tw')
        res = reqss.get(url, headers=headers, timeout=60)'''
        #res.encoding = 'big5' #cite要加此行才會顯示中文
        pure_html = res.text
        soup = BeautifulSoup(pure_html,features="html.parser",from_encoding='utf-8') #cite要加此行才會顯示中文

        # ---- 取下整頁的urls ----
        #elems = soup.select('div.book_3 div.item div.photo > a')
        #prd_urls = ['https://www.cite.com.tw' + a['href'] for a in elems]
        prd_urls = []
        for item in soup.select('div[class^=book_] div.item'):
            u='https://www.cite.com.tw' + item.select_one('div.photo > a')['href']
            match = re.search('[^\d]*(\d+)?元', item.select_one('div.b_price').text)
            p=''
            if match:
                p = match.group(1) if match.group(1) else None
            prd_urls.append({'url': u, 
                           'price':int(p)})

        # ---- 檢查有無下一頁，有則回填url ----
        elem = soup.select_one('a.pageNext')
        if elem:
            self._next_pg_url = 'https://www.cite.com.tw' + elem['href']
        else:
            self._next_pg_url = None

        return prd_urls

 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    