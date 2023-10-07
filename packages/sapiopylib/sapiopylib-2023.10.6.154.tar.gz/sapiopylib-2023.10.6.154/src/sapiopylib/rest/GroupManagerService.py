from __future__ import annotations

from typing import List, Dict, Any
from weakref import WeakValueDictionary

from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.UserInfo import UserGroupInfo, UserInfo


class VeloxGroupManager:
    """
    Obtains info for groups in Sapio.
    """
    user: SapioUser

    __instances: WeakValueDictionary[SapioUser, VeloxGroupManager] = WeakValueDictionary()
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

    def get_user_group_name_list(self) -> List[str]:
        """
        Get the list of all user group names in the system.
        """
        sub_path = '/usergroup/namelist/'
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        return response.json()

    def get_user_group_info_list(self) -> List[UserGroupInfo]:
        """
        Get the list of all User Group Info objects representing all User Groups in the system.
        """
        sub_path = '/usergroup/infolist/'
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        return [UserGroupInfo.parse(x) for x in response.json()]

    def get_user_group_info_by_id(self, group_id: int) -> UserGroupInfo:
        """
        Get a user group info by its group id
        :param group_id: The group ID we are getting info for.
        """
        sub_path = self.user.build_url(['usergroup', 'info', 'id', str(group_id)])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        return UserGroupInfo.parse(response.json())

    def get_user_group_info_by_name(self, group_name: str) -> UserGroupInfo:
        """
        Get a user group info by its name
        """
        sub_path = self.user.build_url(['usergroup', 'info', 'name', group_name])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        return UserGroupInfo.parse(response.json())

    def get_user_info_list_for_group(self, group_name: str) -> List[UserGroupInfo]:
        """
        Given the group name, retrieve user info list of all users who have membership to the given group.
        """
        sub_path = self.user.build_url(['usergroup', 'userassignment', group_name])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        return [UserInfo.parse(x) for x in response.json()]

    def get_user_info_map_for_groups(self, group_names: List[str]) -> Dict[str, List[UserInfo]]:
        """
        Given a collection of group names, retrieve a user info list for each group, mapped by group names.
        """
        sub_path = '/usergroup/userassignment/'
        response = self.user.post(sub_path, payload=group_names)
        self.user.raise_for_status(response)
        raw_json: Dict[str, List[Dict[str, Any]]] = response.json()
        ret: Dict[str, List[UserInfo]] = dict()
        for key, value in raw_json.items():
            user_info_list = [UserInfo.parse(x) for x in value]
            ret[key] = user_info_list
        return ret

    def get_user_group_info_list_for_user(self, username: str) -> List[UserGroupInfo]:
        """
        Get a list of user groups the given user has membership of.
        :param username The username to search membership for.
        """
        sub_path = self.user.build_url(['usergroup', 'groupassignment', username])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        return [UserGroupInfo.parse(x) for x in response.json()]