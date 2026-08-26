from abc import ABC, abstractmethod

class DataSource(ABC):
    name: str
    table: str
    query_fields: dict
    schema: str
    database_fields: list
    # NOTE: database_fields *MUST* be in the same order as query_fields

    @abstractmethod
    def fetch(self, limit):
        """Fetch data from the remote source"""
        pass

    @abstractmethod
    def normalise(self, data):
        """Convert source-specific data into Hyperion data model"""
        pass

