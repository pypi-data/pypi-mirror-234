# emacs mycoding: utf-8
# mypy: disallow-untyped-defs
# mypy: check-untyped-defs
# mypy: disallow-incomplete-defs

import logging
from typing import Union, Any, Optional, TYPE_CHECKING
from .msg import msg

console = logging
if TYPE_CHECKING:
    from . import PropertyValue, Field, GetResult

class Property:
    '''
    Property classs
    '''
    # TODO: how to delete values, or undefine them or something...

    # TODO: also add methods to guard against the use of this
    # type of item for array/set access, etc

    # TODO: add methods from https://docs.python.org/3/reference/datamodel.html

    def __real_init__(self, __internal : bool = False) -> None:
        '''
        constructor2
        '''
        if not __internal:
            msg._tell_dev(msg.M519_called_class_constructor,{})
        self._value_type : Optional[str] = None
        self._value : PropertyValue= None

    def __init__(self,*args) -> None: # type: ignore [no-untyped-def] # Hide the arguments from autodoc
        '''        '''        '''
        constructor2
        '''
        return self.__real_init__(args) # type: ignore [arg-type]

    # self is set in the internal localdb set meaning. NOT set at the server.
    def _setValue(self, value: "PropertyValue") -> None:
        # consider type at some point.
        if (self._value_type=="str"):
            self._value= str(self._value)
        elif (self._value_type=="bol"):
            self._value= (self._value==True)
        elif (self._value_type=="num"):
            try:
                self._value=int(value) # type: ignore
            except ValueError:
                try:
                    self._value=float(value) # type: ignore
                except ValueError:
                    raise Exception("Cannot convert into python int or float")
        elif self._value_type is not None and (self._value_type[0:2]=="no"):
            return None
        else:
            raise Exception("Unknown value type in property recall:"+ str(self._value_type))

        self._value = value

    def __str__(self) -> str:
        console.debug("VAL TO STRING")
        return str(self._value)

    def valueOf(self) -> "PropertyValue":
        return self._value

    def on_update(self, f: Any =None) -> None:
        raise Exception("cannot define on_update on a value property. define it on the item")

    def create(self) -> None:
        raise Exception("cannot create on a value property. create on a relation: see http:#??")

    def _setValueType(self, valtype: str) -> None:
        self._value_type = valtype

    def recall(self) -> "PropertyValue":
        return self._value

    def __iter__(self) -> None:
        raise Exception("cannot iter on property")
