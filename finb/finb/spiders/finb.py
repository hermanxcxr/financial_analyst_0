import scrapy

#URL finance.yahoo = https://finance.yahoo.com/

class FinbSpider(scrapy.Spider):
    name = 'finb'
    start_urls = [
        'https://www.cual-es-mi-ip.net/'
    ]
    custom_settings = {
        'USER_AGENT' : 'PEPITO'
    }
    
    def parse(self, response):
        variable = response.xpath('//span[contains(@class,"big-text")]/text()').get()
        print('finb******')
        print(variable)
        print('finb******')
        with open('resultados.html', 'w', encoding= 'utf-8') as f:
            f.write(variable)