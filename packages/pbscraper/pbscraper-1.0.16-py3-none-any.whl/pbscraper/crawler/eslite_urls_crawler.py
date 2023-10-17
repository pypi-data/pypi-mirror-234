from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml

class EsliteUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        #match = re.search('www\.eslite\.com\/category\/.+', url.lower())
        # 列表頁改讀API https://athena.eslite.com/api/v2/search?final_price=0,&sort=manufacturer_date+desc&size=40&start=0&status=add_to_shopping_cart&categories=[%2281%22]
        match = re.search('athena\.eslite\.com\/api\/v2\/search?.+', url.lower())
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        pure_data = res.json()

        # ---- 取下整頁的urls ----
        prd_urls = []
        for item in pure_data['hits']['hit']:
            #https://athena.eslite.com/api/v2/search?final_price=0,&sort=manufacturer_date+desc&size=40&start=0&status=add_to_shopping_cart&categories=[%2281%22]
            #https://athena.eslite.com/api/v2/search?final_price=0,&sort=manufacturer_date+desc&size=40&start=1&status=add_to_shopping_cart&categories=[%2281%22]
            # 商品頁改讀API https://athena.eslite.com/api/v1/products/10012168942682440818001
            prd_urls.append({'url': f'https://athena.eslite.com/api/v1/products/{item["id"]}', 
                           'price':int(item['fields']['final_price'])})

        # ---- 檢查有無下一頁，有則回填url ----
        if len(prd_urls) > 0:
            match = re.search('athena\.eslite\.com\/api\/v2\/search?.+&start=(\d+?)&.+', url.lower())
            if match:
                old_idx_page = int(match.group(1))
                new_idx_page = old_idx_page + 1
                self._next_pg_url = url.replace(f'&start={old_idx_page}', f'&start={new_idx_page}')
            else:
                self._next_pg_url = None

        return prd_urls
 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    