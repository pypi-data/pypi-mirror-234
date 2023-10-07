from __future__ import annotations
from weakref import WeakValueDictionary

from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.Message import VeloxEmail, VeloxMessage


class SapioMessenger:
    """
    Send messages to users in Sapio. The message can be read later by user if offline.
    """
    user: SapioUser

    __instances: WeakValueDictionary[SapioUser, SapioMessenger] = WeakValueDictionary()
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

    def send_email(self, email: VeloxEmail) -> None:
        """
        Send an email using the SMTP server configured in the Sapio Platform.
        """
        sub_path = '/email/send/'
        response = self.user.post(sub_path, payload=email.to_json())
        self.user.raise_for_status(response)

    def send_message(self, message: VeloxMessage) -> None:
        """
        Send a message to users in the app based on username or group.
        """
        sub_path = '/message'
        response = self.user.post(sub_path, payload=message.to_json())
        self.user.raise_for_status(response)

