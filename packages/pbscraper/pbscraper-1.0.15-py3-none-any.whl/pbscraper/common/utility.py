import hashlib
import random
import requests
import logging
import re

class utility:

    def gen_str_hash(value):
        hash_object = hashlib.md5(value.encode())
        return hash_object.hexdigest()

    def gen_random_useragent():
        uas = [ 
            'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
        ]

        idx = random.randint(0,len(uas)-1)
        return uas[idx]

    def gen_spider_headers(user_agent, referer):
        headers = {
            'User-Agent': user_agent, 
            'referer': referer,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,en;q=0.9',
            'Pragma': 'no-cache'
        }
        return headers

        
    def gen_random_proxy(): 
        '''
        需要月付買proxy
        '''
        res = requests.get('https://gimmeproxy.com/api/getProxy?get=true&cookies=true&country=US&supportsHttps=true&maxCheckPeriod=1800&minSpeed=10')
        data = res.json()
        proxy = {
            "https": "https://" + data['ipPort']
        }
        return proxy
        
    def retry_request(url): #改統一含session，不用 
        html = None
        #for i in range(10):
        try:
            user_agent = self._get_useragent()
            headers = {'User-Agent': user_agent, 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
            proxies = {
                "http": "http://178.210.129.11:8080",
                "https": "https://194.44.61.10:43485",
            }
            res = requests.get(url, headers=headers)
            html = res.text
            res.connection.close()
        except Exception as e:
            print(f'**** error: {e}')
            logging.exception("Something awful happened!")
        #except SocketError as e:
        #    if e.errno != errno.ECONNRESET:
        #        raise # Not error we are looking for
            #if i >= 9:
            #    print(f'**** error: conn pool err cant open {url}')
            #else:
            #    time.sleep(1)
            #    print(f'**** error: sleep 1 sec and retry {i} times')
        #else:
        #    break
        return html

    def remove_emojis_str(text):
        #text = u'This dog \U0001f602'
        #print(text) # with emoji
        emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags=re.UNICODE)
        #print(emoji_pattern.sub(r'', text)) # no emoji
        return emoji_pattern.sub(r'', text)

    def filter_invalid_str(text):
        """
        过滤非BMP字符, refer:http://ladder1984.github.io/post/emojipythonmysql-utf8mb4%E4%B8%8Eutf/
        """
        try:
            # UCS-4
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            # UCS-2
            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

        return highpoints.sub(u'', text)
    