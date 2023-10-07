import json
from .credential_provider import CredentialProvider

class ConfigurationFileProvider(CredentialProvider):
    """
    A subclass of CredentialProvider that provides database credentials from a configuration file.

    This provider reads a JSON configuration file to fetch database credentials based on a specified 
    database type. The file is expected to contain a mapping of database types to their respective credentials.

    Attributes:
        filepath (str): Path to the JSON configuration file containing database credentials.
        credentials (dict): Parsed credentials from the configuration file.

    Methods:
        get_credentials(db_type, db_host): Retrieves credentials for the specified database type from the loaded data.

    Example:
        provider = ConfigurationFileProvider("path/to/config.json")
        mysql_credentials = provider.get_credentials("sql_server", "easypost_main")

    Raises:
        FileNotFoundError: If the provided filepath does not exist.
        json.JSONDecodeError: If there's an issue parsing the JSON configuration file.
    """

    def __init__(self, filepath: str) -> None:
        super().__init__()
        self.filepath = filepath
        self.credentials: dict = self._load_credentials()


    def _load_credentials(self) -> dict:
        with open(self.filepath, 'r') as file:
            return json.load(file)


    def get_credentials(self, db_type: str, db_host: str) -> dict:
        """
        Retrieves credentials for the specified database type.

        Args:
            db_type (str): Type of the database, e.g., `mysql` or `sql_server`
            db_host (str): Host of the database, e.g., `easypost_main`, `bluecrest` or `connect`.

        Returns:
            dict: Credentials for the specified database type or an empty dictionary if not found.
        """
        return self.credentials[db_type][db_host]