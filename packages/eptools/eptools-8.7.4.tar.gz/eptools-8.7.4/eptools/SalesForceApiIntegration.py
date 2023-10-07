import json, requests
from eptools.SQLFactory import SQLConnection, SQLFactory
from simple_salesforce import Salesforce, SalesforceLogin
from sqlalchemy import except_all
from eptools.configuration import *


apiVersion = 'v46.0'
token = None
sf = None
logs = None

# CONFIGURATION #
# To use the configuration methods in a function set decorator! #
def reloadconfig(func):  
    def wrap(*args, **kwargs):
        setglobals(globals())
        getglobals_new_globals = getglobals()
        globals().update(getglobals_new_globals)
        func_new_globals = func(*args,**kwargs)
        # Overwrites token with None ? 
        # after_func_new_globals = getglobals()
        # globals().update(after_func_new_globals)
        return func_new_globals
    return wrap

# loadconfigwithfile = reloadconfig(loadconfigwithfile)
# loadconfigwithjson = reloadconfig(loadconfigwithjson)

@reloadconfig  
def oauth(retry = 0):
    global token, sf
    body = {
        "username": globals()['C_SFUsername'],
        "password": globals()['C_SFPassword'],
        "grant_type": 'password',
        "client_id": globals()['C_SFClientID'],
        "client_secret": globals()['C_SFClientSecret'],
        "content-type": 'application/x-www-form-urlencoded',
        "redirect_uri": 'https://login.salesforce.com/services/oauth2/callback',
    }
    headers = {
        "Connection": "close"
    }
    try:
        r = requests.post('https://login.salesforce.com/services/oauth2/token', data=body, headers=headers,timeout=5)
        response = json.loads(r.content)
        token = response['access_token']
        session_id, instance = SalesforceLogin(username=globals()['C_SFUsername'],password=globals()['C_SFPassword'])
        sf = Salesforce(instance=instance, session_id=session_id)
    except Exception as ex:
        print("read timeout ****************" + str(ex))
        if retry < 5:
            oauth(retry=retry+1)
        else:
            raise Exception('OAuth/Session Exception','Failed 5 times with last exception : ' + str((ex)))

def loadGlobals(json= None, path=None):
    if json is None and path is None:
        loadconfigwithfile()
    elif json is not None:
        loadconfigwithjson(json)
    elif path is not None:
        loadconfigwithfile(path)

def apiRequest(url, retry=0):
    global token
    if not token:
        oauth()
    try:
        response = requests.get(url, headers = {
            "Content-Type": "application/json",
            "Authorization":"Bearer " + token,
            "Connection": "close"
            }, timeout=5)
        if response.status_code != 200:
            raise Exception('apiRequest','statuscode != 200')
        return response
    except requests.exceptions.ReadTimeout as ex:
        print("read timeout ****************" + str(ex))
        oauth()
        if retry < 5:
            return apiRequest(url, retry = retry + 1)
        else:
            raise Exception('apiRequest','Request failed 5 times' + str(ex))

def getApiSObject(resource):
    global token
    response = requests.get('https://easypost.my.salesforce.com/services/data/' + apiVersion + '/sobjects/' + resource, headers = {
        "Content-Type": "application/json",
        "Authorization":"Bearer " + token
        })
    result = json.loads(response.text)
    return result

def getAllObjectFields(object):
    url = 'https://easypost.my.salesforce.com/services/data/' + apiVersion + '/sobjects/' + object + '/describe'
    response = apiRequest(url)
    result = json.loads(response.text)
    field_names = []
    for field in result['fields']:
        field_names.append(field['name'])
    return field_names

def getAccountFields():
    url = 'https://easypost.my.salesforce.com/services/data/' + apiVersion + '/sobjects/Account/describe'
    response = apiRequest(url)
    result = json.loads(response.text)
    account_field_names = []
    for field in result['fields']:
        account_field_names.append(field['name'])
    return account_field_names    

def getAllAccounts():
    # url = 'https://easypost.my.salesforce.com/services/data/' + apiVersion + '/sobjects/Account/listviews/00B1t0000073xoYEAQ/results?limit=2000'
    url = 'https://easypost.my.salesforce.com/services/data/' + apiVersion + '/query/?q=SELECT+Id+from+Account'
    response = apiRequest(url)
    result = json.loads(response.text)
    return result

def getAccountDetails(id):
    global apiVersion
    url = 'https://easypost.my.salesforce.com/services/data/' + apiVersion + '/sobjects/Account/' + id
    response = apiRequest(url)
    result = json.loads(response.text)
    return result

def getAccountIdByName(name):
    result = None
    try:
        url = "https://easypost.my.salesforce.com/services/data/" + apiVersion + "/query/?q=SELECT+Id+from+Account+where+Name='{}'".format(name)
        res = apiRequest(url)
        result = json.loads(res.text)['records']
    except Exception as ex:
        print(ex)
    return result
    
def getAccountContactRelation(id):
    global apiVersion
    url = 'https://easypost.my.salesforce.com/services/data/' + apiVersion + '/sobjects/AccountContactRelation/' + id
    response = apiRequest(url)
    result = json.loads(response.text)
    return result
    
def getAllAccountContacts():
    global apiVersion
    url = 'https://easypost.my.salesforce.com/services/data/' + apiVersion + '/sobjects/Contact/listviews/00B1t0000073xp1EAA/results?limit=2000'
    response = apiRequest(url)
    result = json.loads(response.text)
    return result

def getContact(id):
    global apiVersion
    url = 'https://easypost.my.salesforce.com/services/data/' + apiVersion + '/sobjects/Contact/' + id
    response = apiRequest(url)
    result = json.loads(response.text)
    return result

def getCompanyIdByName(name):
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q=SELECT+Klantnr_Easypost__c+from+Account+where+name='{}'".format(name)
    res = apiRequest(url)
    return json.loads(res.text)['records']

def queryAccountByName(name, fields):    
    fields = ', '.join(fields)
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q=SELECT+{}+from+Account+where+Name='{}'".format(fields, name)
    res = apiRequest(url)
    return json.loads(res.text)['records']

def queryByCompanyId(klantennr, fields):    
    fields = ', '.join(fields)
    print(fields)
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q=SELECT+{}+from+Account+where+Klantnr_Easypost__c={}".format(fields, klantennr)
    res = apiRequest(url)
    return json.loads(res.text)['records']

def queryRelatedContactsByCompanyId(klantennr):    
    fields = ['Contact.Rollen__c','Contact.Functie__c','Contact.Email']
    fields = ', '.join(fields)
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q=SELECT+{}+from+AccountContactRelation+where+Account.Klantnr_Easypost__c={}".format(fields, klantennr)
    res = apiRequest(url)
    return json.loads(res.text)['records']

def queryRelatedContactsByAccountId(accountId):    
    fields = ['Contact.Rollen__c','Contact.Functie__c','Contact.Email']
    fields = ', '.join(fields)
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q=SELECT+{}+from+AccountContactRelation+where+Account.Id={}".format(fields, accountId)
    res = apiRequest(url)
    return json.loads(res.text)['records']

def queryByCompanyId(klantennr, fields):    
    fields = ', '.join(fields)
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q=SELECT+{}+from+Account+where+Klantnr_Easypost__c={}".format(fields, klantennr)
    res = apiRequest(url)
    return json.loads(res.text)['records']

def queryByAccountId(id, fields):    
    fields = ', '.join(fields)
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q=SELECT+{}+from+Account+where+Id='{}'".format(fields, id)
    res = apiRequest(url)
    return json.loads(res.text)['records']

def getEmailByAccountId(id):
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q=SELECT+email+from+Contact+where+AccountId='{}'".format(id)
    res = apiRequest(url)
    return json.loads(res.text)['records']

def getEmailByAccountName(name):
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q=SELECT+email+from+Contact+where+Name='{}'".format(name)
    res = apiRequest(url)
    return json.loads(res.text)['records']

def getAllIndustryCategories():
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q=SELECT+Industry+from+Account+group+by+Industry"
    res = apiRequest(url)
    return json.loads(res.text)['records']

def queryContactsByAccountId(account_id, fields):
    fields = ', '.join(fields)
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q=SELECT+{}+FROM+Contact+where+AccountId='{}'".format(fields, account_id)
    res = apiRequest(url)
    return json.loads(res.text)

def query(table, fields):
    fields = ', '.join(fields)
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q=SELECT+{}+from+{}".format(fields, table)
    res = apiRequest(url)
    return json.loads(res.text)['records']

def customQuery(query):
    url = "https://easypost.my.salesforce.com/services/data/v46.0/query/?q={}".format(query)
    res = apiRequest(url)
    return json.loads(res.text)['records']

def updateAccount(Id, hub, hubvalue, round, roundvalue, retry = 0):
    try:
        sf.Account.update(str(Id),{hub:str(hubvalue),round:str(roundvalue)})
    except Exception as ex:
        if retry < 5:
            return updateAccount(Id=Id, hub=hub, hubvalue=hubvalue, round=round, roundvalue=roundvalue, retry=retry + 1)
        else:
            raise Exception('UpdateAccount Exception', 'Failed 5 times wiht last ex : ' + str(ex))

def getParentAccountEmail(client_nr):
    oauth()
    parentID = queryByCompanyId(client_nr, ['ParentId'])
    if parentID:
        parentID = parentID[0]['ParentId']
    if parentID:
        contacts = queryRelatedContactsByAccountId(parentID)
        email_address = False
        for contactWrapper in contacts:
            print(contactWrapper)
            contact = contactWrapper['Contact']
            print("roll: " + str(contact['Rollen__c']))
            print("func: " + str(contact['Functie__c']))
            print("parent roll: " + str(contact['Rollen__c']))
            print("parent func: " + str(contact['Functie__c']))
            if contact['Rollen__c']:
                if contact['Rollen__c'][-9:] == 'Postkamer':
                    if len(str(contact['Email'])) > 4:
                        print("oke Roll")
                        email_address = contact['Email']
            if contact['Functie__c']:
                if contact['Functie__c'][-9:] == 'Postkamer':
                    if len(str(contact['Email'])) > 4:
                        print("oke Func")
                        email_address = contact['Email']
    else:
        print("also no parent")
        return False
    return email_address


##
#
# PART WORKING BY DATABASE
#

def getEmailFromDB(client_nr, logger = None):
    global logs
    if logger:
        logs = logger
    try: 
        sql = """
                SELECT EmailMailRoom 
                FROM [EasyPost].[dbo].[SFAccounts]
                WHERE CustomerIdPost = {}""".format(client_nr)
        results = []
        with SQLFactory(SQLConnection.PRINTDB, config_path='c:\Software\Configs\eptools.json', logger = logs) as sql_factory:
            sql_factory.execute(sql)
            result = sql_factory.fetchone()
        return ';'.join(result)
    except Exception as ex:
        print(ex)
 
def AddressFromDB(client_nr, logger = None):
    global logs
    if logger:
        logs = logger
    try: 
        sql = """
                SELECT BillingPostalCode, BillingCity, BillingAddress as BillingStreet, Name
                FROM [EasyPost].[dbo].[SFAccounts]
                WHERE CustomerIdPost = {}""".format(client_nr)
        results = []
        with SQLFactory(SQLConnection.PRINTDB, config_path='c:\Software\Configs\eptools.json', logger = logs) as sql_factory:
            sql_factory.execute(sql)
            columns = [column[0] for column in sql_factory.cursor.description]
            for row in sql_factory.fetchall():
                results.append(dict(zip(columns, row)))
        return results
    except Exception as ex:
        print(ex)

def getHubAndRound(client_nr, logger = None):
    global logs
    if logger:
        logs = logger
    try: 
        sql = """
                DECLARE @CustomerIdPost INT -- replace INT with the data type of your CustomerIdPost column
                SET @CustomerIdPost = {}
				SELECT top(1) * FROM (
					-- PART 1 -- CHECK PickupLocations
					SELECT CustomerIdPost, Hub,RouteName, P.Name, 'SFPickupLocations' as Location, 1 as Priority
					FROM EasyPost.dbo.SFPickupLocations P
					WHERE CustomerIdPost = @CustomerIdPost -- and P.Hub is not null and P.Hub !='' and P.RouteName is not null and P.RouteName !=''
					UNION ALL
					-- PART 1 -- CHECK Departments
					SELECT  D.CustomerIdPost, Hub,RouteName,D.Name, 'SFDepartment' as Location, 2 as Priority
					FROM EasyPost.dbo.SFPickupLocations P
					LEFT JOIN EasyPost.dbo.SFDepartments D ON D.SFId = P.SFDepartmentId and P.CustomerIdPost = ''
					WHERE D.CustomerIdPost = @CustomerIdPost -- and P.Hub is not null and P.Hub !='' and P.RouteName is not null and P.RouteName !=''
					UNION ALL
					-- PART 1 -- CHECK Accounts
					SELECT  A.CustomerIdPost, P.Hub, P.RouteName,A.Name, 'SFAccount' as Location, 3 as Priority
					FROM EasyPost.dbo.SFPickupLocations P
					LEFT JOIN EasyPost.dbo.SFAccounts A ON A.SFId = P.SFAccountId and P.CustomerIdPost = '' and P.SFDepartmentId is null
					WHERE A.CustomerIdPost = @CustomerIdPost  and P.SFDepartmentId is null -- and P.Hub is not null and P.Hub !='' and P.RouteName is not null and P.RouteName !=''
					UNION ALL -- P.SFDepartmentId is null toegevoegd op 23/06
					-- PART 2 -- CHECK Department Parent Account
					SELECT  D.CustomerIdPost, P.Hub,P.RouteName, A.Name, 'SFDepartmentParentAccount' as Location, 4 as Priority
					FROM EasyPost.dbo.SFPickupLocations P
					LEFT JOIN EasyPost.dbo.SFAccounts A ON P.SFAccountId = A.SFId  and P.CustomerIdPost = '' and P.SFDepartmentId is null -- Get Parent PickupLocations
					LEFT JOIN EasyPost.dbo.SFDepartments D ON A.SFId = D.SFAccountId -- Get Department Parent Account
					WHERE D.CustomerIdPost = @CustomerIdPost -- Filter by DepartmentId
					UNION ALL
					-- CHECK PARENT Companies Id --
					-- LAST OPTION -- Check CustomerHub (Build From Excels Logistics)
					SELECT ch.CustomerId, ch.HubName as Hub, ch.RoundName as RouteName, c.Name, 'CustomerHub' as Location, 99 as Priority
					FROM EasyPostLogistiek.dbo.CustomerHub ch
					LEFT JOIN EasyPost.dbo.Companies c on ch.CustomerId=c.Id
					WHERE ch.CustomerId = @CustomerIdPost
				) innr
				order by Priority""".format(client_nr)
        results = []
        with SQLFactory(SQLConnection.PRINTDB, config_path='c:\Software\Configs\eptools.json', logger = logs) as sql_factory:
            sql_factory.execute(sql)
            columns = [column[0] for column in sql_factory.cursor.description]
            for row in sql_factory.fetchall():
                results.append(dict(zip(columns, row)))
        return results
    except Exception as ex:
        print(ex)

def getIdByName(client_name, logger = None):
    global logs
    if logger:
        logs = logger
    try: 
        sql = """
                SELECT CustomerIdPost
                FROM [EasyPost].[dbo].[SFAccounts]
                WHERE Name = '{}'""".format(client_name)
        results = []
        with SQLFactory(SQLConnection.PRINTDB, config_path='c:\Software\Configs\eptools.json', logger = logs) as sql_factory:
            sql_factory.execute(sql)
            columns = [column[0] for column in sql_factory.cursor.description]
            for row in sql_factory.fetchall():
                results.append(dict(zip(columns, row)))
        return results
    except Exception as ex:
        print(ex)

def getEmail(client_nr):
    reset_query = """IF OBJECT_ID('tempdb..#TempContacts') IS NOT NULL
                    BEGIN
                        DROP TABLE #TempContacts;
                    END
                    SET NOCOUNT ON;"""
    sql_query1 = """
        DECLARE @CustomerIdPost INT = {};
        WITH Contacts AS (
            SELECT Email, '1' as priority, Role
            FROM EasyPost.dbo.SFContacts
            WHERE SFPickupLocationId = (
                SELECT TOP 1 SFId
                FROM EasyPost.dbo.SFPickupLocations
                WHERE CustomerIdPost = @CustomerIdPost
            )
            AND (Role LIKE '%Contactpersoon Postkamer%' OR Role LIKE '%Hoofd Postkamer%')

            UNION ALL

            SELECT Email, '2' as priority, Role
            FROM EasyPost.dbo.SFContacts
            WHERE SFDepartmentId = (
                SELECT TOP 1 SFId
                FROM EasyPost.dbo.SFDepartments
                WHERE CustomerIdPost = @CustomerIdPost
            )
            AND (Role LIKE '%Contactpersoon Postkamer%' OR Role LIKE '%Hoofd Postkamer%')

            UNION ALL

            
            SELECT Email, '3' as priority, Role
            FROM EasyPost.dbo.SFContacts
            WHERE SFId in (
                SELECT SFContactId
                FROM [EasyPost].[dbo].[SFAccountContactRelations]
                WHERE SFAccountId = ( 
                    SELECT TOP 1 SFId
                    FROM EasyPost.dbo.SFAccounts
                    WHERE CustomerIdPost = @CustomerIdPost)
            )
            AND (Role LIKE '%Contactpersoon Postkamer%' OR Role LIKE '%Hoofd Postkamer%')
        )

        SELECT *
        INTO #TempContacts
        FROM Contacts

        IF EXISTS (
            SELECT *
            FROM #TempContacts
            WHERE Role LIKE '%Hoofd Postkamer%'
        )
        BEGIN
            SELECT *
            FROM #TempContacts
            WHERE Role LIKE '%Hoofd Postkamer%'
        END
        ELSE
        BEGIN
            SELECT *
            FROM #TempContacts
            WHERE Role LIKE '%Contactpersoon Postkamer%'
        END
        """.format(client_nr)
    results = []
    with SQLFactory(SQLConnection.PRINTDB, config_path='c:\Software\Configs\eptools.json', logger = logs) as sql_factory:
        sql_factory.execute(reset_query)
        sql_factory.commit()
        sql_factory.execute(sql_query1)
        columns = [column[0] for column in sql_factory.cursor.description]
        for row in sql_factory.fetchall():
            results.append(dict(zip(columns, row)))
    unique_emails = list(set(item['Email'] for item in results))

    return unique_emails

if __name__ == "__main__":
    print(getEmail(13326))
    getEmail(1499)
    getEmail(1627)
    # print(getHubAndRound(15555))
    # print(getIdByName('BVBA Gdw Legia'))
    # print(AddressFromDB(7255))

    # print(getParentAccountEmail(7255))
    # print(getEmailFromDB(7255))