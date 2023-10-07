from __future__ import annotations

from weakref import WeakValueDictionary

from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.chartdata.DashboardDefinition import DashboardDefinition, DashboardDefinitionParser


class DashboardManager:
    """
    Manages creation, modification, deletion of charts in Sapio.
    """

    user: SapioUser

    __instances: WeakValueDictionary[SapioUser, DashboardManager] = WeakValueDictionary()
    __initialized: bool

    def __new__(cls, user: SapioUser):
        """
        Observes singleton pattern per record model manager object.
        """
        obj = cls.__instances.get(user)
        if not obj:
            obj = object.__new__(cls)
            obj.__initialized = False
            cls.__instances[user] = obj
        return obj

    def __init__(self, user: SapioUser):
        """
        Obtain a dashboard manager to create, modify, or delete charts in Sapio.
        :param user: The Sapio user context.
        """
        if self.__initialized:
            return
        self.user = user

    def delete_dashboard_definition(self, dashboard_guid: str) -> None:
        """
        Delete an existing dashboard by the dashboard GUID.
        """
        if not dashboard_guid:
            raise ValueError("Dashboard GUID must be specified.")
        url = self.user.build_url(['dashboard', dashboard_guid])
        response = self.user.delete(url)
        self.user.raise_for_status(response)
        return

    def get_dashboard(self, dashboard_guid: str) -> DashboardDefinition:
        """
        Get an existing dashboard stored in the system by its dashboard GUID.
        """
        if not dashboard_guid:
            raise ValueError("Dashboard GUID must be specified.")
        url = self.user.build_url(['dashboard', dashboard_guid])
        response = self.user.get(url)
        self.user.raise_for_status(response)
        json = response.json()
        return DashboardDefinitionParser.parse_dashboard_definition(json)

    def store_dashboard_definition(self, dashboard: DashboardDefinition) -> DashboardDefinition:
        """
        Store either a new or existing dashboard to the system.
        :param dashboard: The dashboard object to be stored
        :return: The returned dashboard object after store has completed.
        If this is a new dashboard, the GUIDs, etc., will not be populated.
        """
        url = self.user.build_url(['dashboard'])
        response = self.user.post(url, payload=dashboard.to_json())
        self.user.raise_for_status(response)
        json = response.json()
        return DashboardDefinitionParser.parse_dashboard_definition(json)

