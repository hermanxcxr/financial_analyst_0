import scrapy
import random
import json

# MAIN_URL = https://free-proxy-list.net/
# XPATH_IP = //tr/td[1]/text()
# XPATH_PORT = //tr/td[2]/text()
# XPATH_HTTPS_FLAG = //tr/td[7]/text()

LIST_OF_SEUDONIMS = ['AAA', 'PEPITO', 'MANITO', 'TRADER', 'LOVE', 'MICHI', 'WHAT_ELSE'] 

class ProxyFinder(scrapy.Spider):
    name = 'proxyfinder'
    start_urls = [
            'https://free-proxy-list.net/'
    ]
    custom_settings = {
        'USER_AGENT': random.choice(LIST_OF_SEUDONIMS)
    }

    def parse(self,response):
        ips = response.xpath('//tr/td[1]/text()').getall()
        ports = response.xpath('//tr/td[2]/text()').getall()
        https_flags = response.xpath('//tr/td[7]/text()').getall()
      
        # with open('../../proxies_list.csv','wt',encoding='utf-8') as f:
        #     f.write('IP,PORT,HTTPS')
        #     f.write("\n")
        #     for ip,port,https_flag in zip(ips,ports,https_flags):
        #         f.write(ip)
        #         f.write(",")
        #         f.write(port)
        #         f.write(",")
        #         f.write(https_flag)
        #         f.write("\n")
        
        proxies = {}
        proxies["servers"] = []        
        with open('../../temp_output/proxies_list.txt','wt',encoding='utf-8') as f:
            for ip,port,https_flag,idx in zip(ips,ports,https_flags,range(1,len(ips)+1)):
                ip_port = ip + ":" + port
                
                proxies["servers"].append({"ip_port" : ip_port , "https_flag": https_flag})
    
            json.dump(proxies,f)