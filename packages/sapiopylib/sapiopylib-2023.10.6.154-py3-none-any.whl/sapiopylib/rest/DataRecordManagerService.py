from __future__ import annotations
import urllib.parse
from typing import Union, Any, List, Dict, IO, Callable, Optional
from weakref import WeakValueDictionary

from pandas import DataFrame
from sapiopylib.rest.pojo.DataRecordPaging import DataRecordPojoPageCriteria, DataRecordPojoListPageResult, \
    DataRecordPojoHierarchyPageCriteria, DataRecordPojoHierarchyListPageResult

from sapiopylib.rest.User import SapioUser, SapioServerException
from sapiopylib.rest.pojo.DataRecord import from_json_record_list, to_record_json_list, DataRecord
from sapiopylib.rest.pojo.DataRecordSideLinkPaging import DataRecordSideLinkFromPageCriteria, \
    DataRecordSideLinkFromListPageResult, DataRecordSideLinkToPageCriteria, DataRecordSideLinkToListPageResult
from sapiopylib.rest.pojo.SapioAccessType import SapioAccessType


class DataRecordManager:
    """
    Manages data records in Sapio.
    """
    user: SapioUser

    __instances: WeakValueDictionary[SapioUser, DataRecordManager] = WeakValueDictionary()
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

    @staticmethod
    def get_data_frame(records: List[DataRecord]) -> DataFrame:
        """
        Get a pandas data frame for a list of records.
        :param records: The records to get data frames for.
        :return: A consolidated data frame among all columns across all data records.
        The data records does not have to be of the same time, and records with same field names
        will be joined under a single key.
        """
        data_dict: Dict[str, List[Any]] = dict()
        cur_length = 0
        for record in records:
            fields = record.get_fields()
            for key, value in fields.items():
                if key not in data_dict:
                    init_list = [None] * cur_length
                    data_dict[key] = init_list
                data_dict[key].append(value)
            cur_length += 1
        return DataFrame.from_dict(data_dict, orient='columns')

    def query_data_records(self, data_type_name: str, data_field_name: str,
                           value_list: list,
                           paging_criteria: DataRecordPojoPageCriteria = None) -> DataRecordPojoListPageResult:
        """
        Query the system for records of the given type that have values in the given field that match the given values
        :param data_type_name: The data type name to use in the query for records.
        :param data_field_name: The data field name that will be used when querying for records.
        :param value_list: The list of values to be used in the query. Think of SQL "IN" Clause
        :param paging_criteria optional paging criteria info for the current page.
        :return: The result query of the current page.
        """
        params = {'dataTypeName': data_type_name,
                  'dataFieldName': data_field_name}
        self._append_query_param(paging_criteria, params)
        sub_path = '/datarecordmanager/querydatarecords'
        response = self.user.post(sub_path, params, value_list)
        self.user.raise_for_status(response)
        json_dict = response.json()
        return DataRecordPojoListPageResult.from_json(json_dict)

    def query_data_records_by_id(self, data_type_name: str, record_id_list: List[int],
                                 paging_criteria: DataRecordPojoPageCriteria = None) -> DataRecordPojoListPageResult:
        """
        Get a list of records given the given list of Record IDs provided in a comma delimited
        list.  This method will only return records of the given type that have one of the
        provided Record IDs.  The records are not guaranteed to be returned, in the same
        order as the provided list.
        :param data_type_name: The data type name to use in the query for records.
        :param record_id_list: Comma delimited list of Record IDs to be found in the system.
        :param paging_criteria: optional paging criteria info for the current page.
        :return:
        """
        record_id_list.sort()
        params = {'dataTypeName': data_type_name}
        self._append_query_param(paging_criteria, params)
        sub_path = '/datarecordlist'
        response = self.user.post(sub_path, params=params, payload=record_id_list)
        self.user.raise_for_status(response)
        json_dict = response.json()
        return DataRecordPojoListPageResult.from_json(json_dict)

    def query_all_records_of_type(self, data_type_name: str,
                                  paging_criteria: DataRecordPojoPageCriteria = None) -> DataRecordPojoListPageResult:
        """
        Get a list of all records of the given data type.
        :param data_type_name: The data type name to retrieve for.
        :param paging_criteria: The current page info.
        :return: The paged data
        """
        params = {'dataTypeName': data_type_name}
        self._append_query_param(paging_criteria, params)
        sub_path = '/datarecordlist/all'
        response = self.user.get(sub_path, params)
        self.user.raise_for_status(response)
        json_dict = response.json()
        return DataRecordPojoListPageResult.from_json(json_dict)

    def query_system_for_record(self, data_type_name: str,
                                record_id: int) -> Optional[DataRecord]:
        """
        Get the record of the given type that has the provided Record ID.
        :param data_type_name: The Data Type Name of the record in the system.
        :param record_id: The Record ID of the record in the system.
        :return: The data record if available. None if not found.
        """
        params = {'dataTypeName': data_type_name,
                  'recordId': record_id}
        sub_path = '/datarecord'
        response = self.user.get(sub_path, params)
        self.user.raise_for_status(response)
        if self.user.is_null_response(response):
            return None
        json_dict = response.json()
        return DataRecord.from_json(json_dict)

    def get_parents(self, record_id: int, child_type_name: str, parent_type_name: str,
                    paging_criteria: Optional[DataRecordPojoPageCriteria] = None) -> DataRecordPojoListPageResult:
        """
        Get the parents of the given type above the record with the given Record ID.
        :param record_id: The data type of the child record.
        :param child_type_name: The data type name of the child of specified Record ID.
        :param parent_type_name: The data type name of the parent to look for above he given Record ID.
        :param paging_criteria: Optional criteria for next page info.
        :return: The result of parents of the given child record, at the current page.
        """
        params = {'recordId': record_id,
                  'childTypeName': child_type_name,
                  'parentTypeName': parent_type_name}
        self._append_query_param(paging_criteria, params)
        sub_path = '/datarecord/parents'
        response = self.user.get(sub_path, params)
        self.user.raise_for_status(response)
        json_dict = response.json()
        return DataRecordPojoListPageResult.from_json(json_dict)

    def get_parents_list(self, record_id_list: List[int], child_type_name: Optional[str], parent_type_name: str,
                         paging_criteria: Optional[DataRecordPojoHierarchyPageCriteria] = None) -> \
            DataRecordPojoHierarchyListPageResult:
        """
        Get the parents of the given type above the records with the given Record IDs.
        :param record_id_list: The list of record IDs to retrieve parents for.
        :param child_type_name: The child data type name of records in the record_id_list.
        This is only required in high-performance high-volume data retrieval.
        :param parent_type_name: The parent data type name to get for each child.
        :param paging_criteria: Optionally specify the page to retrieve for. Note the page size may be enforced in SaaS.
        :return: The current page's result.
        """
        try:
            record_id_list.sort()
            params = {'childTypeName': child_type_name,
                      'parentTypeName': parent_type_name}
            self._append_query_param(paging_criteria, params)
            sub_path = '/datarecordlist/parents'
            response = self.user.post(sub_path, params=params, payload=record_id_list)
            self.user.raise_for_status(response)
            json_dict = response.json()
            return DataRecordPojoHierarchyListPageResult.from_json(json_dict)
        except SapioServerException as e:
            if e.client_error.response.status_code == 405:
                # Method not found. Use the deprecated version to re-request
                self.user.log_warn("""
SAPIO PLATFORM VERSION MISMATCH. USING DEPRECATED WEBSERVICE CALL FORMAT.
This is unsupported. Use at your own risk!
                """)
                params = {'recordIdList': ','.join(str(x) for x in record_id_list),
                          'childTypeName': child_type_name,
                          'parentTypeName': parent_type_name}
                self._append_query_param(paging_criteria, params)
                sub_path = '/datarecordlist/parents'
                response = self.user.get(sub_path, params)
                response.raise_for_status()
                json_dict = response.json()
                return DataRecordPojoHierarchyListPageResult.from_json(json_dict)
            else:
                raise e

    def get_children(self, record_id: int, child_type_name: str,
                     paging_criteria: Optional[DataRecordPojoPageCriteria] = None) -> DataRecordPojoListPageResult:
        """
        Get the children of the given type below the record with the given Record ID.
        :param record_id: The Record ID of the parent record.
        :param child_type_name: The data type name of the children to look for below the given Record ID.
        :param paging_criteria: Optionally specify the page to retrieve for. Note the page size may be enforced in SaaS.
        :return:
        """
        params = {'recordId': record_id,
                  'childTypeName': child_type_name}
        self._append_query_param(paging_criteria, params)
        sub_path = '/datarecord/children'
        response = self.user.get(sub_path, params)
        self.user.raise_for_status(response)
        json_dict = response.json()
        return DataRecordPojoListPageResult.from_json(json_dict)

    def get_children_list(self, record_id_list: List[int], child_type_name: str,
                          paging_criteria: Optional[DataRecordPojoHierarchyPageCriteria] = None) -> \
            DataRecordPojoHierarchyListPageResult:
        """
        Get the children of the given type below the records with the given Record IDs.
        :param record_id_list: Parent Record IDs to get children of.
        :param child_type_name: The data type name of the children to look for below the given Record IDs.
        :param paging_criteria: Optionally specify the page to retrieve for. Note the page size may be enforced in SaaS.
        """
        try:
            record_id_list.sort()
            params = {'childTypeName': child_type_name}
            self._append_query_param(paging_criteria, params)
            sub_path = '/datarecordlist/childrenbyid'
            response = self.user.post(sub_path, params=params, payload=record_id_list)
            self.user.raise_for_status(response)
            json_dict = response.json()
            return DataRecordPojoHierarchyListPageResult.from_json(json_dict)
        except SapioServerException as e:
            if e.client_error.response.status_code == 405:
                # Method not found. Use the deprecated version to re-request
                self.user.log_warn("""
SAPIO PLATFORM VERSION MISMATCH. USING DEPRECATED WEBSERVICE CALL FORMAT.
This is unsupported. Use at your own risk!
                """)
                params = {'recordIdList': ','.join(str(x) for x in record_id_list),
                          'childTypeName': child_type_name}
                self._append_query_param(paging_criteria, params)
                sub_path = '/datarecordlist/children'
                response = self.user.get(sub_path, params)
                response.raise_for_status()
                json_dict = response.json()
                return DataRecordPojoHierarchyListPageResult.from_json(json_dict)
            else:
                raise e

    def get_ancestors(self, record_id: int, descendant_type_name: str, ancestor_type_name: str,
                      paging_criteria: Optional[DataRecordPojoPageCriteria] = None) -> DataRecordPojoListPageResult:
        """
        Get the ancestors of the given type above the records with the given Record ID.
        :param record_id: The Record ID of the descendant record.
        :param descendant_type_name: The data type name of descendants ancestors to look for above the given Record ID.
        :param ancestor_type_name: The data type name of the ancestors to look for above the given Record ID.
        :param paging_criteria: Optionally specify the page to retrieve for. Note the page size may be enforced in SaaS.
        :return: ancestors of the current record at this page.
        """
        params = {'recordId': record_id,
                  'descendantTypeName': descendant_type_name,
                  "ancestorTypeName": ancestor_type_name}
        self._append_query_param(paging_criteria, params)
        sub_path = '/datarecord/ancestors'
        response = self.user.get(sub_path, params)
        self.user.raise_for_status(response)
        json_dict = response.json()
        return DataRecordPojoListPageResult.from_json(json_dict)

    def get_ancestors_list(self, record_id_list: List[int], descendant_type_name: str, ancestor_type_name: str,
                           paging_criteria: Optional[DataRecordPojoHierarchyPageCriteria] = None) -> \
            DataRecordPojoHierarchyListPageResult:
        """
        Get the ancestors of the given type above the records with the given Record IDs.
        :param record_id_list: Record IDs to get ancestors of.
        :param descendant_type_name: The data type name of the descendants to look for above the given Record IDs.
        :param ancestor_type_name: The data type name of the ancestors to look for above the given Record IDs.
        :param paging_criteria: Optionally specify the page to retrieve for. Note the page size may be enforced in SaaS.
        :return: Current page's result, ancestors of the records.
        """
        record_id_list.sort()
        params = {'descendantTypeName': descendant_type_name,
                  "ancestorTypeName": ancestor_type_name}
        self._append_query_param(paging_criteria, params)
        sub_path = '/datarecordlist/ancestors'
        response = self.user.post(sub_path, params=params, payload=record_id_list)
        self.user.raise_for_status(response)
        json_dict = response.json()
        return DataRecordPojoHierarchyListPageResult.from_json(json_dict)

    def get_descendants(self, record_id: int, descendant_type_name: str,
                        paging_criteria: Optional[DataRecordPojoPageCriteria] = None) -> DataRecordPojoListPageResult:
        """
        Get the descendants of the given type below the records with the given Record ID.
        :param record_id: The Record ID of the ancestor record.
        :param descendant_type_name: The data type name of the descendants to look for above the given Record ID.
        :param paging_criteria: Optionally specify the page to retrieve for. Note the page size may be enforced in SaaS.
        :return: The result descendants, of current page.
        """
        params = {'recordId': record_id,
                  'descendantTypeName': descendant_type_name}
        self._append_query_param(paging_criteria, params)
        sub_path = '/datarecord/descendants'
        response = self.user.get(sub_path, params)
        self.user.raise_for_status(response)
        json_dict = response.json()
        return DataRecordPojoListPageResult.from_json(json_dict)

    def get_descendants_list(self, record_id_list: List[int], descendant_type_name: str,
                             paging_criteria: Optional[DataRecordPojoHierarchyPageCriteria] = None) -> \
            DataRecordPojoHierarchyListPageResult:
        """
        Get the descendants of the given type below the records with the given Record IDs.
        :param record_id_list: Record IDs to get descendants of.
        :param descendant_type_name: The data type name of the descendants to look for above the given Record ID.
        :param paging_criteria: Optionally specify the page to retrieve for. Note the page size may be enforced in SaaS.
        :return: The result descendants, of current page.
        """
        record_id_list.sort()
        params = {'descendantTypeName': descendant_type_name}
        self._append_query_param(paging_criteria, params)
        sub_path = '/datarecordlist/descendants'
        response = self.user.post(sub_path, params=params, payload=record_id_list)
        self.user.raise_for_status(response)
        json_dict = response.json()
        return DataRecordPojoHierarchyListPageResult.from_json(json_dict)

    def add_data_record(self, data_type_name: str) -> DataRecord:
        """
        Create a new record of the provided data type.  Only default values and system fields will be set on the record
        before it is stored.

        The record will be filled with default value, followed by changes by on-save plugins.
        You may want to use a record setter method in this manager following this call
        :param data_type_name: The data type of the record to create in the system.
        :return: The record pojo representing the record that was created.
        """
        sub_path = '/datarecord/' + urllib.parse.quote(data_type_name)
        response = self.user.post(sub_path)
        self.user.raise_for_status(response)
        json_dict = response.json()
        return DataRecord.from_json(json_dict)

    def add_data_records(self, data_type_name: str, num_to_add: int) -> List[DataRecord]:
        """
        Add multiple data records and create them with default values.
        :param data_type_name: The data type name of added records.
        :param num_to_add: The number of records to be added.
        :return: The new data record pojo list.
        """
        sub_path = '/datarecordlist/' + urllib.parse.quote(data_type_name)
        params = {'numberToAdd': num_to_add}
        response = self.user.post(sub_path, params)
        self.user.raise_for_status(response)
        json_list = response.json()
        return [DataRecord.from_json(json) for json in json_list]

    def add_data_records_with_data(self, data_type_name: str,
                                   field_map_list: List[Dict[str, Any]]
                                   ) -> List[DataRecord]:
        """
        A shortcut to add data records in a list and provide data as field map list in a single call.
        :param data_type_name: The data type name of added records.
        :param field_map_list: The field map list of the data of the data records to be added.
        """
        sub_path = '/datarecordlist/fields/' + urllib.parse.quote(data_type_name)
        response = self.user.post(sub_path, payload=field_map_list)
        self.user.raise_for_status(response)
        json_list = response.json()
        return [DataRecord.from_json(json) for json in json_list]

    def set_attachment_data(self, record: DataRecord,
                            file_name: str, data_stream: IO) -> None:
        """
        Upload file bytes to be used as the attachment data for the given record.
        :param record: The attachment record to upload the file bytes to.
        :param file_name: The name of the file being uploaded as the attachment data.
        :param data_stream: The stream to be consumed as upload binary data.
        """
        data_type_name = record.get_data_type_name()
        record_id = record.get_record_id()
        sub_path = '/datarecord/attachment/' + urllib.parse.quote(data_type_name) + "/" + \
                   urllib.parse.quote(str(record_id)) + "/" + urllib.parse.quote(file_name)
        response = self.user.post_data_stream(sub_path, data_stream)
        self.user.raise_for_status(response)

    def get_attachment_data(self, record: DataRecord,
                            data_sink: Callable[[bytes], None]) -> None:
        """
        Take the attachment data stream and consume the data in a data sink method.
        :param record: The record to obtain attachment data from.
        :param data_sink: The data sink method to consume data stream
        """
        data_type_name = record.get_data_type_name()
        record_id = record.get_record_id()
        sub_path = '/datarecord/attachment/' + urllib.parse.quote(data_type_name) + "/" + \
                   urllib.parse.quote(str(record_id))
        self.user.consume_octet_stream_get(sub_path, data_sink)

    def set_record_image(self, record: DataRecord,
                         data_stream: IO) -> None:
        """
        Set the record image on the record defined by the data type name and record ID parameters.
        :param record: The record to set image for.
        :param data_stream: The stream to be consumed as upload image data.
        """
        data_type_name = record.get_data_type_name()
        record_id = record.get_record_id()
        sub_path = '/datarecord/image/' + urllib.parse.quote(data_type_name) + "/" + \
                   urllib.parse.quote(str(record_id))
        response = self.user.post_data_stream(sub_path, data_stream)
        self.user.raise_for_status(response)

    def get_record_image(self, record: DataRecord,
                         data_sink: Callable[[bytes], None]) -> None:
        """
        Get the data record image and consume it with data sink.
        :param record: The record to get image from.
        :param data_sink: The data sink to consume image data.
        """
        data_type_name = record.get_data_type_name()
        record_id = record.get_record_id()
        sub_path = '/datarecord/image/' + urllib.parse.quote(data_type_name) + "/" + urllib.parse.quote(str(record_id))
        self.user.consume_octet_stream_get(sub_path, data_sink)

    def delete_data_record(self, record: DataRecord, recursive_delete: bool = False) -> None:
        """
        Delete a single data record from Sapio.
        :param record: The record to be deleted.
        :param recursive_delete: Whether we will delete the record's descendants if there is no other lineage.
        """
        data_type_name = record.get_data_type_name()
        record_id = record.get_record_id()
        sub_path = '/datarecord/' + urllib.parse.quote(data_type_name) + "/" + urllib.parse.quote(str(record_id))
        params = {'recursiveDelete': recursive_delete}
        response = self.user.delete(sub_path, params)
        self.user.raise_for_status(response)

    def delete_data_record_list(self, delete_list: List[DataRecord], recursive_delete: bool = False) -> None:
        """
        Recurisvely delete a list of data records.
        :param delete_list: The record list to be deleted from Sapio.
        :param recursive_delete: Whether we will delete the record's descendants if there is no other lineage.
        """
        sub_path = '/datarecordlist/delete/'
        params = {'recursiveDelete': recursive_delete}
        response = self.user.post(sub_path, params, to_record_json_list(delete_list))
        self.user.raise_for_status(response)

    # noinspection PyProtectedMember,PyUnresolvedReferences
    def commit_data_records(self, records_to_update: List[DataRecord]) -> None:
        """
        Update a list of records with their new field maps within each pojo.
        Unlike the regular web service 'set fields for records' method, only fields that has been changed will be set.
        Should this commit operation be successful, the field data changes being tracked will be cleared,
        and the new field maps will be committed.
        :param records_to_update: The records to be updated.
        """
        sub_path = '/datarecordlist/fields'
        changed_record_list: List[DataRecord] = list()
        for record in records_to_update:
            changed_record = DataRecord(record.get_data_type_name(), record.get_record_id(),
                                        record.get_changed_fields_clone())
            changed_record_list.append(changed_record)
        payload = [x.to_json() for x in changed_record_list]
        response = self.user.put(sub_path, payload=payload)
        try:
            self.user.raise_for_status(response)
            for record in records_to_update:
                record.commit_changes()
        except Exception as e:
            for record in records_to_update:
                record.rollback()
            raise e

    def add_child(self, parent_record: DataRecord, child_record: DataRecord) -> Optional[DataRecord]:
        """
        Add an existing record as a child of another existing record.
        :param parent_record: The parent data record to add the child record to.
        :param child_record: The child data record to be added under the parent.
        """
        sub_path = self.user.build_url(['datarecord', 'child',
                                        parent_record.get_data_type_name(), str(parent_record.get_record_id())])
        params = {'childTypeName': child_record.get_data_type_name(),
                  'childRecordId': child_record.get_record_id()}
        response = self.user.post(sub_path, params)
        self.user.raise_for_status(response)
        if self.user.is_null_response(response):
            return None
        json = response.json()
        return DataRecord.from_json(json)

    def add_children(self, parent_children_map: Dict[DataRecord, List[DataRecord]]) -> None:
        """
        Add children to the parents.
        :param parent_children_map: The map of (parent) -> (All children to be added to this parent)
        """
        payload = dict()
        for parent, children_list in parent_children_map.items():
            if parent is None:
                continue
            if children_list is None or len(children_list) == 0:
                continue
            payload[parent.get_map_key_reference()] = to_record_json_list(children_list)
        sub_path = '/datarecordlist/children'
        response = self.user.put(sub_path, payload=payload)
        self.user.raise_for_status(response)

    def remove_children(self, parent_children_map: Dict[DataRecord, List[DataRecord]]) -> None:
        """
        Remove children from parents.
        :param parent_children_map: The map of (parent) -> (All children to be removed from this parent)
        """
        payload = dict()
        for parent, children_list in parent_children_map.items():
            if parent is None:
                continue
            if children_list is None or len(children_list) == 0:
                continue
            payload[parent.get_map_key_reference()] = to_record_json_list(children_list)
        sub_path = '/datarecordlist/children/delete'
        response = self.user.post(sub_path, payload=payload)
        self.user.raise_for_status(response)

    def add_children_for_record(self, parent: DataRecord, child_list: List[DataRecord]) -> None:
        """
        Add children of a data record POJO.
        :param parent: The parent record.
        :param child_list: The children list to be added to this parent record.
        """
        data_type_name = parent.get_data_type_name()
        record_id = parent.get_record_id()
        sub_path = '/datarecord/children/' + urllib.parse.quote(data_type_name) + \
                   "/" + urllib.parse.quote(str(record_id))
        response = self.user.put(sub_path, payload=to_record_json_list(child_list))
        self.user.raise_for_status(response)

    def create_children_for_record(self, parent: DataRecord,
                                   child_type_name: str, num_to_add: int) -> List[DataRecord]:
        """
        Add new children for a parent record.
        :param parent: The parent data record.
        :param child_type_name: The child data type name.
        :param num_to_add: The number of children to be created.
        """
        sub_path = self.user.build_url(['datarecord', 'children',
                                        parent.get_data_type_name(), str(parent.get_record_id())])
        params = {'childTypeName': child_type_name, 'numberToAdd': num_to_add}
        response = self.user.post(sub_path, params=params)
        self.user.raise_for_status(response)
        json_list = response.json()
        return [DataRecord.from_json(json) for json in json_list]

    def create_children_fields_for_record(self, parent: DataRecord, child_type_name: str,
                                          child_field_list: List[Dict[str, Any]]) -> \
            List[DataRecord]:
        """
        Create children prefilled with values in field map list.
        :param parent: The parent to create children for.
        :param child_type_name: The children's data type name.
        :param child_field_list: The field map list of data in the new children.
        :return: The newly created children records.
        """
        sub_path = self.user.build_url(['datarecord', 'children', 'fields',
                                        parent.get_data_type_name(), str(parent.get_record_id())])
        params = {'childTypeName': child_type_name}
        response = self.user.post(sub_path, params, child_field_list)
        self.user.raise_for_status(response)
        json_list = response.json()
        return [DataRecord.from_json(json) for json in json_list]

    def create_children_fields_for_parents(self, child_type_name: str,
                                           children_field_map_list_by_parent:
                                           Dict[DataRecord, List[Dict[str, Any]]]
                                           ) -> Dict[DataRecord, List[DataRecord]]:
        """
        Create new children for parents.
        :param child_type_name The data type name for all new children records.
        :param children_field_map_list_by_parent: a map of (parent) -> (list of new children data field map list)
        :return: a map of (parent) -> (newly created children data record list)
        """
        parent_record_by_map_key = {rec.get_map_key_reference(): rec for rec in
                                    children_field_map_list_by_parent.keys()}

        sub_path = self.user.build_url(['datarecordlist', 'children'])
        params = {'childTypeName': child_type_name}
        payload: Dict[str, List[Dict[str, Any]]] = dict()
        for parent, children_field_map_list in children_field_map_list_by_parent.items():
            if parent is None:
                continue
            if children_field_map_list is None or len(children_field_map_list) == 0:
                continue
            payload[parent.get_map_key_reference()] = children_field_map_list
        response = self.user.post(sub_path, params, payload)
        self.user.raise_for_status(response)
        json: dict = response.json()
        ret: Dict[DataRecord, List[DataRecord]] = dict()
        for parent_map_key, value in json.items():
            key_pojo = parent_record_by_map_key.get(parent_map_key)
            value_list = from_json_record_list(value)
            ret[key_pojo] = value_list
        return ret

    def has_access(self, access_type: SapioAccessType, record_list: List[DataRecord]) -> \
            List[DataRecord]:
        """
        Check to see if the user requesting the operation has the requested access to the provided records.
        :param access_type: The type of access to check for.
        :param record_list: List of records to check access for.
        :return: A sub-list of original list of records that have the requested access.
        """
        sub_path = self.user.build_url(['datarecord', 'access', access_type.name])
        payload = to_record_json_list(record_list)
        response = self.user.post(sub_path, payload=payload)
        self.user.raise_for_status(response)
        json = response.json()
        return from_json_record_list(json)

    def add_data_records_data_pump(self, data_type_name: str, field_map_list: List[Dict[str, Any]]) -> List[int]:
        """
        Create New High Volume Records Via Data Pump With Field Maps.

        This method can only be used to support the creation of High Volume data types.

        It will bypass many overheads surrounding object creations of data records in server and directly stream data
        to the database. This method cannot return DataRecord objects and can only provide you the new record id list.
        :param data_type_name: The data type name to insert records for.
        :param field_map_list: The field map list to add to data type.
        :return: The ordered list of record IDs that are added to DB, in the same order as original field map list data.
        """
        sub_path = self.user.build_url(['datarecordlist', 'fields', data_type_name, 'datapump'])
        response = self.user.post(sub_path, payload=field_map_list)
        self.user.raise_for_status(response)
        ret: List[int] = response.json()
        return ret

    def add_children_data_pump(self, child_type_name: str,
                               parent_child_field_map: Dict[DataRecord, List[Dict[str, Any]]]) \
            -> Dict[DataRecord, List[int]]:
        """
        Create New High Volume Children Via Data Pump For Parent List.

        This method can only be used to support the creation of High Volume data types.

        It will bypass many overheads surrounding object creations of data records in server and directly stream data
        to the database. This method cannot return DataRecord objects and can only provide you the new record id list.
        :param child_type_name: The data type name of the new children for these data records.
        :param parent_child_field_map: The dictionary of (Parent Data Record) -> (List of new children field map data)
        :return: The dictionary of (Parent Data Record) -> (List of new children record ID in order of field map list)
        """
        sub_path = self.user.build_url(['datarecordlist', 'children', 'datapump'])
        params = {
            'childTypeName': child_type_name
        }
        map_key_to_record: Dict[str, DataRecord] = dict()
        parent_child_field_map_pojo: Dict[str, List[Dict[str, Any]]] = dict()
        for record, children_field_map_list in parent_child_field_map.items():
            map_key = record.get_map_key_reference()
            parent_child_field_map_pojo[map_key] = children_field_map_list
            map_key_to_record[map_key] = record
        response = self.user.post(sub_path, params=params, payload=parent_child_field_map_pojo)
        self.user.raise_for_status(response)
        ret_json: Dict[str, List[int]] = response.json()
        ret: Dict[DataRecord, List[int]] = dict()
        for map_key, record_id_list in ret_json.items():
            parent_record: DataRecord = map_key_to_record.get(map_key)
            ret[parent_record] = record_id_list
        return ret

    def get_side_link_to_list(self, data_record_list: List[DataRecord], linked_data_type_name: str,
                              side_link_field_name: str, paging_criteria: Optional[DataRecordSideLinkToPageCriteria]
                              = None) -> DataRecordSideLinkToListPageResult:
        """
        Get the side linked records of the given type that point back to the given records.
        :param data_record_list: The list of records to retrieve side links to.
        :param linked_data_type_name: The data type name of the side linked records.
        :param side_link_field_name: The data field name on the linkedDataTypeName that points back to the given records.
        :param paging_criteria: The current page to retrieve.
        :return:  An object containing a map from the record key 'DataTypeName:RecordId' to arrays of data records that
         are side linked to the provided list of Records as well as a criteria object that details how to retrieve the
         next page of data.
        """
        data_record_list.sort()
        params = {'linkedDataTypeName': linked_data_type_name,
                  'sideLinkedFieldName': side_link_field_name}
        self._append_query_param(paging_criteria, params)
        sub_path = '/datarecordlist/sidelinksto'
        request_body = [x.to_json() for x in data_record_list]
        response = self.user.post(sub_path, params, request_body)
        self.user.raise_for_status(response)
        json_dict = response.json()
        return DataRecordSideLinkToListPageResult.from_json(json_dict)

    def get_side_link_from_list(self, data_record_list: List[DataRecord], side_link_field_name: str,
                                paging_criteria: Optional[DataRecordSideLinkFromPageCriteria] = None) -> \
            DataRecordSideLinkFromListPageResult:
        """
        Get the side linked records from the given records referenced by the given field name.
        :param data_record_list: The list of records to retrieve side links.
        :param side_link_field_name: The data field name on the given record that points to the records to retrieve.
        :param paging_criteria: The current page to retrieve.
        :return: An object containing a map from the record key 'DataTypeName:RecordId'
        to arrays of data records that are side linked from the provided list of Records as well as a criteria object
        that details how to retrieve the next page of data.
        """
        data_record_list.sort()
        params = {'sideLinkedFieldName': side_link_field_name}
        self._append_query_param(paging_criteria, params)
        sub_path = '/datarecordlist/sidelinksfrom'
        request_body = [x.to_json() for x in data_record_list]
        response = self.user.post(sub_path, params, request_body)
        self.user.raise_for_status(response)
        json_dict = response.json()
        return DataRecordSideLinkFromListPageResult.from_json(json_dict)

    @staticmethod
    def _append_query_param(paging_criteria: Union[
        None, DataRecordPojoPageCriteria, DataRecordPojoHierarchyPageCriteria, DataRecordSideLinkFromPageCriteria,
        DataRecordSideLinkToPageCriteria],
                            params: dict):
        if paging_criteria is None:
            return
        if isinstance(paging_criteria, DataRecordPojoPageCriteria):
            params['lastRetrievedRecordId'] = paging_criteria.last_retrieved_record_id
            params['pageSize'] = paging_criteria.page_size
        if isinstance(paging_criteria, DataRecordPojoHierarchyPageCriteria):
            params['lastSourceRecordId'] = paging_criteria.last_retrieved_source_record_id
            params['lastRetrievedRecordId'] = paging_criteria.last_retrieved_target_record_id
            params['pageSize'] = paging_criteria.page_size
        if isinstance(paging_criteria, DataRecordSideLinkFromPageCriteria):
            params['lastSourceRecordId'] = paging_criteria.last_retrieved_source_record_id
            params['pageSize'] = paging_criteria.page_size
        if isinstance(paging_criteria, DataRecordSideLinkToPageCriteria):
            params['lastSourceRecordId'] = paging_criteria.last_retrieved_source_recordId
            params['lastRetrievedRecordId'] = paging_criteria.last_retrieved_target_recordId
            params['pageSize'] = paging_criteria.page_size
