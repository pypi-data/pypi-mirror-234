import sqlite3
from enum import Enum
from typing import Union

import oracledb
import pandas as pd
import psycopg2
import psycopg2.extras
import pymssql
import pyodbc

from bsc_utils.config import config
from bsc_utils.exceptions import NotDatabaseError
from bsc_utils.helpers import dict_factory


class Database(Enum):
    MSSQL = 'mssql'
    ORACLE = 'oracle'
    POSTGRESQL = 'postgresql'
    SQLITE = 'sqlite'
    ACCESS = 'access'


def connect(database: Database):
    if not isinstance(database, Database):
        raise NotDatabaseError('Must be a database.Database instance.')

    if database == Database.MSSQL:
        return pymssql.connect(
            server=config.mssql.server,
            user=config.mssql.user,
            password=config.mssql.password,
            database=config.mssql.database,
        )

    elif database == Database.ORACLE:
        oracledb.init_oracle_client()
        return oracledb.connect(
            user=config.oracle.user,
            password=config.oracle.password,
            dsn=config.oracle.dsn,
        )

    elif database == Database.POSTGRESQL:
        return psycopg2.connect(
            dsn=config.postgresql.url,
            cursor_factory=psycopg2.extras.RealDictCursor
        )

    elif database == Database.SQLITE:
        return sqlite3.connect(database=config.sqlite.path)

    elif database == Database.ACCESS:
        return pyodbc.connect(
            f'''
            Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};
            DBQ={config.access.path};
            '''
        )


def query(
    database: Database,
    query: str,
    params: Union[list, tuple] = None,
    fetch: bool = True,
    as_df: bool = True,
    datetime_cols: list = None,
    index_col: str = None
) -> Union[list, pd.DataFrame]:
    con = connect(database)
    if database == Database.MSSQL:
        cur = con.cursor(as_dict=True)

    elif database == Database.SQLITE:
        con.row_factory = dict_factory
        cur = con.cursor()

    elif database in [Database.ORACLE, Database.ACCESS, Database.POSTGRESQL]:
        cur = con.cursor()

    cur.execute(query) if params is None else (
        cur.executemany(query, params)
        if isinstance(params, list) else cur.execute(query, params)
    )

    if database == Database.ORACLE:
        cols = [col[0] for col in cur.description]
        cur.rowfactory = lambda *args: dict(zip(cols, args))

    obj = None
    if fetch:
        obj = cur.fetchall()

        if database == Database.POSTGRESQL:
            obj = [dict(row) for row in obj]

        elif database == Database.ACCESS:
            obj = [
                dict(zip([col[0] for col in cur.description], row))
                for row in obj
            ]

        if as_df:
            obj = make_tabular(obj, index_col, datetime_cols)

    con.commit()
    con.close()

    return obj


def make_tabular(
    obj: list[dict],
    index_col: str,
    datetime_cols: list = None
) -> pd.DataFrame:
    df = pd.DataFrame(obj)
    if index_col:
        df.set_index(index_col, inplace=True)
    if datetime_cols:
        df[datetime_cols] = df[datetime_cols].apply(pd.to_datetime)

    return df