'''python pipe_00.py 0 '''
import subprocess
import sys

with open('temp_output/exchanges_length.csv','rt',encoding='utf-8') as f:
    EXCHANGES_QUANTITY = int(f.read())

def run(*args):
    print(args)
    print(type(args[0][1]))
    #print(EXCHANGES_QUANTITY)
    activador_proxy = int(args[0][1])
    if activador_proxy == 0:
        #procedimiento de obtencion de EXCHANGES
        subprocess.run(['scrapy','crawl','proxyfinder'],cwd='./proxy_finder/proxy_finder')
        #subprocess.run(['mv','proxies_list.txt','temp_output/']) YA NO ES NECESARIO SE UBICA EL ARCHIVO DIRECTAMENTE
        subprocess.run(['python','depurador_proxies.py'],cwd='./operaciones')
        #subprocess.run(['scrapy','crawl','finb','-a','target=0'],cwd='./finb/finb')
        #probable ciclo for en base al resultado esperado de la cantidad de EXCHANGES descargados repitiendo el proceso anterior
        subprocess.run(['scrapy','crawl','proxyfinder'],cwd='./proxy_finder/proxy_finder')
        subprocess.run(['python','depurador_proxies.py'],cwd='./operaciones')
        subprocess.run(['scrapy','crawl','finb','-a','target=1'],cwd='./finb/finb')
    elif activador_proxy == 1:
        subprocess.run(['scrapy','crawl','proxyfinder'],cwd='./proxy_finder/proxy_finder')
        subprocess.run(['python','depurador_proxies.py'],cwd='./operaciones')
        subprocess.run(['scrapy','crawl','finb','-a','target=1'],cwd='./finb/finb')
        for i in range(1,EXCHANGES_QUANTITY+1):
            print(i)
        print('ensayo')
    else:
        print("Ni idea porqué no funcionó")
    

if __name__ == '__main__':
    args = sys.argv
    run(args)