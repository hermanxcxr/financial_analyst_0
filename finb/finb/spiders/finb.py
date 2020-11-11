import scrapy
import random

#URL finance.yahoo = https://finance.yahoo.com/
#URL eoddata main = https://eoddata.com/default.aspx
#xpath exchange_simbolos = '//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a/text()'
#xpath exchange_names = '//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td[2]'
#xpath exchange_url = '//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a[contains(@title,"Browse")]/@href'
#ejemplo URl lista =  https://eoddata.com/stocklist/NYSE.htm
#URL eoddata = https://eoddata.com/symbols.aspx
#xpath simbolos = '//tr[contains(@class,"ro") or contains(@class,"re")]/td/a[contains(@title,"Display Quote")]/text()'
#xpath nombres_simbolos = '//tr[contains(@class,"ro") or contains(@class,"re")]/td[not(@align)]/text()'

LIST_OF_SEUDONIMS = ['AAA', 'PEPITO', 'MANITO', 'TRADER', 'LOVE', 'MICHI', 'WHAT_ELSE'] 

class FinbSpider(scrapy.Spider):
    name = 'finb'
    start_urls = [
        'https://eoddata.com/default.aspx'        
    ]
    custom_settings = {
        'USER_AGENT' : random.choice(LIST_OF_SEUDONIMS)
    }
    
    def parse(self, response):
        exchange_url = response.xpath('//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a[contains(@title,"Browse")]/@href').getall()
        exchange_ticker = response.xpath('//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a/text()').getall()
        exchange_name = response.xpath('//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td[2]').getall()
        #print('finb******')
        #print(variable)
        #print('finb******')
        with open('resultados.csv', 'w', encoding= 'utf-8') as f:
            f.write("Ticker_Exchange,Name_Exchange,URL_Exchange")
            f.write("\n")
            for ticker, name, url in zip(exchange_ticker,exchange_name,exchange_url):
                f.write(ticker)
                f.write(",")
                name = name.replace("<td>","")
                name = name.replace("</td>","")
                f.write(name)
                f.write(",")
                f.write(url)
                f.write("\n")              