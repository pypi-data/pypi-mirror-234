from abc import ABC, abstractmethod
from typing import List

from ..model import DataAppAttributes, DataAppFunction, DataAppProfile


class IDataAppsService(ABC):

    @abstractmethod
    def get_all(self, user_id: int) -> List[DataAppProfile]:
        pass

    @abstractmethod
    def user_local_dataapp_list(self, user_id: int) -> List[DataAppProfile]:
        pass

    @abstractmethod
    def user_group_dataapp_list(self, user_id: int) -> List[DataAppProfile]:
        pass

    @abstractmethod
    def create(self, attributes: DataAppAttributes, data: List[str] = None,
               dataapp_functions: List[DataAppFunction] = None) -> DataAppProfile:
        pass

    @abstractmethod
    def get_dataapp_by_name(self, dataapp_name: str) -> DataAppProfile:
        pass

    @abstractmethod
    def get_dataapp_by_id(self, uid: int) -> DataAppProfile:
        pass

    @abstractmethod
    def delete_dataapp(self, uid: int, user_id: int) -> bool:
        pass

    @abstractmethod
    def delete_all(self) -> bool:
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
    def get_dataapp_privileges(self, dataapp_name: str) -> List[DataAppAttributes]:
        pass
