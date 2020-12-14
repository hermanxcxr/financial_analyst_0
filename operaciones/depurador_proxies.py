import json

def depurador():

    list_of_servers = []
    # ".."" BAJA UN NIVEL, "/TEMP_OUTPUT" SE DIRECCIONA LA CARPETA, "/NAME" UBICA EL ARCHIVO
    with open ('../temp_output/proxies_list.txt','rt',encoding='utf-8') as f:
        data = json.load(f)
        for servers in data.values():
            #print(servers)
            for server in servers:
                #print(server["https_flag"])
                if server["https_flag"] ==  "yes":
                    list_of_servers.append(server["ip_port"])     

    with open('../temp_output/depurados.txt','wt',encoding='utf-8') as f:
        for server in list_of_servers:
            f.write("https://" + server )
            f.write("\n")
    
    
    #TEST DE APERTURA Y CREACIÓN DE LA VARIABLE LISTA_DE_PROXIES
    # lista_de_proxies = []
    # with open('../depurados.txt','rt',encoding='utf-8') as f:
    #     for line in f:
    #         line = line.replace("\n","")
    #         lista_de_proxies.append(line)
    # print(lista_de_proxies)

if __name__ == '__main__':
    depurador()