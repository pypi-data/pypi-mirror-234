from .connectors import MySQLConnector, SQLServerConnector

class ConnectionFactory:
    """
    A factory class responsible for providing database connectors based on the given database type.

    This factory currently supports `mysql` and `sql_server` databases. It uses the specified credential provider
    to establish the connection.

    Methods:
        get_connector(database_type, credential_provider): Returns a connector instance for the specified database type.

    Example:
        connection = ConnectionFactory.get_connector('mysql', EnvironmentVariableProvider())

    Attributes:
        database_type (str): Type of the database, e.g., 'mysql' or 'sql_server'.
        credential_provider (CredentialProvider): Provides credentials for the database connection. Instances of `EnvironmentVariableProvider` or `ConfigurationFileProvider` are expected.

    Raises:
        ValueError: If an unsupported database type is provided.
    """

    @staticmethod
    def get_connector(database_type, database_host, credential_provider):
        """
        Returns a connector instance for the specified database type.

        The function maps the provided database type to its corresponding connector class and then
        invokes its `get_connection` method with the given credential provider.

        Args:
            database_type (str): Type of the database. Can be either 'mysql' or 'sql_server'.
            credential_provider (CredentialProvider): Provides credentials for the database connection.

        Returns:
            object: A connection object for the specified database.

        Raises:
            ValueError: If the provided database type is unsupported.
        """

        connectors = {
            'mysql': MySQLConnector,
            'sql_server': SQLServerConnector
        }

        connector_class = connectors.get(database_type)
        if not connector_class:
            raise ValueError(f"Unsupported database type: {database_type}")
        
        return connector_class.get_connection(database_host, credential_provider)