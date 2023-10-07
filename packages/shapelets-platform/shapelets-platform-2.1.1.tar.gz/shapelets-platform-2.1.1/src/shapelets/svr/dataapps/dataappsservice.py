from typing import List, Optional, Set, Tuple

from .idataappsrepo import IDataAppsRepo
from .idataappsservice import IDataAppsService
from ..model import (
    DataAppAllFields,
    DataAppAttributes,
    DataAppField,
    DataAppFunction,
    DataAppProfile
)


class DataAppsService(IDataAppsService):
    __slots__ = ('_dataapps_repo',)

    def __init__(self, dataapp_repo: IDataAppsRepo) -> None:
        self._dataapp_repo = dataapp_repo

    def get_all(self,
                user_id: int,
                attributes: Optional[Set[DataAppField]] = DataAppAllFields,
                sort_by: Optional[List[Tuple[DataAppField, bool]]] = None,
                skip: Optional[int] = None,
                limit: Optional[int] = None) -> List[DataAppProfile]:
        return self._dataapp_repo.load_all(user_id, attributes, sort_by, skip, limit)

    def user_local_dataapp_list(self, user_id: int) -> List[DataAppProfile]:
        return self._dataapp_repo.user_local_dataapp_list(user_id)

    def user_group_dataapp_list(self, user_id: int) -> List[DataAppProfile]:
        return self._dataapp_repo.user_group_dataapp_list(user_id)

    def create(self, attributes: DataAppAttributes, data: List[str] = None,
               dataapp_functions: List[DataAppFunction] = None) -> DataAppProfile:
        return self._dataapp_repo.create(attributes, data, dataapp_functions)

    def get_dataapp_by_name(self, dataapp_name: str):
        return self._dataapp_repo.load_by_name(dataapp_name)

    def get_dataapp_by_id(self, uid: int) -> DataAppProfile:
        return self._dataapp_repo.load_by_id(uid)

    def delete_dataapp(self, uid: int, user_id: int) -> bool:
        return self._dataapp_repo.delete_dataapp(uid, user_id)

    def delete_all(self) -> bool:
        self._dataapp_repo.delete_all()

    def get_dataapp_versions(self, dataapp_name: str) -> List[float]:
        return self._dataapp_repo.get_dataapp_versions(dataapp_name)

    def get_dataapp_by_version(self, dataapp_name: str, major: int, minor: int) -> DataAppAttributes:
        return self._dataapp_repo.get_dataapp_by_version(dataapp_name, major, minor)

    def get_dataapp_last_version(self, dataapp_name: str) -> float:
        self._dataapp_repo.get_dataapp_last_version(dataapp_name)

    def get_dataapp_tags(self, dataapp_name: str) -> List[str]:
        self._dataapp_repo.get_dataapp_tags(dataapp_name)

    def get_dataapp_privileges(self, dataapp_name: str) -> List[DataAppAttributes]:
        pass
