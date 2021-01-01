import psycopg2
import json

def acum_return(cursor,stock_tickers):
    dict_RA = {}
    for stock in stock_tickers:
        cursor.execute("""select close
                        from {}_stock 
                        where dates >= current_date - interval '6 month' 
                        order by id asc 
                        limit 1;""".format(stock))
        value_init = cursor.fetchone()
        cursor.execute("""select close 
                            from {}_stock
                            where dates >= current_date - interval '6 month'
                            order by id asc
                            offset(
                                    select count(*)-1
                                    from {}_stock
                                    where dates >= current_date - interval '6 month'
                                    );""".format(stock,stock))
        value_last = cursor.fetchone()
        RA = ((value_last[0]/value_init[0])-1)*100
        dict_RA[stock] = RA
    return dict_RA

def run(menu):
    with open('../old/pgsql.json','r') as f:
        reader = json.load(f)
        user = reader['user']
        password = reader['password']
        port = reader['port']
        database = reader['database']
    f.close()

    conn_sql = psycopg2.connect(user=user,password=password,port=port,database=database)
    cursor = conn_sql.cursor()    
    
    stock_tickers = open('../temp_output/stocks_data_tickers.txt').read().splitlines()

    while(menu == True):
        print("(1) Retorno acumulado de los últimos 6 meses")
        print("(2) Salir")

        opcion = int(input('Opción:'))
        
        if opcion == 1:
            dict_RA = acum_return(cursor,stock_tickers)
            for key,value in dict_RA.items():
                print(str(key)+": "+str(value))

        elif opcion == 2:
            menu = False


if __name__ == '__main__':
    menu = True
    run(menu)