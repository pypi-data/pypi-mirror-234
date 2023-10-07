from __future__ import annotations

from typing import List
from weakref import WeakValueDictionary

from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.UserInfo import UserInfoCriteria, UserInfo


class VeloxUserManager:
    """
    Obtains info for users in Sapio.
    """
    user: SapioUser

    __instances: WeakValueDictionary[SapioUser, VeloxUserManager] = WeakValueDictionary()
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

    def get_user_info_list(self, criteria: UserInfoCriteria = UserInfoCriteria()) -> List[UserInfo]:
        """
        Retrieve list of user info data.
        :param criteria filters for the results.
        """
        sub_path = '/user/infolist/'
        response = self.user.post(sub_path, payload=criteria.to_json())
        self.user.raise_for_status(response)
        json_dct_list = response.json()
        return [UserInfo.parse(x) for x in json_dct_list]

    def get_user_name_list(self, include_deactivated_users: bool = False) -> List[str]:
        """
        Get a list of all available usernames in the Sapio system.
        :param include_deactivated_users: Whether to include the users that are deactivated.
        """
        sub_path = '/user/namelist/'
        params = {
            'includeDeactivatedUsers': include_deactivated_users
        }
        response = self.user.get(sub_path, params=params)
        self.user.raise_for_status(response)
        return response.json()