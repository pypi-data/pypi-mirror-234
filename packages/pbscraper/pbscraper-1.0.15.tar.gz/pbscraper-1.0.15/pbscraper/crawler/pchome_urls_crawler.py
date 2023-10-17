from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml
from requests_html import HTMLSession

class PchomeUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('24h\.pchome\.com\.tw\/books\/store\/.+', url.lower())
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        # ---- 下載response回來 ---- pchome需等js載完才會有商品資料
        session = HTMLSession(browser_args=["--no-sandbox", "--user-agent='Testing'"])
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
        headers = {
                'User-Agent': user_agent, 
                'referer':'https://24h.pchome.com.tw',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-TW,en;q=0.9',
                'Pragma': 'no-cache'
            }
        r = session.get('https://24h.pchome.com.tw/books/store/DJAK2V?p=16', headers=headers)
        r.html.render()

        # ---- 取下整頁的urls ----
        hrefs = r.html.xpath('//dl[contains(@id,"ProdGridContainer")]//h5[contains(@class, "prod_name")]/a/@href')
        prd_urls = [(('https:' + u) if 'htts:' not in u else u) for u in hrefs]
        #print(prd_urls)

        # ---- 檢查有無下一頁，有則回填url ----
        next_url = r.html.xpath('//li[contains(@class, "sp")]/a[text()="下一頁>"]/@href')
        if next_url:
            self._next_pg_url = ('https://24h.pchome.com.tw' + next_url[0]) if '24h.pchome.com.tw' not in next_url[0] else next_url[0]
        else:
            self._next_pg_url = None

        return prd_urls
 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    