from blacksheep import WebSocket
from dataclasses import dataclass


@dataclass
class Message:
    """
    Websocket message so the UI knows when to refresh the dataapp section
    """
    dataapp_name: str
    dataapp_id: str
    user_id: str
    is_delete: bool
    major: int = None
    minor: int = None

    def to_string(self, root_panel_dataapp: str = None) -> str:
        """
        UI expects message in specific formats:
        - *:delete:NAME:{dataapp_name}:VERSION:{major}.{minor} -> when a dataapp must be removed from the dataapp section
        - *:NAME:{dataapp_id} -> when a dataapp must be added to the dataapp section
        """
        if root_panel_dataapp is not None:
            if self.is_delete:
                return f"{root_panel_dataapp}:delete:NAME:{self.dataapp_name}:USER:{self.user_id}:VERSION:{self.major}.{self.minor}"
            return f"{root_panel_dataapp}:NAME:{self.dataapp_id}:USER:{self.user_id}"
        else:
            if self.is_delete:
                return f"{self.dataapp_name}:delete:USER:{self.user_id}:VERSION:{self.major}.{self.minor}"
            return f"NAME:{self.dataapp_id}:USER:{self.user_id}"


@dataclass
class DataAppChangeListeners:
    ROOT_PANEL_DATA_APP = "*"
    by_app_name = {}
    listener_to_app_name = {}

    def add(self, dataapp_name: str, listener):
        """
        Add listener route to the class.
        """
        listener_ws = self.by_app_name.get(dataapp_name)
        if not listener_ws:
            self.by_app_name[dataapp_name] = listener
        self.listener_to_app_name[listener] = dataapp_name

    async def notify(self, dataapp_name: str, dataapp_id: str, user_id: str, is_delete: bool, major: int = None, minor: int = None):
        """
        Server notifies that there is change in a dataapp, either created or deleted.
        """
        change_listeners = self.by_app_name.get(dataapp_name)
        if change_listeners:
            message = Message(dataapp_name, dataapp_id, user_id, is_delete, major, minor)
            sent = await self.send(message.to_string(), change_listeners)
            if not sent or is_delete:
                self.remove(change_listeners)
        root_page_listeners = self.by_app_name.get(self.ROOT_PANEL_DATA_APP)
        if root_page_listeners:
            message = Message(dataapp_name, dataapp_id, user_id, is_delete, major, minor)
            sent = await self.send(message.to_string(self.ROOT_PANEL_DATA_APP), root_page_listeners)
            if not sent:
                self.remove(root_page_listeners)

    async def send(self, message: str, listener: WebSocket) -> bool:
        """
        Send message to client.
        """
        can_notify = True
        try:
            if can_notify:
                await listener.send_text(message)
        except:
            can_notify = False
        return can_notify

    def remove(self, listener: WebSocket):
        """
        Remove listener from class.
        """
        dataapp_name = self.listener_to_app_name.get(listener)
        if dataapp_name:
            del self.listener_to_app_name[listener]
            change_listeners = self.by_app_name.get(dataapp_name)
            if change_listeners:
                del self.by_app_name[dataapp_name]
