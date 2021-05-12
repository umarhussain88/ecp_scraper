import logging
import sys
from pathlib import Path

import pandas as pd
from requests import get
from sqlalchemy.exc import ProgrammingError

from utils import create_sql_engine, insert_job, logger, rm_old_logs



# logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def import_data():

    engine_azure = create_sql_engine()
    files = list(Path(__file__).parent
                               .parent.joinpath('output').glob('*.csv*'))
    df = pd.concat([pd.read_csv(f) for f in files])
    logger.info(f"Writing {', '.join([f.stem for f in files])} to Azure DB")

    try:
        job_key = insert_job('ecp spider',engine_azure)
        df.to_sql('product_data', schema='stg_ecp', con=engine_azure,
                  if_exists='replace', index=False)

    except ProgrammingError:
        ip = get('https://api.ipify.org').text
        logger.exception(
            f'Program failed due to firewall rule mistach current IP address is - {ip}', exec_info=True)
        sys.exit(1)

    with engine_azure.begin() as conn:
        # log success of insert stg table. 

        logger.info(f'Executing dim Product with {job_key}')
        conn.execute('stg_ecp.p_InsertDwDimProduct ?', [str(job_key)])
        logger.info(f'Executing fact ProductPrices with {job_key}')
        conn.execute('stg_ecp.p_InsertDwFactProductPrices ?', [str(job_key)])


if __name__ == '__main__':
    import_data()
    rm_old_logs()
