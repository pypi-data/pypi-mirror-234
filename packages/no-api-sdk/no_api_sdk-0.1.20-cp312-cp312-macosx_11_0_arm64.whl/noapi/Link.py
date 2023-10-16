# emacs mycoding: utf-8
# mypy: disallow-untyped-defs
# mypy: check-untyped-defs
# mypy: disallow-incomplete-defs

import logging
console = logging
from .await_async import _await_async
from typing import Dict, Optional, Any, TYPE_CHECKING
from .msg import msg

if TYPE_CHECKING:
    from .List import List
    from .Item import Item
    from . import PropertyValue, Field, GetResult
class Link:
    '''
    Link class
    '''
    # TODO: how to set to undefined or unknown or deleted or something

    # TODO: also add methods to guard against the use of self
    # type of item for array/set access, etc

    # TODO: add methods from https://docs.python.org/3/reference/datamodel.htm

    def __init__(self, localdb: Dict, of_item: "Item", relation: str, internal : bool = False) -> None:
        if not internal:
            msg._tell_dev(msg.M519_called_class_constructor,{})
        self._localdb = localdb
        self._relation = relation
        self._of_item: "Item" = of_item
        self._r_1 : Optional[str] = None

    def _setRelation1(self, tlink: str) -> None:
        self._r_1 = tlink

    def on_update(self, f: Any) -> None: # FIXME: shouul be something like callable instead of Any
        raise Exception("cannot define on_update on a link. define it on the item")

    def __iter__(self) -> None:
        raise Exception("cannot iter on link")

    def recall(self) -> "Optional[Item]":
        try:
            if self._r_1 is None:
                return None
            # obj does not exists in localdb, so lets create it
            if not (self._r_1 in self._localdb):
                console.debug("CREATED NEWOBJ")
                from .Item import Item

                newobj = Item(self._localdb, self._r_1, self._of_item._datastore, True)

            console.debug("RECALL R-1 localdb r_1 = result")
            console.debug(self)
            console.debug(self._localdb)
            console.debug(self._r_1)
            console.debug(self._localdb[self._r_1])
            console.debug("ENDRECALL R-1")

            tor = self._localdb[self._r_1]
            if self._r_1 == None:
                if "exception_on_none_links" in self._of_item._datastore.features:
                    item_name = self._of_item.get("name")
                    prop_name = _await_async(self._of_item._propid_to_propstring(self._relation))
                    raise RuntimeError("Encountered None when accessing the field "+prop_name+" of an item named "+item_name)
                return None
            return tor
        except:
            raise
