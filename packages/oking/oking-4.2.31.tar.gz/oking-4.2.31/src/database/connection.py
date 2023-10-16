import sys

import cx_Oracle
import mysql.connector
# import oracledb as oracledb
import pyodbc
# import os

from src.database.utils import DatabaseConfig
import src
import firebirdsql

class Connection:
    def __init__(self, db_config: DatabaseConfig):
        self.db_type = db_config.db_type.lower()
        self.db_config = db_config
        if self.db_type == 'mysql':
            self.conn = get_mysql_connection(db_config.db_host, db_config.db_name, db_config.db_user, db_config.db_pwd,
                                             db_config.port)
        elif self.db_type == 'oracle':
            self.conn = get_oracle_client_connection(db_config.db_client, db_config.db_user, db_config.db_pwd,
                                                     db_config.db_host)
        elif self.db_type == 'sql':
            self.conn = get_sql_server_connection(db_config.db_client, db_config.db_host, db_config.db_name,
                                                  db_config.db_user, db_config.db_pwd)
        elif self.db_type == 'firebird':
            self.conn = get_firebird_connection(db_config.db_user, db_config.db_pwd, db_config.db_client,
                                                db_config.db_host)

    def get_conect(self):
        # if self.db_type == 'oracle':
        #     return get_oracle_connection(self.db_config.db_host, self.db_config.db_user, self.db_config.db_pwd)
        # else:
        return self.conn


def get_mysql_connection(db_host: str, db_name: str, db_user: str, db_pwd: str, db_port: str = '3306'):
    if db_host.__contains__(':'):
        data = db_host.split(':')
        db_host = data[0]
        db_port = data[1]
    elif db_port is None or db_port == '':
        db_port = '3306'

    return mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_pwd,
        port=db_port)


# def get_oraclethin_connection(db_dsn: str, db_user: str, db_pwd: str):
#    return oracledb.connect(user=db_user, password=db_pwd,
#                             host=db_host, port=1521, service_name=db_name) "dbhost.example.com/orclpdb"

#    return oracledb.connect(user=db_user, password=db_pwd,
#                              dsn=db_dsn)


def get_oracle_client_connection(db_client: str, db_user: str, db_pwd: str, db_host: str):
    if src.is_connected_oracle_client is False:

        _caminho = sys.path
        caminho = ''

        for i in range(len(_caminho)):
            if _caminho[i].__contains__('site-packages'):
                caminho = _caminho[i]
                print('MOSTRA O CAMINHO: ' + caminho)

        print(rf'{caminho}\src\database\oracle2\instantclient_21_6')
        caminho = rf'{caminho}\src\database\oracle2\instantclient_21_6'
        cx_Oracle.init_oracle_client(lib_dir=caminho)
        src.is_connected_oracle_client = True

    # return cx_Oracle.connect(user='system',
    #                        password='oracle',
    #                       dsn='192.168.4.62:49161/XE')
    return cx_Oracle.connect(user=db_user, password=db_pwd, dsn=db_host)


# def get_oracle_connection(db_host: str, db_user: str, db_pwd):
#    conn_str = db_user + '/' + db_pwd + '@' + db_host
#    return cx_Oracle.connect(conn_str)


# def get_oracle_client_connection(db_client: str, db_user: str, db_pwd: str, db_host: str):
#    if src.is_connected_oracle_client is False:
#        cx_Oracle.init_oracle_client(lib_dir=rf'{db_client}')
#        src.is_connected_oracle_client = True

#    return cx_Oracle.connect(user=db_user,
#                             password=db_pwd,
#                             dsn=db_host)


def get_sql_server_connection(db_driver: str, db_host: str, db_name: str, db_user: str, db_pwd: str):
    return pyodbc.connect(f'Driver={{{db_driver}}};Server={db_host.replace(":", ",")};Database={db_name};UID={db_user};PWD={db_pwd}')


def get_firebird_connection(db_user: str, db_pwd: str, port: str, db_host: str):
    db_port = '3050'
    if db_host.__contains__(':'):
        data = db_host.split(':')
        db_host = data[0]
        db_port = data[1]
    return firebirdsql.Connection(user=db_user, password=db_pwd, database=port, host=db_host, port=db_port)


def output_type_handler(cursor, name, default_type, size, precision, scale):
    if default_type == cx_Oracle.DB_TYPE_CLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize)
    if default_type == cx_Oracle.DB_TYPE_BLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG_RAW, arraysize=cursor.arraysize)
