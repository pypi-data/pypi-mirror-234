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

class BooksParser(BaseParser):
    def __init__(self):
        self._ecid = 1
        self._ecpid = None
    def get_ec_popidx(self):
        return 100
    def is_target_page(self, url):
        is_book = False
        ecpid = None
        match = re.search('www\.books\.com\.tw\/products\/(\w+)?', url)
        if match:
            ecpid = match.group(1) if match.group(1) else None
        if ecpid:
            self._ecpid = ecpid
            # 商品id開頭規則:
            # CN 簡體書
            # F 外文書
            # E 電子書
            # 00 中文書
            # R 雜誌
            # M MOOK
            # N 商品
            prefixes = ["CN", "F", "E", "0", "R", "M", "S", "J", "H"]
            is_book = ecpid.startswith(tuple(prefixes))
        return is_book
    def scrape_page_to_strprd(self, url, res):
        '''# ---- 下載response回來 ----
        reqss = requests.Session()
        reqss.mount('https://', HTTPAdapter(max_retries=0))
        user_agent = utility.gen_random_useragent()
        headers = utility.gen_spider_headers(user_agent, referer='https://www.books.com.tw/')
        # proxyDict = utility.gen_random_proxy()
        res = reqss.get(url, headers=headers, timeout=10)'''
        if res.status_code == 404:
            print('-- 商品已下架? 404找不到商品頁') 
            return None
        if res.status_code != 200:
            raise ValueError(f'-- status_code is {res.status_code}')
        pure_html = res.text
        #print(pure_html[0:300])
        res.connection.close()
        # ---- 準備剖析html ----
        popIdx = self.get_ec_popidx()
        prd = {}
        soup = BeautifulSoup(pure_html,features="lxml")
        is_r18 = self._extract_is_r18(soup)
        if is_r18:
            print('-- 商品為限制級，需登入爬取') 
            return None #回傳None則在main_parser下架商品
        is_offshelf = self._extract_if_offshelf(soup)
        if is_offshelf == 1: 
            # ---- step1 未執行js即可取得的資訊 ----
            prd['Name'] = soup.find("meta", property="og:title")['content']
            prd['Url'] = soup.find("meta", property="og:url")['content']
            prd['ImgUrl'] = soup.find("meta", property="og:image")['content']
            prd['ImgUrlList'] = self._extract_imgurl_list(soup) if self._extract_imgurl_list(soup) else prd['ImgUrl']
            prd['VideoUrl'] = None
            prd['VideoUrlList'] = None
            prd['OriPrice'] = self._extract_oriprice(soup)
            prd['Price'] = self._extract_price(soup) if self._extract_price(soup) else prd['OriPrice']
            prd['Author'] = self._extract_author(soup)
            prd['ISBN'] = self._extract_isbn(soup)
            prd['ECID'] = self._ecid
            prd['ECPID'] = self._extract_ecpid_by_url(soup)
            prd['ECCatlog'] = self._extract_eccatlog(soup) 
            prd['isOnShelf'] = is_offshelf
            
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

            # ---- step2 需執行js才能取得----
            #isEnable = 1 if soup.select_one('a.type02_btn04 > span > span').get_text() == '放入購物車' else 0
            #print(isEnable)
            return prd

        else:
            print('-- 商品已下架? 找不到購物車鈕') #TODO:下架商品
            return None
        
    # ======== 私有 萃取各值的方法 ========
    def _extract_is_r18(self, soup):
        val = False
        elem = soup.find(text=re.compile(r'本商品為限制級商品'))
        if elem:
            val = True
        return val
    
    def _extract_if_offshelf(self, soup):
        val = 1
        elem = soup.select_one("h2.msg_info")
        if elem:
            val = 0 if elem.get_text() == '頁面連結錯誤' else 1
        elem = soup.select_one("h1.msg_title")
        if elem:
            val = 0 if elem.get_text() == '錯誤頁面訊息提示' else 1
        return val    

    def _extract_imgurl_list(self, soup):
        val = ','.join([img["src"] for img in soup.select('ul.li_box img')])
        return val #已測試若沒有為''

    def _extract_ecpid_by_url(self, soup):
        string = soup.find("meta", property="og:url")['content']
        match = re.search('\/products\/(\w+)?', string)
        return match.group(1)

    def _extract_eccatlog(self, soup):
        eccats = [item.get_text() for item in soup.select('ul#breadcrumb-trail a')[1:]]
        return '>'.join(eccats)

    def _extract_author(self, soup):
        val = None
        string = soup.find("meta", property="og:description")['content']
        match = re.search(r'\，作者：(.+?)\，', string)
        val = match.group(1) if match else None
        if val:
            return val
        for elem in soup(text=re.compile(r'作者：')):
            match = re.search(r'作者：(.+)', elem)
            val = match.group(1) if match else None
            if val:
                return val
        for elem in soup(text=re.compile(r'編者：')):
            match = re.search(r'編者：(.+)', elem.parent.text)
            val = match.group(1) if match else None
            if val:
                val = val.strip()
        return val

    def _extract_isbn(self, soup):
        val = None
        string = soup.find("meta", property="og:description")['content']
        match = re.search(r'\，ISBN：(.+?)\，', string)
        val = match.group(1) if match else None
        if val:
            return val
        for elem in soup(text=re.compile(r'條碼：')):
            match = re.search(r'條碼：(\d+)', elem)
            val = match.group(1) if match else None
            if val:
                return val
        return val
    
    def _extract_desc(self, soup):
        val = None
        div = soup.select_one('div.content')
        if div:
            val = html.escape(div.decode_contents())[:8000] #注意db大小只有8000字元
        return val
    
    def _extract_translator(self, soup):
        val = None
        string = soup.find("meta", property="og:description")['content']
        match = re.search(r'\，譯者：(.+?)\，', string)
        val = match.group(1) if match else None
        if val:
            return val
        for elem in soup(text=re.compile(r'譯者：')):
            match = re.search(r'譯者：(.+)', elem)
            val = match.group(1) if match else None
            if val:
                return val
        return val

    def _extract_pub_date(self, soup):
        val = None
        string = soup.find("meta", property="og:description")['content']
        match = re.search(r'\，出版日期：(.+?)\，', string)
        val = match.group(1) if match else None
        if not val:
            for elem in soup(text=re.compile(r'出版日期：')):
                match = re.search(r'出版日期：(.+)', elem)
                val = match.group(1) if match else None
        if not val:
            for elem in soup(text=re.compile(r'上架日期：')):
                match = re.search(r'上架日期：(.+)', elem)
                val = match.group(1) if match else None
        return val

    def _extract_publisher(self, soup):
        val = None
        string = soup.find("meta", property="og:description")['content']
        match = re.search(r'\，出版社：(.+?)\，', string)
        val = match.group(1) if match else None
        if val:
            return val
        for elem in soup(text=re.compile(r'出版社：')):
            match = re.search(r'出版社：(.+)', elem)
            val = match.group(1) if match else None
            if val:
                return val
        return val

    def _extract_oriprice(self, soup):
        val = None
        elem = soup.select_one('ul.price > li > em')
        if elem:
            return elem.get_text()
        for elem in soup(text=re.compile(r'定價：')):
            match = re.search(r'定價：(\d+)元', elem.parent.get_text())
            val = match.group(1) if match else None
            if val:
                return val
        return val

    def _extract_price(self, soup):
        val = None
        for elem in soup(text=re.compile(r'dataLayer.push\(\{\"ecommerce\"')):
            match = re.search(r'\"price\"\:(\d+?)\,', elem)
            val = match.group(1) if match else None
            if val:
                return val
        for elem in soup(text=re.compile(r'特價：')):
            match = re.search(r'特價：(\d+)', elem.parent.get_text())
            val = match.group(1) if match else None
            if val:
                return val
        for elem in soup(text=re.compile(r'優惠價：')):
            match = re.search(r'優惠價：.*折(\d+)元', elem.parent.get_text())
            val = match.group(1) if match else None
            if val:
                return val
        return val
    
    # ---- esc index v2 ---- 
    def _extract_painter(self, soup):
        val = None
        for elem in soup(text=re.compile(r'繪者：')):
            match = re.search(r'繪者：(.+)', elem.parent.text)
            val = match.group(1) if match else None
            if val:
                val = val.strip()
        return val
    def _extract_origin_name(self, soup):
        val = None
        elem = soup.select_one("div.mod.type02_p002 h2")
        if elem:
            val = elem.text.strip()
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
    
    
    
    