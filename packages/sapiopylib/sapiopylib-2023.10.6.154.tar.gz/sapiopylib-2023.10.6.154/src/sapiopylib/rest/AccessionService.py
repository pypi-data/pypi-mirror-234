from __future__ import annotations
from typing import Optional, Dict, Any, List
from weakref import WeakValueDictionary

from sapiopylib.rest.User import SapioUser
from enum import Enum


class AccessionCriteriaType(Enum):
    """
    Accessioning cache type.

    SYSTEM: Global accessioning. Note that Accession Service from Sapio Foundations do not use this cache.

    DATA_FIELD: Cached per data type's maximum value of a data field.
    """
    SYSTEM = 1
    DATA_FIELD = 2


class AbstractAccessionCriteriaPojo:
    """
    Describes a criteria for server accession service request, in order to obtain a list of accession IDs.
    """
    criteria_type: AccessionCriteriaType
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    sequence_key: Optional[str]
    initial_sequence_value: int = 1

    def __init__(self, criteria_type: AccessionCriteriaType, sequence_key: str):
        """
        INTERNAL ONLY. Use one of the sub-classes.
        """
        self.criteria_type = criteria_type
        self.sequence_key = sequence_key

    def from_pojo(self, json_dct: dict) -> None:
        self.prefix = json_dct.get('prefix')
        self.suffix = json_dct.get('suffix')
        self.sequence_key = json_dct.get('sequenceKey')
        self.initial_sequence_value = int(json_dct.get('initialSequenceValue'))

    def to_pojo(self) -> Dict[str, Any]:
        return {
            'criteriaType': self.criteria_type.name,
            'prefix': self.prefix,
            'suffix': self.suffix,
            'sequenceKey': self.sequence_key,
            'initialSequenceValue': self.initial_sequence_value
        }


class AccessionSystemCriteriaPojo(AbstractAccessionCriteriaPojo):
    """
    Describes request to accession a global (unrelated to data records) accession IDs.
    """
    def __init__(self, sequence_key: str):
        """
        Accession by sequence order in sequence key, regardless of existing record values.
        :param sequence_key: The sequence table ID to accession for. IDs in the same sequence will not duplicate.
        """
        super().__init__(AccessionCriteriaType.SYSTEM, sequence_key)


class AccessionDataFieldCriteriaPojo(AbstractAccessionCriteriaPojo):
    """
    Describes request to accession data record's IDs for a data field under a specified format.
    """
    data_type_name: str
    data_field_name: str

    def __init__(self, data_type_name: str, data_field_name: str, sequence_key: str):
        """
        Accession for a data field's value
        :param data_type_name: The data type name to accession
        :param data_field_name: The data field name to accession
        :param sequence_key: The sequence key that must be unique for the same formatting (prefix, suffix) of IDs.
        """
        super().__init__(AccessionCriteriaType.DATA_FIELD, sequence_key)
        self.data_type_name = data_type_name
        self.data_field_name = data_field_name

    def from_pojo(self, json_dct: dict):
        super().from_pojo(json_dct)
        self.data_type_name = json_dct.get('dataTypeName')
        self.data_field_name = json_dct.get('dataFieldName')

    def to_pojo(self) -> Dict[str, Any]:
        ret = super().to_pojo()
        ret['dataTypeName'] = self.data_type_name
        ret['dataFieldName'] = self.data_field_name
        return ret


class AccessionManager:
    """
    Accession new IDs for the system to be consistent with plugin logic.
    """
    user: SapioUser
    __instances: WeakValueDictionary[SapioUser, AccessionManager] = WeakValueDictionary()
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
        Obtains REST accession manager to perform accessioning operations.
        """
        if self.__initialized:
            return
        self.user = user
        self.__initialized = True

    def accession_for_system(self, num_to_accession: int, criteria: AccessionSystemCriteriaPojo) -> List[str]:
        """
        Accession IDs that do not need to get starting value from a data field.
        :param num_to_accession: Number of IDs to return
        :param criteria: The accession format.
        :return: list if unique IDs that will never be generated with this method again.
        """
        sub_path = self.user.build_url(['accession', 'accessionForSystem'])
        param = {'numToAccession': num_to_accession}
        payload = criteria.to_pojo()
        response = self.user.post(sub_path, param, payload)
        self.user.raise_for_status(response)
        return response.json()

    def accession_for_field(self, num_to_accession: int, criteria: AccessionDataFieldCriteriaPojo) -> List[str]:
        """
        Accession IDs for the data fields.
        If this is the first time, look up starting value to be greater than the maximum of existing ID (+1).
        :param num_to_accession: Number of IDs to return
        :param criteria: The rules on how an ID should be generated.
        :return: List of generated IDs
        """
        sub_path = self.user.build_url(['accession', 'accessionForField'])
        param = {'numToAccession': num_to_accession}
        payload = criteria.to_pojo()
        response = self.user.post(sub_path, param, payload)
        self.user.raise_for_status(response)
        return response.json()
