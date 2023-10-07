from __future__ import annotations
from typing import List, Dict, Any
from weakref import WeakValueDictionary

from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.Picklist import PickListConfig, PicklistParser


class PicklistManager:
    """
    Manages picklists in Sapio.
    """
    user: SapioUser
    __instances: WeakValueDictionary[SapioUser, PicklistManager] = WeakValueDictionary()
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
        if self.__initialized:
            return
        self.user = user
        self.__initialized = True

    def get_picklist_config_list(self) -> List[PickListConfig]:
        """
        Get a list of all pick list configurations in the system.
        """
        sub_path: str = '/picklist/getConfigList'
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        json_list: List[Dict[str, Any]] = response.json()
        return [PicklistParser.parse_picklist_config(x) for x in json_list]

    def update_picklist_value_list(self, pick_list_name: str, pick_list_new_value_list: List[str]) \
            -> PickListConfig:
        """
        Update the specified pick list config in the system.
        :param pick_list_name: Name of the pick list to update.
        If there is no picklist by this pick list name, will create a new picklist with this name.
        :param pick_list_new_value_list: The list of values in the pick list
        :return: The new picklist config object.
        """
        sub_path = self.user.build_url(['picklist', 'updateConfigValueList', pick_list_name])
        response = self.user.post(sub_path, payload=pick_list_new_value_list)
        self.user.raise_for_status(response)
        json_dct = response.json()
        return PicklistParser.parse_picklist_config(json_dct)


# Alias classes
PickListManager: type = PicklistManager
