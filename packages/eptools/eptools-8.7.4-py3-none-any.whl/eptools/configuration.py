import json
C_DEFAULT_CONFIG_PATH = "c:\\Software\\Configs\\eptools.json"
C_DEFAULT_LOG_PATH = "c:\\Logs"

def getglobals():
    return globals()

def setglobals(new_globals):
    globals().update(new_globals) 

def loadconfigwithjson(value= {}):
    if type(value) == str:
        value = json.loads(value)
    all_variables = globals()
    for name in value:
        if name.startswith('C_'):
            if all_variables.get(name,None):
                globals()[name]= value[name]
            else:
                globals()[name]= value[name] 
        
        
def loadconfigwithfile(value = C_DEFAULT_CONFIG_PATH):
    with open((value if value else C_DEFAULT_CONFIG_PATH),'r') as file:
        text = file.read()
        loadconfigwithjson(json.loads(text))
