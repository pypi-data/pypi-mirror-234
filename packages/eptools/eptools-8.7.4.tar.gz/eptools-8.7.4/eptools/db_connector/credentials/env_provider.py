import os
from .credential_provider import CredentialProvider

class EnvironmentVariableProvider(CredentialProvider):
    """
    A subclass of CredentialProvider that retrieves database credentials from environment variables.

    This provider fetches credentials based on a given database type using predefined environment variable patterns.
    The expected pattern for environment variables is `<DB_TYPE>_<DB_HOST>_<KEY>`, where `<DB_TYPE>` is the uppercase form 
    of the database type (e.g., MYSQL, SQL_SERVER), `<DB_HOST>` is the uppercase form 
    of the database host (e.g., EASYPOST_MAIN, BLUECREST or CONNECT) and `<KEY>` corresponds to specific credential fields 
    (e.g., HOST, USER, PASSWORD, NAME).

    Methods:
        get_credentials(db_type, db_host): Retrieves the credentials for a specified database type from environment variables.

    Example:
        provider = EnvironmentVariableProvider()
        mysql_credentials = provider.get_credentials("sql_server", "easypost_main")

    Note:
        For this class to function correctly, the relevant environment variables must be set before usage.
    """

    def get_credentials(self, db_type: str, db_host: str):
        """
        Retrieves credentials for the specified database type from environment variables.

        The method forms the names of environment variables based on the provided database type and looks them up.
        If any of the variables are not set, their corresponding values in the resulting dictionary will be None.

        Args:
            db_type (str): Type of the database, e.g., `mysql` or `sql_server`
            db_host (str): Host of the database, e.g., `easypost_main`, `bluecrest` or `connect`.

        Returns:
            dict: A dictionary containing keys (host, user, password, database) and their corresponding values 
                  retrieved from environment variables.
        """

        return {
            'host': os.getenv(f'{db_type.upper()}_{db_host.upper()}_HOST'),
            'user': os.getenv(f'{db_type.upper()}_{db_host.upper()}_USER'),
            'password': os.getenv(f'{db_type.upper()}_{db_host.upper()}_PASSWORD'),
            'database': os.getenv(f'{db_type.upper()}_{db_host.upper()}_NAME'),
        }