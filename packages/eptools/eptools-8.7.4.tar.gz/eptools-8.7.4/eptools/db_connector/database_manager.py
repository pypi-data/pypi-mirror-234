from .connection_factory import ConnectionFactory


class DatabaseManager:
    """
    A manager for database operations.

    This manager supports operations such as SELECT, INSERT, UPDATE, DELETE and executing stored procedures.
    The database connections are established based on the given database type and credential provider.

    Attributes:
        database_type (str): Type of the database. Can be either `mysql` or `sql_server`.
        database_host (str): Host of the database. Can be either `easypost_main`, `bluecrest` or `connect`.
        credential_provider (CredentialProvider): Provides credentials for the database connection. Can be an instance of `EnvironmentVariableProvider` or `ConfigurationFileProvider`.

    Methods:
        select_query(query, params=None): Executes a SELECT query and returns the result set.
        insert_update_delete_query(query, params=None): Executes an INSERT, UPDATE, or DELETE query.
        execute_stored_procedure(procedure_name, *args): Executes a stored procedure and returns the result set if available.

    Example:
        db_manager = DatabaseManager('mysql', EnvironmentVariableProvider())
        results = db_manager.select_query("SELECT * FROM users")
    """

    def __init__(self, database_type, database_host, credential_provider):
        self.database_type = database_type
        self.database_host = database_host
        self.credential_provider = credential_provider


    def select_query(self, query, params=None):
        """
        Executes a SELECT query and returns the result set.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): Parameters to be passed to the SQL query. Default is None.

        Returns:
            list: A list of rows returned from the query.
        """

        connection = ConnectionFactory.get_connector(self.database_type, self.database_host, self.credential_provider)
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()


    def insert_update_delete_query(self, query, params=None):
        """
        Executes an INSERT, UPDATE, or DELETE query.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): Parameters to be passed to the SQL query. Default is None.
        """
        connection = ConnectionFactory.get_connector(self.database_type, self.credential_provider)
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
        finally:
            connection.close()


    def execute_stored_procedure(self, procedure_name, *args):
        """
        Executes a stored procedure and returns the result set if available.

        Args:
            procedure_name (str): Name of the stored procedure to be executed.
            *args: Variable arguments to be passed to the stored procedure.

        Returns:
            list: A list of rows returned from the stored procedure (if any).
        """
        connection = ConnectionFactory.get_connector(self.database_type, self.credential_provider)
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"EXEC {procedure_name} {', '.join(args)}")
                connection.commit()
                if cursor.description:  # Check if the procedure returned a result set
                    return cursor.fetchall()
        finally:
            connection.close()