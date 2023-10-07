from abc import ABC, abstractmethod
from .native import Connection

class SchemaBuilder(ABC):
    """
    Helper class to setup and migrate schemas 
    """

    @property
    def version(self) -> int: 
        """
        Returns the version of this schema 
        """
        ...
    
    @abstractmethod
    def setup(self, conn: Connection):
        """
        Creates the schema in an empty database
        
        This method should run its own transactions 
        """
        ...
    
    @abstractmethod
    def patch(self, conn: Connection):
        """
        Patches the schema.  This method assumes the 
        existing version is the previous schema version.
        
        This method should run its own transactions
        
        """
        ... 
        
__all__ = ['SchemaBuilder']