import logging
import sys
from pathlib import Path

import pandas as pd
from requests import get
from sqlalchemy.exc import ProgrammingError

from utils import create_sql_engine, insert_job, logger



logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def import_data():

    engine_azure = create_sql_engine()
    files = list(Path(__file__).parent
                               .parent.joinpath('output').glob('*.csv*'))
    df = pd.concat([pd.read_csv(f) for f in files])
    logger.info(f"Writing {', '.join([f.stem for f in files])} to Azure DB")

    try:
        stg_key = insert_job('inserting stg product data',engine_azure)
        df.to_sql('product_data', schema='stg_ecp', con=engine_azure,
                  if_exists='replace', index=False)
        with engine_azure.begin() as conn:
            conn.execute('etl_audit.p_UpdateJob ?,?', [str(stg_key), 'Success'])

    except ProgrammingError:
        ip = get('https://api.ipify.org').text
        logger.exception(
            f'Program failed due to firewall rule mistach current IP address is - {ip}', exec_info=True)
        sys.exit(1)

    with engine_azure.begin() as conn:
        # log success of insert stg table. 

        dim_product_key = insert_job('executing insert dim product proc',engine_azure)
        logger.info(f'Executing dim Product with {dim_product_key}')

        fact_product = insert_job('executing insert fact product prices proc',engine_azure)
        logger.info(f'Executing fact ProductPrices with {fact_product}')


if __name__ == '__main__':
    import_data()
