from __future__ import annotations

from weakref import WeakValueDictionary

from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.DataRecordPaging import DataRecordPojoPageCriteria, DataRecordPojoListPageResult
from sapiopylib.rest.pojo.datatype.FieldDefinition import FieldDefinitionParser, AbstractVeloxFieldDefinition
from sapiopylib.rest.pojo.eln.ElnExperiment import *
from sapiopylib.rest.pojo.eln.ExperimentEntry import ExperimentEntryParser, ExperimentEntry
from sapiopylib.rest.pojo.eln.ExperimentEntryCriteria import ElnEntryCriteria, AbstractElnEntryUpdateCriteria
from sapiopylib.rest.pojo.eln.SapioELNEnums import ExperimentEntryStatus, ElnBaseDataType


class ElnManager:
    """
    Manages ELN notebook experiments in the system.
    """
    user: SapioUser

    __instances: WeakValueDictionary[SapioUser, ElnManager] = WeakValueDictionary()
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

    def create_notebook_experiment(self, pojo: InitializeNotebookExperimentPojo) -> ElnExperiment:
        """
        Use the provided criteria to create a new Notebook Experiment.
        :param pojo: The details about how to create the experiment.
        :return: The new experiment's info data.
        """
        sub_path = '/eln/notebookexperiment/'
        response = self.user.post(sub_path, payload=pojo.to_json())
        self.user.raise_for_status(response)
        json_dict = response.json()
        return ELNExperimentParser.parse_eln_experiment(json_dict)

    def delete_notebook_experiment(self, notebook_experiment_id: int) -> None:
        """
        Delete a notebook experiment when providing a notebook experiment ID.
        """
        subpath = self.user.build_url(['eln', 'experiment', str(notebook_experiment_id)])
        response = self.user.delete(subpath)
        self.user.raise_for_status(response)

    def get_template_experiment_list(self, query: TemplateExperimentQueryPojo) -> List[ElnTemplate]:
        """
        Get a list of TemplateExperimentPojo objects using the provided criteria object to search
        the templates in the app.
        :return: List of templates matching the provided criteria in the system.
        """
        sub_path = "/eln/templateexperiment/"
        response = self.user.post(sub_path, payload=query.to_json())
        self.user.raise_for_status(response)
        json_list: List[Dict[str, Any]] = response.json()
        return [ELNExperimentParser.parse_template_experiment(x) for x in json_list]

    def get_experiment_entry_list(self, eln_experiment_id: int, to_retrieve_field_definitions: bool) \
            -> List[ExperimentEntry]:
        """
        Get all experiment entries for an ELN experiment.
        :param eln_experiment_id: The ELN experiment ID these entries are made under.
        :param to_retrieve_field_definitions: If true, the resulting entries will be filled with field definition data.
        :return: The experiment entry data list.
        """
        sub_path = self.user.build_url(['eln', 'getExperimentEntryList', str(eln_experiment_id)])
        params = {
            'retrieveDataDefinitions': to_retrieve_field_definitions
        }
        response = self.user.get(sub_path, params)
        self.user.raise_for_status(response)
        json_list: List[Dict[str, Any]] = response.json()
        return [ExperimentEntryParser.parse_experiment_entry(x) for x in json_list]

    def get_experiment_entry(self, eln_experiment_id: int, entry_id: int,
                             to_retrieve_field_definitions: bool) -> Optional[ExperimentEntry]:
        """
        Get a specific entry from ELN experiment.
        :param eln_experiment_id: The ELN experiment ID the entry was created under.
        :param entry_id: The Experiment ID entry we are searching for.
        :param to_retrieve_field_definitions:  If true, the resulting entries will be filled with field definition data.
        :return: The experiment entry if exists, or None if not.
        """
        sub_path = self.user.build_url(['eln', 'getExperimentEntry', str(eln_experiment_id), str(entry_id)])
        params = {
            'retrieveDataDefinitions': to_retrieve_field_definitions
        }
        response = self.user.get(sub_path, params)
        self.user.raise_for_status(response)
        json_dct: Optional[Dict[str, Any]] = response.json()
        if json_dct is None:
            return None
        return ExperimentEntryParser.parse_experiment_entry(json_dct)

    def get_eln_experiment_by_record_id(self, record_id: int):
        """
        Given the record ID of the data record that is the title record of the experiment entry, find the experiment.

        This can be useful when trying to retrieve ELN experiment from global data type hierarchy.
        """
        sub_path = '/eln/queryExperimentByRecordId'
        params = {
            'recordId': record_id
        }
        response = self.user.get(sub_path, params)
        self.user.raise_for_status(response)
        return ELNExperimentParser.parse_eln_experiment(response.json())

    def get_eln_experiment_list(self, owner_username: Optional[str] = None,
                                status_types: Optional[List[ExperimentEntryStatus]] = None) \
            -> List[ElnExperiment]:
        """
        Retrieves the metadata of notebook experiments in the system. It may run faster when filters are specified.
        :param owner_username: The owner filter specifies that notebook experiment must be owned by
        this user to be retrieved.
        :param status_types: The status type specifies the notebook experiment must have one of
        these statuses to be retrieved.
        :return:
        """
        sub_path = '/eln/getExperimentInfoList'
        params = dict()
        if owner_username is not None:
            params['ownerUsername'] = owner_username
        if status_types is not None:
            params['statusTypes'] = [x.name for x in status_types]
        response = self.user.get(sub_path, params)
        self.user.raise_for_status(response)
        json_list: List[Dict[str, Any]] = response.json()
        return [ELNExperimentParser.parse_eln_experiment(x) for x in json_list]

    def get_eln_experiment_by_criteria(self, criteria: ElnExperimentQueryCriteria) -> List[ElnExperiment]:
        """
        Searches ELN experiment by a complex query criteria object
        :param criteria: The search request details
        :return: A list of ELN experiments.
        """
        sub_path = '/eln/queryExperimentByCriteria'
        response = self.user.post(sub_path, payload=criteria.to_json())
        self.user.raise_for_status(response)
        json_list: List[Dict[str, Any]] = response.json()
        return [ELNExperimentParser.parse_eln_experiment(x) for x in json_list]

    def get_eln_experiment_by_id(self, eln_experiment_id: int) -> Optional[ElnExperiment]:
        """
        Get the ELN experiment by its experiment ID.
        :param eln_experiment_id: The experiment ID to search for.
        :return: The ELN experiment object. Returns None if it does not exist, or the current user does not have access.
        """
        criteria = ElnExperimentQueryCriteria(notebook_experiment_id_white_list=[eln_experiment_id])
        results = self.get_eln_experiment_by_criteria(criteria)
        if results:
            return results[0]
        return None

    def add_experiment_entry(self, eln_experiment_id: int, entry_criteria: ElnEntryCriteria) -> ExperimentEntry:
        """
        Creates a new entry under the ELN experiment. May pre-populate with data.
        :param eln_experiment_id: The experiment ID to create the entry under.
        :param entry_criteria The criteria specifies how we the new entry should be.
        :return:the entry created if successful, without field definitions.
        """
        sub_path = self.user.build_url(['eln', 'addExperimentEntry', str(eln_experiment_id)])
        response = self.user.post(sub_path, payload=entry_criteria.to_json())
        self.user.raise_for_status(response)
        json_dct: Dict[str, Any] = response.json()
        return ExperimentEntryParser.parse_experiment_entry(json_dct)

    def add_predefined_entry_fields(self, eln_experiment_id: int, entry_id: int,
                                    predefined_field_name_list: List[str]) -> ExperimentEntry:
        """
        Add additional predefined fields to ELN experiment entry.
        :param eln_experiment_id: The experiment ID the entry is under.
        :param entry_id: The entry ID in experiment to modify.
        :param predefined_field_name_list: The predefined field list to be added to experiment entry.
        :return: The entry with field definitions filled in after processing.
        """
        sub_path = self.user.build_url(['eln', 'addPredefinedEntryFields', str(eln_experiment_id), str(entry_id)])
        response = self.user.post(sub_path, payload=predefined_field_name_list)
        self.user.raise_for_status(response)
        json_dct: Dict[str, Any] = response.json()
        return ExperimentEntryParser.parse_experiment_entry(json_dct)

    def get_predefined_fields(self, eln_base_data_type: ElnBaseDataType) -> List[AbstractVeloxFieldDefinition]:
        """
        Given the base ELN data type, what are the available pre-defined fields in the system?
        :param eln_base_data_type: The base data type to query.
        :return: All defined field definitions for this ELN data type.
        """
        sub_path = self.user.build_url(['eln', 'getPredefinedFields', eln_base_data_type.data_type_name])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        json_list: List[Dict[str, Any]] = response.json()
        return [FieldDefinitionParser.to_field_definition(x) for x in json_list]

    def get_predefined_field_by_id(self, field_id: int) -> AbstractVeloxFieldDefinition:
        """
        Given the base ELN data type and the predefined field ID, retrieve its full definition. Error 422 if not found.
        :param field_id: The system generated ID for the predefined field.
        :return: The field definition.
        """
        sub_path = self.user.build_url(['eln', 'getPredefinedFieldById', str(field_id)])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        json_dct: Dict[str, Any] = response.json()
        return FieldDefinitionParser.to_field_definition(json_dct)

    def get_predefined_field_by_name(self, eln_base_data_type: ElnBaseDataType, field_name: str) \
            -> AbstractVeloxFieldDefinition:
        """
        Given the base ELN data type and name created by administrator, retrieve its full definition.
        Error 422 if not found.
        :param eln_base_data_type: The base data type to query.
        :param field_name: The unique identifier defined by administrator for the field.
        :return: The field definition.
        """
        sub_path = self.user.build_url(['eln', 'getPredefinedFieldByName', eln_base_data_type.data_type_name,
                                        field_name])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        json_dct: Dict[str, Any] = response.json()
        return FieldDefinitionParser.to_field_definition(json_dct)

    def get_data_records_for_entry(self, eln_experiment_id: int, entry_id: int,
                                   paging_criteria: DataRecordPojoPageCriteria = None) -> DataRecordPojoListPageResult:
        """
        Retrieve the data records that will be displayed inside the entry.
        :param eln_experiment_id: The experiment ID the entry is under.
        :param entry_id: The entry ID in experiment to get records for
        :param paging_criteria: Optional criteria for next page info, when retrieving the next page.
        :return: The current page of data record results.
        """
        sub_path = self.user.build_url(['eln', 'getDataRecordsForEntry', str(eln_experiment_id), str(entry_id)])
        params = dict()
        if paging_criteria is not None:
            params['lastRetrievedRecordId'] = paging_criteria.last_retrieved_record_id
            params['pageSize'] = paging_criteria.page_size
        response = self.user.get(sub_path, params)
        self.user.raise_for_status(response)
        json_dct: Dict[str, Any] = response.json()
        return DataRecordPojoListPageResult.from_json(json_dct)

    def submit_experiment_entry(self, eln_experiment_id: int, entry_id: int) -> None:
        """
        Submitting an entry locks down the entry. If the entry enters completed status (default),
        then dependent steps becomes available.
        :param eln_experiment_id: The experiment ID the entry is under.
        :param entry_id: The entry ID of the entry to be locked down.
        """
        sub_path = self.user.build_url(['eln', 'submitExperimentEntry', str(eln_experiment_id), str(entry_id)])
        response = self.user.post(sub_path)
        self.user.raise_for_status(response)

    def add_records_to_table_entry(self, eln_experiment_id: int, entry_id: int,
                                   records_to_add: List[DataRecord]) -> None:
        """
        Add one or more data records to an experiment table entry.
        :param eln_experiment_id: The experiment ID the entry is under.
        :param entry_id: The entry ID in experiment to modify. Must be a table entry.
        :param records_to_add: These may be new or existing records. To add an existing record, fill in the record ID.
        If the record ID is not specified, it is assumed that this is a new record.
        Any field updates will be in the field map of the DataRecordPojo.
        If the field do not exist, then the service do not perform field updates on the data record.
        """
        sub_path = self.user.build_url(['eln', 'addRecordsToTableEntry', str(eln_experiment_id), str(entry_id)])
        record_pojo_list = [x.to_json() for x in records_to_add]
        response = self.user.post(sub_path, payload=record_pojo_list)
        self.user.raise_for_status(response)

    def remove_records_from_table_entry(self, eln_experiment_id: int, entry_id: int,
                                        record_id_remove_list: List[int]) -> None:
        """
        Remove one or more data records from an experiment entry
        :param eln_experiment_id: The experiment ID the entry is under.
        :param entry_id: The entry ID in experiment to modify. Must be a table entry.
        :param record_id_remove_list: A list of record ID integers to remove.
        """
        sub_path = self.user.build_url(['eln', 'removeRecordsFromTableEntry', str(eln_experiment_id), str(entry_id)])
        response = self.user.post(sub_path, payload=record_id_remove_list)
        self.user.raise_for_status(response)

    def update_experiment_entry(self, eln_experiment_id: int, entry_id: int,
                                entry_update_criteria: AbstractElnEntryUpdateCriteria) -> None:
        """
        Updates some metadata of an experiment entry.
        :param eln_experiment_id: The experiment ID the entry is under.
        :param entry_id: The entry ID in experiment to modify. Must be a table entry.
        :param entry_update_criteria: The update fields are all optional.
        If the update is only to be performed on some properties, may leave out the unrelated properties from the
        JSON passed in.
        """
        sub_path = self.user.build_url(['eln', 'updateExperimentEntry', str(eln_experiment_id), str(entry_id)])
        response = self.user.post(sub_path, payload=entry_update_criteria.to_json())
        self.user.raise_for_status(response)

    def update_notebook_experiment(self, eln_experiment_id: int,
                                   experiment_update_criteria: ElnExperimentUpdateCriteria) -> None:
        """
        Updates some metadata of a notebook experiment.
        :param eln_experiment_id: The experiment ID of the experiment being edited.
        :param experiment_update_criteria:The update fields are all optional.
        If the update is only to be performed on some properties, may leave out the unrelated properties as 'None'
        """
        sub_path = self.user.build_url(['eln', 'updateNotebookExperiment', str(eln_experiment_id)])
        response = self.user.post(sub_path, payload=experiment_update_criteria.to_json())
        self.user.raise_for_status(response)

    def get_experiment_entry_options(self, eln_experiment_id: int, entry_id: int) -> Dict[str, str]:
        """
        Get the current experiment entry options. These may be used to store plugin data or configurations.
        :param eln_experiment_id: The ELN experiment ID the entry is under.
        :param entry_id: The entry ID of the entry to get options for.
        """
        sub_path = self.user.build_url(['eln', 'getExperimentEntryOptions', str(eln_experiment_id), str(entry_id)])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        return response.json()

    def get_notebook_experiment_options(self, eln_experiment_id: int) -> Dict[str, str]:
        """
        Get the current notebook experiment options. These may be used to store plugin data or configurations.
        :param eln_experiment_id: The ELN experiment ID to get the options for.
        :return:
        """
        sub_path = self.user.build_url(['eln', 'getNotebookExperimentOptions', str(eln_experiment_id)])
        response = self.user.get(sub_path)
        self.user.raise_for_status(response)
        return response.json()
