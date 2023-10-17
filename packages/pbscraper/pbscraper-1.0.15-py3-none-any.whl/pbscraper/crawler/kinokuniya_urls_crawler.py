from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml

class KinokuniyaUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('taiwan\.kinokuniya\.com\/t\/books\/.+', url.lower())
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        '''# ---- 下載response回來 ----
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
        headers = {
            'User-Agent': user_agent, 
            'referer':'https://www.rakuten.com.tw',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,en;q=0.9',
            'Pragma': 'no-cache'
        }
        res = requests.get(url, headers=headers)'''
        res.connection.close()
        pure_html = res.text
        soup = BeautifulSoup(pure_html,features="lxml")

        # ---- 取下整頁的urls ----
        prd_urls = []
        #print(pure_html[:2000])
        for item in soup.select('div#image_or_detail div.box'):
            u=item.select_one('div.inner_box a')
            p=item.select_one('li.price span').text.replace('NT$','').replace(',','').strip()
            prd_urls.append({'url': 'https://taiwan.kinokuniya.com/' + u['href'], 
                            'price':int(p)})

        # ---- 檢查有無下一頁，有則回填url ----
        if prd_urls:
            # 取得目前頁數
            cpg = 1
            match = re.search('.+\?page=(\d+)?', url.lower())
            if match:
                cpg = match.group(1) if match.group(1) else 1

            npg = str(int(cpg) + 1)
            para_npg = f'?page={npg}'
            para_cpg = f'?page={cpg}'

            self._next_pg_url = url.replace(para_cpg, para_npg)
        else:
            self._next_pg_url = None
        
        return prd_urls

 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    