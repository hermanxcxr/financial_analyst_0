'''python pipe_00.py 0 '''
import subprocess
import sys


with open('temp_output/exchanges_length.csv','rt',encoding='utf-8') as f:
    EXCHANGES_QUANTITY = int(f.read())

def run(*args):
    print(args)
    print(type(args[0][1]))
    #print(EXCHANGES_QUANTITY)
    
    activador = int(args[0][1])

    if activador == 0:
        #1.exchanges_download, target=0; 2.stocks_download, target=1; 
        #procedimiento de obtencion de EXCHANGES
        subprocess.run(['scrapy','crawl','proxyfinder'],cwd='./proxy_finder/proxy_finder')
        subprocess.run(['python','depurador_proxies.py'],cwd='./operaciones')
        subprocess.run(['scrapy','crawl','finb','-a','target=0'],cwd='./finb/finb')
        #for i in range(1,EXCHANGES_QUANTITY+1):
        subprocess.run(['scrapy','crawl','proxyfinder'],cwd='./proxy_finder/proxy_finder')
        subprocess.run(['python','depurador_proxies.py'],cwd='./operaciones')
        subprocess.run(['scrapy','crawl','finb','-a','target=1'],cwd='./finb/finb')
    elif activador == 1:
        #Posible uso: Activador para reiniciar "specific exchange stocks download"
        for i in range(2,4):
            subprocess.run(['scrapy','crawl','proxyfinder'],cwd='./proxy_finder/proxy_finder')
            subprocess.run(['python','depurador_proxies.py'],cwd='./operaciones')
            subprocess.run(['scrapy','crawl','finb','-a','target={}'.format(str(i))],cwd='./finb/finb')
            print('~~~~~~~~~~~~{}~~~~~~~~~~~~'.format(i))
        print('ensayo')
    elif activador == 2:
        #subprocess no encuentra los módulos selenium y psycopg2
        #historical_data_download; create_sql_stock_table
        subprocess.run(['python','OHLCV_getter.py'],cwd='./operaciones')
        subprocess.run(['python','conv_sql_prime.py'],cwd='./operaciones')
    elif activador == 3:
        #analysis
        subprocess.run(['python','analyst_00.py'],cwd='./operaciones')
    else:
        print("Argumentos inválidos")
    
    

if __name__ == '__main__':
    args = sys.argv
    run(args)