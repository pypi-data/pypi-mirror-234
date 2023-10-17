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

class UdnParser(BaseParser):
    def __init__(self):
        self._ecid = 11
        self._ecpid = None
    def get_ec_popidx(self):
        return 100
    def is_target_page(self, url):
        is_book = False
        ecpid = None
        match = re.search('shopping\.udn\.com\/mall\/cus\/cat\/Cc1c02\.do\?.*dc_cargxuid_0=([A-Za-z0-9]+)?', url)
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
        headers = utility.gen_spider_headers(user_agent, referer='https://www.rakuten.com.tw/')
        res = reqss.get(url, headers=headers, timeout=60)'''
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
        is_r18 = self._extract_is_r18(soup)
        if is_r18:
            print('-- 商品為限制級，需登入爬取') 
            return None #回傳None則在main_parser下架商品
        is_onshelf = self._extract_is_onshelf(soup)
        if is_onshelf == 1: 
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
            prd['ECPID'] = self._extract_ecpid(soup)
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
    def _extract_is_r18(self, soup):
        val = False
        elem = soup.find(text=re.compile(r'未滿18歲請勿進入'))
        if elem:
            val = True
        return val
    
    def _extract_is_onshelf(self, soup):
        val = 1
        return val
    
    def _extract_name(self, soup):
        val = soup.select_one('div.pd_maininfo h1.pd_name').text
        return val.strip()
    
    def _extract_url(self, soup):
        val = soup.find("link", rel="canonical")['href'].replace('http:', 'https:')
        return val
    
    def _extract_imgurl(self, soup):
        val = None
        elem = soup.select_one('div.pd_block div.pd_pic_zoom div.zoom > img')
        if elem:
            val = 'https:' + elem['src']
        return val
    
    def _extract_imgurl_list(self, soup):
        val = None
        return val

    def _extract_ecpid(self, soup):
        val = None
        url = soup.find("link", rel="canonical")['href']
        match = re.search('shopping\.udn\.com\/mall\/cus\/cat\/Cc1c02\.do\?dc_cargxuid_0=([A-Za-z0-9]+)?', url)
        if match:
            val = match.group(1) if match.group(1) else None
        return val

    def _extract_eccatlog(self, soup):
        val = None
        elems = soup.select('div.top_inner .crumb_item span a')
        cats = [a.text.strip() for a in elems[2:]]
        last = soup.select_one('div.top_inner a.crumb_item.now')
        if cats and last:
            val = '>'.join(cats)
            val = val + '>' + last.text.strip()
        return val

    def _extract_author(self, soup):
        val = None
        #elems = soup.find_all(text=re.compile(r'作者：'))
        #for elem in elems:
        #    if elem.parent.name == 'div' or elem.parent.name == 'p':
        #        val = elem.replace('作者：', '').strip()
        elem = soup.select_one('div.pd_point_list_div div.pd_point_item')
        if elem:
            match = re.search('作者：([^<]+)?', elem.decode_contents())
            if match:
                val = match.group(1) if match.group(1) else None
        if not val:
            elems = soup.find_all(text=re.compile(r'作者：'))
            for elem in elems:
                match = re.search('作者：([^<]+)?', elem)
                if match:
                    val = match.group(1) if match.group(1) else None
        val = val.strip() if val else val
        return val

    def _extract_isbn(self, soup):
        val = None
        elems = soup.find_all(text=re.compile(r'ISBN：'))
        for elem in elems:
            if elem.parent.name == 'div' or elem.parent.name == 'p':
                val = elem.replace('ISBN：', '').replace('-','').strip()
        # 發現會有ISBN：9789869173308-PT2，9789869173308PT2
        if val:
            match = re.search('(\d{10,13})', val)
            if match:
                isbn = match.group(1) if match.group(1) else ''
                val = isbn
        return val

    def _extract_desc(self, soup):
        val = None
        elem = soup.select_one('div.pd_detail_cont')
        if elem:
            val = html.escape(elem.decode_contents())[:8000]
        if not val:
            elem = soup.select_one('div.spec_cont')
            if elem:
                val = html.escape(elem.decode_contents())[:8000]
            
        return val

    def _extract_translator(self, soup):
        val = None
        elems = soup.find_all(text=re.compile(r'譯者：'))
        for elem in elems:
            if elem.parent.name == 'div' or elem.parent.name == 'p':
                val = elem.replace('譯者：', '').strip()
        return val

    def _extract_pub_date(self, soup):
        val = None
        elems = soup.find_all(text=re.compile(r'出版日期：'))
        for elem in elems:
            if (elem.parent.name == 'div' or elem.parent.name == 'p') and '線上' not in elem:
                val = elem.replace('出版日期：', '').replace('-', '/').replace('年', '/').replace('月', '/').replace('日', '').strip()
        if val == '0000/00/00':
            val = None
        if val:
            aryVal = val.split('/')
            if len(aryVal) == 1: # 發現會有20190608 這種格式
                val = val[:4] + '/' + val[4:-2] + '/' + val[-2:]
            if len(aryVal) == 2: # 發現會有2019/6 這種格式
                val = val + '/01'
            if len(aryVal) == 3 and aryVal[2] == '00': # 發現會有2012/08/00 這種格式
                val = val.replace('00', '01')
        return val

    def _extract_publisher(self, soup):
        val = None
        #elem = soup.select_one('div.pd_point_item')
        #inhtml = str(elem.encode_contents)
        #match = re.search('出版社：(.+?)<br/>', inhtml)
        #if match:
        #    val = match.group(1) if match.group(1) else None
        #    val = val.strip()
        elems = soup.find_all(text=re.compile(r'出版社：'))
        for elem in elems:
            if elem.parent.name == 'div' or elem.parent.name == 'p':
                val = elem.replace('出版社：', '').strip()
        return val

    def _extract_oriprice(self, soup):
        val = None
        elem = soup.select_one('div.pd_buyinfo p.pd_oprice span.del')
        if elem:
            val = elem.text.replace('$','').replace('元','').replace(',','').strip()
        return val

    def _extract_price(self, soup):
        val = None
        elem = soup.select_one('div.pd_buyinfo p.k_normal_price_tit span.hlight')
        val = elem.text.replace('元','').replace(',','').strip()
        return val

    # ---- esc index v2 ---- 
    def _extract_painter(self, soup):
        val = None
        elems = soup.find_all(text=re.compile(r'繪者：'))
        for elem in elems:
            if elem.parent.name == 'div' or elem.parent.name == 'p':
                val = elem.replace('繪者：', '').strip()
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
    