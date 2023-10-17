from .books_urls_crawler import BooksUrlsCrawler
from .kingstone_urls_crawler import KingstoneUrlsCrawler
from .sanmin_urls_crawler import SanminUrlsCrawler
from .eslite_urls_crawler import EsliteUrlsCrawler
#from Crawler.pchome_urls_crawler import PchomeUrlsCrawler
from .momo_urls_crawler import MomoUrlsCrawler
from .caves_urls_crawler import CavesUrlsCrawler
from .tcsb_urls_crawler import TcsbUrlsCrawler #TODO:2019/6/10 - 發現ajax失效
#from Crawler.cwbook_urls_crawler import CwbookUrlsCrawler
from .yahoo_urls_crawler import YahooUrlsCrawler
from .udn_urls_crawler import UdnUrlsCrawler
#from Crawler.silkbook_urls_crawler import SilkbookUrlsCrawler
from .taaze_urls_crawler import TaazeUrlsCrawler
from .rakuten_urls_crawler import RakutenUrlsCrawler
from .tenlong_urls_crawler import TenlongUrlsCrawler
#from Crawler.linking_urls_crawler import LinkingUrlsCrawler
from .cite_urls_crawler import CiteUrlsCrawler
#from .kinokuniya_urls_crawler import KinokuniyaUrlsCrawler
from .cwbook_urls_crawler import CwbookUrlsCrawler
from .suncolor_urls_crawler import SuncolorUrlsCrawler

class UrlsCrawlerFactory():
    _crawlers = [
        BooksUrlsCrawler(),
        KingstoneUrlsCrawler(),
        SanminUrlsCrawler(),
        EsliteUrlsCrawler(),
        #PchomeUrlsCrawler(),
        MomoUrlsCrawler(),
        CavesUrlsCrawler(),
        TcsbUrlsCrawler(),
        #CwbookUrlsCrawler(),
        YahooUrlsCrawler(),
        UdnUrlsCrawler(),
        #SilkbookUrlsCrawler(),
        TaazeUrlsCrawler(),
        RakutenUrlsCrawler(),
        TenlongUrlsCrawler(),
        #LinkingUrlsCrawler(),
        CiteUrlsCrawler(),
        #KinokuniyaUrlsCrawler(),
        CwbookUrlsCrawler(),
        SuncolorUrlsCrawler(),
        
    ]
    def __init__(self):
        pass
    
    def get_crawler(self, url):
        for c in self._crawlers:
            if c.is_target_list(url):
                return c
        return None
    