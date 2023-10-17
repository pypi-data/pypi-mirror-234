from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml
import json

class TaazeUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('www\.taaze\.tw\/beta\/viewdataagent.+', url.lower())
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        '''# ---- 下載response回來 ----
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
        headers = {
            'User-Agent': user_agent, 
            'referer':'https://www.taaze.tw',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,en;q=0.9',
            'Pragma': 'no-cache'
        }
        res = requests.get(url, headers=headers)'''
        pure_html = res.text
        json_data = json.loads(pure_html)

        # ---- 取下整頁的urls ----
        #prd_urls = ['https://www.taaze.tw/goods/' + item['prodId'] + '.html' for item in json_data['result1']]
        prd_urls = []
        for item in json_data['result1']:
            prd_urls.append({'url': 'https://www.taaze.tw/goods/' + item['prodId'] + '.html', 
                           'price':int(item['salePrice'])})

        # ---- 檢查有無下一頁，有則回填url ----
        # 取得目前頁數
        #first pge is 0-35
        start = 0
        end = 35
        match = re.search('.+\?.*startnum=(\d+)?', url.lower())
        if match:
            start = match.group(1) if match.group(1) else 0
        match = re.search('.+\?.*endnum=(\d+)?', url.lower())
        if match:
            end = match.group(1) if match.group(1) else 35

        if prd_urls:
            startNum = int(start) + 36
            endNum = startNum + 36 -1
            para_st = f'&startNum={start}'
            para_nst = f'&startNum={startNum}'
            para_ed = f'&endNum={end}'
            para_ned = f'&endNum={endNum}'
            self._next_pg_url = url.replace(para_st, para_nst).replace(para_ed, para_ned)
        else:
            self._next_pg_url = None

        return prd_urls

 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    