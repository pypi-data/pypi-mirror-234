from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml
import json

class CavesUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('www\.cavesbooks\.com\.tw\/.+', url.lower())
        if match:
            is_list = True
        return is_list

    def scrape_list_to_urls(self, url, res):
        pg = 1
        shopid = ''
        match = re.search('.+shopID\=(\w+)?', url)
        if match:
            shopid = match.group(1) if match.group(1) else ''
        match = re.search('.+\?page\=(\d+)?', url)
        if match:
            pg = int(match.group(1) if match.group(1) else 1)
            
        pure_html = res.text
        json_data = json.loads(pure_html)
        if 'GoodsList' not in json_data:
            return []

        # ---- 取下整頁的urls ----
        #prd_urls = [f'https://www.cavesbooks.com.tw/EC/Books_Prod_Content.aspx?SHOPID={shopid}&GID=' + item['GoodsID'] for item in json_data['GoodsList']]
        prd_urls = []
        for item in json_data['GoodsList']:
            prd_urls.append({'url': f'https://www.cavesbooks.com.tw/EC/Books_Prod_Content.aspx?SHOPID={shopid}&GID={item["GoodsID"]}', 
                           'price': item["Price"]})

        # ---- 檢查有無下一頁，有則回填url ----
        if prd_urls:
            pg += 1
            nexturl = f'https://www.cavesbooks.com.tw/api/Books_Category_List?page={pg}&per_page=8&shopID={shopid}&sortType=name'
            #print(nexturl)
            self._next_pg_url = nexturl
        else:
            #print('no next url')
            self._next_pg_url = None

        return prd_urls
 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    