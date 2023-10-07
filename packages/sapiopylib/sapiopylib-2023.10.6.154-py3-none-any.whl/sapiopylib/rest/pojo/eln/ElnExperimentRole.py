from typing import Dict, Any


class AbstractElnExperimentRole:
    """
    Describes the role permissions a principal will have on a ELN notebook experiment.
    """
    is_author: bool
    is_witness: bool
    is_reviewer: bool
    is_approver: bool

    def __init__(self, is_author: bool, is_witness: bool, is_reviewer: bool, is_approver: bool):
        self.is_author = is_author
        self.is_witness = is_witness
        self.is_reviewer = is_reviewer
        self.is_approver = is_approver


class ElnUserExperimentRole(AbstractElnExperimentRole):
    """
    Describes the role permissions a user will have on a ELN notebook experiment.
    """
    username: str

    def __init__(self, is_author: bool, is_witness: bool, is_reviewer: bool, is_approver: bool,
                 username: str):
        super().__init__(is_author, is_witness, is_reviewer, is_approver)
        self.username = username


class ElnGroupExperimentRole(AbstractElnExperimentRole):
    """
    Describes the role permissions a group will have on a ELN notebook experiment.
    """
    group_id: int

    def __init__(self, is_author: bool, is_witness: bool, is_reviewer: bool, is_approver: bool,
                 group_id: int):
        super().__init__(is_author, is_witness, is_reviewer, is_approver)
        self.group_id = group_id


class ElnExperimentRoleParser:
    @staticmethod
    def parse_user_role(json_dct: Dict[str, Any]) -> ElnUserExperimentRole:
        return _parse_user_role(json_dct)

    @staticmethod
    def parse_group_role(json_dct: Dict[str, Any]) -> ElnGroupExperimentRole:
        return _parse_group_role(json_dct)


def _parse_abstract_role(json_dct: Dict[str, Any]) -> AbstractElnExperimentRole:
    is_author: bool = json_dct.get('author')
    is_witness: bool = json_dct.get('witness')
    is_reviewer: bool = json_dct.get('reviewer')
    is_approver: bool = json_dct.get('approver')
    return AbstractElnExperimentRole(is_author=is_author, is_witness=is_witness,
                                     is_reviewer=is_reviewer, is_approver=is_approver)


def _parse_user_role(json_dct: Dict[str, Any]) -> ElnUserExperimentRole:
    abstract_role: AbstractElnExperimentRole = _parse_abstract_role(json_dct)
    username = json_dct.get('username')
    return ElnUserExperimentRole(is_author=abstract_role.is_author, is_witness=abstract_role.is_witness,
                                 is_reviewer=abstract_role.is_reviewer, is_approver=abstract_role.is_approver,
                                 username=username)


def _parse_group_role(json_dct: Dict[str, Any]) -> ElnGroupExperimentRole:
    abstract_role: AbstractElnExperimentRole = _parse_abstract_role(json_dct)
    group_id: int = json_dct.get('groupId')
    return ElnGroupExperimentRole(is_author=abstract_role.is_author, is_witness=abstract_role.is_witness,
                                  is_reviewer=abstract_role.is_reviewer, is_approver=abstract_role.is_approver,
                                  group_id=group_id)
