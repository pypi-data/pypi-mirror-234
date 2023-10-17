import httpx as requests
from rich import print
from functools import cache

class consult:
    def __init__(self):
        self.url_exploitations_feed = 'https://inthewild.io/_next/data/UMG9URuOvdt1CxoJXmUax/feed.json'
        self.url_exploits_feed = 'https://inthewild.io/api/exploits?limit=1000'
        self.url_exploitation_get_vuln_id = 'https://inthewild.io/api/exploitations' # ?query=CVE-2022-22965
        self.url_exploit_get_vuln_id = 'https://inthewild.io/api/exploits' # ?query=CVE-2022-22965
        self.urls = {
            "url_exploitations_feed": 'https://inthewild.io/_next/data/UMG9URuOvdt1CxoJXmUax/feed.json',
            "url_exploits_feed": 'https://inthewild.io/api/exploits?limit=1000',
            "url_exploitation_get_vuln_id": 'https://inthewild.io/api/exploitations',
            "url_exploit_get_vuln_id": 'https://inthewild.io/api/exploits'
        }
    
    @cache
    def get_vuln_id_info(self, type, vulnid=None):
        params = {}
        url = self.urls.get(type)
        if vulnid == None:
            if type == 'feed_exploits': url = self.url_exploits_feed
            if type == 'feed_exploitation': url = self.url_exploitations_feed
        else:
            if type == 'exploitation': url = self.url_exploitation_get_vuln_id
            if type == 'exploits': url = self.url_exploit_get_vuln_id

            params = {
                "query": vulnid
            }
        
        try:
            r = requests.get(url=url, params=params, timeout=50)
            return r.json()
        except:
            return {'error': 'Error API InTheWild'}
        

    @cache
    def exploitations_feed(self):
        return self.get_vuln_id_info(type='feed_exploitation')
    
    @cache
    def exploits_feed(self):
        return self.get_vuln_id_info(type='feed_exploits')
    
    @cache
    def get_exploitation_vuln_id(self, vulnid):
        return self.get_vuln_id_info(type='exploitation', vulnid=vulnid)
    
    @cache
    def get_exploit_vuln_id(self, vulnid):
        return self.get_vuln_id_info(type='exploits', vulnid=vulnid)
    
    @cache
    def get_vuln_total_exploits(self, vulnid):
        return len(self.get_exploit_vuln_id(vulnid))
    
    @cache
    def get_vuln_total_exploitation(self, vulnid):
        return len(self.get_exploitation_vuln_id(vulnid))