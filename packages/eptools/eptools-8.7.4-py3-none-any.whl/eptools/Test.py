from db_connector.credentials import ConfigurationFileProvider
from db_connector import DatabaseManager

provider = ConfigurationFileProvider("C:\\Software\\Configs\\eptools.json")
db_manager = DatabaseManager("sql_server", provider)

select_sql = "SELECT * FROM PostaliaMailId..MailIdOCRBatchSFStatus WHERE BatchId = ?"

results = db_manager.select_query(select_sql, (1,))
for row in results:
    print(row)