from __future__ import annotations
from weakref import WeakValueDictionary

from sapiopylib.rest.User import SapioUser
from sapiopylib.rest.pojo.CustomReport import *
from sapiopylib.rest.pojo.Sort import SortDirectionParser


class _CustomReportParser:
    """
    Internal class holding logic to parse custom report JSON POJO objects.
    """

    @staticmethod
    def parse_related_record_criteria(json_dct: Dict[str, Any]) -> RelatedRecordCriteria:
        query_restriction = QueryRestriction[json_dct.get('queryRestriction')]
        related_record_id = None
        if 'relatedRecordId' in json_dct:
            related_record_id = int(json_dct.get('relatedRecordId'))
        related_record_type = None
        if 'relatedRecordType' in json_dct:
            related_record_type = json_dct.get('relatedRecordType')
        return RelatedRecordCriteria(query_restriction,
                                     related_record_id=related_record_id, related_record_type=related_record_type)

    @staticmethod
    def parse_report_term(json_dct: Dict[str, Any]) -> AbstractReportTerm:
        """
        Assuming the dictionary is only containing the term itself right now, parse it as a report term.
        :param json_dct: The JSON dictionary.
        :return: A report term
        """
        term_type_name = json_dct.get('termType')
        negated = bool(json_dct.get('negated'))
        term_type = TermType[term_type_name]
        if term_type == TermType.RAW_TERM:
            data_type_name: str = json_dct.get('dataTypeName')
            data_field_name: str = json_dct.get('dataFieldName')
            term_operation: RawTermOperation = RawTermOperation[json_dct.get('termOperation')]
            trim: bool = bool(json_dct.get('trim'))
            value: str = json_dct.get('value')
            ret = RawReportTerm(data_type_name, data_field_name, term_operation, value, trim=trim, is_negated=negated)
            return ret
        elif term_type == TermType.COMPOSITE_TERM:
            term_operation: CompositeTermOperation = CompositeTermOperation[json_dct.get('termOperation')]
            left_child = _CustomReportParser.parse_report_term(json_dct.get('leftChild'))
            right_child = _CustomReportParser.parse_report_term(json_dct.get('rightChild'))
            ret = CompositeReportTerm(left_child, term_operation, right_child, is_negated=negated)
            return ret
        elif term_type == TermType.JOIN_TERM:
            left_data_type_name: str = json_dct.get('leftDataTypeName')
            left_data_field_name: str = json_dct.get('leftDataFieldName')
            term_operation: RawTermOperation = RawTermOperation[json_dct.get('termOperation')]
            right_data_type_name: str = json_dct.get('rightDataTypeName')
            right_data_field_name: str = json_dct.get('rightDataFieldName')
            trim: bool = bool(json_dct.get('trim'))
            return FieldCompareReportTerm(left_data_type_name, left_data_field_name, term_operation,
                                          right_data_type_name=right_data_type_name,
                                          right_data_field_name=right_data_field_name, trim=trim)
        raise ValueError(json_dct)

    @staticmethod
    def parse_report_column(json_dct: Dict[str, Any]) -> ReportColumn:
        data_type_name: str = json_dct.get('dataTypeName')
        data_field_name: str = json_dct.get('dataFieldName')
        field_type: FieldType = FieldType[json_dct.get('fieldType')]
        sort_order: int = int(json_dct.get('sortOrder'))
        sort_order_direction_name = json_dct.get('sortDirection')
        sort_direction = SortDirectionParser.parse_sort_direction(sort_order_direction_name)
        return ReportColumn(data_type_name, data_field_name, field_type, sort_order, sort_direction)

    @staticmethod
    def parse_explicit_join_definition(json_dct: Dict[str, Any]) -> ExplicitJoinDefinition:
        data_type_name: str = json_dct.get('dataTypeName')
        # noinspection PyTypeChecker
        report_term: FieldCompareReportTerm = _CustomReportParser.parse_report_term(json_dct.get('reportTermPojo'))
        return ExplicitJoinDefinition(data_type_name, report_term)

    @staticmethod
    def parse_custom_report_criteria(json_dct: Dict[str, Any]) -> CustomReportCriteria:
        column_list = [_CustomReportParser.parse_report_column(dct) for dct in json_dct.get('columnList')]
        root_term = _CustomReportParser.parse_report_term(json_dct.get('rootTerm'))
        related_record_criteria = RelatedRecordCriteria(QueryRestriction.QUERY_ALL)
        if json_dct.get('relatedRecordCriteria') is not None:
            related_record_criteria = _CustomReportParser.parse_related_record_criteria(
                json_dct.get('relatedRecordCriteria'))
        case_sensitive = bool(json_dct.get('caseSensitive'))
        page_size = int(json_dct.get('pageSize'))
        page_number = int(json_dct.get('pageNumber'))
        root_data_type = None
        if json_dct.get('rootDataType') is not None:
            root_data_type = json_dct.get('rootDataType')
        owner_restriction_set = None
        if json_dct.get('ownerRestrictionSet') is not None:
            owner_restriction_set = json_dct.get('ownerRestrictionSet')
        join_list: Optional[List[ExplicitJoinDefinition]] = None
        if json_dct.get('joinList') is not None:
            join_list = [_CustomReportParser.parse_explicit_join_definition(x) for x in json_dct.get('joinList')]
        return CustomReportCriteria(column_list, root_term, related_record_criteria=related_record_criteria,
                                    root_data_type=root_data_type, case_sensitive=case_sensitive,
                                    page_size=page_size, page_number=page_number,
                                    owner_restriction_set=owner_restriction_set, join_list=join_list)

    @staticmethod
    def parse_custom_report(json_dct: Dict[str, Any]) -> CustomReport:
        criteria = _CustomReportParser.parse_custom_report_criteria(json_dct)
        has_next_page: bool = json_dct.get('hasNextPage')
        result_table: List[List[Any]] = json_dct.get('resultTable')
        return CustomReport(has_next_page, result_table, criteria)


class CustomReportManager:
    """
    A suite to run a simple or complex query with conditions across a linage of records.
    """

    user: SapioUser
    __instances: WeakValueDictionary[SapioUser, CustomReportManager] = WeakValueDictionary()
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
        Obtain a custom report manager to run advanced searches for a user context.
        :param user: The user context to create custom report.
        """
        if self.__initialized:
            return
        self.user = user
        self.__initialized = True

    def run_system_report_by_name(self, system_report_name: str,
                                  page_size: Optional[int] = None, page_number: Optional[int] = None) -> CustomReport:
        """
        Given a custom report name of a saved custom report, run it and return results.
        :param system_report_name: The system report name to search for.
        :param page_size: The page size of this report.
        If this is greater than the license limit, it will be limited by license on result.
        :param page_number: The page number of this report.
        """
        sub_path = self.user.build_url(['report', 'runSystemReportByName', system_report_name])
        params = dict()
        if page_size is not None:
            params['pageSize'] = page_size
        if page_number is not None:
            params['pageNumber'] = page_number
        response = self.user.get(sub_path, params)
        self.user.raise_for_status(response)
        json_dct = response.json()
        return _CustomReportParser.parse_custom_report(json_dct)

    def run_custom_report(self, custom_report_request: CustomReportCriteria) -> CustomReport:
        """
        Run on-demand custom report.
        :param custom_report_request: The custom report request object containing all attributes about the request.
        :return: A custom report that has been executed by server.
        """
        sub_path = self.user.build_url(['report', 'runCustomReport'])
        payload = custom_report_request.to_json()
        response = self.user.post(sub_path, payload=payload)
        self.user.raise_for_status(response)
        json_dct = response.json()
        return _CustomReportParser.parse_custom_report(json_dct)

    def run_quick_report(self, report_term: RawReportTerm,
                         page_size: Optional[int] = None, page_number: Optional[int] = None) -> CustomReport:
        """
        Restricted to single condition but easier to use.
        :param page_size: The page size of this report. If this is greater than the license limit,
        it will be limited by license on result.
        :param page_number: The page number of this report.
        :param report_term:
        :return:
        """
        sub_path = self.user.build_url(['report', 'runQuickReport'])
        payload = report_term.to_json()
        params = dict()
        if page_size is not None:
            params['pageSize'] = page_size
        if page_number is not None:
            params['pageNumber'] = page_number
        response = self.user.post(sub_path, params=params, payload=payload)
        self.user.raise_for_status(response)
        json_dct = response.json()
        return _CustomReportParser.parse_custom_report(json_dct)
