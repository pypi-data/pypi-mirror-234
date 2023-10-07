import pyodbc

pyodbc.pooling = True

class SQLServerConnector:

    @classmethod
    def get_connection(cls, database_host, credential_provider):
        creds = credential_provider.get_credentials("sql_server", database_host)
        conn_str = f"DRIVER={{SQL Server Native Client 11.0}};SERVER={creds['host']};DATABASE={creds['database']};UID={creds['user']};PWD={creds['password']}"
        return pyodbc.connect(conn_str)