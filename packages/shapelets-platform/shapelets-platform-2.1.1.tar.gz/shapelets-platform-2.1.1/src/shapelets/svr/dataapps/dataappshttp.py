import json
import os
from decimal import Decimal
from collections import Counter

from blacksheep import FromJSON, Request, unauthorized, WebSocket
from blacksheep.server.controllers import ApiController, delete, file, get, post, ws
from guardpost.authentication import Identity
from requests import Session
from typing import List, Optional, Union

from .dataapps_ws import DataAppChangeListeners
from .idataappsservice import IDataAppsService

from ..groups import InvalidGroupName
from ..model import DataAppAttributes, DataAppFunction, DataAppProfile, SignedPrincipalId
from ..telemetry import ITelemetryService
from ..users import UserDoesNotBelong, WritePermission


def _tel_extract_types(data: Union[dict, List]):
    """
    Extract widget types. This function is recursive when a Layout is found, and we need to go 'deeper'.
    """
    types = []

    if isinstance(data, dict):
        if "type" in data:
            types.append(data["type"])

        for key, value in data.items():
            types.extend(_tel_extract_types(value))

    elif isinstance(data, list):
        for item in data:
            types.extend(_tel_extract_types(item))

    return types


def _tel_count_widgets(spec: str) -> Union[dict, List]:
    try:
        widgets = json.loads(spec)["mainPanel"]["properties"]["widgets"]
        widget_types = _tel_extract_types(widgets)
        return dict(Counter(widget_types))
    except Exception:
        return []


def _check_user_identity(request: Request) -> int:
    if request.identity:
        return request.identity.claims["userId"]
    elif request.get_first_header(b"authorization"):
        header_value = request.get_first_header(b"authorization")
        token = header_value.decode('ascii').split("Bearer ", 1)[1]
        principal = SignedPrincipalId.from_token(token)
        if principal is None:
            raise RuntimeError(f"Invalid bearer token: {header_value}")
        return principal.userId
    else:
        message = "Unable to find user for dataApp registration. Please, login."
        print(message)
        return unauthorized(message)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


class DataAppsHttpServer(ApiController):
    def __init__(self, svr: IDataAppsService, telemetry: ITelemetryService) -> None:
        self._svr = svr
        self._telemetry = telemetry
        super().__init__()
        self.dataapp_change_listeners = DataAppChangeListeners()

    @classmethod
    def route(cls) -> Optional[str]:
        return '/api/dataapps'

    @ws("/ws")
    async def ws(self, websocket: WebSocket):
        await websocket.accept()
        try:
            msg = await websocket.receive_text()
            self.dataapp_change_listeners.add(msg, websocket)
            while True:
                msg = await websocket.receive_text()
        except Exception as e:
            print(e)
        finally:
            self.dataapp_change_listeners.remove(websocket)

    @get("/")
    async def dataapp_list(self, user: Identity) -> List[DataAppProfile]:
        if user is None:
            raise RuntimeError(f"Unable to find user for dataApp registration. Please, login.")
        try:
            user_id = user.claims["userId"]
            self._svr.get_all(user_id)
            return self.ok()
        except Exception as e:
            return self.status_code(500, str(e))

    @get("/user")
    async def user_local_dataapp_list(self, user: Identity) -> List[DataAppAttributes]:
        """
        Returns all dataApps that belong only to the user. Like the user local develop section.
        """
        if user is None:
            raise RuntimeError(f"Unable to find user for dataApp registration. Please, login.")
        user_id = user.claims["userId"]
        return self._svr.user_local_dataapp_list(user_id)

    @get("/groups")
    async def user_group_dataapp_list(self, user: Identity) -> List[DataAppAttributes]:
        """
        Returns all dataApps that belong to any group that the user belongs.
        """
        if user is None:
            raise RuntimeError(f"Unable to find user for dataApp registration. Please, login.")
        user_id = user.claims["userId"]
        return self._svr.user_group_dataapp_list(user_id)

    @post("/")
    async def create(self, request: Request, attributes: FromJSON[DataAppAttributes], data) -> DataAppProfile:
        """
        Endpoint to create a dataApp.

        param request: info from the request. It is used to check the identity of the user trying to register the dataApp.
                       First, the user must be logged in in order to register a dataApp. Once the user is logged in,
                       the user permission are checked to make sure the user can register or update the desired dataApp.
        param attributes: contains the main information from the dataApp.
        param data: contains additional information of the files (uid) that the dataApp uses,
                    so we can keep track of the files used by the dataApp and update/delete when needed.
        """
        try:
            user_id = _check_user_identity(request)
            dataapp_attributes = DataAppAttributes(name=attributes.value.name,
                                                   major=attributes.value.major,
                                                   minor=attributes.value.minor,
                                                   description=attributes.value.description,
                                                   specId=attributes.value.specId,
                                                   tags=attributes.value.tags,
                                                   groups=attributes.value.groups,
                                                   userId=user_id)
            dataapp_functions = []
            for fn in attributes.value.functions:
                dataapp_functions.append(DataAppFunction(uid=fn["uid"], ser_body=fn["ser_body"]))

            dataapp = self._svr.create(dataapp_attributes, data, dataapp_functions)
            tel_info = {
                "dataapp_id": dataapp.uid,
                "dataapp_version": f"{dataapp.major}.{dataapp.minor}",
                "dataapp_creation_date": dataapp.creationDate,
                "dataapp_update_date": dataapp.updateDate,
                "user_id": user_id,
                "dataapp_groups": dataapp.groups,
                "amount_custom_fn": len(dataapp_functions),
                "widgets": _tel_count_widgets(attributes.value.specId)
            }
            self._telemetry.send_telemetry(event="DataAppCreated", info=tel_info)
            await self.dataapp_change_listeners.notify(dataapp.name, dataapp.uid, user_id, False)
            return dataapp
        except UserDoesNotBelong as e:
            return self.bad_request(str(e))
        except InvalidGroupName as e:
            return self.bad_request(str(e))
        except WritePermission as e:
            return self.bad_request(str(e))
        except Exception as e:
            return self.status_code(500, str(e))

    @get("/name/{dataAppName}")
    async def get_dataapp_by_name(self, request: Request, dataAppName: str) -> DataAppAttributes:
        user_id = _check_user_identity(request)
        dataapp = self._svr.get_dataapp_by_name(dataAppName)
        tel_info = {
            "dataapp_id": dataapp.uid,
            "from": "Home",
            "user_id": user_id
        }
        self._telemetry.send_telemetry(event="DataAppVisualization", info=tel_info)
        return dataapp

    @get("/{id}")
    async def get_dataapp_by_id(self, id: str) -> DataAppAttributes:
        return self._svr.get_dataapp_by_id(id)

    @delete("/")
    async def delete_all(self, request: Request) -> bool:
        user_id = _check_user_identity(request)
        response = self._svr.delete_all()
        self._telemetry.send_telemetry(event="DataAppDeleteAll", info={"user_id": user_id})
        return response

    @delete("/{id}")
    async def delete(self, uid: int, user: Identity) -> bool:
        if user is None:
            raise RuntimeError(f"Unable to find user. Please, login.")
        user_id = user.claims["userId"]
        dataapp = self._svr.get_dataapp_by_id(uid)
        if self._svr.delete_dataapp(uid, user_id):
            await self.dataapp_change_listeners.notify(dataapp.name, dataapp.uid, user_id, True, dataapp.major,
                                                       dataapp.minor)
            tel_info = {
                "dataapp_id": dataapp.uid,
                'user_id': user_id,
            }
            self._telemetry.send_telemetry(event="DataAppDelete", info=tel_info)
            return self.ok("DataApp removed successfully.")
        return self.bad_request()

    @get("/{id}/privileges")
    async def get_dataapp_privileges(self, dataapp_id: int) -> List[DataAppAttributes]:
        return self._svr.get_dataapp_privileges(dataapp_id)

    @get("/{id}/versions")
    async def get_dataapp_versions(self, dataAppName: str) -> List[float]:
        return json.dumps(self._svr.get_dataapp_versions(dataAppName), cls=DecimalEncoder)

    @get("spec/{specId}")
    async def get_dataapp_spec(self, specId: str) -> file:
        shapelets_dir = os.path.expanduser('~/.shapelets')
        data_apps_store = os.path.join(shapelets_dir, 'dataAppsStore')
        spec_path = os.path.join(data_apps_store, f"{specId}.json")
        return file(spec_path, "multipart/form-data")

    @get("/{id}/{major}/{minor}")
    async def get_dataapp_by_version(self, request: Request, dataAppName: str, major: int,
                                     minor: int) -> DataAppProfile:
        user_id = _check_user_identity(request)
        dataapp = self._svr.get_dataapp_by_version(dataAppName, major, minor)
        tel_info = {
            "dataapp_id": dataapp.uid,
            "from": "dataAppSection",
            "user_id": user_id
        }
        self._telemetry.send_telemetry(event="DataAppVisualization", info=tel_info)
        return dataapp

    @get("/{id}/lastVersion")
    async def get_dataapp_last_version(self, dataAppName: str) -> float:
        return self._svr.get_dataapp_last_version(dataAppName)

    @get("/{id}/tags")
    async def get_dataapp_tags(self, dataAppName: str) -> List[str]:
        return self._svr.get_dataapp_tags(dataAppName)


class DataAppsHttpProxy(IDataAppsService):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> List[DataAppProfile]:
        return self.session.get('/api/dataapps/')

    def user_local_dataapp_list(self) -> List[DataAppProfile]:
        return self.session.get('/api/dataapps/user')

    def user_group_dataapp_list(self) -> List[DataAppProfile]:
        return self.session.get('/api/dataapps/groups')

    def create(self, dataapp) -> DataAppProfile:
        params = []
        if dataapp.functions is not None:
            dataapp_functions = []
            for key, item in dataapp.functions.items():
                dataapp_functions.append(DataAppFunction(uid=key, ser_body=item["ser_body"]))

        payload = DataAppAttributes(name=dataapp.name,
                                    major=dataapp.version[0] if dataapp.version else None,
                                    minor=dataapp.version[1] if dataapp.version else None,
                                    description=dataapp.description,
                                    specId=dataapp.to_json(),
                                    tags=dataapp.tags,
                                    groups=dataapp.groups,
                                    functions=dataapp_functions)

        if dataapp._data:
            params.append(("data", dataapp._data))
        response = self.session.post('/api/dataapps/', json=json.loads(payload.json()), params=params)
        if response.status_code != 200:
            raise RuntimeError(response.content)
        return response

    def get_dataapp_by_name(self, dataAppName: str) -> DataAppAttributes:
        return self.session.get('/api/dataapps/name/', params=[("dataAppName", dataAppName)])

    def get_dataapp_by_id(self, id: str) -> DataAppAttributes:
        return self.session.get('/api/dataapps/', params=[("id", id)])

    def delete_dataapp(self, uid: int):
        self.session.delete('/api/dataapps/{id}', params=[("uid", uid)])

    def delete_all(self) -> bool:
        self.session.delete('/api/dataapps/')
        return True

    def get_dataapp_privileges(self, dataAppName: str) -> List[DataAppAttributes]:
        pass

    def get_dataapp_versions(self, dataAppName: str) -> List[float]:
        return self.session.get('/api/{id}/versions', params=[("dataAppName", dataAppName)])

    def get_dataapp_by_id(self, uid: int) -> DataAppProfile:
        return self.session.get('/api/{id}', params=[("uid", uid)])

    def get_dataapp_by_version(self, dataAppName: str, major: int, minor: int) -> DataAppProfile:
        response = self.session.get(f'/api/dataapps/{id}/{major}/{minor}', params=[("dataAppName", dataAppName),
                                                                                   ("major", major),
                                                                                   ("minor", minor)])
        return response.json()

    def get_dataapp_last_version(self, dataAppName: str) -> float:
        return self.session.get('/api/{id}/lastVersion', params=[("dataAppName", dataAppName)])

    def get_dataapp_tags(self, dataAppName: str) -> List[str]:
        return self.session.get('/api/{id}/tags', params=[("dataAppName", dataAppName)])
