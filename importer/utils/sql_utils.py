from sqlalchemy.engine.base import Engine
import pyodbc
import os
from sqlalchemy import create_engine
import urllib


def insert_job(activity_summary: str, azure_sql_engine: Engine) -> int:
    """Returns a job key from the sql database"""

    sql_string = """DECLARE @Jobkey INT
                EXEC etl_audit.p_InsertJob 'ecp', '%s',
                @Jobkey = @Jobkey OUT
                SELECT jobkey = @Jobkey
                """ % activity_summary
                    
    with azure_sql_engine.begin() as conn:
        job_exec = conn.execute(sql_string)
        jobkey = job_exec.first()[0]
    return jobkey


def create_sql_engine() -> Engine:
    """Creates a sql engine from env vars"""

    sql_server = os.environ.get('sql_server')
    sql_user = os.environ.get('sql_uid')
    sql_pw = os.environ.get('sql_pw')

    params = urllib.parse.quote_plus(
        r'Driver={ODBC Driver 17 for SQL Server};'
        + fr'Server={sql_server}'
        + r',1433;Database=ecp;'
        + fr'Uid={sql_user};Pwd={sql_pw};'
        + r'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

    conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    return create_engine(conn_str, fast_executemany=True)
