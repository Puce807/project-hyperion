from abc import ABC, abstractmethod

class DataSource(ABC):
    name: str
    table: str
    query_fields: dict
    schema: str

    @abstractmethod
    def fetch(self, limit):
        """Fetch data from the remote source"""
        pass

    @abstractmethod
    def normalise(self, data):
        """Convert source-specific data into Hyperion data model"""
        pass

