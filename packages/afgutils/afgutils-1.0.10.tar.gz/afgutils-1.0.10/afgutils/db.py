# CHANGE LOG
#
# 2023-09-05
# Added:
# type hints to function definitions

from os import getenv
import pyodbc
from pyodbc import Cursor


class DB:
    __connections = {}

    @classmethod
    def get_connection(cls, db_name: str)-> pyodbc.Connection:
        if cls.__connections.get(db_name):
            return cls.__connections.get(db_name)
        return cls._create_connection(db_name)

    @classmethod
    def _create_connection(cls, db_name):
        prefix = db_name

        dsn = getenv(prefix + '_dsn')

        driver = getenv(prefix + '_driver')
        database = getenv(prefix + '_db')
        user = getenv(prefix + '_user')
        password = getenv(prefix + '_pass')
        server = getenv(prefix + '_host')
        port = getenv(prefix + '_port')

        if dsn:
            conn_str = f"DSN={dsn}"
        elif prefix and driver and driver and user and password and server and port:
            conn_str = (
                f"DRIVER={driver};"
                f"DATABASE={database};"
                f"UID={user};"
                f"PWD={password};"
                f"SERVER={server};"
                f"PORT={port};"
            )
        else:
            raise ValueError(f"DB configurations could not be found for {db_name}")

        conn = pyodbc.connect(conn_str)
        cls.__connections[db_name] = conn
        return conn

    @classmethod
    def close_connections(cls):
        # print("Connections are closed")
        for key in cls.__connections:
            cls.__connections[key].close()
        cls.__connections = {}

    @staticmethod
    def execute(cursor: Cursor, query: str, fetch=None, parameters=None, commit: bool=False)-> dict | list:
        # Execute the query
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        if commit:
            cursor.connection.commit()

        if cursor.rowcount and fetch:
            # Fetch the rows
            if fetch == 'all':
                rows = cursor.fetchall()
            else:
                rows = cursor.fetchone()

            index_map = {index: column[0] for index, column in enumerate(cursor.description)}
            if type(rows) == list:
                dict_rows = []
                for row in rows:
                    new_row = {index_map[index]: value for index, value in enumerate(row)}
                    dict_rows.append(new_row)
                return dict_rows
            else:
                return {index_map[index]: value for index, value in enumerate(rows)}


def sql(sql_name: str, sql_version: int, sql_custom_folder: str = None)-> str:
    if sql_custom_folder:
        afg_sqls_folder = sql_custom_folder
    else:
        afg_sqls_folder = getenv("afg_sqls_folder")

    sql_filename = afg_sqls_folder + sql_name + "/" + sql_name + "." + str(sql_version).zfill(3) + ".sql"

    sql_file = open(sql_filename, "r")
    sql_text = sql_file.read()
    sql_file.close()

    return sql_text