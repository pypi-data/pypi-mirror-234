from .books_parser import BooksParser
from .kingstone_parser import KingstoneParser
from .sanmin_parser import SanminParser
from .eslite_parser import EsliteParser
#from Parser.pchome_parser import PchomeParser
from .momo_parser import MomoParser
from .caves_parser import CavesParser
from .tcsb_parser import TcsbParser

from .yahoo_parser import YahooParser
from .udn_parser import UdnParser

from .taaze_parser import TaazeParser
from .rakuten_parser import RakutenParser
from .tenlong_parser import TenlongParser
#from Parser.linking_parser import LinkingParser
from .cite_parser import CiteParser
from .cwbook_parser import CwbookParser
from .suncolor_parser import SuncolorParser

class ParserFactory():
    _parsers = [
        BooksParser(),
        KingstoneParser(),
        SanminParser(),
        EsliteParser(),
        #PchomeParser(),
        MomoParser(),
        CavesParser(),
        TcsbParser(),
        
        YahooParser(),
        UdnParser(),
        
        TaazeParser(),
        RakutenParser(),
        TenlongParser(),
        #LinkingParser(),
        CiteParser(),
        CwbookParser(),
        SuncolorParser(),
        
    ]
    def __init__(self):
        pass
    
    def get_parser(self, url):
        for p in self._parsers:
            if p.is_target_page(url):
                return p
        return None
    
    
    