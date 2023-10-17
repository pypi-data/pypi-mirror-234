from .base_parser import BaseParser
import requests
from bs4 import BeautifulSoup
import re
import datetime
import time
import logging
from ..common.utility import utility
from requests.adapters import HTTPAdapter
requests.adapters.DEFAULT_RETRIES = 0
import html

class EsliteParser(BaseParser):
    def __init__(self):
        self._ecid = 4
        self._ecpid = None
    def get_ec_popidx(self):
        return 90
    def is_target_page(self, url):
        is_book = False
        ecpid = None
        #match = re.search('www\.eslite\.com\/product\/(\w+)?', url.lower())
        # 改讀API https://athena.eslite.com/api/v1/products/10012168942682440818001
        match = re.search('athena\.eslite\.com\/api\/v1\/products\/(\w+)?', url.lower())
        if match:
            ecpid = match.group(1) if match.group(1) else None
        if ecpid:
            self._ecpid = ecpid
            is_book = True
        return is_book

    def scrape_page_to_strprd(self, url, res):
        '''# ---- 下載response回來 ----
        reqss = requests.Session()
        reqss.mount('https://', HTTPAdapter(max_retries=0))
        user_agent = utility.gen_random_useragent()
        headers = utility.gen_spider_headers(user_agent, referer='http://www.eslite.com/')
        res = reqss.get(url, headers=headers, timeout=10)'''
        if res.status_code == 404:
            print('-- 商品已下架? 404找不到商品頁') 
            return None
        if res.status_code != 200:
            raise ValueError(f'-- status_code is {res.status_code}')
        #pure_html = res.text
        pure_data = res.json()
        res.connection.close()
        # ---- 準備剖析html ----
        popIdx = self.get_ec_popidx()
        prd = {}
        #soup = BeautifulSoup(pure_html,features="lxml")
        soup = pure_data
        is_onshelf = self._extract_if_onshelf(soup)
        #if is_onshelf == 1: 
        # ---- step1 商品頁可取得的資訊 ----
        prd['Name'] = self._extract_name(soup)
        prd['Url'] = self._extract_url(soup)
        prd['ImgUrl'] = self._extract_imgurl(soup)
        prd['ImgUrlList'] = self._extract_imgurl_list(soup) if self._extract_imgurl_list(soup) else prd['ImgUrl']
        prd['VideoUrl'] = None
        prd['VideoUrlList'] = None
        prd['OriPrice'] = self._extract_oriprice(soup)
        prd['Price'] = self._extract_price(soup)
        prd['Author'] = self._extract_author(soup)
        prd['ISBN'] = self._extract_isbn(soup)
        prd['ECID'] = self._ecid
        prd['ECPID'] = self._extract_ecpid_by_url(url)
        prd['ECCatlog'] = self._extract_eccatlog(soup) 
        prd['isOnShelf'] = is_onshelf
        
        prd['isEnable'] = True # esc index v2是用boolean
        prd['Desc'] = self._extract_desc(soup)
        prd['ModifyTime'] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        prd['CreateTime'] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        prd['PopIdx'] = popIdx
        prd['CatID'] = None
        prd['Translator'] = self._extract_translator(soup)
        prd['PublishDate'] = self._extract_pub_date(soup)
        
        prd['Publisher'] = self._extract_publisher(soup) # esc index v2改名為publishcompany->publisher
        prd['Painter'] = self._extract_painter(soup)
        prd['OriginName'] = self._extract_origin_name(soup)
        prd['Summary'] = self._extract_summary(soup)
        prd['ISBN10'] = self._extract_isbn10(soup)
        prd['ISBNADD'] = self._extract_isbnadd(soup)
        prd['BookType'] = self._extract_booktype(soup, prd)
        prd['Text1'] = None
        prd['Text2'] = None
        prd['Text3'] = None
        prd['Keyword1'] = None
        prd['Keyword2'] = None
        prd['Keyword3'] = None
            
        # ---- step2 特殊處理的資訊 ----
        # 沒有原價的商品:https://www.kingstone.com.tw/basics/basics.asp?kmcode=2019920474639&lid=book_class_sec_se&actid=WISE
        if prd['OriPrice'] is None:
            prd['OriPrice'] = prd['Price']
        
        return prd

        #else:
        #    print('-- 商品已下架? 找不到購物車鈕') 
        #    return None #回傳None則在main_parser下架商品

    # ======== 私有 萃取各值的方法 ========
    def _extract_if_onshelf(self, soup):
        val = 1 if soup['stock'] > 0 else 0
        return val
    
    def _extract_name(self, soup):
        val = soup['name']
        return val
    
    def _extract_url(self, soup):
        val = f'https://www.eslite.com/product/{soup["product_guid"]}'
        return val
    
    def _extract_imgurl(self, soup):
        val = None
        if soup['photos']:
            val = soup['photos'][0]['medium_path']
        return val
    
    def _extract_imgurl_list(self, soup):
        val = ','.join([item['medium_path'] for item in soup['photos']])
        return val #已測試若沒有為''

    def _extract_ecpid_by_url(self, url):
        val = self._ecpid
        return val

    def _extract_eccatlog(self, soup):
        val = None #json只有回傳代號
        return val

    def _extract_author(self, soup):
        val = soup['author']
        return val

    def _extract_isbn(self, soup):
        val = soup['ean']
        return val

    def _extract_desc(self, soup):
        val = None
        if soup['short_description']:
            val = html.escape(soup['short_description'])[:8000]
        return val

    def _extract_translator(self, soup):
        val = soup['translator']
        return val

    def _extract_pub_date(self, soup):
        val = soup['manufacturer_date']
        if val:
            val = val[:10].replace('-', '/')
        return val

    def _extract_publisher(self, soup):
        val = soup['supplier']
        return val

    def _extract_oriprice(self, soup):
        val = soup['final_price']
        return val

    def _extract_price(self, soup):
        val = int(soup['retail_price'])
        return val

    # ---- esc index v2 ---- 
    def _extract_painter(self, soup):
        val = soup['painter']
        return val
    def _extract_origin_name(self, soup):
        val = soup['original_name']
        return val  
    def _extract_summary(self, soup):
        val = soup['sub_title']
        return val
    def _extract_isbn10(self, soup):
        val = soup['isbn10']
        return val
    def _extract_isbnadd(self, soup):
        val = soup['isbn13']
        return val
    
    def _extract_booktype(self, soup, prd):
        book_type = 'book'
        #book_type = 'ebook'
        return book_type
    
    