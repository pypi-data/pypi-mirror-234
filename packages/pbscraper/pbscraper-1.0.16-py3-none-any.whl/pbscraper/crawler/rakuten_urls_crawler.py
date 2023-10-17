from .base_urls_crawler import BaseUrlsCrawler

import requests
from bs4 import BeautifulSoup
import re
import datetime
import lxml

class RakutenUrlsCrawler(BaseUrlsCrawler):
    def __init__(self):
        pass
        
    def is_target_list(self, url):
        is_list = False
        match = re.search('www\.rakuten\.com\.tw\/shop\/rbook\/category\/.+', url.lower())
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
        pure_html = res.text
        soup = BeautifulSoup(pure_html,features="lxml")

        # ---- 取下整頁的urls ----
        #prd_urls = ['https://www.rakuten.com.tw' + u['href'] for u in soup.select('div.b-text a.product-name')]
        prd_urls = []
        for item in soup.select('li.b-item div.b-text'):
            if 'b-content' not in item.attrs['class']:
                u=item.select_one('a.product-name')
                #print(item.select_one('span.b-text-prime'))
                p=item.select_one('span.b-text-prime').text.replace(',','')
                prd_urls.append({'url': 'https://www.rakuten.com.tw' + u['href'], 
                               'price':int(p)})

        # ---- 檢查有無下一頁，有則回填url ----
        elem = soup.select_one('div.b-tabs-utility')
        if elem:
            cr = 1
            match = re.search('- 第 (\d+)? 筆，', elem.text)
            if match:
                cr = match.group(1) if match.group(1) else 1
            lr = 1
            match = re.search('，共 (\d+)? 筆', elem.text)
            if match:
                lr = match.group(1) if match.group(1) else 1

            is_last_pg = int(cr) >= int(lr)
            is_redirected = False
            if res.history:
                is_redirected = True
            if not is_redirected and not is_last_pg and prd_urls:
                # 取得目前頁數
                cpg = 1
                match = re.search('.+\?.*p=(\d+)?', url.lower())
                if match:
                    cpg = match.group(1) if match.group(1) else 1

                npg = str(int(cpg) + 1)
                para_npg = f'?p={npg}'
                para_cpg = f'?p={cpg}'
                if int(cpg) > 1:
                    self._next_pg_url = url.replace(para_cpg, para_npg)
                else:
                    self._next_pg_url = f'{url}{para_npg}'
        else:
            self._next_pg_url = None

        return prd_urls

 
    def get_next_pg_after_scraped(self):
        return self._next_pg_url
        
        
    