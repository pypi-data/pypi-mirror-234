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

class RakutenParser(BaseParser):
    def __init__(self):
        self._ecid = 14
        self._ecpid = None
    def get_ec_popidx(self):
        return 100
    def is_target_page(self, url):
        is_book = False
        ecpid = None
        match = re.search('www\.rakuten\.com\.tw\/shop\/rbook\/product\/(\d+)?', url.lower())
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
            prd['ECPID'] = self._extract_ecpid_by_url(soup)
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
        elem = soup.find(text=re.compile(r'未滿18歲'))
        if elem:
            val = True
        return val
    
    def _extract_is_onshelf(self, soup):
        val = 1
        return val
    
    def _extract_name(self, soup):
        val = elem = soup.select_one('h1.qa-ttl-main').text
        return val.strip()
    
    def _extract_url(self, soup):
        val = soup.find("meta", property="og:url")['content']
        return val
    
    def _extract_imgurl(self, soup):
        val = None
        elem = soup.select_one('img.magnifier-image')
        if elem:
            val = elem['src'].replace('?_ex=330x330', '').replace('?_ex=486x486', '')
        return val
    
    def _extract_imgurl_list(self, soup):
        elems = soup.select('div.LdhM5I5j7uNr3na7Bnki div.swiper-slide img')
        val = ','.join([img['src'].replace('?_ex=60x60', '').replace('?_ex=486x486', '') for img in elems])
        return val #已測試若沒有為''

    def _extract_ecpid_by_url(self, soup):
        val = None
        url = soup.find("meta", property="og:url")['content']
        match = re.search('www\.rakuten\.com\.tw\/shop\/rbook\/product\/(\d+)?', url.lower())
        if match:
            val = match.group(1) if match.group(1) else None
        return val

    def _extract_eccatlog(self, soup):
        val = None
        elems = soup.select('li.I2gjNxGvPGJhllkKIiZz a')
        if elems:
            eccats = [cat.text for cat in elems[2:-1]]
            val = '>'.join(eccats)
        return val

    def _extract_author(self, soup):
        val = None
        elem = soup.find('li', text=re.compile(r'作者：'))
        if elem:
            val = elem.text.replace('作者：','').strip()
        if not val:
            elem = soup.select_one('script[data-hypernova-key="ProductInfoTabs"]')
            if elem:
                match = re.search('作者：([^<]+)?', elem.text)
                if match:
                    val = match.group(1).strip() if match.group(1) else None
        return val

    def _extract_isbn(self, soup):
        val = None
        elem = soup.find('li', text=re.compile(r'ISBN：'))
        if elem:
            val = elem.text.replace('ISBN：','').replace('-', '').strip()
        if not val:
            elem = soup.select_one('script[data-hypernova-key="ProductInfoTabs"]')
            if elem:
                match = re.search('ISBN：([\d-]+)?', elem.text)
                if match:
                    val = match.group(1).replace('-', '') if match.group(1) else None
        return val

    def _extract_desc(self, soup):
        val = None
        elem = soup.select_one('div#books_content')
        if elem:
            val = elem.decode_contents()
            val = utility.remove_emojis_str(val)
            val = html.escape(val)[:8000]
        return val

    def _extract_translator(self, soup):
        val = None
        elem = soup.find('li', text=re.compile(r'譯者：'))
        if elem:
            val = elem.text.replace('譯者：','').strip()
        if not val:
            elem = soup.select_one('script[data-hypernova-key="ProductInfoTabs"]')
            if elem:
                match = re.search('譯者介紹(.+?)<strong&gt;(\w+)?', elem.text)
                if match:
                    val = match.group(2) if match.group(2) else None
        return val

    def _extract_pub_date(self, soup):
        val = None
        elem = soup.find('li', text=re.compile(r'出版日：'))
        if elem:
            val = elem.text.replace('出版日：','').strip()
            if val[:1] == '1':
                val = '{0}/{1}/{2}'.format(str(int(val[0:3]) + 1911), val[3:5], val[5:7])
            else:
                val = '{0}/{1}/{2}'.format(str(int(val[0:2]) + 1911), val[2:4], val[4:6])
        if not val:
            elem = soup.select_one('script[data-hypernova-key="ProductInfoTabs"]')
            if elem:
                match = re.search('出版日：(\d+)?', elem.text)
                if match:
                    val = match.group(1) if match.group(1) else None
                    if len(val) == 7:
                        val = '{0}/{1}/{2}'.format(str(int(val[0:3]) + 1911), val[3:5], val[5:7])
                    elif len(val) == 6:
                        val = '{0}/{1}/{2}'.format(str(int(val[0:2]) + 1911), val[2:4], val[4:6])
                    else:
                        val = '{0}/{1}/{2}'.format(val[0:4], val[4:6], val[6:8])
        return val

    def _extract_publisher(self, soup):
        val = None
        elem = soup.find('li', text=re.compile(r'出版社：'))
        if elem:
            val = elem.text.replace('出版社：','').strip()
        if not val:
            elem = soup.select_one('script[data-hypernova-key="ProductInfoTabs"]')
            if elem:
                match = re.search('出版社：([^<]+)?', elem.text)
                if match:
                    val = match.group(1).strip() if match.group(1) else None
        return val

    def _extract_oriprice(self, soup):
        val = None
        elem = soup.select_one('span.qa-product-list-price')
        if elem:
            val = elem.text.replace('元', '').replace(',', '').replace('$', '').strip()
        return val

    def _extract_price(self, soup):
        val = None
        elem = soup.select_one('span.qa-product-actual-price')
        if elem:
            val = elem.text.replace('元', '').replace(',', '').replace('$', '').strip()
        return val

    # ---- esc index v2 ---- 
    def _extract_painter(self, soup):
        val = None
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
    
    
    