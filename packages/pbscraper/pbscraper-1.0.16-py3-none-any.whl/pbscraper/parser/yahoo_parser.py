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

class YahooParser(BaseParser):
    def __init__(self):
        self._ecid = 10
        self._ecpid = None
        self._url = None
    def get_ec_popidx(self):
        return 100
    def is_target_page(self, url):
        self._url = url
        is_book = False
        ecpid = None
        match = re.search('tw\.buy\.yahoo\.com\/gdsale\/gdsale\.asp\?gdid=([A-Za-z0-9]+)?', url.lower())
        if match:
            ecpid = match.group(1) if match.group(1) else None
        if not ecpid:
            match = re.search('tw\.buy\.yahoo\.com\/gdsale\/gdbksale\.asp\?gdid=([A-Za-z0-9]+)?', url.lower())
            if match:
                ecpid = match.group(1) if match.group(1) else None
        if not ecpid:
            match = re.search('tw\.buy\.yahoo\.com\/gdsale\/.+-([A-Za-z0-9]+)?\.html', url.lower())
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
        headers = utility.gen_spider_headers(user_agent, referer='https://tw.buy.yahoo.com/')
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
    def _extract_is_onshelf(self, soup):
        val = 1
        return val
    
    def _extract_name(self, soup):
        val = None
        if 'gdbksale' in self._url:
            elem = soup.select_one('div.item-spec div.title h1')
            if elem:
                return elem.text
        '''else:
            elem = soup.select_one('div#isoredux-data')
            info = json.loads(elem['data-state'])
            spec_tb_text = info['ecgql']['gqlItemPage']['detailDescription']['specifics']
            match = re.search('<th>書名</th><td>(.+?)</td>', spec_tb_text)
            if match:
                val = match.group(1) if match.group(1) else None
            if not val:
                match = re.search('<li>書名：(.+?)</li>', spec_tb_text)
                if match:
                    val = match.group(1) if match.group(1) else None
            if not val:
                val = info['ecgql']['gqlItemPage']['title']
        return val'''
        elem = soup.select_one('h1.HeroInfo__title___57Yfg')
        if elem:
            val = elem.text.strip()
        return val
    
    def _extract_url(self, soup):
        val = None
        if 'gdbksale' in self._url:
            return self._url
        
        val = soup.find("meta", property="og:url")['content']
        return val
    
    def _extract_imgurl(self, soup):
        val = None
        if 'gdbksale' in self._url:
            elem = soup.select_one('img.main-image')
            return elem['src']
        '''else:
            elem = soup.select_one('div#isoredux-data')
            info = json.loads(elem['data-state'])
            val = info['ecgql']['gqlItemPage']['images'][0][0]['url']
        return val'''
        elem = soup.select_one('img.ImageHover__mainImage___2I2Li')
        if elem:
            val = elem['src']
        return val
    
    def _extract_imgurl_list(self, soup):
        val = None
        '''if 'gdbksale' in self._url:
            val = ''
        else:
            elem = soup.select_one('div#isoredux-data')
            info = json.loads(elem['data-state'])
            info['ecgql']['gqlItemPage']['images'][0][0]['url']
            val = ','.join([img[0]['url'] for img in info['ecgql']['gqlItemPage']['images']])
        return val #已測試若沒有為''
        '''
        elems = soup.select('img.LightBox__largeImg___2qKXW')
        val = ','.join([img['src'] for img in elems])
        return val #已測試若沒有為''

    def _extract_ecpid(self, soup):
        val = None
        if 'gdbksale' in self._url:
            return self._ecpid
        '''else:
            elem = soup.select_one('div#isoredux-data')
            info = json.loads(elem['data-state'])
            val = info['ecgql']['gqlItemPage']['id']
        return val'''
        url = soup.find("meta", property="og:url")['content']
        match = re.search('.+yahoo\.com\/gdsale\/gdsale\.asp\?gdid=(\d+)?', url.lower())
        if match:
            val = match.group(1) if match.group(1) else None
        return val

    def _extract_eccatlog(self, soup):
        val = None
        if 'gdbksale' in self._url:
            elems = soup.select('div.isoredux-root nav ul li a')
            if elems:
                eccats = [cat.text for cat in elems[2:]]
                return '>'.join(eccats)
        '''else:
            elem = soup.select_one('div#isoredux-data')
            info = json.loads(elem['data-state'])
            if info['ecgql']['gqlItemPage']['categories']:
                val = info['ecgql']['gqlItemPage']['categories'][-2]['title']
        return val'''
        elems = soup.select('li.CategoryBreadCrumb__breadCrumbListItem___3vM3j a')
        if elems:
            eccats = [cat.text for cat in elems[2:]]
            val = '>'.join(eccats)
        return val

    def _extract_author(self, soup):
        val = None
        if 'gdbksale' in self._url:
            elem = soup.find('li', text=re.compile(r'作　者： '))
            if elem:
                return elem.text.replace('作　者： ','').replace('\xa0',' ').strip()
        '''else:
            elem = soup.select_one('div#isoredux-data')
            info = json.loads(elem['data-state'])
            spec_tb_text = info['ecgql']['gqlItemPage']['detailDescription']['specifics']
            match = re.search('<th>作者</th><td>(.+?)</td>', spec_tb_text)
            if match:
                val = match.group(1).strip() if match.group(1) else None
            if not val:
                match = re.search('<li>作者：(.+?)</li>', spec_tb_text)
                if match:
                    val = match.group(1) if match.group(1) else None
            if not val:
                elemA = soup.find('div', {"data-state" : re.compile(r'作者：')})
                if elemA:
                    match = re.search('作者：([ |\w]+)?', elemA['data-state'])
                    if match:
                        val = match.group(1) if match.group(1) else None
                        val = val.strip()
        return val'''
        pattern = re.compile(r'APOLLO\_STATE')
        script = soup.find("script", text=pattern)
        if script:
            str_start = '作者\\u003c/'
            str_end = '\\u003c/'
            if str_start in script.text:
                str_content = script.text[script.text.index(str_start):]
                str_content = str_content.replace(str_start, '')
                str_content = str_content[:str_content.index(str_end)]
                str_content = str_content[str_content.rindex('>')+1:]
                return str_content.strip()
            
            match = re.search(r'>作者：(.+?)\\u003c', script.text)
            if match:
                val = match.group(1) if match.group(1) else None
                return val.strip()
            
        return val
        '''
        elem = soup.select_one('script[data-hypernova-key="ProductInfoTabs"]')
            if elem:
                match = re.search('作者：([^<]+)?', elem.text)
                if match:
                    val = match.group(1).strip() if match.group(1) else None'''

    def _extract_isbn(self, soup):
        val = None
        if 'gdbksale' in self._url:
            val = None
            elem = soup.find('li', text=re.compile(r'I S B N ： '))
            if elem:
                return elem.text.replace('I S B N ： ','').strip()
        '''else:
            elem = soup.select_one('div#isoredux-data')
            info = json.loads(elem['data-state'])
            spec_tb_text = info['ecgql']['gqlItemPage']['detailDescription']['specifics']
            match = re.search('<th>ISBN</th><td>(.+?)</td>', spec_tb_text)
            if match:
                val = match.group(1) if match.group(1) else None
            if not val:
                match = re.search('<li>ISBN：(.+?)</li>', spec_tb_text)
                if match:
                    val = match.group(1) if match.group(1) else None
            if not val:
                elemA = soup.find('div', {"data-state" : re.compile(r'ISBN：')})
                if elemA:
                    match = re.search('ISBN：([ |\w]+)?', elemA['data-state'])
                    if match:
                        val = match.group(1) if match.group(1) else None
                        val = val.strip()
        return val'''
        pattern = re.compile(r'APOLLO\_STATE')
        script = soup.find("script", text=pattern)
        if script:
            str_start = 'ISBN\\u003c/'
            str_end = '\\u003c/'
            if str_start in script.text:
                str_content = script.text[script.text.index(str_start):]
                str_content = str_content.replace(str_start, '')
                str_content = str_content[:str_content.index(str_end)]
                str_content = str_content[str_content.rindex('>')+1:]
                return str_content.strip()
            
            match = re.search(r'>ISBN：(\d+?)\\u003c', script.text)
            if match:
                val = match.group(1) if match.group(1) else None
                return val.strip()
            
        return val

    def _extract_desc(self, soup):
        val = None
        if 'gdbksale' in self._url:
            elem = soup.select_one('div#cl-gdintro blockquote')
            val = elem.decode_contents()
            val = utility.remove_emojis_str(val)
            val = html.escape(val)[:8000]
        else:
            pattern = re.compile(r'APOLLO\_STATE')
            script = soup.find("script", text=pattern)
            if script:
                str_json = script.text[script.text.index('={')+1 : script.text.index('};')+1]
                info = json.loads(str_json)
                val = info[f'Shopping_Product:{self._ecpid}']['detailDescription']['longDescription']
                val = utility.remove_emojis_str(val)
                if val:
                    val = html.escape(val)[:8000]
        return val

    def _extract_translator(self, soup):
        val = None
        if 'gdbksale' in self._url:
            elem = soup.find('li', text=re.compile(r'譯　者： '))
            if elem:
                return elem.text.replace('譯　者： ','').strip()
        '''else:
            elem = soup.select_one('div#isoredux-data')
            info = json.loads(elem['data-state'])
            spec_tb_text = info['ecgql']['gqlItemPage']['detailDescription']['specifics']
            match = re.search('<th>譯者</th><td>(.+?)</td>', spec_tb_text)
            if match:
                val = match.group(1) if match.group(1) else None
            else:
                match = re.search('<li>譯者：(.+?)</li>', spec_tb_text)
                if match:
                    val = match.group(1) if match.group(1) else None
        return val'''
        pattern = re.compile(r'APOLLO\_STATE')
        script = soup.find("script", text=pattern)
        if script:
            str_start = '譯者\\u003c/'
            str_end = '\\u003c/'
            if str_start in script.text:
                str_content = script.text[script.text.index(str_start):]
                str_content = str_content.replace(str_start, '')
                str_content = str_content[:str_content.index(str_end)]
                str_content = str_content[str_content.rindex('>')+1:]
                return str_content.strip()
            
            match = re.search(r'>譯者：(.+?)\\u003c', script.text)
            if match:
                val = match.group(1) if match.group(1) else None
                return val.strip()
            
        return val

    def _extract_pub_date(self, soup):
        val = None
        if 'gdbksale' in self._url:
            elem = soup.find('li', text=re.compile(r'出版日： '))
            if elem:
                val = elem.text
        else:
            pattern = re.compile(r'APOLLO\_STATE')
            script = soup.find("script", text=pattern)
            if script:
                str_start = '出版日期\\u003c/'
                str_end = '\\u003c/'
                if str_start in script.text:
                    str_content = script.text[script.text.index(str_start):]
                    str_content = str_content.replace(str_start, '')
                    str_content = str_content[:str_content.index(str_end)]
                    str_content = str_content[str_content.rindex('>')+1:]
                    val = str_content.strip()
                
                match = re.search(r'>出版日期：(.+?)\\u003c', script.text)
                if match:
                    val = match.group(1) if match.group(1) else None
                
        if val:
            if 'k' in val: # 發現會有kk0487585的格式
                return None
            if len(val) < 6: # 發現會有-的格式
                return None
            val = val.replace('00:00:00.000', '').strip()
            val = val.replace('出版日： ','').replace(' 年 ','/').replace(' 月 ','/').replace(' 日','').strip()
            val = val.replace('出版日：','').replace('年','/').replace('月','/').replace('日','').strip()
            val = val.replace('-','/').strip()
            aryVal = val.split('/')
            if len(aryVal) == 2: # 發現會有2019/6 這種格式
                val = val + '/01'
            elif len(aryVal) == 3 and not aryVal[2]: # 發現會有2019年6月 這種格式
                val = val + '01'
            elif len(aryVal) == 1 and len(val) == 8: # 發現會有20180701 這種格式
                val = val[:4] + '/' + val[4:-2] + '/' + val[-2:]
        
        return val

    def _extract_publisher(self, soup):
        val = None
        if 'gdbksale' in self._url:
            elem = soup.find('li', text=re.compile(r'出版社： '))
            if elem:
                return elem.text.replace('出版社： ','').strip()
        '''else:
            elem = soup.select_one('div#isoredux-data')
            info = json.loads(elem['data-state'])
            spec_tb_text = info['ecgql']['gqlItemPage']['detailDescription']['specifics']
            match = re.search('<th>出版社</th><td>(.+?)</td>', spec_tb_text)
            if match:
                val = match.group(1).strip() if match.group(1) else None
            if not val:
                match = re.search('<li>出版社：(.+?)</li>', spec_tb_text)
                if match:
                    val = match.group(1) if match.group(1) else None
            if not val:
                elemA = soup.find('div', {"data-state" : re.compile(r'出版社：')})
                if elemA:
                    match = re.search('出版社：([ |\w]+)?', elemA['data-state'])
                    if match:
                        val = match.group(1) if match.group(1) else None
                        val = val.strip()
        if val:
            val = val.strip()
        return val'''
        pattern = re.compile(r'APOLLO\_STATE')
        script = soup.find("script", text=pattern)
        if script:
            str_start = '出版社\\u003c/'
            str_end = '\\u003c/'
            if str_start in script.text:
                str_content = script.text[script.text.index(str_start):]
                str_content = str_content.replace(str_start, '')
                str_content = str_content[:str_content.index(str_end)]
                str_content = str_content[str_content.rindex('>')+1:]
                val = str_content.strip()
            
            match = re.search(r'>出版社：(.+?)\\u003c', script.text)
            if match:
                val = match.group(1) if match.group(1) else None
         
        return None if val=='其他出版社' else val

    def _extract_oriprice(self, soup):
        val = None
        if 'gdbksale' in self._url:
            elem = soup.select_one('div.suggest span.price')
            if elem:
                return elem.text.replace('$','').replace(',','')
        '''else:
            elem = soup.select_one('div#isoredux-data')
            info = json.loads(elem['data-state'])
            val = info['ecgql']['gqlItemPage']['currentPrice']
        return val'''
        elem = soup.select_one('div.HeroInfo__subPriceNumber___3N0y7')
        if elem:
            val = elem.text.replace('$','').replace(',','')
        return val

    def _extract_price(self, soup):
        val = None
        if 'gdbksale' in self._url:
            elem = soup.select_one('div.priceinfo span[itemprop="price"]')
            if elem:
                return elem.text.replace('$','').replace(',','')
        '''else:
            elem = soup.select_one('div#isoredux-data')
            info = json.loads(elem['data-state'])
            val = info['ecgql']['gqlItemPage']['currentPrice']
        return val'''
        return soup.select_one('div.HeroInfo__mainPrice___1xP9H').text.replace('$','').replace(',','')

    # ---- esc index v2 ---- 
    def _extract_painter(self, soup):
        val = None
        if 'gdbksale' in self._url:
            elem = soup.find('li', text=re.compile(r'繪　者： '))
            if elem:
                return elem.text.replace('繪　者： ','').strip()
        '''else:
            elem = soup.select_one('div#isoredux-data')
            info = json.loads(elem['data-state'])
            spec_tb_text = info['ecgql']['gqlItemPage']['detailDescription']['specifics']
            match = re.search('<th>繪者</th><td>(.+?)</td>', spec_tb_text)
            if match:
                val = match.group(1) if match.group(1) else None
            else:
                elems = soup.find_all("div", {"data-state" : re.compile(r'繪者：')})
                for elem in elems:
                    match = re.search('繪者：([^<]+)?', elem["data-state"])
                    if match:
                        val = match.group(1) if match.group(1) else None
                val = val.strip() if val else val'''
                    
        pattern = re.compile(r'APOLLO\_STATE')
        script = soup.find("script", text=pattern)
        if script:
            str_start = '繪者\\u003c/'
            str_end = '\\u003c/'
            if str_start in script.text:
                str_content = script.text[script.text.index(str_start):]
                str_content = str_content.replace(str_start, '')
                str_content = str_content[:str_content.index(str_end)]
                str_content = str_content[str_content.rindex('>')+1:]
                return str_content.strip()
            
            match = re.search(r'>繪者：(.+?)\\u003c', script.text)
            if match:
                val = match.group(1) if match.group(1) else None
                return val.strip()
            
        return val
        
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
