import abc

class BaseUrlsCrawler(abc.ABC):
    _next_pg_url = None
    def __init__(self):
        pass
    @abc.abstractmethod
    def is_target_list(self, url):
        pass
    @abc.abstractmethod
    def scrape_list_to_urls(self, url, res):
        pass
    @abc.abstractmethod
    def get_next_pg_after_scraped(self):
        pass