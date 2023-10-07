from enum import Enum


class SapioAccessType(Enum):
    """
    All access types that are visible to webservice.

    This is used both in record ACL and data type access.
    """
    READ = 0
    WRITE = 1
    DELETE = 2
