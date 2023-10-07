from __future__ import annotations
from typing import Any, Dict, List
from weakref import WeakValueDictionary

from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.datatype.DataType import DataTypeDefinition, DataTypeParser
from sapiopylib.rest.pojo.datatype.DataTypeLayout import DataTypeLayoutParser
from sapiopylib.rest.pojo.datatype.FieldDefinition import FieldDefinitionParser, AbstractVeloxFieldDefinition


class DataTypeManager:
    """
    Obtain information about data types in the system.
    """
    user: SapioUser

    __instances: WeakValueDictionary[SapioUser, DataTypeManager] = WeakValueDictionary()
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

    def get_field_definition_list(self, data_type_name: str) -> List[AbstractVeloxFieldDefinition]:
        """
        Get the list of field definitions that back the provided data type. These fields can be
        used to know what fields will be returned when getting records of this type.
        :param data_type_name: The data type name of the type containing the field definitions to return.
        """
        sub_path: str = self.user.build_url(['datatypemanager', 'veloxfieldlist', data_type_name])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        json_list: List[Dict[str, Any]] = response.json()
        return [FieldDefinitionParser.to_field_definition(x) for x in json_list]

    def get_data_type_name_list(self) -> List[str]:
        """
        The list of all data type names that exist in the system.
        These data type names can be used to query for fields and records of that type.
        The names can also be used to get field definitions of the type to know what fields can be retrieved.
        """
        sub_path: str = '/datatypemanager/datatypenamelist'
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        json_list: List[str] = response.json()
        return json_list

    def get_data_type_definition(self, data_type_name: str) -> DataTypeDefinition:
        """
        Get Data Type Definition
        :param data_type_name: The data type name of the data type definition to return.
        """
        sub_path: str = self.user.build_url(['datatypemanager', 'datatypedefinition', data_type_name])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        json_dct = response.json()
        return DataTypeParser.parse_data_type_definition(json_dct)

    def get_data_type_layout_list(self, data_type_name: str):
        """
        Get all available layouts for the provided data type name.
        :param data_type_name: The data type name to get layouts for.
        """
        sub_path: str = self.user.build_url(['datatypemanager', 'layout', data_type_name])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        json_list: List[Dict[str, Any]] = response.json()
        return [DataTypeLayoutParser.parse_layout(x) for x in json_list]
