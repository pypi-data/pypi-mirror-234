from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml
import json

class TcsbUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('\.cloudfront\.net\/webapi/shopcategory\/getsalepagelist\/32014\/.+', url.lower())
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        # ---- 下載response回來 ----
        #user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
        #headers = {
        #    'User-Agent': user_agent, 
        #    'referer':'https://www.tcsb.com.tw',
        #    'Accept-Encoding': 'gzip, deflate, br',
        #    'Accept-Language': 'zh-TW,en;q=0.9',
        #    'Pragma': 'no-cache'
        #}
        #res = requests.get(url, headers=headers)
        pure_html = res.text
        json_data = json.loads(pure_html)

        # ---- 取下整頁的urls ----
        #prd_urls = ['https://www.tcsb.com.tw/SalePage/Index/' + str(item['Id']) for item in json_data['Data']['SalePageList']]
        prd_urls = []
        for item in json_data['Data']['SalePageList']:
            prd_urls.append({'url': 'https://www.tcsb.com.tw/SalePage/Index/' + str(item['Id']), 
                           'price':int(item['Price'])})
        
        # ---- 檢查有無下一頁，有則回填url ----
        # 取得目前頁數
        #first pge is 0-60
        start = 0
        pagesize = 60
        match = re.search('.+\?.*startindex=(\d+)?', url.lower())
        if match:
            start = match.group(1) if match.group(1) else 0

        if prd_urls:
            startNum = int(start) + pagesize
            para_st = f'&startIndex={start}'
            para_nst = f'&startIndex={startNum}'
            self._next_pg_url = url.replace(para_st, para_nst)
        else:
            self._next_pg_url = None

        return prd_urls

 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    