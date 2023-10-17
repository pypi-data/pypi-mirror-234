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

class TcsbParser(BaseParser):
    def __init__(self):
        self._ecid = 8
        self._ecpid = None
    def get_ec_popidx(self):
        return 90
    def is_target_page(self, url):
        is_book = False
        ecpid = None
        match = re.search('www\.tcsb\.com\.tw\/salepage\/index\/(\d+)?', url.lower())
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
        headers = utility.gen_spider_headers(user_agent, referer='https://www.tcsb.com.tw/')
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
        
        # 要求商品資訊 ajax api --> https://www.tcsb.com.tw/webapi/SalePageV2/GetSalePageAdditionalInfo/32014/5425798?source=1&v=0
        url = f'https://www.tcsb.com.tw/webapi/SalePageV2/GetSalePageAdditionalInfo/32014/{self._ecpid}?source=1&v=0'
        res = reqss.get(url, headers=headers, timeout=60)
        res.connection.close()
        pure_html = res.text
        json_data = None
        try:
            json_data = json.loads(pure_html)
        except ValueError: 
            print('#Decoding JSON has failed')
        
        
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
            prd['Desc'] = self._extract_desc(json_data)
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
        #elem = json_data['Data']['MoreInfo']['SaleProduct_Title']
        #val = elem
        val = soup.select_one('h1.salepage-title').text.strip()
        return val
    
    def _extract_url(self, soup):
        val = None
        #elem = json_data['Data']['Id']
        #val = f'https://www.tcsb.com.tw/SalePage/Index/{str(elem)}'
        script = soup.find("script", text=re.compile(r'window.ServerRenderData\["SalePageIndexViewModel"\]'))
        txt = script.text.replace('\r\n','')
        p = re.compile('.*window.ServerRenderData\["SalePageIndexViewModel"\] = (.*?);')
        m = p.match(txt)
        if m:
            info = json.loads(m.groups()[0])
            val = f'https://www.tcsb.com.tw/SalePage/Index/{str(info["Id"])}'
        return val
    
    def _extract_imgurl(self, soup):
        val = None
        #elem = json_data['Data']['Id']
        #val = f'https://diz36nn4q02zr.cloudfront.net/webapi/imagesV3/Original/SalePage/{str(elem)}/0/135704?v=1'
        script = soup.find("script", text=re.compile(r'window.ServerRenderData\["SalePageIndexViewModel"\]'))
        txt = script.text.replace('\r\n','')
        p = re.compile('.*window.ServerRenderData\["SalePageIndexViewModel"\] = (.*?);')
        m = p.match(txt)
        if m:
            info = json.loads(m.groups()[0])
            if info['ImageList']:
                imgurl = info['ImageList'][0]['PicUrl']
                val = "https:" + imgurl if 'https:' not in imgurl else imgurl
        return val
    
    def _extract_imgurl_list(self, soup):
        val = None
        script = soup.find("script", text=re.compile(r'window.ServerRenderData\["SalePageIndexViewModel"\]'))
        txt = script.text.replace('\r\n','')
        p = re.compile('.*window.ServerRenderData\["SalePageIndexViewModel"\] = (.*?);')
        m = p.match(txt)
        if m:
            info = json.loads(m.groups()[0])
            pics = []
            for pic in info['ImageList']:
                imgurl = pic['PicUrl']
                imgurl_fix = "https:" + imgurl if 'https:' not in imgurl else imgurl
                pics.append(imgurl_fix)
            val = ','.join(pics)
        return val

    def _extract_ecpid(self, soup):
        val = None
        #elem = json_data['Data']['Id']
        #val = str(elem)
        script = soup.find("script", text=re.compile(r'window.ServerRenderData\["SalePageIndexViewModel"\]'))
        txt = script.text.replace('\r\n','')
        p = re.compile('.*window.ServerRenderData\["SalePageIndexViewModel"\] = (.*?);')
        m = p.match(txt)
        if m:
            info = json.loads(m.groups()[0])
            val = info['Id']
        return str(val)

    def _extract_eccatlog(self, soup):
        val = None
        elems = soup.select('div.location-bar ol.breadcrumb li.breadcrumb-li span')
        cats = [span.text for span in elems[1:]]
        val = '>'.join(cats)
        return val

    def _extract_author(self, soup):
        val = None
        #elems = json_data['Data']['NotKeyPropertyList']
        #for obj in elems:
        #    if obj['Title'] == '作者' or obj['Title'] == '作 者':
        #        if obj['ContentList']:
        #            val = ','.join(obj['ContentList'])
        #            break
        
        #json檔常載不到，不可信任，改用取script
        script = soup.find("script", text=re.compile(r'window.ServerRenderData\["SalePageIndexViewModel"\]'))
        txt = script.text.replace('\r\n','')
        p = re.compile('.*window.ServerRenderData\["SalePageIndexViewModel"\] = (.*?);')
        m = p.match(txt)
        if m:
            info = json.loads(m.groups()[0])
            in_soup = BeautifulSoup(info['SubDescript'],features="lxml")
            li = in_soup.find('li', text=re.compile(r'作者'))
            if li:
                val = li.text.replace('作者：','').replace('作者:','').strip()
                if '/' in val:
                    val = val.split('/')[0]
        return val

    def _extract_isbn(self, soup):
        val = None
        #elems = json_data['Data']['NotKeyPropertyList']
        #for obj in elems:
        #    if obj['Title'] == 'ISBN':
        #        if obj['ContentList']:
        #            val = obj['ContentList'][0]
        #            break
        script = soup.find("script", text=re.compile(r'window.ServerRenderData\["SalePageIndexViewModel"\]'))
        txt = script.text.replace('\r\n','')
        p = re.compile('.*window.ServerRenderData\["SalePageIndexViewModel"\] = (.*?);')
        m = p.match(txt)
        if m:
            info = json.loads(m.groups()[0])
            in_soup = BeautifulSoup(info['SubDescript'],features="lxml")
            li = in_soup.find('li', text=re.compile(r'ISBN'))
            if li:
                val = li.text.replace('ISBN：','').replace('ISBN:','').strip()
        return val

    def _extract_desc(self, json_data):
        val = None
        if json_data:
            elem = json_data['Data']['MoreInfo']['SaleProductDesc_Content']
            if elem:
                val = html.escape(elem)[:8000]
        return val

    def _extract_translator(self, soup):
        val = None
        #elems = json_data['Data']['NotKeyPropertyList']
        #for obj in elems:
        #    if obj['Title'] == '譯者':
        #        if obj['ContentList']:
        #            val = ','.join(obj['ContentList'])
        #            break
        script = soup.find("script", text=re.compile(r'window.ServerRenderData\["SalePageIndexViewModel"\]'))
        txt = script.text.replace('\r\n','')
        p = re.compile('.*window.ServerRenderData\["SalePageIndexViewModel"\] = (.*?);')
        m = p.match(txt)
        if m:
            info = json.loads(m.groups()[0])
            in_soup = BeautifulSoup(info['SubDescript'],features="lxml")
            li = in_soup.find('li', text=re.compile(r'譯者'))
            if li:
                val = li.text.replace('譯者：','').replace('譯者:','').strip()
        return val

    def _extract_pub_date(self, soup):
        val = None
        #elems = json_data['Data']['NotKeyPropertyList']
        #for obj in elems:
        #    if obj['Title'] == '出版日期':
        #        if obj['ContentList']:
        #            val = obj['ContentList'][0]
        #            break
        script = soup.find("script", text=re.compile(r'window.ServerRenderData\["SalePageIndexViewModel"\]'))
        txt = script.text.replace('\r\n','')
        p = re.compile('.*window.ServerRenderData\["SalePageIndexViewModel"\] = (.*?);')
        m = p.match(txt)
        if m:
            info = json.loads(m.groups()[0])
            in_soup = BeautifulSoup(info['SubDescript'],features="lxml")
            li = in_soup.find('li', text=re.compile(r'出版日'))
            if li:
                val = li.text.replace('出版日：','').replace('出版日期:','').strip()
        if val:
            val = val.replace('-','/').replace('／','/')
            if '/' not in val:
                if len(val) == 6:
                    val = val[:4] + '/' + val[4:-1] + '/' + val[-1:]
                elif len(val) >= 7:
                    val = val[:4] + '/' + val[4:-2] + '/' + val[-2:] 
        if val and '版' in val: #發現有「2018/16版」的格式
            val = None
        return val

    def _extract_publisher(self, soup):
        val = None
        #elems = json_data['Data']['NotKeyPropertyList']
        #for obj in elems:
        #    if obj['Title'] == '出版社':
        #        if obj['ContentList']:
        #            val = obj['ContentList'][0]
        #            break
        script = soup.find("script", text=re.compile(r'window.ServerRenderData\["SalePageIndexViewModel"\]'))
        txt = script.text.replace('\r\n','')
        p = re.compile('.*window.ServerRenderData\["SalePageIndexViewModel"\] = (.*?);')
        m = p.match(txt)
        if m:
            info = json.loads(m.groups()[0])
            in_soup = BeautifulSoup(info['SubDescript'],features="lxml")
            li = in_soup.find('li', text=re.compile(r'出版社'))
            if li:
                val = li.text.replace('出版社：','').replace('出版社:','').strip()
        return val

    def _extract_oriprice(self, soup):
        val = None
        elem = soup.select_one('div[data-ng-if="!SalePageIndexCtrl.SelectedSkuSuggestPrice"] span')
        if elem:
            val = elem.text.replace('NT$','').replace(',','').strip()
        return val

    def _extract_price(self, soup):
        val = None
        elem = soup.find('meta', itemprop="price")
        val = int(float(elem['content']))
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

    