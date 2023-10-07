from __future__ import annotations

from abc import abstractmethod, ABC
from typing import List, Type, TypeVar, Dict, Any, Optional, Iterable

from sapiopylib.rest.pojo.datatype.FieldDefinition import FieldType

from sapiopylib.rest.pojo.DataRecord import DataRecord

from sapiopylib.rest.utils.recordmodel.PyRecordModel import PyRecordModel, SapioRecordModelException, \
    RecordModelFieldMap, AbstractRecordModelPropertyGetter, RecordModelPropertyType, AbstractRecordModelPropertyAdder, \
    AbstractRecordModelPropertyRemover, AbstractRecordModelPropertySetter


class WrapperField:
    """
    Describes a wrapper field used in auto-generated wrappers
    """
    _field_name: str
    _field_type: FieldType

    @property
    def field_name(self) -> str:
        """
        The name of the data field represented in this object of the Sapio data type.
        """
        return self._field_name

    @property
    def field_type(self) -> FieldType:
        """
        The data field's type for the data type's data field with the object's field name in Sapio.
        """
        return self._field_type

    def __init__(self, field_name: str, field_type: FieldType):
        self._field_name = field_name
        self._field_type = field_type

    def __str__(self):
        return self.field_name

    def __hash__(self):
        return hash([self._field_name, self._field_type])

    def __eq__(self, other):
        if not isinstance(other, WrapperField):
            return False
        return self._field_name == other._field_name and self._field_type == other._field_type


class WrappedRecordModel(ABC):
    """
    Wraps a record model so that it can be extended via interfacing types.
    Supporting auto-generated interfaces or any other decorations for base record model impl.

    A wrapped record model maintains its singleton under the record model root in the record model manager.
    You can create multiple instances of wrapper objects, but they will share the same data and cache.
    """
    _backing_model: PyRecordModel

    def __init__(self, backing_model: PyRecordModel):
        self._backing_model = backing_model

    def __hash__(self):
        return hash(self._backing_model)

    def __eq__(self, other):
        if not isinstance(other, WrappedRecordModel):
            return False
        return self._backing_model == other._backing_model

    def __str__(self):
        return str(self._backing_model)

    @property
    def backing_model(self):
        """
        The base model is the root model backing the decorated type.
        """
        return self._backing_model

    @property
    def record_id(self) -> int:
        """
        The system-unique Record ID for this record. It is possible for this to be a negative number for new records.
        """
        return self._backing_model.record_id

    @property
    def is_deleted(self) -> bool:
        """
        Test whether this record is flagged for deletion.
        """
        return self._backing_model.is_deleted

    @property
    def is_new(self) -> bool:
        """
        Tests whether this is a new record that has not been stored in Sapio yet.
        """
        return self._backing_model.is_new

    @property
    def fields(self) -> RecordModelFieldMap:
        """
        The field map of the record model, which could include cached changed not committed to data record.
        """
        return self._backing_model.fields

    @property
    def data_type_name(self) -> str:
        """
        The data type name of this record model.
        """
        return self._backing_model.data_type_name

    def get_field_value(self, field_name: str) -> Any:
        """
        Get the model's field value for a field
        """
        return self._backing_model.get_field_value(field_name)

    def get_record_field_value(self, field_name: str) -> Any:
        """
        Get the backing record's field value for a field.
        """
        return self._backing_model.get_record_field_value(field_name)

    def get_data_record(self) -> DataRecord:
        """
        Get the backing data record for this record model instance.
        """
        return self._backing_model.get_data_record()

    def add_parent(self, parent_record: WrappedRecordModel) -> None:
        """
        Add a record model as a parent for this record model.
        """
        return self._backing_model.add_parent(RecordModelWrapperUtil.unwrap(parent_record))

    def add_parents(self, parent_records: List[WrappedRecordModel]) -> None:
        """
        Add multiple record models as parents for this record model.
        """
        for record in parent_records:
            self.add_parent(record)

    def remove_parent(self, parent_record: WrappedRecordModel) -> None:
        """
        Remove a parent relation from this record model.
        """
        return self._backing_model.remove_parent(RecordModelWrapperUtil.unwrap(parent_record))

    def remove_parents(self, parent_records: List[WrappedRecordModel]) -> None:
        """
        Remove multiple parent relations from this record model.
        """
        for record in parent_records:
            self.remove_parent(record)

    def add_child(self, child_record: WrappedRecordModel) -> None:
        """
        Add a child record model for this record model.
        """
        return self._backing_model.add_child(RecordModelWrapperUtil.unwrap(child_record))

    def add_children(self, children_records: List[WrappedRecordModel]) -> None:
        """
        Add multiple children record model for this record model.
        """
        for record in children_records:
            self.add_child(record)

    def remove_child(self, child_record: WrappedRecordModel) -> None:
        """
        Remove a child record model relation from this record model.
        """
        return self._backing_model.remove_child(RecordModelWrapperUtil.unwrap(child_record))

    def remove_children(self, children_records: List[WrappedRecordModel]) -> None:
        """
        Remove multiple children record model relations from this record model.
        """
        for record in children_records:
            self.remove_child(record)

    def set_side_link(self, field_name: str, link_to: Optional[WrappedRecordModel]) -> None:
        """
        Change the forward side link on this record's field to another record.
        """
        if link_to is None:
            self._backing_model.set_side_link(field_name, None)
        else:
            self._backing_model.set_side_link(field_name, RecordModelWrapperUtil.unwrap(link_to))

    def get_forward_side_link(self, field_name: str, forward_link_type: Type[WrappedType]) -> Optional[WrappedType]:
        """
        Get the current forward side links. If the side links have not been loaded, throw an exception.
        :param field_name: The forward link field on this record to load its reference for.
        :param forward_link_type: The returned forward link record's class type.
        """
        ret: Optional[PyRecordModel] = self._backing_model.get_forward_side_link(field_name)
        if ret is None:
            return None
        return RecordModelWrapperUtil.wrap(ret, forward_link_type)

    def get_reverse_side_link(self, field_name: str, reverse_link_type: Type[WrappedType]) -> List[WrappedType]:
        """
        Get currently loaded reverse side link models. This will throw exception if it has not been loaded before.
        :param field_name: The reverse link's field name on the record that will point to one of provided records.
        :param reverse_link_type: The reverse link's model class type of records that will point to provided records.
        """
        ret: List[PyRecordModel] = self._backing_model.get_reverse_side_link(reverse_side_link_data_type_name=
                                                                             reverse_link_type.
                                                                             get_wrapper_data_type_name(),
                                                                             reverse_side_link_field_name=field_name)
        return RecordModelWrapperUtil.wrap_list(ret, reverse_link_type)

    def delete(self) -> None:
        """
        Flag the current record model to be deleted on commit.
        """
        return self._backing_model.delete()

    def set_field_value(self, field_name: str, field_value: Any) -> None:
        """
        Set a current record model's field value to a new value.
        """
        return self._backing_model.set_field_value(field_name, field_value)

    def set_field_values(self, field_change_map: Dict[str, Any]) -> None:
        """
        Set multiple field values for this record model to new values.
        """
        return self._backing_model.set_field_values(field_change_map)

    def get_parents_of_type(self, parent_type: Type[WrappedType]) -> List[WrappedType]:
        """
        Get all parents for a particular data type name for this record model.
        """
        models: List[PyRecordModel] = self._backing_model.get_parents_of_type(parent_type.get_wrapper_data_type_name())
        return RecordModelWrapperUtil.wrap_list(models, parent_type)

    def get_children_of_type(self, child_type: Type[WrappedType]) -> List[WrappedType]:
        """
        Get all children for a particular data type name for this record model.
        """
        models: List[PyRecordModel] = self._backing_model.get_children_of_type(child_type.get_wrapper_data_type_name())
        return RecordModelWrapperUtil.wrap_list(models, child_type)

    def get_parent_of_type(self, parent_type: Type[WrappedType]) -> Optional[WrappedType]:
        """
        Obtains the parent of the current record of the provided data type name.
        If the parent is not found, return None.
        If there are more than one parent exists, then we will throw an exception.
        """
        parents = self.get_parents_of_type(parent_type)
        if not parents:
            return None
        if len(parents) > 1:
            raise SapioRecordModelException("Too many parent records of type " +
                                            parent_type.get_wrapper_data_type_name(), self._backing_model)
        return parents[0]

    def get_child_of_type(self, child_type: Type[WrappedType]) -> Optional[WrappedType]:
        """
        Obtains the only child of the current record of the provided data type name.
        If the child is not found, return None.
        If there are more than one child exists, then we will throw an exception.
        """
        children = self.get_children_of_type(child_type)
        if not children:
            return None
        if len(children) > 1:
            raise SapioRecordModelException("Too many child records of type " + child_type.get_wrapper_data_type_name(),
                                            self._backing_model)
        return children[0]

    @classmethod
    @abstractmethod
    def get_wrapper_data_type_name(cls):
        """
        The name of the data type in Sapio system that the wrapper class's attributes and methods will represent.
        """
        pass

    def get(self, getter: AbstractRecordModelPropertyGetter[RecordModelPropertyType]) -> Optional[RecordModelPropertyType]:
        """
        Obtain a specific record model property. This is a java-like syntax sugar for users used the old record models.
        """
        return getter.get_value(self._backing_model)

    def add(self, adder: AbstractRecordModelPropertyAdder[RecordModelPropertyType]) -> RecordModelPropertyType:
        """
        Add a value to a property, assuming the property itself is an iterable type.
        """
        return adder.add_value(self._backing_model)

    def remove(self, remover: AbstractRecordModelPropertyRemover[RecordModelPropertyType]) -> RecordModelPropertyType:
        """
        Remove a value from a property, assuming the property itself is an iterable type.
        """
        return remover.remove_value(self._backing_model)

    def set(self, setter: AbstractRecordModelPropertySetter[RecordModelPropertyType]) -> RecordModelPropertyType:
        """
        Set a value onto a record model property.
        """
        return setter.set_value(self._backing_model)


WrappedType = TypeVar("WrappedType", bound=WrappedRecordModel)


class RecordModelWrapperUtil:
    """
    Wraps or unwraps a record model that has a wrapper function.
    """

    @staticmethod
    def unwrap(wrapped_record_model: WrappedRecordModel | PyRecordModel) -> PyRecordModel:
        if isinstance(wrapped_record_model, PyRecordModel):
            return wrapped_record_model
        return wrapped_record_model.backing_model

    @staticmethod
    def unwrap_list(wrapped_record_model_list: Iterable[WrappedRecordModel | PyRecordModel]) -> List[PyRecordModel]:
        return [RecordModelWrapperUtil.unwrap(x) for x in wrapped_record_model_list]

    @staticmethod
    def wrap(py_record_model: PyRecordModel | WrappedRecordModel, clazz: Type[WrappedType]) -> WrappedType:
        if isinstance(py_record_model, PyRecordModel):
            return clazz(backing_model=py_record_model)
        elif isinstance(py_record_model, WrappedRecordModel):
            if isinstance(py_record_model, clazz):
                return py_record_model
            else:
                return clazz(backing_model=py_record_model.backing_model)

    @staticmethod
    def wrap_list(py_record_model_list: Iterable[PyRecordModel | WrappedRecordModel], clazz: Type[WrappedType]) -> List[WrappedType]:
        return [RecordModelWrapperUtil.wrap(x, clazz) for x in py_record_model_list]
