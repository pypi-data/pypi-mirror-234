from abc import ABC, abstractmethod

class CredentialProvider(ABC):
    @abstractmethod
    def get_credentials(self, db_type: str, db_host: str):
        pass