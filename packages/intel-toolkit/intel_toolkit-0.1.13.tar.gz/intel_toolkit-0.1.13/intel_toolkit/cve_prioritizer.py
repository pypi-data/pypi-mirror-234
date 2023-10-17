import httpx as requests
from httpx import ConnectError
from uuid import uuid4
from operator import itemgetter, attrgetter
from rich import print
import re
import json
from functools import cache


class consult:
    def __init__(self, api_key_nvd, cvss_score=0.2, epss_score=6.0, semaphore=5) -> None:
        self.nvd_key = api_key_nvd
        self.cvss_score = cvss_score
        self.epss_score = epss_score
        self.semaphore = semaphore
        self.PRIORITIES_LIST = []
        self.NIST_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.EPSS_URL = "https://api.first.org/data/v1/epss"

    def __check_cve_string(self, cve):
        return re.search('CVE-\d{4}-\d{4,7}', cve)
    
    def __model_append(self, priority_number, cve_id, priority, epss, cvss_num, cvss_version, cvss_severity, cisa_key, status_cve):
        model = {
            "cve": cve_id,
            "priority": priority,
            "priority_number": priority_number,
            "epss": epss,
            "cvss_baseScore": cvss_num,
            "cvss_version": cvss_version,
            "severity": cvss_severity,
            "cisa_key": cisa_key,
            "status": status_cve
        }
        self.PRIORITIES_LIST.append(model)
        self.PRIORITIES_LIST = sorted(self.PRIORITIES_LIST, key=lambda x: x['priority_number'])


    def __model_get(self, cve):
        data = [x for x in self.PRIORITIES_LIST if x.get('cve') == cve]
        if len(data) > 0:
            return data[0]
        else:
            return None

    @cache
    def __nist_check(self, cve_id):
        try:
            params = {
                "cveId": cve_id
            }

            header = {'apiKey': f'{self.nvd_key}'}

            # Check if API has been provided
            if self.nvd_key:
                nvd_response = requests.get(self.NIST_BASE_URL, headers=header, params=params, timeout=50)
            else:
                nvd_response = requests.get(self.NIST_BASE_URL, params=params, timeout=50)

            nvd_status_code = nvd_response.status_code

            if nvd_status_code == 200:
                cisa_kev = False
                if nvd_response.json().get("totalResults") > 0:
                    for unique_cve in nvd_response.json().get("vulnerabilities"):

                        # Check if present in CISA's KEV
                        if unique_cve.get("cve").get("cisaExploitAdd"):
                            cisa_kev = True

                        # Collect CVSS Data
                        if unique_cve.get("cve").get("metrics").get("cvssMetricV31"):
                            for metric in unique_cve.get("cve").get("metrics").get("cvssMetricV31"):
                                results = {"cvss_version": "CVSS 3.1",
                                        "cvss_baseScore": float(metric.get("cvssData").get("baseScore")),
                                        "cvss_severity": metric.get("cvssData").get("baseSeverity"),
                                        "cisa_kev": cisa_kev, "status": unique_cve.get("cve").get("vulnStatus")}
                                return results
                        elif unique_cve.get("cve").get("metrics").get("cvssMetricV30"):
                            for metric in unique_cve.get("cve").get("metrics").get("cvssMetricV30"):
                                results = {"cvss_version": "CVSS 3.0",
                                        "cvss_baseScore": float(metric.get("cvssData").get("baseScore")),
                                        "cvss_severity": metric.get("cvssData").get("baseSeverity"),
                                        "cisa_kev": cisa_kev, "status": unique_cve.get("cve").get("vulnStatus")}
                                return results
                        elif unique_cve.get("cve").get("metrics").get("cvssMetricV2"):
                            for metric in unique_cve.get("cve").get("metrics").get("cvssMetricV2"):
                                results = {"cvss_version": "CVSS 2.0",
                                        "cvss_baseScore": float(metric.get("cvssData").get("baseScore")),
                                        "cvss_severity": metric.get("cvssData").get("baseSeverity"),
                                        "cisa_kev": cisa_kev, "status": unique_cve.get("cve").get("vulnStatus")}
                                return results
                        elif unique_cve.get("cve").get("vulnStatus") == "Awaiting Analysis":
                            results = {"cvss_version": "",
                                        "cvss_baseScore": 0.0,
                                        "cvss_severity": "",
                                        "cisa_kev": False, "status": unique_cve.get("cve").get("vulnStatus")}
                            return results
                        
                        results = {"cvss_version": "",
                                            "cvss_baseScore": 0.0,
                                            "cvss_severity": "",
                                            "cisa_kev": False, "status": unique_cve.get("cve").get("vulnStatus")}
                        return results
                else:
                    results = {"cvss_version": "",
                                            "cvss_baseScore": 0.0,
                                            "cvss_severity": "",
                                            "cisa_kev": False, "status": f"{cve_id:<18}Not Found in NIST NVD.", "error": 404}
                    return results
            else:
                results = {"cvss_version": "",
                                            "cvss_baseScore": 0.0,
                                            "cvss_severity": "",
                                            "cisa_kev": False, "status": f"{cve_id:<18}Error code {nvd_status_code}", "error": 503}
                return results
        except ConnectError:
            print(f"Unable to connect to NIST NVD, Check your Internet connection or try again")
            return None
        
    @cache
    def __epss_check(self, cve_id):
        try:
            params = {
                "cve": cve_id
            }

            epss_response = requests.get(self.EPSS_URL, params=params, timeout=50)
            epss_status_code = epss_response.status_code

            if epss_status_code == 200:
                if epss_response.json().get("total") > 0:
                    for cve in epss_response.json().get("data"):
                        results = {"epss": float(cve.get("epss")),
                                "percentile": int(float(cve.get("percentile"))*100),
                                "status": True}
                        return results
                else:
                    results = {"epss": 0.0,
                                "percentile": 0.0,
                                "status": False}
                    return results
            else:
                results = {"epss": 0.0,
                                "percentile": 0.0,
                                "status": False}
                return results
        except requests.exceptions.ConnectionError:
            # print(f"Unable to connect to EPSS, Check your Internet connection or try again")
            return None
    
    def __del_cve_list(self, cve):
        for num in range(0,len(self.PRIORITIES_LIST)):
            if self.PRIORITIES_LIST[num].get('cve') == cve:
                self.PRIORITIES_LIST.pop(num)

    @cache
    def calc_priority_cve(self, cve_id, cache_flag=0):
        nist_result = self.__nist_check(cve_id)
        self.__del_cve_list(cve=cve_id)
        epss_result = self.__epss_check(cve_id)
        if epss_result.get('status') == None:
            return self.PRIORITIES_LIST

        # try:
        if nist_result.get("cisa_kev"):
            self.__model_append(0, cve_id, 'Priority 1+', epss_result.get('epss'),
                            nist_result.get('cvss_baseScore'), nist_result.get('cvss_version'),
                            nist_result.get('cvss_severity'), 'TRUE', nist_result.get('status'))
        elif nist_result.get("cvss_baseScore") >= self.cvss_score:
            if epss_result.get("epss") >= self.epss_score:
                self.__model_append(1, cve_id, 'Priority 1', epss_result.get('epss'),
                                nist_result.get('cvss_baseScore'), nist_result.get('cvss_version'),
                                nist_result.get('cvss_severity'), 'FALSE', nist_result.get('status'))
            else:
                self.__model_append(2, cve_id, 'Priority 2', epss_result.get('epss'),
                                nist_result.get('cvss_baseScore'), nist_result.get('cvss_version'),
                                nist_result.get('cvss_severity'), 'FALSE', nist_result.get('status'))
        else:
            if epss_result.get("epss") >= self.epss_score:
                self.__model_append(3, cve_id, 'Priority 3', epss_result.get('epss'),
                                nist_result.get('cvss_baseScore'), nist_result.get('cvss_version'),
                                nist_result.get('cvss_severity'), 'FALSE', nist_result.get('status'))
            else:
                self.__model_append(4, cve_id, 'Priority 4', epss_result.get('epss'),
                                nist_result.get('cvss_baseScore'), nist_result.get('cvss_version'),
                                nist_result.get('cvss_severity'), 'FALSE', nist_result.get('status'))
        # except (TypeError, AttributeError):
        
        #     pass
        
        return self.PRIORITIES_LIST
    
    def process_list(self, cves_list):
        if type(cves_list) == list:
            for cve in cves_list:
                if self.__check_cve_string(cve=cve):
                    result = self.calc_priority_cve(cve_id=cve)
                    if self.__model_get(cve=cve):
                        while self.__model_get(cve=cve).get('error') != None:
                            result = self.calc_priority_cve(cve_id=cve, cache_flag=str(uuid4()))
        else:
            return {'error': 'no list type'}
        
        return self.PRIORITIES_LIST