import scrapy
import random

# SE DEBEN DEPURAR LOS XPATH, PERO DE RESTO EL FUNCIONAMIENTO ES PERFECTO
# SE REQUERIRÁN MÁS PROXIES Y UNA OPCIÓN PARA ELIMINARLOS A MEDIDA QUE MUESTRE ERROR

LIST_OF_SEUDONIMS = ['AAA', 'PEPITO', 'MANITO', 'TRADER', 'LOVE', 'MICHI', 'WHAT_ELSE'] 

class FinbSpider(scrapy.Spider):
    name = 'finb'
    start_urls = [
        'https://eoddata.com'        
    ]
    custom_settings = {
        'USER_AGENT' : random.choice(LIST_OF_SEUDONIMS)
    }
    
    def parse(self, response):
        ''' Parse toma los nombres,tickers y urls de los Exchange mkts 
        y crea el archivo csv que contiene los EXCHANGE MARKETS 
        XPATHS : DEPURADOS
        #URL eoddata main = https://eoddata.com
        #xpath exchange_simbolos = '//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a/text()'
        #xpath exchange_names = '//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td[2]'
        #xpath exchange_url = '//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a[contains(@title,"Browse")]/@href'
        '''
        
        #borra el contenido del archivo final 
        with open('../../output/stocks_prev.csv', 'wt', encoding= 'utf-8') as f:
            f.write("Ticker_Stock,Name_Stock,Ticker_Exch")

        exchange_url = response.xpath('//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a[contains(@title,"Browse")]/@href').getall()
        exchange_ticker = response.xpath('//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a/text()').getall()
        exchange_name = response.xpath('//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td[2]').getall()
        #print('finb******')
        #print(variable)
        #print('finb******')
        with open('../../output/exchange.csv', 'w', encoding= 'utf-8') as f:
            f.write("Ticker_Exchange,Name_Exchange,URL_Exchange")
            f.write("\n")
            for ticker, name, url in zip(exchange_ticker,exchange_name,exchange_url):
                f.write(ticker)
                f.write(",")
                name = name.replace("<td>","")
                name = name.replace("</td>","")
                f.write(name)
                f.write(",")
                f.write(response.urljoin(url))
                f.write("\n")

        for url,exc_ticker in zip(exchange_url,exchange_ticker):
            url_complete = response.urljoin(url)
            yield response.follow(
                url_complete,
                callback = self.parse_link,
                cb_kwargs = { "url" : url_complete, "exc_ticker" : exc_ticker}
            )

    def parse_link(self,response, **kwargs):
        '''parse_link se ubica en la primera página de cada Exchange mkt
        y se direccionará a las página de c/ stock
        XPATHS: DEPURADOS
        URL de los links a c/stock pag. de c/exch = '//td[@class="ld"]/a/@href'
        '''    
        #exchange_page = kwargs["url"]
        exc_ticker = kwargs["exc_ticker"]

        exchange_page_urls = response.xpath('//td[@class="ld"]/a/@href').getall()
        
        for url in exchange_page_urls:
            url_complete = response.urljoin(url)
            yield response.follow(
                url_complete,
                callback = self.parse_stocks,
                cb_kwargs = { "url" : url_complete, "exc_ticker" : exc_ticker}
            )

    def parse_stocks(self,response,**kwargs):
        '''parse_stock es la función que recoge la info base del stock
        XPATHS: DEBEN SER DEPURADOS
        URL de los tickers de c/stock ='//tr[contains(@class,"ro") or contains(@class,"re")]/td/a[contains(@title,"Display Quote")]/text()'
        URL de los nombres de c/stock = '//tr[contains(@class,"ro") or contains(@class,"re")]/td[not(@align)]/text()'
        '''
        
        stocks_tickers = response.xpath('//tr[contains(@class,"ro") or contains(@class,"re")]/td/a[contains(@title,"Display Quote")]/text()').getall()
        stocks_names = response.xpath('//tr[contains(@class,"ro") or contains(@class,"re")]/td[not(@align)]/text()').getall()
        
        with open('../../output/stocks_prev.csv', 'at', encoding= 'utf-8') as f:
            f.write("\n")
            for ticker, name in zip(stocks_tickers,stocks_names):
                f.write(ticker)
                f.write(",")
                f.write(name)
                f.write(",")
                f.write(kwargs["exc_ticker"])
                f.write("\n")

