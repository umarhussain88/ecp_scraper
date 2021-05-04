from pathlib import Path
import json
import os 
import urllib
import logging

import pandas as pd
from sqlalchemy import create_engine
import pyodbc

file_dt = pd.Timestamp('now').strftime('%Y_%m_%d-%H%M%S')
log_path = Path(__file__).parent.parent.joinpath('logs',f'{file_dt}_export.log')

logging.basicConfig(filename=log_path, 
                    filemode='w', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)


def import_data():
    key_path = Path(__file__).parent.joinpath('key.csv')
    key = pd.read_csv(key_path)['key'][0]
    sql_server = os.environ.get('sql_server')
    sql_user   = os.environ.get('sql_uid')
    sql_pw     = os.environ.get('sql_pw')


    params = urllib.parse.quote_plus(r'Driver={ODBC Driver 17 for SQL Server};' 
                                    + fr'Server={sql_server}' 
                                    + r',1433;Database=ecp;' 
                                    + fr'Uid={sql_user};Pwd={sql_pw};' 
                                    + fr'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

    conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    engine_azure = create_engine(conn_str,fast_executemany = True)

    files = Path(__file__).parent.parent.joinpath('output').glob('*.csv')

    df = pd.concat([pd.read_csv(f) for f in files])

    logging.info('Writing to Azure DB')
    df.to_sql('product_data',schema='stg_ecp',con=engine_azure,if_exists='replace',index=False)

    logging.info(f'Executing dim Product with {key}')
    engine_azure.execute('stg_ecp.p_InsertDwDimProduct ?', [str(key)])
    logging.info(f'Executing fact ProductPrices with {key}')
    engine_azure.execute('stg_ecp.p_InsertDwFactProductPrices ?', [str(key)])

    key += 1 
    logging.info(f'updating key with value {key}')
    pd.DataFrame({'key' : key},index=[0]).to_csv(key_path,index=False)


if __name__ == '__main__':
    import_data()    