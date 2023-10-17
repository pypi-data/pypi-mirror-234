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

class KingstoneParser(BaseParser):
    def __init__(self):
        self._ecid = 2
        self._ecpid = None
    def get_ec_popidx(self):
        return 100
    def is_target_page(self, url):
        is_book = False
        ecpid = None
        match = re.search('www\.kingstone\.com\.tw\/basic\/(\w+)?', url.lower())
        if match:
            ecpid = match.group(1) if match.group(1) else None
        if ecpid:
            self._ecpid = ecpid
            # 商品id開頭規則:
            #prd_signs = ["/basics/", "/english/", "/mag/", "/ebook/"]
            #if any(sign in url for sign in prd_signs):
            #    is_book = True
            is_book = True
        return is_book

    def scrape_page_to_strprd(self, url, res):
        '''# ---- 下載response回來 ----
        reqss = requests.Session()
        reqss.mount('https://', HTTPAdapter(max_retries=0))
        user_agent = utility.gen_random_useragent()
        headers = utility.gen_spider_headers(user_agent, referer='https://www.kinstone.com.tw/')
        res = reqss.get(url, headers=headers, timeout=10)'''
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
        is_offshelf = self._extract_if_offshelf(soup)
        if is_offshelf == 1: 
            # ---- step1 商品頁可取得的資訊 ----
            prd['Name'] = self._extract_name(soup)
            prd['Url'] = self._extract_url(soup)
            prd['ImgUrl'] = self._extract_imgurl(soup)
            prd['ImgUrlList'] = self._extract_imgurl_list(soup) if self._extract_imgurl_list(soup) else prd['ImgUrl']
            prd['VideoUrl'] = None
            prd['VideoUrlList'] = None
            prd['OriPrice'] = self._extract_oriprice(soup)
            prd['Price'] = self._extract_price(soup) if self._extract_price(soup) else prd['OriPrice']
            prd['Author'] = self._extract_author(soup)
            prd['ISBN'] = self._extract_isbn(soup)
            prd['ECID'] = self._ecid
            prd['ECPID'] = self._ecpid
            prd['ECCatlog'] = self._extract_eccatlog(soup) 
            prd['isOnShelf'] = is_offshelf
            prd['isEnable'] = 1
            prd['Desc'] = self._extract_desc(soup)
            prd['ModifyTime'] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            prd['CreateTime'] = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            prd['PopIdx'] = popIdx
            prd['CatID'] = None
            prd['Translator'] = self._extract_translator(soup)
            prd['PublishDate'] = self._extract_pub_date(soup)
            prd['Publisher'] = self._extract_pub_company(soup)

            prd['Painter'] = self._extract_painter(soup)
            prd['OriginName'] = self._extract_origin_name(soup)
            prd['Summary'] = self._extract_summary(soup)
            prd['ISBN10'] = None
            prd['ISBNADD'] = self._extract_isbnadd(soup)
            prd['BookType'] = self._extract_booktype(soup)
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
        elem = soup.find(text=re.compile(r'此為18禁書籍'))
        if elem:
            val = True
        return val
    def _extract_if_offshelf(self, soup):
        val = 1
        elem = soup.find(text=re.compile(r'施工中!!'))
        if elem:
            val = 0
        elem = soup.find(text=re.compile(r'查無此商品'))
        if elem:
            val = 0
        return val  
    
    def _extract_name(self, soup):
        val = soup.select_one("div.pdnamemix_main h1.pdname_basic").get_text().strip()
        return val
    
    def _extract_url(self, soup):
        val = soup.find("meta", property="og:url")['content']
        return val
    
    def _extract_imgurl(self, soup):
        val = soup.select_one('div.mainpdarea div.sliderGalleryBox ul.my-gallery li a img')['src']
        return val
    
    def _extract_imgurl_list(self, soup):
        elems = soup.select('div.mainpdarea div.sliderGalleryBox ul.my-gallery li a img')
        imgs = []
        for img in elems:
            if img.has_attr('data-src'):
                imgs.append(img['data-src'])
            else:
                imgs.append(img['src'])
        val = ','.join(imgs)
        return val #已測試若沒有為''

    def _extract_ecpid(self, soup):
        val = None #self._ecpid
        return val

    def _extract_eccatlog(self, soup):
        elems = soup.select('li.catbreadcrumb a')
        cats = [elem.text.strip() for elem in elems[:-1]]
        return '>'.join(cats)

    def _extract_author(self, soup):
        val = None
        elem = soup.find('span', {"class": "title_basic"}, text=re.compile(r'作者：'))
        if elem:
            val = elem.next_sibling.strip()
            if val == '':
                val = elem.next_sibling.next_sibling.text.strip()
        return val

    def _extract_isbn(self, soup):
        val = None
        elem = soup.find('li', text=re.compile(r'ISBN'))
        if elem:
            val = elem.next_sibling.next_sibling.text.strip()
        return val
    
    def _extract_isbnadd(self, soup):
        val = None
        elem = soup.find('li', text=re.compile(r'ISBN'))
        if elem:
            val = elem.next_sibling.next_sibling.text.strip()
            val = val if val.find('471') == 0 else None
        return val

    def _extract_desc(self, soup):
        val = None
        div = soup.select_one('div.pdintro_txt1field')
        if div:
            val = div.decode_contents()
            val = utility.remove_emojis_str(val)
            val = html.escape(val)[:8000] #注意db大小只有8000字元
        return val

    def _extract_translator(self, soup):
        val = None
        elem = soup.find('span', text=re.compile(r'譯者：'))
        if elem:
            val = elem.next_sibling.strip()
            if val == '':
                val = elem.next_sibling.next_sibling.text.strip()
        if val is None:
            elem = soup.find('span', text=re.compile(r'編／譯者：'))
            if elem:
                val = elem.next_sibling.strip()
                if val == '':
                    val = elem.next_sibling.next_sibling.text.strip()
        return val

    def _extract_pub_date(self, soup):
        val = None
        elem = soup.find('span', text=re.compile(r'出版日：'))
        if elem:
            val = elem.next_sibling.strip()
        return val

    def _extract_pub_company(self, soup):
        val = None
        elem = soup.find('span', text=re.compile(r'出版社：'))
        if elem:
            val = elem.next_sibling.strip()
            if val == '':
                val = elem.next_sibling.next_sibling.text.strip()
        return val

    def _extract_oriprice(self, soup):
        val = None
        '''elem = soup.find('span', text=re.compile(r'定價：'))
        if elem:
            val = elem.next_sibling.text.replace(',','').strip()'''
        elem = soup.select_one("li.price1 b.sty00")
        if elem:
            val = elem.get_text().strip()
        return val

    def _extract_price(self, soup):
        val = None
        '''elem = soup.find('span', text=re.compile(r'特價：'))
        if elem:
            val = elem.next_sibling.next_sibling.text.replace('元','').replace(',','').strip()'''
        val = soup.select_one("li.price1 b.txtSize2").get_text().strip()
        return val
    
    def _extract_painter(self, soup):
        val = None
        elem = soup.find('span', text=re.compile(r'繪者：'))
        if elem:
            val = elem.next_sibling.strip()
            if val == '':
                val = elem.next_sibling.next_sibling.text.strip()
        return val
    
    def _extract_origin_name(self, soup):
        val = None
        elem = soup.select_one('div.subpdname')
        if elem:
            val = elem.get_text().strip()
        return val
    
    def _extract_summary(self, soup):
        val = None
        elem = soup.select_one('div.pdnamemix_main strong.saleslogan2')
        if elem:
            val = elem.get_text().strip()
        return val
    
    def _extract_booktype(self, soup):
        book_type = 'book'
        name = soup.select_one("div.pdnamemix_main h1.pdname_basic").get_text().strip()
        if '【電子書】' in name:
            book_type = 'ebook'
        if '【電子雜誌】' in name:
            book_type = 'ebook'
        return book_type
    
    