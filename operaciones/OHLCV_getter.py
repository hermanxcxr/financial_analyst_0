import random
import re

import datetime as dt
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

RANDOM_STOCKS = []
STOCKS_TO_ANALYZE = 4
FILE_NAME = "AMEX_stocks.csv"
FECHA_INICIAL = '2019-01-01'
EXCHANGE = "1"

def stocks_chooser():

    lines = open('../output/{}'.format(FILE_NAME)).read().splitlines()
    for i  in range(STOCKS_TO_ANALYZE):
        #print(type(lines))
        RANDOM_STOCKS.append(random.choice(lines))
    #print(RANDOM_STOCKS)

    stock_tickers = []
    with open('../temp_output/stocks_data_tickers.txt','w',encoding='utf-8') as f:
        for stock in RANDOM_STOCKS:    
            stock_tickers.append(re.match(r'[\w]{2,4}',stock).group())
            f.write(str(re.match(r'[\w]{2,4}',stock).group()))
            f.write('\n')
    f.close()
    
    return stock_tickers

def data_getter(stocks):
    """
    stocks = tickers a investigar;
    A FUTURO: Otro parametro a recibir será el EXCHANGE, parametro que determinará la página a CRAWLEAR
    Cada EXCH debe llamar a un módulo diferente
    """
    
    delay = 10
    driver = webdriver.Chrome('C:/Program Files/Google/Chrome/Application/chromedriver')
    
    for stock in stocks:
        
        try:
            driver.get('https://www.nyse.com/index/')
            time.sleep(3)
            search_box = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,'//div[@class="navbar__right hidden-xs"]//input[@name="q"]')))
            search_box.send_keys(stock)
            stock_url = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,'//ul[@class="dropdown-menu"]/li/a'))).get_attribute('href')
            driver.get(stock_url)
            historic_prices_init = WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,'//*[@id="content-9d1f8b01-08a6-4db5-99fa-c40f5873615a"]/div/div[1]/div/div[2]/div[1]/div[4]/div[2]/span/div[2]/div[1]/div/div/div/input')))
            historic_prices_init.send_keys(Keys.CONTROL + "a")
            historic_prices_init.send_keys(Keys.DELETE)
            historic_prices_init.send_keys(FECHA_INICIAL)
            time.sleep(0.5)
            go_button = driver.find_element_by_xpath('//button[@class="d-button-normal"]')
            go_button.click()
            time.sleep(0.5)

            #XPATH A CADA DATO DEL STOCK
            historic_dates = WebDriverWait(driver,delay).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="flex_tr"]//div[@class="data-table-cell"]')))
            open_prices = WebDriverWait(driver,delay).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="flex_td Open"]/div[@class="data-table-cell-price-align"]')))
            high_prices = WebDriverWait(driver,delay).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="flex_td High"]/div[@class="data-table-cell-price-align"]')))
            low_prices = WebDriverWait(driver,delay).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="flex_td Low"]/div[@class="data-table-cell-price-align"]')))
            close_prices = WebDriverWait(driver,delay).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="flex_td Close"]/div[@class="data-table-cell-price-align"]')))
            volume_data = WebDriverWait(driver,delay).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="flex_td Volume"]/div[@class="data-table-cell-price-align"]')))

            #CREACION DEL ARCHIVO CONTENEDOR
            with open('../temp_output/{}_data.csv'.format(stock), 'w', encoding= 'utf-8') as f:
                    f.write("ID,Date,Open,High,Low,Close,Volume")
                    f.write("\n")
                    inv_idx = len(historic_dates)
                    # for ticker, name, url in zip(exchange_ticker,exchange_name,exchange_url):
                    for idx in range(len(historic_dates)):
                        f.write(str(inv_idx))
                        inv_idx -= 1 
                        f.write(",")
                        date = historic_dates[idx].get_attribute('innerHTML')
                        date = dt.datetime.strptime(date, '%m/%d/%Y')
                        f.write(str(date))
                        f.write(",")
                        temp_str = str(open_prices[idx].get_attribute('innerHTML'))
                        temp_str = temp_str.replace(",",".")
                        f.write(temp_str)
                        f.write(",")
                        temp_str = str(high_prices[idx].get_attribute('innerHTML'))
                        temp_str = temp_str.replace(",",".")
                        f.write(temp_str)
                        f.write(",")
                        temp_str = str(low_prices[idx].get_attribute('innerHTML'))
                        temp_str = temp_str.replace(",",".")
                        f.write(temp_str)
                        f.write(",")
                        temp_str = str(close_prices[idx].get_attribute('innerHTML'))
                        temp_str = temp_str.replace(",",".")
                        f.write(temp_str)
                        f.write(",")
                        temp_str = str(volume_data[idx].get_attribute('innerHTML'))
                        temp_str = temp_str.replace(",","")
                        f.write(temp_str)
                        f.write(",{}".format(EXCHANGE))
                        f.write("\n")
            f.close()
        except Exception as e :
            #print('Hubo un error')
            print(e)
        except TimeoutException :
            print(TimeoutException)
            with open('../temp_output/{}_data.csv'.format(stock), 'w', encoding= 'utf-8') as f:
                f.write('El ticker no existe')
            f.close()
        finally:
            #time.sleep(5) # Let the user actually see something!
            #driver.quit()
            pass
    driver.quit()

def run():
    """
    """
    stock_tickers = stocks_chooser()
    data_getter(stock_tickers)





if __name__ == "__main__":
    run()