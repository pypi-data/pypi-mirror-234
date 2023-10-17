from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml

class SanminUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('www\.sanmin\.com\.tw\/.+', url)
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        '''# ---- 下載response回來 ----
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
        headers = {
            'User-Agent': user_agent, 
            'referer':'https://www.sanmin.com.tw',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,en;q=0.9',
            'Pragma': 'no-cache'
        }
        res = requests.get(url, headers=headers)'''
        pure_html = res.text
        soup = BeautifulSoup(pure_html,features="lxml")

        # ---- 取下整頁的urls ----
        #prd_urls = [(('https://www.sanmin.com.tw' + u['href']) if 'sanmin.com' not in u['href'] else u['href']) for u in soup.select('div.ProductView div.resultBooks div.resultBooksInfor h3 > a')]
        prd_urls = []
        items = soup.select('div.ProductView div.Info')
        for item in items:
            u=item.select_one('h3 > a')
            p = item.select_one('span.Price')
            price = 0
            if p:
                price = p.text.replace(',', '')
            prd_urls.append({'url': (('https://www.sanmin.com.tw' + u['href']) if 'sanmin.com' not in u['href'] else u['href']), 
                           'price':int(price)})

        # ---- 檢查是否最後一頁，有則回填url ----
        '''# 使用自訂參數pi(當前頁)及fp(最終頁)
        fpg = 0
        match = re.search('\&fp=(\d+)?', url.lower())
        if match:
            fpg = match.group(1) if match.group(1) else 0
        '''

        cpg = 1
        match = re.search('\&pi=(\d+)?', url.lower())
        if match:
            cpg = match.group(1) if match.group(1) else 0

        if prd_urls:
            npg = int(cpg) + 1
            self._next_pg_url = url.replace(f'&pi={cpg}', '') + f'&pi={npg}'
        else:
            self._next_pg_url = None

        return prd_urls
        
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    