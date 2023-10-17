from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml

class UdnUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('shopping\.udn\.com\/mall\/cus\/cat\/cc1c01.do.+', url.lower())
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        '''# ---- 下載response回來 ----
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
        headers = {
            'User-Agent': user_agent, 
            'referer':'https://shopping.udn.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,en;q=0.9',
            'Pragma': 'no-cache'
        }
        res = requests.get(url, headers=headers)'''
        pure_html = res.text
        soup = BeautifulSoup(pure_html,features="lxml")

        # ---- 取下整頁的urls ----
        prd_urls = []
        items = soup.select('li.lv3_item div.caption p.pd_name a')
        if not items:
            items = soup.select('li.demand_pd div.caption p.pd_name a') #第2種頁面
        for item in items:
            u='https://shopping.udn.com/mall/cus/cat/Cc1c02.do?dc_cargxuid_0=' + item['data-pdid']
            p=item['data-price'].replace(',', '')
            prd_urls.append({'url': u, 
                           'price':int(p)})

        #if not prd_urls:
        #    raise ValueError('prd_urls 不應該沒商品')

        # ---- 檢查有無下一頁，有則回填url ----
        elem = soup.find('a', title=re.compile(r'下一頁'))
        if elem:
            # 取得目前頁數
            cpg = 1
            match = re.search('.+\?.*dc_page_0=(\d+)?', url.lower())
            if match:
                cpg = match.group(1) if match.group(1) else 1
            npg = int(cpg) + 1    
            para_npg = f'&dc_page_0={npg}'
            para_cpg = f'&dc_page_0={cpg}'
            if int(cpg) > 1:
                self._next_pg_url = url.replace(para_cpg, para_npg)
            else:
                self._next_pg_url = f'{url}{para_npg}'
        else:
            self._next_pg_url = None

        return prd_urls

 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    