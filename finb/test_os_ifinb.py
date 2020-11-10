import os
import sys
import scrapy
from scrapy.crawler import CrawlerProcess

def run():
    #variable = os.getcwd()
    #variable = os.system("whoami")
    #str_path = str(os.getcwd()).lower()
    #str_path = str_path.replace("\\","/")
    #str_path = str_path.replace(":","")
    #print(str_path)
    #variable = "cd /" + str_path + "/finb" 
    #variable = "cd finb"
    #print(variable)
    #arg_1 = "cd finb"
    arg_2 = "scrapy crawl finb"
    #os.system(arg_1)
    os.system(arg_2)
    
    
    
    
    #for variable, valor in os.environ.items(): 
    #    print( "{} : {}".format(variable, valor))
    '''
    print(sys.argv)
    print(sys.executable)	#Retorna el path absoluto del binario ejecutable del intérprete de Python
    print(sys.maxsize ) #	Retorna el número positivo entero mayor, soportado por Python
    print(sys.platform)	# Retorna la plataforma sobre la cuál se está ejecutando el intérprete
    print(sys.version) #Retorna el número de versión de Python con información adicional
    '''

if __name__ == '__main__':
    run()