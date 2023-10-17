from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml
import json

class YahooUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('tw\.buy\.yahoo\.com\/category\/.+', url.lower())
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        '''# ---- 下載response回來 ----
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
        headers = {
            'User-Agent': user_agent, 
            'referer':'https://tw.buy.yahoo.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,en;q=0.9',
            'Pragma': 'no-cache'
        }
        res = requests.get(url, headers=headers)'''
        pure_html = res.text
        soup = BeautifulSoup(pure_html,features="lxml")

        # ---- 取下整頁的urls ----
        elem = soup.select_one('div#isoredux-data')
        val = json.loads(elem['data-state'])
        items = val['search']['ecsearch']['hits']
        #prd_urls = [ 'https://tw.buy.yahoo.com/gdsale/gdbksale.asp?gdid=' + item['ec_productid'] if 'ec_gd_type_new' in item and item['ec_gd_type_new'] == '3' else 'https://tw.buy.yahoo.com/gdsale/gdsale.asp?gdid=' + item['ec_productid'] for item in items]
        prd_urls = []
        for item in items:
            prd_urls.append({'url': 'https://tw.buy.yahoo.com/gdsale/gdbksale.asp?gdid=' + item['ec_productid'] if 'ec_gd_type_new' in item and item['ec_gd_type_new'] == '3' else 'https://tw.buy.yahoo.com/gdsale/gdsale.asp?gdid=' + item['ec_productid'], 
                           'price':int(float(item['ec_price']))})
    
        # ---- 檢查有無下一頁，有則回填url ----
        btn_right = soup.select_one('a.Pagination__icoArrowRight___2KprV')
        if btn_right and 'Pagination__icoArrowRightDisabled___1s37n' not in btn_right.get('class'):
            purl = btn_right['href']
            self._next_pg_url = f'https://tw.buy.yahoo.com/category/{purl}'
        else:
            self._next_pg_url = None
        
        return prd_urls

 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    