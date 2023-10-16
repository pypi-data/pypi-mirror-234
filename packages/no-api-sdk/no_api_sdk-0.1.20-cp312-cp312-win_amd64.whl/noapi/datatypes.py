# emacs coding: utf-8
# mypy: disallow-untyped-defs
# mypy: check-untyped-defs
# mypy: disallow-incomplete-defs

# WARNING; this file is shared between noapi-src and noapi-apps/sdk/python
# If you update one, you need to update the other

class datatypes:
    STRING= 'str'
    NO_STRING='nos'
    NUMBER='num'
    NO_NUM='non'
    DATE='dat'
    NO_DATE='nod'
    BOOL='bol'
    NO_BOOL='nob'
    value_types=[STRING,NUMBER,DATE,BOOL]
    UNKNOWN='unk'
    LINK='r-1'
    NO_LINK='noi'
    LIST='r-n'
    NO_LIST='nol'
    no_types=[NO_LINK, NO_LIST, NO_STRING, NO_NUM, NO_DATE, NO_BOOL, UNKNOWN]
    ERROR='err'
    METHOD_ARGS='arg'
    SUCCEED='suc'
    WRONG_TYPE='wdt'
    SAME_OPERATION='sop'
    CALC_VERSION='cal'
    NEWER_VERSION='nev'

    @staticmethod
    def unknown_of(t: str) -> str:
        if t==datatypes.STRING:
            return datatypes.NO_STRING
        if t==datatypes.NUMBER:
            return datatypes.NO_NUM
        if t==datatypes.DATE:
            return datatypes.NO_DATE
        if t==datatypes.BOOL:
            return datatypes.NO_BOOL
        elif t==datatypes.LINK:
            return datatypes.NO_LINK
        elif t==datatypes.LIST:
            return datatypes.NO_LIST
        elif t in datatypes.no_types:
            raise RuntimeError("unknown_of called on an already unknown datatype:"+t)
        else:
            raise RuntimeError("dont know how to find unknown_of datatype:"+t)

    @staticmethod
    def from_str(s: str) -> str:
        if s ==  'str':
            return datatypes.STRING
        if s == 'nos':
            return datatypes.NO_STRING
        if s == 'num':
            return datatypes.NUMBER
        if s == 'non':
            return datatypes.NO_NUM
        if s == 'dat':
            return datatypes.DATE
        if s == 'nod':
            return datatypes.NO_DATE
        if s == 'bol':
            return datatypes.BOOL
        if s == 'nob':
            return datatypes.NO_BOOL
        if s == 'unk':
            return datatypes.UNKNOWN
        if s == 'r-1':
            return datatypes.LINK
        if s == 'noi':
            return datatypes.NO_LINK
        if s == 'r-n':
            return datatypes.LIST
        if s == 'nol':
            return datatypes.NO_LIST
        else:
            raise RuntimeError("dont know how to find datatype of:"+s)
