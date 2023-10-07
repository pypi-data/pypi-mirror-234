import pymysql
from dbutils.pooled_db import PooledDB

class MySQLConnector:
    _pool = None

    @classmethod
    def get_connection(cls, database_host, credential_provider):
        pool = cls.get_pool(database_host, credential_provider)
        return pool.connection()
    
    @classmethod
    def get_pool(cls, database_host, credential_provider):
        if not cls._pool:
            creds = credential_provider.get_credentials("mysql", database_host)
            cls._pool = PooledDB(
                creator=pymysql,
                host=creds['host'],
                user=creds['user'],
                password=creds['password'],
                database=creds['database'],
                autocommit=True,
                blocking=True,
                maxconnections=10
            )
        return cls._pool
