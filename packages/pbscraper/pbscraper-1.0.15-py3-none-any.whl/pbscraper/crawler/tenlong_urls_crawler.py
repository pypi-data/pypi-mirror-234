from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml
import json

class TenlongUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('www\.tenlong\.com\.tw\/categories\/', url.lower())
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        '''# ---- 下載response回來 ----
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
        headers = {
            'User-Agent': user_agent, 
            'referer':'https://www.tenlong.com.tw',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,en;q=0.9',
            'Pragma': 'no-cache'
        }
        res = requests.get(url, headers=headers)'''
        pure_html = res.text
        soup = BeautifulSoup(pure_html,features="lxml")

        # ---- 取下整頁的urls ----
        prd_urls = []
        for item in soup.select('div.book-list-event div.list-wrapper li.single-book'):
            h = item.select_one('strong.title a')['href']
            st_c = h.find('?')
            val = h[0:st_c]
            u = 'https://www.tenlong.com.tw' + val
            p = re.findall('\$(\d+)?', item.select_one('div.pricing').text.replace(',',''))[-1]
            prd_urls.append({'url': u, 
                           'price':int(p)})

        # ---- 檢查有無下一頁，有則回填url ----
        elem = soup.find('a', text=re.compile(r'下一頁'))
        if elem:
            # 取得目前頁數
            cpg = 1
            match = re.search('.+\?.*page=(\d+)?', url.lower())
            if match:
                cpg = match.group(1) if match.group(1) else 1
            npg = int(cpg) + 1    
            para_npg = f'page={npg}'
            para_cpg = f'page={cpg}'
            if int(cpg) > 1:
                self._next_pg_url = url.replace(para_cpg, para_npg)
            else:
                self._next_pg_url = f'{url}?{para_npg}'
        else:
            self._next_pg_url = None

        return prd_urls

 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    