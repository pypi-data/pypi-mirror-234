from eptools.SQLFactory import SQLConnection, SQLFactory
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

class SFFactory():
    @reloadconfig
    def __init__(self, config_path=None, logger = None):
        global C_DEFAULT_CONFIG_PATH
        if config_path:
            C_DEFAULT_CONFIG_PATH = config_path
        loadconfigwithfile(config_path)
        self.config_path = config_path
        self.logger = logger
        if not self.logger:
            self.logger = EasyPostLogger('SlackFactory', globals()['C_DEFAULT_LOG_PATH'])

    def fetch_query(self,query,arguments = None):
        with SQLFactory(SQLConnection.PRINTDB, config_path=self.config_path) as sqlfactory:
            if arguments:
                sqlfactory.execute(query,arguments)
            else:
                sqlfactory.execute(query)
            data = sqlfactory.fetchall(withColumns=True)
            return data

    def fetchHubAndRound(self,client_number):
        data = self.fetch_query("""
            SELECT inr.CustomerIdPost,inr.CustomerParentIdPost,inr.Hub as Hub, outr.Hub as ParentHub, inr.RouteName as RouteName, outr.RouteName as ParentRouteName, inr.Name
  FROM [EasyPost].[dbo].[SFAccounts2] inr
  left join [EasyPost].[dbo].[SFAccounts2] outr  on inr.CustomerParentIdPost = outr.CustomerIdPost and inr.CustomerIdPost != 0 and outr.CustomerIdPost != 0
  WHERE inr.CustomerIdPost = ?
        
        """, client_number)
        return data
        

if __name__ == "__main__":
    fact = SFFactory()#config_path='c:\Software\Configs\eptools.json')
    print(fact.fetchHubAndRound('7255'))
    print(fact.fetchHubAndRound(7255))