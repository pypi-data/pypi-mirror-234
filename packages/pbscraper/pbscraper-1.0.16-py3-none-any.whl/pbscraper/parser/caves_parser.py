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
import json

class CavesParser(BaseParser):
    def __init__(self):
        self._ecid = 7
        self._ecpid = None
    def get_ec_popidx(self):
        return 90
    def is_target_page(self, url):
        is_book = False
        ecpid = None
        match = re.search('www\.cavesbooks\.com\.tw\/ec\/books_prod_content\.aspx\?.*gid=(\w+)?', url.lower())
        if match:
            ecpid = match.group(1) if match.group(1) else None
        if ecpid:
            self._ecpid = ecpid
            is_book = True
        return is_book

    def scrape_page_to_strprd(self, url, res):
        # ---- 下載response回來 ----
        reqss = requests.Session()
        reqss.mount('https://', HTTPAdapter(max_retries=0))
        user_agent = utility.gen_random_useragent()
        headers = utility.gen_spider_headers(user_agent, referer='https://www.cavesbooks.com.tw/')
        #res = reqss.get(url, headers=headers, timeout=60)
        if res.status_code == 404:
            print('-- 商品已下架? 404找不到商品頁') 
            return None
        if res.status_code != 200:
            raise ValueError(f'-- status_code is {res.status_code}')
        pure_html = res.text
        res.connection.close()
        # ---- 準備剖析html ----
        popIdx = self.get_ec_popidx()
        prd = {}
        soup = BeautifulSoup(pure_html,features="lxml")
        
        # 要求商品資訊 ajax api
        pid = self._ecpid
        json_url = f'https://www.cavesbooks.com.tw/api/Books_Prod_Content?pID={pid}'
        res = reqss.get(json_url, headers=headers, timeout=60)
        pure_html = res.text
        res.connection.close()
        json_data = None
        try:
            json_data = json.loads(pure_html)
        except ValueError: 
            print('#Decoding JSON has failed')
            
        is_onshelf = self._extract_if_onshelf(soup)
        if is_onshelf == 1: 
            # ---- step1 商品頁可取得的資訊 ----
            prd['Name'] = self._extract_name(soup)
            prd['Url'] = url
            prd['ImgUrl'] = self._extract_imgurl(soup)
            prd['ImgUrlList'] = self._extract_imgurl_list(soup) if self._extract_imgurl_list(soup) else prd['ImgUrl']
            prd['VideoUrl'] = None
            prd['VideoUrlList'] = None
            prd['OriPrice'] = self._extract_oriprice(json_data)
            prd['Price'] = self._extract_price(json_data) if self._extract_price(json_data) else self._extract_oriprice(json_data)
            prd['Author'] = self._extract_author(soup)
            prd['ISBN'] = self._extract_isbn(soup)
            prd['ECID'] = self._ecid
            prd['ECPID'] = self._ecpid
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

        else:
            print('-- 商品已下架? 找不到購物車鈕') 
            return None #回傳None則在main_parser下架商品

    # ======== 私有 萃取各值的方法 ========
    def _extract_if_onshelf(self, soup):
        val = 1
        return val
    
    def _extract_name(self, soup):
        val = soup.select_one("div.proData div.main h3").get_text()
        return val.strip()
    
    def _extract_url(self, soup):
        val = soup.find("link", rel="canonical")['href']
        return val
    
    def _extract_imgurl(self, soup):
        val = soup.select_one("div#navigation ul li a")['original']
        return val
    
    def _extract_imgurl_list(self, soup):
        elems = soup.select("div#navigation ul li a")
        val = ','.join([img['original'] for img in elems])
        return val #已測試若沒有為''

    def _extract_ecpid_by_url(self, soup):
        elem = soup.select_one('div.addCartBox a#btnCart')
        return elem['data-id']

    def _extract_eccatlog(self, soup):
        elem = soup.select("div.breadcrumbs ul li")[-1]
        return elem.text.strip()

    def _extract_author(self, soup):
        val = None
        elem = soup.select_one("tr#ContentPlaceHolder1_trAut td")
        if elem:
            val = elem.text.strip()
        return val

    def _extract_isbn(self, soup):
        val = None
        elem = soup.select_one("tr#ContentPlaceHolder1_trISBN td")
        if elem:
            val = elem.text.strip().replace('-', '')
        return val

    def _extract_desc(self, soup):
        val = None
        elem = soup.select_one("div#ContentPlaceHolder1_pro1 div.freeText")
        if elem:
            val = html.escape(elem.decode_contents())[:8000]
        return val

    def _extract_translator(self, soup):
        val = None
        elem = soup.select_one("tr#ContentPlaceHolder1_trTran td")
        if elem:
            tr = elem.text.strip()
            if tr != 'N/A':
                val = tr
        return val

    def _extract_pub_date(self, soup):
        val = None
        elem = soup.select_one("tr#ContentPlaceHolder1_trPublishDate td")
        if elem:
            val = elem.text.strip()
        return val

    def _extract_publisher(self, soup):
        val = None
        elem = soup.select_one("tr#ContentPlaceHolder1_trPress td")
        if elem:
            val = elem.text.strip()
        return val

    def _extract_oriprice(self, json_data):
        val = json_data['GoodsInfo']['Price']
        return val

    def _extract_price(self, json_data):
        val = json_data['GoodsInfo']['SalesPrice']
        if not val:
            val = json_data['GoodsInfo']['Price']
        return val

    # ---- esc index v2 ---- 
    def _extract_painter(self, soup):
        val = None
        elem = soup.select_one("tr#ContentPlaceHolder1_trPainter td")
        if elem:
            val = elem.text.strip()
        return val
    def _extract_origin_name(self, soup):
        val = None
        return val  
    def _extract_summary(self, soup):
        val = None
        return val
    def _extract_isbn10(self, soup):
        val = None
        return val
    def _extract_isbnadd(self, soup):
        val = None
        elem = soup.select_one("tr#ContentPlaceHolder1_trEAN td")
        if elem:
            val = elem.text.strip().replace('-', '')
        return val
    
    def _extract_booktype(self, soup, prd):
        book_type = 'book'
        ary_name = [prd['Name'] , prd['ECCatlog']]
        filtered_ary_name = [x for x in ary_name if x is not None]
        if any('電子書' in x for x in filtered_ary_name):
            book_type = 'ebook'
        if any('電子雜誌' in x for x in filtered_ary_name):
            book_type = 'ebook'
        return book_type
    

    
    
    
    