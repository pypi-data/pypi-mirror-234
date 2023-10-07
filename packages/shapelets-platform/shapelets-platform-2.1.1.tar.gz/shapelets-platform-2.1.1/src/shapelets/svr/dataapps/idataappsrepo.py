from abc import ABC, abstractmethod
from typing import List, Optional, Set, Tuple

from ..model import DataAppField, DataAppAttributes, DataAppFunction, DataAppProfile, PrincipalId


class IDataAppsRepo(ABC):
    @abstractmethod
    def load_all(self,
                 user_id: int,
                 attributes: Set[DataAppField],
                 skip: Optional[int],
                 sort_by: Optional[List[Tuple[DataAppField, bool]]],
                 limit: Optional[int]) -> List[DataAppProfile]:
        pass

    @abstractmethod
    def user_local_dataapp_list(self, user_id: int) -> List[DataAppProfile]:
        pass

    @abstractmethod
    def user_group_dataapp_list(self, user_id: int) -> List[DataAppProfile]:
        pass

    @abstractmethod
    def create(self, details: DataAppAttributes, data: List[str] = None,
               dataapp_functions: List[DataAppFunction] = None) -> Optional[DataAppProfile]:
        pass

    @abstractmethod
    def load_by_name(self, dataapp_name: str) -> Optional[DataAppProfile]:
        pass

    @abstractmethod
    def load_by_id(self, uid: str) -> Optional[DataAppProfile]:
        pass

    @abstractmethod
    def delete_dataapp(self, uid: int, user_id: int) -> bool:
        pass

    @abstractmethod
    def delete_all(self):
        pass

    @abstractmethod
    def get_dataapp_versions(self, dataapp_name: str) -> List[float]:
        pass

    @abstractmethod
    def get_dataapp_by_version(self, dataapp_name: str, major: int, minor: int) -> DataAppAttributes:
        pass

    @abstractmethod
    def get_dataapp_last_version(self, dataapp_name: str) -> float:
        pass

    @abstractmethod
    def get_dataapp_tags(self, dataapp_name: str) -> List[str]:
        pass

    @abstractmethod
    def load_by_principal(self, principal: PrincipalId) -> Optional[DataAppAttributes]:
        pass
