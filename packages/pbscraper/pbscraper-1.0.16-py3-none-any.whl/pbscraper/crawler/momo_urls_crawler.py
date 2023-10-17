from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml

class MomoUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('momoshop\.com\.tw\/.+', url.lower())
        if match:
            is_list = True
        return is_list
    
    def scrape_list_to_urls(self, url, res):
        '''# ---- 下載response回來 ----
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
        headers = {
           'User-Agent': user_agent, 
           'referer':'https://www.google.com',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh-TW,en;q=0.9',
           'Pragma': 'no-cache'
        }
        res = requests.get(url, headers=headers)'''
        pure_html = res.text
        soup = BeautifulSoup(pure_html,features="lxml")

        # ---- 取下整頁的urls ----
        #prd_urls = ['https://m.momoshop.com.tw/goods.momo?i_code=' + u['value'] for u in soup.select('article.prdListArea ul > li > input#goodsCode')]
        prd_urls = []
        for item in soup.select('article.prdListArea ul > li'):
            u=item.select_one('input#goodsCode')
            p=item.select_one('p.priceArea b.price').text.replace(',','')
            prd_urls.append({'url': 'https://m.momoshop.com.tw/goods.momo?i_code=' + u['value'], 
                           'price':int(p)})

        # ---- 檢查有無下一頁，有則回填url ----
        elem = soup.select_one('div.pageArea')
        if elem and prd_urls:
            cpg = elem.select_one('dd.selected a').text
            lpg = elem.select('dd a')[-1].text
            if cpg == lpg:
                self._next_pg_url = None
            else:
                npg = str(int(cpg) + 1)
                para_npg = f'&page={npg}'
                para_cpg = f'&page={cpg}'
                if para_cpg in url:
                    self._next_pg_url = url.replace(para_cpg, para_npg)
                else:
                    self._next_pg_url = f'{url}{para_npg}'
        else:
            self._next_pg_url = None

        return prd_urls
 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    