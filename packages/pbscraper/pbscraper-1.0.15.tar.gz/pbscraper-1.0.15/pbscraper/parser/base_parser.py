import abc
import datetime

class BaseParser(abc.ABC):
    _ecid = -1
    def __init__(self):
        if _ecid == -1:
            raise ValueError('you need to specify _ecid when __init__()')
    @abc.abstractmethod
    def get_ec_popidx(self):
        pass
    @abc.abstractmethod
    def is_target_page(self, url):
        pass
    @abc.abstractmethod
    def scrape_page_to_strprd(self, url, res):
        pass
    def verify_strprd_to_verprd(self, prd):
        # 必要欄都要驗證
        price = int(prd['Price']) if str(prd['Price']).isdigit() else None
        if price is None:
            raise ValueError('price is none')
        oriprice = int(prd['OriPrice']) if str(prd['OriPrice']).isdigit() else None
        if oriprice is None:
            raise ValueError('oriprice is none') # ua若用非桌機會取不到oriprice
        if not prd['Name']:
            raise ValueError('name is none')
        if not prd['Url']:
            raise ValueError('url is none')
        if not prd['ImgUrl']:
            raise ValueError('imgurl is none')
        if not prd['Author']:
            print('# author is none')
        if not prd['ISBN']:
            print('# isbn is none')
        if not prd['ECPID']:
            raise ValueError('ecpid is none')
        if not prd['ECCatlog']:
            print('#eccatlog is none')
        if not prd['Desc']:
            print('# desc is none')
        if not prd['PublishDate']:
            print('# pubdate is none')
        if not prd['Publisher']:
            print('# publisher is none')
        
        # 欄位統一format 檢查&轉換
        if prd['ImgUrlList']:
            imgs = prd['ImgUrlList'].split(',')
            if len(imgs) > 20:
                prd['ImgUrlList'] = ','.join(imgs[:20])
        if prd['ISBN']:
            prd['ISBN'] = prd['ISBN'].replace('ISBN:', '').replace('-', '')
        
        verprd = {
            'ID': str(prd['ECID']) + '_' + prd['ECPID'],
            'Name': prd['Name'],
            'Url': prd['Url'],
            'ImgUrl': prd['ImgUrl'],
            'ImgUrlList': prd['ImgUrlList'],
            'VideoUrl': prd['VideoUrl'],
            'VideoUrlList': prd['VideoUrlList'],
            'OriPrice': oriprice,
            'Price': price,
            'Author': prd['Author'],
            'ISBN': prd['ISBN'],
            'ECID': prd['ECID'],
            'ECPID': prd['ECPID'],
            'ECCatlog': prd['ECCatlog'],
            'isOnShelf': prd['isOnShelf'],
            'isEnable': prd['isEnable'],
            'Desc': prd['Desc'],
            'ModifyTime': prd['ModifyTime'],
            'CreateTime': prd['CreateTime'],
            'PopIdx': prd['PopIdx'],
            'CatID': prd['CatID'],
            'Translator': prd['Translator'],
            'PublishDate': prd['PublishDate'],
            
            'Publisher': prd['Publisher'],
            'Painter': prd['Painter'],
            'OriginName': prd['OriginName'],
            'Summary': prd['Summary'],
            'ISBN10': prd['ISBN10'],
            'ISBNADD': prd['ISBNADD'],
            'BookType': prd['BookType'],
            'Text1': prd['Text1'],
            'Text2': prd['Text2'],
            'Text3': prd['Text3'],
            'Keyword1': prd['Keyword1'],
            'Keyword2': prd['Keyword2'],
            'Keyword3': prd['Keyword3'],
        }
        return verprd
    
    
    