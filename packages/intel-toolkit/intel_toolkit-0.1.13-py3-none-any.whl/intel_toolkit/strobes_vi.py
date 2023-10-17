import re
import json
import httpx as requests
from rich import print
from functools import cache

class consult:
    def __init__(self):
        self.url_api_strobes = 'https://intel.strobes.co/api/vulnerabilities'

    def __check_cve_string(self, cve):
        return re.search('CVE-\d{4}-\d{4,7}', cve)
    
    @cache
    def get_vuln_id_info(self, vulnid):
        vulnid = vulnid.upper()
        if self.__check_cve_string(vulnid):
            url = f'{self.url_api_strobes}/{vulnid}'
        else:
            msg = {
                "error": 'CVE Model Error',
                "received": vulnid,
                "model_example": 'CVE-2000-0000000',
                "match_regex": 'CVE-\d{4}-\d{4,7}'
            }
            print(msg)
            exit(1)
        try:
            r = requests.get(url=url, timeout=50)
            return r.json()
        except:
            return {'error': 'Error API StribesVI'}
        
    @cache
    def check_vuln_has_patch(self, vulnid):
        vulnid_data = self.get_vuln_id_info(vulnid)
        try:
            return vulnid_data.get('patches').get('patch_available')
        except:
            return False

    @cache
    def get_refs_vuln_patch(self, vulnid):
        vulnid_data = self.get_vuln_id_info(vulnid)
        return vulnid_data.get('patches').get('references')

    @cache
    def check_vuln_is_zeroday(self, vulnid):
        vulnid_data = self.get_vuln_id_info(vulnid)
        try:
            return vulnid_data.get('zeroday').get('is_zeroday')
        except:
            return False
    
    @cache
    def get_refs_vuln_zeroday(self, vulnid):
        vulnid_data = self.get_vuln_id_info(vulnid)
        return vulnid_data.get('zeroday').get('references')

    @cache
    def check_vuln_has_exploit(self, vulnid):
        vulnid_data = self.get_vuln_id_info(vulnid)
        try:
            return vulnid_data.get('exploits').get('exploit_available')
        except:
            return False
    
    @cache
    def get_refs_vuln_exploits(self, vulnid):
        vulnid_data = self.get_vuln_id_info(vulnid)
        return vulnid_data.get('exploits').get('references')
    
    @cache
    def get_cwes(self, vulnid):
        vulnid_data = self.get_vuln_id_info(vulnid)
        return vulnid_data.get('taxonomy').get('cwe')
    
    @cache
    def get_owasp_top_10(self, vulnid):
        owasp = {}
        vulnid_data = self.get_vuln_id_info(vulnid)
        if vulnid_data.get('taxonomy').get('owasp_2021'):
            owasp['owasp_2021'] = vulnid_data.get('taxonomy').get('owasp_2021')
        if vulnid_data.get('taxonomy').get('owasp_2007'):
            owasp['owasp_2007'] = vulnid_data.get('taxonomy').get('owasp_2007')
        if vulnid_data.get('taxonomy').get('owasp_2004'):
            owasp['owasp_2004'] = vulnid_data.get('taxonomy').get('owasp_2004')
        
        return owasp