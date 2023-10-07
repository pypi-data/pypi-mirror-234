import datetime
from typing import List, Dict, Any

from sapiopylib.rest.pojo.TableColumn import TableColumn, TableColumnParser
from sapiopylib.rest.pojo.datatype.FieldDefinition import AbstractVeloxFieldDefinition, FieldDefinitionParser
from sapiopylib.rest.pojo.eln.SapioELNEnums import *
from sapiopylib.rest.utils.SapioDateUtils import java_millis_to_datetime


class EntryAttachment:
    """
    Attachment metadata for an ELN attachment entry.
    """
    attachment_type: EntryAttachmentType
    attachment_name: Optional[str]

    def __init__(self, attachment_type: EntryAttachmentType, attachment_name: Optional[str] = None):
        self.attachment_name = attachment_name
        self.attachment_type = attachment_type


class EntryRecordAttachment(EntryAttachment):
    """
    Attachment metadata for an ELN attachment entry, when data of attachment is backed by a data record.
    """
    record_id: Optional[int]

    def __init__(self, attachment_name: Optional[str] = None,
                 record_id: Optional[int] = None):
        super().__init__(EntryAttachmentType.ElnExperimentEntryRecordAttachmentPojo, attachment_name)
        self.record_id = record_id


class EntryStaticAttachment(EntryAttachment):
    """
    Attachment metadata for an ELN attachment entry, when data of attachment is backed by template data.
    """
    static_attachment_checksum: Optional[str]

    def __init__(self, attachment_name: Optional[str] = None,
                 static_attachment_checksum: Optional[str] = None):
        super().__init__(EntryAttachmentType.ElnExperimentEntryStaticAttachmentPojo, attachment_name)
        self.static_attachment_checksum = static_attachment_checksum


class ExperimentEntry:
    """
    ELN Experiment Entry is a single widget of an ELN experiment.

    The experiment entry can be a form, table, custom view, attachment, free-text, or a chart.
    """
    field_definition_list: Optional[List[AbstractVeloxFieldDefinition]]
    entry_type: ElnEntryType
    data_type_name: Optional[str]
    entry_id: int
    parent_experiment_id: int
    entry_name: str
    order: int
    description: Optional[str]
    related_entry_id_set: Optional[List[int]]
    dependency_set: Optional[List[int]]
    requires_grabber_plugin: Optional[bool]
    is_initialization_required: Optional[bool]
    singleton_id: Optional[str]
    notebook_experiment_tab_id: Optional[int]
    entry_height: Optional[int]
    column_order: Optional[int]
    column_span: Optional[int]
    is_removable: Optional[bool]
    is_renamable: Optional[bool]
    source_entry_id: Optional[int]
    is_collapsed: Optional[bool]
    is_hidden: Optional[bool]
    is_static_view: Optional[bool]
    is_created_from_template: Optional[bool]
    template_item_fulfilled_timestamp: Optional[int]
    has_comments: Optional[bool]
    is_shown_in_template: Optional[bool]
    entry_status: ExperimentEntryStatus
    submitted_by: Optional[str]
    # Date is in timestamp millis format.
    submitted_date: Optional[int]
    last_modified_by: Optional[str]
    last_modified_date: Optional[int]
    created_by: Optional[str]
    date_created: Optional[int]
    approval_due_date: Optional[int]

    def __init__(self, entry_type: ElnEntryType, entry_id: int, experiment_id: int,
                 entry_name: str, order: int):
        self.entry_type = entry_type
        self.entry_id = entry_id
        self.parent_experiment_id = experiment_id
        self.entry_name = entry_name
        self.order = order

    def __eq__(self, other):
        if not isinstance(other, ExperimentEntry):
            return False
        other_pojo: ExperimentEntry = other
        return self.entry_id == other_pojo.entry_id and self.parent_experiment_id == other.parent_experiment_id

    def __hash__(self):
        return hash((self.parent_experiment_id, self.entry_id))

    def get_submitted_date(self) -> Optional[datetime.datetime]:
        """
        Get the date when entry is submitted (validated).
        Return None if the entry is never submitted.
        """
        return java_millis_to_datetime(self.submitted_date)

    def get_last_modified_date(self) -> Optional[datetime.datetime]:
        """
        Get the date when entry was last modified.
        """
        return java_millis_to_datetime(self.last_modified_date)

    def get_date_created(self) -> Optional[datetime.datetime]:
        """
        Get the date when entry was last created.
        """
        return java_millis_to_datetime(self.date_created)


class ExperimentTextEntry(ExperimentEntry):
    """
    An experiment entry that contains a large block of text.
    """
    record_id: Optional[int]

    def __init__(self, entry_id: int, experiment_id: int, entry_name: str, order: int,
                 record_id: Optional[int] = None):
        super().__init__(ElnEntryType.Text, entry_id, experiment_id, entry_name, order)
        self.record_id = record_id


class ExperimentTempDataEntry(ExperimentEntry):
    """
    An experiment entry that displays custom data retrieved through a custom plugin to display data
    that may or may not be backed by DataRecords.
    """
    plugin_path: Optional[str]

    def __init__(self, entry_id: int, experiment_id: int, entry_name: str, order: int,
                 plugin_path: Optional[str] = None):
        super().__init__(ElnEntryType.TempData, entry_id, experiment_id, entry_name, order)
        self.plugin_path = plugin_path


class ExperimentTableEntry(ExperimentEntry):
    """
    An experiment entry that will display a table of data records.
    """
    base_data_type: Optional[str]
    data_type_layout_name: Optional[str]
    field_set_id_list: Optional[List[int]]
    extension_type_set: Optional[List[str]]
    attachment_record_id: Optional[int]
    attachment_data_type_name: Optional[str]
    is_created_from_file_import: Optional[bool]
    is_auto_created_records: Optional[bool]
    auto_run_plugin_field_set_id: Optional[int]
    show_key_fields: Optional[bool]
    is_field_addable: Optional[bool]
    is_existing_field_removable: Optional[bool]
    template_field_name_set: Optional[List[str]]
    table_column_list: Optional[List[TableColumn]]

    def __init__(self, entry_id: int, experiment_id: int, entry_name: str, order: int,
                 base_data_type: Optional[str] = None, data_type_layout_name: Optional[str] = None,
                 field_set_id_list: Optional[List[int]] = None,
                 extension_type_set: Optional[List[str]] = None,
                 attachment_record_id: Optional[int] = None, attachment_data_type_name: Optional[str] = None,
                 is_created_from_file_import: Optional[bool] = None, is_auto_created_records: Optional[bool] = None,
                 auto_run_plugin_field_set_id: Optional[int] = None, show_key_fields: Optional[bool] = None,
                 is_field_addable: Optional[bool] = None, is_existing_field_removable: Optional[bool] = None,
                 template_field_name_set: Optional[List[str]] = None,
                 table_column_list: Optional[List[TableColumn]] = None):
        super().__init__(ElnEntryType.Table, entry_id, experiment_id, entry_name, order)
        self.base_data_type = base_data_type
        self.data_type_layout_name = data_type_layout_name
        self.field_set_id_list = field_set_id_list
        self.extension_type_set = extension_type_set
        self.attachment_record_id = attachment_record_id
        self.attachment_data_type_name = attachment_data_type_name
        self.is_created_from_file_import = is_created_from_file_import
        self.is_auto_created_records = is_auto_created_records
        self.auto_run_plugin_field_set_id = auto_run_plugin_field_set_id
        self.show_key_fields = show_key_fields
        self.is_field_addable = is_field_addable
        self.is_existing_field_removable = is_existing_field_removable
        self.template_field_name_set = template_field_name_set
        self.table_column_list = table_column_list


class ExperimentPluginEntry(ExperimentEntry):
    """
    An experiment entry that will display a custom client-side plugin.
    """
    plugin_name: str
    using_template_data: bool
    provides_template_data: bool

    def __init__(self, entry_id: int, experiment_id: int, entry_name: str, order: int,
                 plugin_name: str, using_template_data: bool, provides_template_data: bool):
        super().__init__(ElnEntryType.Plugin, entry_id, experiment_id, entry_name, order)
        self.plugin_name = plugin_name
        self.using_template_data = using_template_data
        self.provides_template_data = provides_template_data


class ExperimentFormEntry(ExperimentEntry):
    """
    An experiment entry that will display a form view of a single data record.
    """
    form_name_list: Optional[List[str]]
    data_type_layout_name: Optional[str]
    base_data_type: Optional[str]
    record_id: Optional[int]
    field_set_id_list: Optional[List[int]]
    extension_type_set: Optional[List[str]]
    auto_run_plugin_field_set_id: Optional[int]
    data_field_name_list: Optional[List[str]]
    is_field_addable: Optional[bool]
    is_existing_field_removable: Optional[bool]
    template_field_name_set: Optional[List[str]]

    def __init__(self, entry_id: int, experiment_id: int, entry_name: str, order: int,
                 form_name_list: Optional[List[str]] = None, data_type_layout_name: Optional[str] = None,
                 base_data_type: Optional[str] = None, record_id: Optional[int] = None,
                 field_set_id_list: Optional[List[int]] = None,
                 extension_type_set: Optional[List[str]] = None,
                 auto_run_plugin_field_set_id: Optional[int] = None,
                 data_field_name_list: Optional[List[str]] = None,
                 is_field_addable: Optional[bool] = None, is_existing_field_removable: Optional[bool] = None,
                 template_field_name_set: Optional[List[str]] = None):
        super().__init__(ElnEntryType.Form, entry_id, experiment_id, entry_name, order)
        self.base_data_type = base_data_type
        self.data_type_layout_name = data_type_layout_name
        self.field_set_id_list = field_set_id_list
        self.extension_type_set = extension_type_set
        self.auto_run_plugin_field_set_id = auto_run_plugin_field_set_id
        self.is_field_addable = is_field_addable
        self.is_existing_field_removable = is_existing_field_removable
        self.template_field_name_set = template_field_name_set
        self.form_name_list = form_name_list
        self.record_id = record_id
        self.data_field_name_list = data_field_name_list


class ExperimentDashboardEntry(ExperimentEntry):
    """
    An experiment entry that displays a chart.
    """
    dashboard_guid: Optional[str]
    data_source_entry_id: Optional[int]

    def __init__(self, entry_id: int, experiment_id: int, entry_name: str, order: int,
                 dashboard_guid: Optional[str] = None, data_source_entry_id: Optional[int] = None):
        super().__init__(ElnEntryType.Dashboard, entry_id, experiment_id, entry_name, order)
        self.dashboard_guid = dashboard_guid
        self.data_source_entry_id = data_source_entry_id


class ExperimentAttachmentEntry(ExperimentEntry):
    """
    An experiment entry that displays attached data for download, and preview if file is available for preview.
    """
    record_id: Optional[int]
    attachment_name: Optional[str]
    static_attachment_checksum: Optional[str]
    entry_attachment_list: Optional[List[EntryAttachment]]
    copy_attachment_bytes_to_template: bool

    def __init__(self, entry_id: int, experiment_id: int, entry_name: str, order: int,
                 record_id: Optional[int] = None, attachment_name: Optional[str] = None,
                 static_attachment_checksum: Optional[str] = None,
                 entry_attachment_list: Optional[List[EntryAttachment]] = None,
                 copy_attachment_bytes_to_template: bool = False):
        super().__init__(ElnEntryType.Attachment, entry_id, experiment_id, entry_name, order)
        self.record_id = record_id
        self.attachment_name = attachment_name
        self.static_attachment_checksum = static_attachment_checksum
        self.entry_attachment_list = entry_attachment_list
        self.copy_attachment_bytes_to_template = copy_attachment_bytes_to_template


class ExperimentEntryParser:
    @staticmethod
    def parse_experiment_entry(json_dct: Dict[str, Any]) -> ExperimentEntry:
        return _parse_experiment_entry(json_dct)


def _parse_entry_attachment(json_dct: Dict[str, Any]) -> EntryAttachment:
    attachment_type: EntryAttachmentType = EntryAttachmentType[json_dct.get('@type')]
    attachment_name: Optional[str] = json_dct.get('attachmentName')
    if attachment_type == EntryAttachmentType.ElnExperimentEntryStaticAttachmentPojo:
        static_attachment_checksum: Optional[str] = json_dct.get('staticAttachmentChecksum')
        return EntryStaticAttachment(attachment_name, static_attachment_checksum)
    elif attachment_type == EntryAttachmentType.ElnExperimentEntryRecordAttachmentPojo:
        record_id: Optional[int] = json_dct.get('recordId')
        return EntryRecordAttachment(attachment_name, record_id)
    else:
        raise ValueError("Unexpected attachment type: " + attachment_type.name)


def _parse_experiment_entry(json_dct: Dict[str, Any]) -> ExperimentEntry:
    entry_type: ElnEntryType = ElnEntryType[json_dct.get('entryType')]
    entry_id: int = int(json_dct.get('entryId'))
    parent_experiment_id: int = int(json_dct.get('parentExperimentId'))
    entry_name: str = json_dct.get('enbEntryName')
    order: int = json_dct.get('order')

    ret: ExperimentEntry
    if entry_type == ElnEntryType.Plugin:
        plugin_name: str = json_dct.get('pluginName')
        using_template_data: bool = json_dct.get('usingTemplateData')
        provides_template_data: bool = json_dct.get('providesTemplateData')
        ret = ExperimentPluginEntry(entry_id=entry_id, experiment_id=parent_experiment_id, entry_name=entry_name,
                                    order=order,
                                    plugin_name=plugin_name,
                                    using_template_data=using_template_data,
                                    provides_template_data=provides_template_data)
    elif entry_type == ElnEntryType.Table:
        base_data_type: Optional[str] = json_dct.get('enbBaseDataType')
        data_type_layout_name: Optional[str] = json_dct.get('dataTypeLayoutName')
        field_set_id_list: Optional[List[int]] = json_dct.get('fieldSetIdList')
        extension_type_set: Optional[List[str]] = json_dct.get('extensionTypeSet')
        attachment_record_id: Optional[int] = json_dct.get('attachmentRecordId')
        attachment_data_type_name: Optional[str] = json_dct.get('attachmentDataTypeName')
        is_created_from_file_import: Optional[bool] = json_dct.get('isCreatedFromFileImport')
        is_auto_created_records: Optional[bool] = json_dct.get('isAutoCreatedRecords')
        auto_run_plugin_field_set_id: Optional[int] = json_dct.get('autoRunPluginFieldSetId')
        show_key_fields: Optional[bool] = json_dct.get('showKeyFields')
        is_field_addable: Optional[bool] = json_dct.get('isFieldAddable')
        is_existing_field_removable: Optional[bool] = json_dct.get('isExistingFieldRemovable')
        template_field_name_set: Optional[List[str]] = json_dct.get('templateFieldNameSet')
        table_column_dict_list: Optional[List[Dict[str, Any]]] = json_dct.get('tableColumnList')
        table_column_list: Optional[List[TableColumn]] = None
        if table_column_dict_list:
            table_column_list = [TableColumnParser.to_table_column(x) for x in table_column_dict_list]
        ret = ExperimentTableEntry(entry_id=entry_id, experiment_id=parent_experiment_id, entry_name=entry_name,
                                   order=order,
                                   base_data_type=base_data_type, data_type_layout_name=data_type_layout_name,
                                   field_set_id_list=field_set_id_list, extension_type_set=extension_type_set,
                                   attachment_record_id=attachment_record_id,
                                   attachment_data_type_name=attachment_data_type_name,
                                   is_created_from_file_import=is_created_from_file_import,
                                   is_auto_created_records=is_auto_created_records,
                                   auto_run_plugin_field_set_id=auto_run_plugin_field_set_id,
                                   show_key_fields=show_key_fields, is_field_addable=is_field_addable,
                                   is_existing_field_removable=is_existing_field_removable,
                                   template_field_name_set=template_field_name_set,
                                   table_column_list=table_column_list)
    elif entry_type == ElnEntryType.Text:
        record_id: Optional[int] = json_dct.get('recordId')
        ret = ExperimentTextEntry(entry_id=entry_id, experiment_id=parent_experiment_id, entry_name=entry_name,
                                  order=order, record_id=record_id)
    elif entry_type == ElnEntryType.Form:
        form_name_list: Optional[List[str]] = json_dct.get('formNameList')
        data_type_layout_name: Optional[str] = json_dct.get('dataTypeLayoutName')
        base_data_type: Optional[str] = json_dct.get('enbBaseDataType')
        record_id: Optional[int] = json_dct.get('recordId')
        field_set_id_list: Optional[List[int]] = json_dct.get('fieldSetIdList')
        extension_type_set: Optional[List[str]] = json_dct.get('extensionTypeSet')
        auto_run_plugin_field_set_id: Optional[int] = json_dct.get('autoRunPluginFieldSetId')
        data_field_name_list: Optional[List[str]] = json_dct.get('dataFieldNameList')
        is_field_addable: Optional[bool] = json_dct.get('isFieldAddable')
        is_existing_field_removable: Optional[bool] = json_dct.get('isExistingFieldRemovable')
        template_field_name_set: Optional[List[str]] = json_dct.get('templateFieldNameSet')
        ret = ExperimentFormEntry(entry_id=entry_id, experiment_id=parent_experiment_id, entry_name=entry_name,
                                  order=order, form_name_list=form_name_list,
                                  data_type_layout_name=data_type_layout_name, base_data_type=base_data_type,
                                  record_id=record_id, field_set_id_list=field_set_id_list,
                                  extension_type_set=extension_type_set,
                                  auto_run_plugin_field_set_id=auto_run_plugin_field_set_id,
                                  data_field_name_list=data_field_name_list, is_field_addable=is_field_addable,
                                  is_existing_field_removable=is_existing_field_removable,
                                  template_field_name_set=template_field_name_set)
    elif entry_type == ElnEntryType.Attachment:
        record_id: Optional[int] = json_dct.get('recordId')
        attachment_name: Optional[str] = json_dct.get('attachmentName')
        static_attachment_checksum: Optional[str] = json_dct.get('staticAttachmentChecksum')
        entry_attachment_list: Optional[List[EntryAttachment]] = None
        if json_dct.get('entryAttachmentList') is not None:
            entry_attachment_list = [_parse_entry_attachment(x) for x in json_dct.get('entryAttachmentList')]
        copy_attachment_bytes_to_template: bool = json_dct.get('copyAttachmentBytesToTemplate')
        ret = ExperimentAttachmentEntry(entry_id=entry_id, experiment_id=parent_experiment_id, entry_name=entry_name,
                                        order=order, record_id=record_id, attachment_name=attachment_name,
                                        static_attachment_checksum=static_attachment_checksum,
                                        entry_attachment_list=entry_attachment_list,
                                        copy_attachment_bytes_to_template=copy_attachment_bytes_to_template)
    elif entry_type == ElnEntryType.Dashboard:
        dashboard_guid: Optional[str] = json_dct.get('dashboardGuid')
        data_source_entry_id: Optional[int] = json_dct.get('dataSourceEntryId')
        ret = ExperimentDashboardEntry(entry_id=entry_id, experiment_id=parent_experiment_id, entry_name=entry_name,
                                       order=order, dashboard_guid=dashboard_guid,
                                       data_source_entry_id=data_source_entry_id)
    elif entry_type == ElnEntryType.TempData:
        plugin_path: Optional[str] = json_dct.get('pluginPath')
        ret = ExperimentTempDataEntry(entry_id=entry_id, experiment_id=parent_experiment_id, entry_name=entry_name,
                                      order=order, plugin_path=plugin_path)
    else:
        raise ValueError("Unexpected Entry Type: " + str(entry_type))

    data_type_name: Optional[str] = json_dct.get('dataTypeName')
    ret.data_type_name = data_type_name
    description: Optional[str] = json_dct.get('description')
    ret.description = description
    related_entry_id_set: Optional[List[int]] = json_dct.get('relatedEntryIdSet')
    ret.related_entry_id_set = related_entry_id_set
    dependency_set: Optional[List[int]] = json_dct.get('dependencySet')
    ret.dependency_set = dependency_set
    requires_grabber_plugin: Optional[bool] = json_dct.get('requiresGrabberPlugin')
    ret.requires_grabber_plugin = requires_grabber_plugin
    is_initialization_required: Optional[bool] = json_dct.get('isInitializationRequired')
    ret.is_initialization_required = is_initialization_required
    entry_singleton_id: Optional[str] = json_dct.get('entrySingletonId')
    ret.singleton_id = entry_singleton_id
    tab_id: int = json_dct.get('notebookExperimentTabId')
    ret.notebook_experiment_tab_id = tab_id
    entry_height: Optional[int] = json_dct.get('entryHeight')
    ret.entry_height = entry_height
    column_order: Optional[int] = json_dct.get('columnOrder')
    ret.column_order = column_order
    column_span: Optional[int] = json_dct.get('columnSpan')
    ret.column_span = column_span
    is_removable: Optional[bool] = json_dct.get('isRemovable')
    ret.is_removable = is_removable
    is_renamable: Optional[bool] = json_dct.get('isRenamable')
    ret.is_renamable = is_renamable
    source_entry_id: Optional[int] = json_dct.get('sourceEntryId')
    ret.source_entry_id = source_entry_id
    is_collapsed: Optional[bool] = json_dct.get('isCollapsed')
    ret.is_collapsed = is_collapsed
    is_hidden: Optional[bool] = json_dct.get('isHidden')
    ret.is_hidden = is_hidden
    is_static_view: Optional[bool] = json_dct.get('isStaticView')
    ret.is_static_view = is_static_view
    is_created_from_template: Optional[bool] = json_dct.get('isCreatedFromTemplate')
    ret.is_created_from_template = is_created_from_template
    template_item_fulfilled_timestamp: Optional[int] = json_dct.get('templateItemFulfilledTimestamp')
    ret.template_item_fulfilled_timestamp = template_item_fulfilled_timestamp
    has_comments: Optional[bool] = json_dct.get('hasComments')
    ret.has_comments = has_comments
    is_shown_in_template: Optional[bool] = json_dct.get('isShownInTemplate')
    ret.is_shown_in_template = is_shown_in_template
    entry_status: ExperimentEntryStatus = json_dct.get('entryStatus')
    ret.entry_status = entry_status
    submitted_by: Optional[str] = json_dct.get('submittedBy')
    ret.submitted_by = submitted_by
    submitted_date: Optional[int] = json_dct.get('submittedDate')
    ret.submitted_date = submitted_date
    last_modified_by: Optional[str] = json_dct.get('lastModifiedBy')
    ret.last_modified_by = last_modified_by
    last_modified_date: Optional[int] = json_dct.get('lastModifiedDate')
    ret.last_modified_date = last_modified_date
    created_by: Optional[str] = json_dct.get('createdBy')
    ret.created_by = created_by
    date_created: Optional[int] = json_dct.get('dateCreated')
    ret.date_created = date_created
    approval_due_date: Optional[int] = json_dct.get('approvalDueDate')
    ret.approval_due_date = approval_due_date
    if json_dct.get('fieldDefinitions') is not None:
        defs: List[AbstractVeloxFieldDefinition] = [FieldDefinitionParser.to_field_definition(x)
                                                    for x in json_dct.get('fieldDefinitions')]
        ret.field_definition_list = defs
    return ret
