import os
import pyodbc
import pymysql
from enum import Enum
from inspect import stack, getmodulename

from eptools.configuration import *
from eptools.logger import EasyPostLogger

def reloadconfig(func):  
    def wrap(*args, **kwargs):
        setglobals(globals())
        getglobals_new_globals = getglobals()
        globals().update(getglobals_new_globals)
        func_new_globals = func(*args,**kwargs)
        after_func_new_globals = getglobals()
        # keep own globals rather than getglobals after func
        after_func_new_globals.update(globals())
        globals().update(after_func_new_globals)
        return func_new_globals
    return wrap

loadconfigwithfile = reloadconfig(loadconfigwithfile)
loadconfigwithjson = reloadconfig(loadconfigwithjson)

class SQLType(Enum):
    MSSQL = 0
    MYSQL = 1

class SQLConnection(Enum):
    # Odd numbers for MySQL, Even for MSSQL
    LOCALDB = 0
    PORTAL = 1
    PRINTDB = 2
    MYSQLDB1 = 3
    MACHINEDB = 4
    MYSQLDB2 = 5
    MSSQLDB2 = 6
    MYSQLDB3 = 7
    MSSQLDB3 = 8
    MYSQLDB4 = 9
    MSSQLDB4 = 10
    MYSQLDB5 = 11
    MSSQLDB5 = 12
    MYSQLDB8 = 17
    MSSQLDB8 = 18
    MYSQLDB9 = 19
    MSSQLDB9 = 20
    MYSQLDB10 = 21
    MSSQLDB10 = 22
    MYSQLDB11 = 23
    MSSQLDB11 = 24
    MYSQLDB12 = 25
    MSSQLDB12 = 26
    MYSQLDB13 = 27
    MSSQLDB13 = 28
    MYSQLDB14 = 29
    MSSQLDB14 = 30
    MYSQLDB15 = 31
    MSSQLDB15 = 32
    MYSQLDB16 = 33
    MSSQLDB16 = 34
    MYSQLDB17 = 35
    MSSQLDB17 = 36
    MYSQLDB18 = 37
    MSSQLDB18 = 38
    MYSQLDB19 = 39
    MSSQLDB19 = 40
    MYSQLDB20 = 41
    MSSQLDB20 = 42
    MYSQLDB21 = 43
    MSSQLDB21 = 44
    MYSQLDB22 = 45
    MSSQLDB22 = 46
    MYSQLDB23 = 47
    MSSQLDB23 = 48
    MYSQLDB24 = 49
    MSSQLDB24 = 50
    MYSQLDB25 = 51
    MSSQLDB25 = 52
    MYSQLDB26 = 53
    MSSQLDB26 = 54
    MYSQLDB27 = 55
    MSSQLDB27 = 56
    MYSQLDB28 = 57
    MSSQLDB28 = 58
    MYSQLDB29 = 59
    MSSQLDB29 = 60
    MYSQLDB30 = 61
    MSSQLDB30 = 62
    MYSQLDB31 = 63
    MSSQLDB31 = 64
    MYSQLDB32 = 65
    MSSQLDB32 = 66
    MYSQLDB33 = 67
    MSSQLDB33 = 68
    MYSQLDB34 = 69
    MSSQLDB34 = 70
    MYSQLDB35 = 71
    MSSQLDB35 = 72
    MYSQLDB36 = 73
    MSSQLDB36 = 74
    MYSQLDB37 = 75
    MSSQLDB37 = 76
    MYSQLDB38 = 77
    MSSQLDB38 = 78
    MYSQLDB39 = 79
    MSSQLDB39 = 80
    MYSQLDB40 = 81
    MSSQLDB40 = 82
    MYSQLDB41 = 83
    MSSQLDB41 = 84
    MYSQLDB42 = 85
    MSSQLDB42 = 86
    MYSQLDB43 = 87
    MSSQLDB43 = 88
    MYSQLDB44 = 89
    MSSQLDB44 = 90
    MYSQLDB45 = 91
    MSSQLDB45 = 92
    MYSQLDB46 = 93
    MSSQLDB46 = 94
    MYSQLDB47 = 95
    MSSQLDB47 = 96
    MYSQLDB48 = 97
    MSSQLDB48 = 98
    MYSQLDB49 = 99
    MSSQLDB49 = 100
    MYSQLDB50 = 101
    MSSQLDB50 = 102


    
    def type_select(self):
        if self.value % 2 == 1:
            return SQLType.MYSQL
        else:
            return SQLType.MSSQL
    
    def type_string(self):
        return self.type_select().name
    
    # @reloadconfig
    def select(self):
        return {
                    'host':globals()['C_DBHOST_' + self.name],
                    'user':globals()['C_DBUSER_' + self.name],
                    'password':globals()['C_DBPW_' + self.name],
                    'name':globals()['C_DBNAME_' + self.name],
                    'type': self.type_select()
                }
    
    def select_env(self):
        type_string = self.type_string()
        return {
                    'host':os.getenv(f'{type_string}_{self.name}_HOST','ep-srv-db'),
                    'user':os.getenv(f'{type_string}_{self.name}_USER','sa'),
                    'password':os.getenv(f'{type_string}_{self.name}_PASSWORD','sql'),
                    'name':os.getenv(f'{type_string}_{self.name}_NAME','master'),
                    'type': self.type_select()
                }

class SQLFactory():    
    @reloadconfig
    def __init__(self,sql_connection:SQLConnection = SQLConnection.PORTAL,connectiondata= None,logger = None, config_path=None, autocommit=None, timeout=None, env=False):
        global C_DEFAULT_CONFIG_PATH
        if config_path:
            C_DEFAULT_CONFIG_PATH = config_path
        loadconfigwithfile(config_path)

        self.sql_connection_selector = {
            SQLType.MYSQL : self.pymysql_connection,
            SQLType.MSSQL : self.pyodbc_connection
        }
        self.sql_connection = sql_connection
        self.connectiondata = connectiondata
        self.autocommit=autocommit
        self.timeout=timeout
        self.connection = None
        self.cursor = None
        self.env = env
        frame_records = stack()[2]
        self.app = getmodulename(frame_records[1])
        if not logger:
            self.logger = EasyPostLogger(name=f'{self.app}SQLFactory', logpath= globals()['C_DEFAULT_LOG_PATH'], config_path=C_DEFAULT_CONFIG_PATH)
        else:
            self.logger = logger
    
    @reloadconfig 
    def createConnection(self, timeout=None, autocommit=None, app=None):
        self.timeout = (timeout if timeout else self.timeout)
        self.autocommit = (autocommit if autocommit else self.autocommit)
        self.app = (app if app else self.app)
        self.close_all()
        if self.env:
            self.connectiondata = self.sql_connection.select_env()
        else:
            self.connectiondata = self.sql_connection.select()
        self.sql_connection_selector[self.connectiondata['type']]()
    
    @reloadconfig 
    def createCursor(self, retry = 0):
        self.close_cursor()
        if not self.connection:
            self.createConnection()
        try:
            self.cursor = self.connection.cursor()
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                self.createCursor(retry=retry+1)
            else:
                raise ex

    def __enter__(self):
        #ttysetattr etc goes here before opening and returning the file object
        self.createCursor()
        return self
    
    @reloadconfig
    def pymysql_connection(self, name = None, app=None, retry=0, timeout=None, autocommit=None):
        self.timeout = (timeout if timeout else self.timeout)
        self.autocommit = (autocommit if autocommit else self.autocommit)
        self.app = (app if app else self.app)
        self.close_all()
        try:
            self.connection = pymysql.connect(     host=self.connectiondata['host'],
                                        user = self.connectiondata['user'],
                                        password = self.connectiondata['password'],
                                        database = name if name else self.connectiondata['name'],
                                        charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor,
                                        program_name=self.app,
                                        connect_timeout=(self.timeout if self.timeout else 10),
                                        autocommit= (self.autocommit if self.autocommit else False)
                                    )
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.pymysql_connection(name=name,retry=retry+1)
            else:
                raise ex
    
    @reloadconfig    
    def pyodbc_connection(self, name = None, app=None, retry=0, timeout=None, autocommit=None):
        self.timeout = (timeout if timeout else self.timeout)
        self.autocommit = (autocommit if autocommit else self.autocommit)
        self.app = (app if app else self.app)
        self.close_all()
        try:
            self.connection = pyodbc.connect(      "APP=" + self.app + ";",
                                        driver='{SQL Server Native Client 11.0}',
                                        server=self.connectiondata['host'],
                                        user=self.connectiondata['user'],
                                        password=self.connectiondata['password'],
                                        database= name if name else self.connectiondata['name'],
                                        timeout=(self.timeout if self.timeout else 0),
                                        autocommit= (self.autocommit if self.autocommit else False)
                                )
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.pyodbc_connection(name=name,retry=retry+1)
            else:
                raise ex
            
    def executemany(self, *args, retry=0, **kwargs):
        if not self.cursor:
            self.createCursor()
        try:
            return self.cursor.executemany(*args,*kwargs)
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                return self.executemany(retry=retry+1)
            else:
                raise ex
               
    def rollback(self, *args, retry=0, **kwargs):
        if not self.cursor:
            self.createCursor()
        try:
            return self.cursor.rollback(*args,*kwargs)
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                return self.rollback(retry=retry+1)
            else:
                raise ex   
        
    def fetchone(self, *args, retry=0, **kwargs):
        if not self.cursor:
            self.createCursor()
        try:
            return self.cursor.fetchone(*args,*kwargs)
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                return self.fetchone(retry=retry+1)
            else:
                raise ex
       
        
    def fetchall(self, withColumns=False,*args, retry=0, **kwargs):
        if not self.cursor:
            self.createCursor()
        try:
            if withColumns:
                return [dict(zip([column[0] for column in self.cursor.description], row)) for row in self.cursor.fetchall()]
            else:
                return self.cursor.fetchall(*args,*kwargs)
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                return self.fetchall(retry=retry+1)
            else:
                raise ex
       
    def commit(self, *args, retry=0, **kwargs):
        if not self.cursor:
            self.createCursor()
        try:
            return self.cursor.commit(*args,**kwargs)
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                return self.commit(retry=retry+1,*args,**kwargs)
            else:
                raise ex
             
    def execute(self, *args, retry=0, **kwargs):
        if not self.cursor:
            self.createCursor()
        try:
            return self.cursor.execute(*args,**kwargs)
        except Exception as ex:
            
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                return self.execute(retry=retry+1,*args,**kwargs)
            else:
                raise ex
    
    def close_all(self):
        self.close_cursor()
        try:
            if self.connection:
                self.connection.close()
        except Exception as ex:
            self.logger.debug(ex)
        finally:
            self.connection = None

    def close_cursor(self):
        try:
            if self.cursor:
                self.cursor.close()
        except Exception as ex:
            self.logger.debug(ex)
        finally:
            self.cursor = None
            
    def __exit__(self, type, value, traceback):
        #Exception handling here
        self.close_all()

   
if __name__ == '__main__':
    # with SQLFactory(SQLConnection.PORTAL) as con:
    #     con.execute("SELECT * FROM easypost_portal.afm_users where company = 7255;")
    #     data = con.fetchall()
    #     print(data)
    # con2 = SQLFactory(SQLConnection.PRINTDB)
    # con2.execute("SELECT * FROM [EasyPost].[dbo].[Companies] where id = 7255;")
    # data = con2.fetchall()
    # con2.close_all()

    with SQLFactory(SQLConnection.PRINTDB, config_path='c:\Software\Configs\eptools.json') as conn:
        conn.execute("Select * from sysdatabases;")
        data = conn.fetchall(withColumns=True)
        print(data)

    # test without with
    logs = None
    sqlf = SQLFactory(SQLConnection.PRINTDB, config_path='c:\Software\Configs\eptools.json', logger=logs)
    sqlf.createConnection()
    conn = sqlf.connection
    cursor = conn.cursor()
    cursor.execute("Select * from sysdatabases;")
    result = cursor.fetchall()
    for x in result:
        print(x)