import scrapy
import random

# SE DEBEN DEPURAR LOS XPATH, PERO DE RESTO EL FUNCIONAMIENTO ES PERFECTO
# SE REQUERIRÁN MÁS PROXIES Y UNA OPCIÓN PARA ELIMINARLOS A MEDIDA QUE MUESTRE ERROR

LIST_OF_SEUDONIMS = ['AAA', 'PEPITO', 'MANITO', 'TRADER', 'LOVE', 'MICHI', 'WHAT_ELSE'] 


class FinbSpider(scrapy.Spider):
    name = 'finb'
    custom_settings = {
        'USER_AGENT' : random.choice(LIST_OF_SEUDONIMS)
    }
    
    start_urls = [
        'https://eoddata.com'        
    ]

    def parse(self, response):

        target = int(self.target)

        if target == 0 : 

            ''' Parse toma los nombres,tickers y urls de los Exchange mkts 
            y crea el archivo csv que contiene los EXCHANGE MARKETS 
            XPATHS : DEPURADOS
            #URL eoddata main = https://eoddata.com
            #xpath exchange_simbolos = '//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a/text()'
            #xpath exchange_names = '//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td[2]'
            #xpath exchange_url = '//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a[contains(@title,"Browse")]/@href'
            '''
            exchange_url = response.xpath('//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a[contains(@title,"Browse")]/@href').getall()
            exchange_ticker = response.xpath('//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a/text()').getall()
            exchange_name = response.xpath('//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td[2]').getall()

            #borra el contenido del archivo final 
            # with open('../../output/stocks_prev.csv', 'wt', encoding= 'utf-8') as f:
            #     f.write("Ticker_Stock,Name_Stock,Ticker_Exch")

            #print('finb******')
            #print(variable)
            #print('finb******')
            with open('../../output/exchange.csv', 'w', encoding= 'utf-8') as f:
                f.write("Ticker_Exchange,Name_Exchange,URL_Exchange")
                f.write("\n")
                idx=0
                for ticker, name, url in zip(exchange_ticker,exchange_name,exchange_url):
                    f.write(ticker)
                    f.write(",")
                    name = name.replace("<td>","")
                    name = name.replace("</td>","")
                    f.write(name)
                    f.write(",")
                    f.write(response.urljoin(url))
                    f.write("\n")
                    idx += 1
                with open('../../temp_output/exchanges_length.csv',"w") as fp:
                    fp.write(str(idx))
                fp.close()

            #print(f.readlines())
                # with open('../../temp_output/csv_lines.csv', 'w', encoding= 'utf-8') as g:
                #     exchange_lines = f.readlines()
                #     exchange_lines = str(len(exchange_lines)) # este numero debe ir a pipe_00 de algun modo
                #     g.write(exchange_lines)
                #     #print(exchange_lines)

        if target > 0:
            
            with open('../../output/exchange.csv', 'r', encoding= 'utf-8') as f:
                exchanges = f.readlines()
            
            exchange = exchanges[target]
            exchange_params = list(exchange.split(","))
            exchange_params[2] = exchange_params[2].replace("\n","")
            print(exchange_params)
            print(exchange)
            
            str_filename =  f'../../output/{exchange_params[0]}_stocks.csv'
            #borra el contenido del archivo final 
            with open(str_filename, 'wt', encoding= 'utf-8') as f:
                f.write("Ticker_Stock,Name_Stock,Ticker_Exch")

            yield response.follow(
                exchange_params[2],
                callback = self.parse_link,
                cb_kwargs = {"url": exchange_params[2], "exc_ticker" : exchange_params[0], "exc_name" : exchange_params[1] }
            )


            # exchange_url = response.xpath('//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a[contains(@title,"Browse")]/@href').getall()
            # exchange_ticker = response.xpath('//div[contains(@id,"Exchange")]/table[@class="quotes"]/tr/td/a/text()').getall()

            # for url,exc_ticker in zip(exchange_url,exchange_ticker):
            #     url_complete = response.urljoin(url)
            #     yield response.follow(
            #         url_complete,
            #         callback = self.parse_link,
            #         cb_kwargs = { "url" : url_complete, "exc_ticker" : exc_ticker}
            #     )

    def parse_link(self,response, **kwargs):
        '''parse_link se ubica en la primera página de cada Exchange mkt
        y se direccionará a las página de c/ stock
        XPATHS: DEPURADOS
        URL de los links a c/stock pag. de c/exch = '//td[@class="ld"]/a/@href'
        '''    
        #exchange_page = kwargs["url"]
        exc_ticker = kwargs["exc_ticker"]
        exc_name = kwargs["exc_name"]

        exchange_page_urls = response.xpath('//td[@class="ld"]/a/@href').getall()
        
        for url in exchange_page_urls:
            url_complete = response.urljoin(url)
            yield response.follow(
                url_complete,
                callback = self.parse_stocks,
                cb_kwargs = { "url" : url_complete, "exc_ticker" : exc_ticker, "exc_name" : exc_name}
            )

    def parse_stocks(self,response,**kwargs):
        '''parse_stock es la función que recoge la info base del stock
        XPATHS: DEBEN SER DEPURADOS
        URL de los tickers de c/stock ='//tr[contains(@class,"ro") or contains(@class,"re")]/td/a[contains(@title,"Display Quote")]/text()'
        URL de los nombres de c/stock = '//tr[contains(@class,"ro") or contains(@class,"re")]/td[not(@align)]/text()'
        '''
        
        stocks_tickers = response.xpath('//tr[contains(@class,"ro") or contains(@class,"re")]/td/a[contains(@title,"Display Quote")]/text()').getall()
        stocks_names = response.xpath('//tr[contains(@class,"ro") or contains(@class,"re")]/td[not(@align)]/text()').getall()
        
        exc_ticker = kwargs["exc_ticker"]
        str_filename =  f'../../output/{exc_ticker}_stocks.csv'
        print(str_filename)
        #borra el contenido del archivo final 
        with open(str_filename, 'at', encoding= 'utf-8') as f:
            f.write("\n")
            for ticker, name in zip(stocks_tickers,stocks_names):
                f.write(ticker)
                f.write(",")
                f.write(name)
                f.write(",")
                f.write(kwargs["exc_ticker"])
                f.write("\n")

