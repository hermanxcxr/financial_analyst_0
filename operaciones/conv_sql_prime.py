import psycopg2
import json


def run():
    """
    creación de tablas con datos historicos de los stocks crawleados
    Los datos para ingresar a la DB se encuentran en un archivo pgsql.json
    """

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

    for stock in stock_tickers:
        
        # Se debe refinar condiciones para las columnas de la tabla (PRIMARY KEY, NOT NULL, AUTO ++)
        create_table = "create table if not exist {}_stock (id INT PRIMARY KEY NOT NULL,dates DATE,open DECIMAL,high DECIMAL,low DECIMAL,close DECIMAL,volume DECIMAL, exch_id INT);".format(stock) 
        cursor.execute(create_table)
        conn_sql.commit()

        #se debe reorganizar los datos
        try:
            with open('../temp_output/{}_data.csv'.format(stock), 'r') as f:
                next(f)
                cursor.copy_from(f, '{}_stock'.format(stock), sep=',')
            conn_sql.commit() 
        except Exception as e:
            print(e)
    
    conn_sql.close()


if __name__ == "__main__":
    run()