import json
from pprint import pprint
import requests
import time
import re
import socket
import sys
from OTXv2 import OTXv2, IndicatorTypes
from stix2 import Indicator
import json
from pandas.io.json import json_normalize
import requests
import urllib3
from base64 import b64encode

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ioc():
    def __init__(self, api_token = "", limit = 10):
        self.api_token = api_token
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        self.limit = limit
        self.json_data = {
            'api_token': self.api_token,
            'limit': self.limit,
        }

    def daily_ioc(self,):
        if self.api_token == "":
            return print("Please Use Your API Token")
        if self.limit > 100:
            return print("Limit can not exceed 100")

        return requests.post(
            'https://ioc.threatmonit.io/api/daily-ioc/',
            headers=self.headers,
            json=self.json_data,
        ).json()

    def QRadarIntegration(self, 
                        import_data,
                        qradar_auth_key,
                        qradar_server,
                        ):  # sourcery skip: avoid-builtin-shadow
        
        def createTable(table_name, type):
            try:
                table_parameters = {
                    "name": table_name,
                    "element_type": type
                }
                requests.request("POST", validate_refSet_url, headers=self.QRadar_headers, params=table_parameters, verify=False)
            except Exception as e:
                pprint(e)

        qradar_ref_set_list = [["ThreatmonIOC_IP", "IP"],["ThreatmonIOC_Domain", "ALNIC"],["ThreatmonIOC_MD5", "ALNIC"],["ThreatmonIOC_SHA256", "ALNIC"]]
        
        self.QRadar_headers = {
            'sec': qradar_auth_key,
            'content-type': "application/json"
        }
        
        for table in qradar_ref_set_list:
            validate_refSet_url = (
                f"https://{qradar_server}/api/reference_data/tables/{table[0]}"
            )
            validate_response = requests.request("GET", validate_refSet_url, headers=self.QRadar_headers, verify=False)
            print(time.strftime("%H:%M:%S") + " -- " + "Validating if reference tables " + table[0] + " exists")
            
            if validate_response.status_code == 200:
                print(time.strftime("%H:%M:%S") + " -- " + "Validating reference tables " + table[0] + " - (Success) ")
            else:
                print(time.strftime("%H:%M:%S") + " -- " + "QRadar Reference tables does not exist, Creating automaticly from ThreatmonIOC Service.")
                createTable(table[0],table[1])

        for qradar_ref_set in qradar_ref_set_list:
            QRadar_POST_url = f"https://{qradar_server}/api/reference_data/tables/bulk_load/{qradar_ref_set}"
        
            validate_response_data = validate_response.json()
            refSet_etype = (validate_response_data["element_type"])
            print(time.strftime("%H:%M:%S") + " -- " + "Identifying Reference tables " + qradar_ref_set + " element type")
            print(time.strftime("%H:%M:%S") + " -- " + "Reference tables element type = " + refSet_etype + " (Success) ")
            
            if qradar_ref_set == "ThreatmonIOC_IP":
                ip_list = [] 
                print (time.strftime("%H:%M:%S") + " -- " + "The QRadar Reference tables " + qradar_ref_set + " Element Type = \"IP\". Only IPs will be imported to QRadar and the other IOC types will be discarded")
                for iocs in import_data["entities"]:
                    for ioc in iocs["hashes"]:
                        if ioc["algorithm"] == "IPV4":
                            value = ioc["hash"]
                            ip_list.append(
                                {
                                    "IP":
                                        {
                                            "hash" : value,
                                            "source" : "Threatmon API"
                                        }
                                }
                            )
                    
                        if ioc["algorithm"] == "IPV6":
                            value = ioc["hash"]
                            ip_list.append(
                                {
                                    "IP":
                                        {
                                            "hash" : value,
                                            "source" : "Threatmon API"
                                        }
                                }
                            )
                
                qradar_response = requests.request("POST", QRadar_POST_url, data=ip_list, headers=self.QRadar_headers, verify=False)
                if qradar_response.status_code == 200:
                    print(time.strftime("%H:%M:%S") + " -- " + " (Finished) Imported IOCs to QRadar (Success)" )
                else:
                    print(time.strftime("%H:%M:%S") + " -- " + "Could not POST IOCs to QRadar (Failure)")
                    
            if qradar_ref_set == "ThreatmonIOC_MD5":
                MD5_list = [] 
                print (time.strftime("%H:%M:%S") + " -- " + "The QRadar Reference tables " + qradar_ref_set + " Element Type = \"MD5\". Only MD5 will be imported to QRadar and the other IOC types will be discarded")
                for iocs in import_data["entities"]:
                    for ioc in iocs["hashes"]:
                        if ioc["algorithm"] == "MD5":
                            value = ioc["hash"]
                            MD5_list.append(
                                {
                                    "MD5":
                                        {
                                            "hash" : value,
                                            "source" : "Threatmon API"
                                        }
                                }
                            )
                            
                qradar_response = requests.request("POST", QRadar_POST_url, data=MD5_list, headers=self.QRadar_headers, verify=False)
                if qradar_response.status_code == 200:
                    print(time.strftime("%H:%M:%S") + " -- " + " (Finished) Imported IOCs to QRadar (Success)" )
                else:
                    print(time.strftime("%H:%M:%S") + " -- " + "Could not POST IOCs to QRadar (Failure)")
                    
            if qradar_ref_set == "ThreatmonIOC_SHA256":
                sha256_list = [] 
                print (time.strftime("%H:%M:%S") + " -- " + "The QRadar Reference tables " + qradar_ref_set + " Element Type = \"SHA-256\". Only SHA-256 will be imported to QRadar and the other IOC types will be discarded")
                for iocs in import_data["entities"]:
                    for ioc in iocs["hashes"]:
                        if ioc["algorithm"] == "SHA-256":
                            value = ioc["hash"]
                            sha256_list.append(
                                {
                                    "SHA-256":
                                        {
                                            "hash" : value,
                                            "source" : "Threatmon API"
                                        }
                                }
                            )

                qradar_response = requests.request("POST", QRadar_POST_url, data=sha256_list, headers=self.QRadar_headers, verify=False)
                if qradar_response.status_code == 200:
                    print(time.strftime("%H:%M:%S") + " -- " + " (Finished) Imported IOCs to QRadar (Success)" )
                else:
                    print(time.strftime("%H:%M:%S") + " -- " + "Could not POST IOCs to QRadar (Failure)")

            if qradar_ref_set == "ThreatmonIOC_Domain":
                domain_list = [] 
                print (time.strftime("%H:%M:%S") + " -- " + "The QRadar Reference tables " + qradar_ref_set + " Element Type = \"Domain\". Only Domains will be imported to QRadar and the other IOC types will be discarded")
                for iocs in import_data["entities"]:
                    for ioc in iocs["hashes"]:
                        if ioc["algorithm"] == "Domain":
                            value = ioc["hash"]
                            domain_list.append(
                                {
                                    "Domain":
                                        {
                                            "hash" : value,
                                            "source" : "Threatmon API"
                                        }
                                }
                            )
                            
                qradar_response = requests.request("POST", QRadar_POST_url, data=domain_list, headers=self.QRadar_headers, verify=False)
                if qradar_response.status_code == 200:
                    print(time.strftime("%H:%M:%S") + " -- " + " (Finished) Imported IOCs to QRadar (Success)" )
                else:
                    print(time.strftime("%H:%M:%S") + " -- " + "Could not POST IOCs to QRadar (Failure)")
            
    def SentinelIntegration(self,
                            import_data,
                            bearerToken,
                            workspaceId,
                            systemName,
                            ):  # sourcery skip: avoid-builtin-shadow
        
        ioc_list = []
        api_url = f"https://sentinelus.azure-api.net/{workspaceId}/threatintelligence:upload-indicators?api-version=2022-07-01"
                        
        for iocs in import_data["entities"]:
            for ioc in iocs["hashes"]:
                if ioc["algorithm"] == "MD5":
                    hash = ioc["hash"]
                    indicator = Indicator(name="indicator",
                        pattern= f"[file:hashes.md5 = '{hash}']",
                        pattern_type="stix")
                    
                if ioc["algorithm"] == "SHA-1":
                    hash = ioc["hash"]
                    indicator = Indicator(name="indicator",
                        pattern= f"[file:hashes.sha1 = '{hash}']",
                        pattern_type="stix")
                    
                if ioc["algorithm"] == "SHA-256":
                    hash = ioc["hash"]
                    indicator = Indicator(name="indicator",
                        pattern= f"[file:hashes.sha256 = '{hash}']",
                        pattern_type="stix")
                    
                indicator = indicator.serialize(sort_keys=True)
                indicator = json.loads(indicator)
                ioc_list.append(indicator)

        request_body = {
            "sourcesystem": systemName,
            "value": ioc_list
        }
        
        headers = {
            'Authorization': bearerToken,
            'Content-Type': 'application/json',
        }
        
        try:
            microsof_api = requests.post(
                url=api_url,
                headers=headers,
                json=request_body,
            )
            if microsof_api.status_code == 200:
                print(time.strftime("%H:%M:%S") + " -- " + " (Finished) Imported IOCs to Sentinel (Success)" )
            else:
                print(time.strftime("%H:%M:%S") + " -- " + "Could not POST IOCs to Sentinel (Failure)")
        except Exception as e:
            print(e)
            
    def CrowdStrikeIntegration(self,
                               bearerToken,
                               import_data):
        # sourcery skip: avoid-builtin-shadow
        
        api_url = "https://api.crowdstrike.com/iocs/entities/indicators/v1"
        
        ioc_list = []
        
        headers = {
            'Authorization': bearerToken,
            'Content-Type': 'application/json',
        }
        
        for iocs in import_data["entities"]:
            for ioc in iocs["hashes"]:
                if ioc["algorithm"] == "MD5":
                    value = ioc["hash"]
                    type = "md5"
                    
                if ioc["algorithm"] == "SHA-256":
                    value = ioc["hash"]
                    type = "sha256"
                    
                if ioc["algorithm"] == "Domain":
                    type = "domain"
                    value = ioc["hash"]
                    
                if ioc["algorithm"] == "IPV4":
                    type = "ipv4"
                    value = ioc["hash"]
                    
                if ioc["algorithm"] == "IPV6":
                    type = "ipv6"
                    value = ioc["hash"]
                    
                ioc_dict = {
                    "type": type,
                    "value": value,
                    "policy": "none",
                    "apply_globally": False,
                }
                
                ioc_list.append(ioc_dict)
            
        response_data = {
            "indicators" : ioc_list,
        }
            
        try:
            crowdstrike = requests.post(
                url=api_url,
                headers=headers,
                json=response_data,
            )
            
            if crowdstrike.status_code == 200:
                print(time.strftime("%H:%M:%S") + " -- " + " (Finished) Imported IOCs to CrowdStrike (Success)" )
            else:
                print(time.strftime("%H:%M:%S") + " -- " + "Could not POST IOCs to CrowdStrike (Failure)")
                
        except Exception as e:
            print(e)

    def SplunkIntegration(self, token, import_data):
        # sourcery skip: avoid-builtin-shadow
        api_url = "https://api.trustar.co/api/2.0/submissions/indicators/upsert"
        
        ioc_list = []
        
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
        }
        
        for iocs in import_data["entities"]:
            for ioc in iocs["hashes"]:
                if ioc["algorithm"] == "MD5":
                    value = ioc["hash"]
                    type = "MD5"
                    
                if ioc["algorithm"] == "SHA-256":
                    value = ioc["hash"]
                    type = "SHA256"
                    
                if ioc["algorithm"] == "Domain":
                    type = "DOMAIN"
                    value = ioc["hash"]
                    
                if ioc["algorithm"] == "IPV4":
                    type = "IP4"
                    value = ioc["hash"]
                    
                if ioc["algorithm"] == "IPV6":
                    type = "IP6"
                    value = ioc["hash"]
                    
                ioc_dict = {
                    "id": "",
                    "title": "Indicator from ThreatMon API",
                    "enclaveGuid": "ThreatMon",
                    "tags":["ioc","threatmon"],
                    "observable": {
                            "type": type,
                            "value": value
                        }
                }
                
                ioc_list.append(ioc_dict)
            
        response_data = ioc_list
            
        try:
            splunk = requests.post(
                url=api_url,
                headers=headers,
                json=response_data,
            )
            
            if splunk.status_code == 200:
                print(time.strftime("%H:%M:%S") + " -- " + " (Finished) Imported IOCs to Splunk (Success)" )
            else:
                print(time.strftime("%H:%M:%S") + " -- " + "Could not POST IOCs to Splunk (Failure)")
                
        except Exception as e:
            print(e)

    def AlienVaultIntegration(self, token, import_data):
        # sourcery skip: avoid-builtin-shadow        
        ioc_list = []
        otx = OTXv2(token)
        
        for iocs in import_data["entities"]:
            for ioc in iocs["hashes"]:
                if ioc["algorithm"] == "MD5":
                    value = ioc["hash"]
                    type = "FileHash-MD5"
                    
                if ioc["algorithm"] == "SHA-256":
                    value = ioc["hash"]
                    type = "FileHash-SHA256"
                    
                if ioc["algorithm"] == "Domain":
                    type = "domain"
                    value = ioc["hash"]
                    
                if ioc["algorithm"] == "IPV4":
                    type = "IPv4"
                    value = ioc["hash"]
                    
                if ioc["algorithm"] == "IPV6":
                    type = "IPv6"
                    value = ioc["hash"]
                    
                ioc_dict = {
                    "indicator": value,
                    "description": "",
                    "type": type,
                }
                
                ioc_list.append(ioc_dict)
                
        try:
            new_pulse = otx.create_pulse(name="Threatmon IOCs", indicators=ioc_list, public=False)
            pprint(json_normalize(new_pulse))
            
        except Exception as e:
            print(e)
