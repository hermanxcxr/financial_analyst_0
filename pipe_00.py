import subprocess
import sys

def run(*args):
    print(args)
    print(type(args[0][1]))
    activador_proxy = int(args[0][1])
    if activador_proxy == 0:
        #procedimiento de obtencion de EXCHANGES
        subprocess.run(['scrapy','crawl','proxyfinder'],cwd='./proxy_finder/proxy_finder')
        #subprocess.run(['mv','proxies_list.txt','temp_output/']) YA NO ES NECESARIO SE UBICA EL ARCHIVO DIRECTAMENTE
        subprocess.run(['python','depurador_proxies.py'],cwd='./operaciones')
        subprocess.run(['scrapy','crawl','finb'],cwd='./finb/finb')
        #probable ciclo for en base al resultado esperado de la cantidad de EXCHANGES descargados repitiendo el proceso anterior
    elif activador_proxy == 1:
        print('ensayo')
    else:
        print("Ni idea porqué no funcionó")
    

if __name__ == '__main__':
    args = sys.argv
    run(args)