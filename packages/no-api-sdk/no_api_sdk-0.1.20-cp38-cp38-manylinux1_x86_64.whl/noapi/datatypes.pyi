from _typeshed import Incomplete

class datatypes:
    STRING: str
    NO_STRING: str
    NUMBER: str
    NO_NUM: str
    DATE: str
    NO_DATE: str
    BOOL: str
    NO_BOOL: str
    value_types: Incomplete
    UNKNOWN: str
    LINK: str
    NO_LINK: str
    LIST: str
    NO_LIST: str
    no_types: Incomplete
    ERROR: str
    METHOD_ARGS: str
    SUCCEED: str
    WRONG_TYPE: str
    SAME_OPERATION: str
    CALC_VERSION: str
    NEWER_VERSION: str
    @staticmethod
    def unknown_of(t: str) -> str: ...
    @staticmethod
    def from_str(s: str) -> str: ...
