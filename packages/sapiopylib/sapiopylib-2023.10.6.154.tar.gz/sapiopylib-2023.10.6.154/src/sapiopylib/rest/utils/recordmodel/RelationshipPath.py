from __future__ import annotations

from enum import Enum
from typing import List, Tuple, Type

from sapiopylib.rest.utils.recordmodel import RecordModelWrapper


class RelationshipPathDir(Enum):
    PARENT = 1
    CHILD = 2


class RelationshipPath:
    """
    Specifies a path of relationship to load, instead of simply loading a single parent/child type at a time.
    """
    path: List[Tuple[RelationshipPathDir, str]]

    def __init__(self):
        self.path = []

    def child_type(self, child_type: Type[RecordModelWrapper]) -> RelationshipPath:
        dt_name = child_type.get_wrapper_data_type_name()
        return self.child(dt_name)

    def parent_type(self, parent_type: Type[RecordModelWrapper]) -> RelationshipPath:
        dt_name = parent_type.get_wrapper_data_type_name()
        return self.parent(dt_name)

    def child(self, child_type: str) -> RelationshipPath:
        self.path.append((RelationshipPathDir.CHILD, child_type))
        return self

    def parent(self, parent_type: str) -> RelationshipPath:
        self.path.append((RelationshipPathDir.PARENT, parent_type))
        return self


