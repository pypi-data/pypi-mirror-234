# emacs mycoding: utf-8
# mypy: disallow-untyped-defs
# mypy: check-untyped-defs
# mypy: disallow-incomplete-defs

import hashlib
import logging
console = logging
from .await_async import _await_async
from typing import Dict, Optional, Any, TYPE_CHECKING, cast, Iterator, Union
from typing_extensions import TypeAlias
import typing
from .Slice import Slice # type: ignore
from itertools import islice, dropwhile
from collections import deque
from .msg import msg

if TYPE_CHECKING:
    from . import PropertyValue, Field, GetResult
    from .Item import Item

PythonClass: TypeAlias = type

class List(object):
    '''
    List class
    '''

    # TODO: how to set to undefined or unknown, or deleted or something

    # TODO: also add methods to guard against the use of self
    # type of item for array/set access, etc

    # TODO: add methods from https://docs.python.org/3/reference/datamodel.html
    def __init__(self, localdb: dict, of_item: "Item", relation: str, internal : bool = False) -> None:
        if not internal:
            msg._tell_dev(msg.M519_called_class_constructor,{})
        self._localdb : "Dict[str,Item]" = localdb
        self._relation : str = relation
        self._of_item : "Item" = of_item
        self._items_in_list : Optional[typing.List[str]] = None
        self._MAX_ITEM_WITHOUT_PAGING = 1024
        if (not self._relation in self._localdb):
            from .Item import Item
            self._prop_obj = Item(self._localdb, self._relation, self._of_item._datastore, True)  # FIXME: there should be a singleton type of get for Item
        else:
            self._prop_obj = self._localdb[self._relation]

    def of_type(self) -> "Item":
        my_type = self._prop_obj.get("oftype")
        from .Item import Item
        if type(my_type)== Item:
            return cast(Item,my_type)
        else:
            raise Exception("unexpected python class when getting of_type of a list")

    @property
    def of_item(self) -> "Item":
        return self._of_item

    @property
    def fields(self) -> "List":
        return self._of_item.type.fields

    @property
    def type(self) -> "List":
        msg._tell_dev(msg.M413_want_oftypelist_not_typelist__list,{"list":str(self._prop_obj)})
        return self._of_item.type

    def __str__(self) -> str:
        name_of_relation = self._prop_obj.get("name")
        return str(self.of_item)+"."+name_of_relation+"("+str(len(self))+")" # FIXME. _relation does not get updates?

    def __repr__(self) -> str:
        name_of_relation = "Listname_not_retrieved"
        if "__name_f" in self._prop_obj._myfields:
            nameval  = self._prop_obj._myfields["__name_f"].recall()
            if nameval is None:
                name_of_relation = "None"
            else:
                name_of_relation = nameval
        myhash = hashlib.shake_128(str(self._relation).encode()).hexdigest(3)
        return "List:"+repr(self.of_item)[5:]+"."+name_of_relation+"-"+myhash+"(len="+str(len(self))+")"  # 5: throws away the "Item:" part

    def __len__(self) -> int:
        if (self._items_in_list is None):
            raise TypeError("len() not possible on a List that is None")
                    # FIXME: this should really be received from the server
        return len(self._items_in_list)

    def _setRelationN(self, value: Optional[str]) -> None:
        if value is None:
            self._items_in_list = None
        else:
            x = 8  # split string into array by length of x
            self._items_in_list = [value[y - x : y] for y in range(x, len(value) + x, x)]

    def on_update(self, f: Any) -> None:
        raise Exception("cannot define on_update on a list. define it on the item")

    def prepend(self, item:  "typing.List[Item] | Item | List",before:bool=True, relative_to_item:Optional["Item"]=None) -> None:
        return self.append(item, before, relative_to_item)

    def append(self, item:  "typing.List[Item] | Item | List",before:bool=False, relative_to_item:Optional["Item"]=None) -> None:
        from .Item import Item # putting this at the beginning creates a circular import
        if type(item) == Item:
            self.__append_item(item,before,relative_to_item)
        elif type(item) == typing.List[Item] or type(item) == List:
            self.__append_items(item,before,relative_to_item)
        else:
            msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(item), "etype":"'list[Item]', 'Item', 'List'"})

    def __append_item(self, item : "Item",before:bool,relative_to_item:Optional["Item"]) -> None:
        _await_async((self._localdb[self._of_item._oid])._async_append(self._relation,item,before,relative_to_item))

    def __append_items(self, items : "typing.List[Item] | List",before:bool,relative_to_item:Optional["Item"]) -> None:
        # Items already in the list raising the exception
        items_errors = []
        for item in items:
            try:
                self.__append_item(item,before,relative_to_item)
            except:  # FIXME:  too generic of an exception
                items_errors.append(item)
                continue
        if items_errors: # FIXME: each item should be accompanied by the reason of its exception
            msg._tell_dev(msg.M525_appending_existing_items__list_items,
                        {"listname": self._prop_obj.name, "items": items_errors})

    # FIXME: this should become _remove_item, but also add remove() that handles python and noapi Lists.
    def remove(self, item : "Item") -> None:
        from .Item import Item
        if item is None:
            raise RuntimeError("got None instead of an item to remove") # FIXME: convert to numbered msg.telldev

        if not isinstance(item,Item):
            raise RuntimeError("arg to remove should be an item ") # FIXME: convert to numbered msg.telldev
        _await_async((self._localdb[self._of_item._oid])._async_remove(self._relation,item._oid))

    # FIXME: this should become _remove_item, but also add remove() that handles python and noapi Lists.
    def destroy(self, item : "Item") -> None:
        from .Item import Item
        if item is None:
            raise RuntimeError("got None instead of an item to destroy ") # FIXME: convert to numbered msg.telldev
        if not isinstance(item,Item):
            raise RuntimeError("arg to destroy should be an item ") # FIXME: convert to numbered msg.telldev
        _await_async((self._localdb[self._of_item._oid])._async_destroy(self._relation,item._oid))

    def create(self,set_value: Optional['typing.List[str | Dict[str, PropertyValue]] | str | Dict[str, PropertyValue]'] = None, set_propname: Optional[str]=None) -> Optional['"Item" | list']:
        if isinstance(set_value, str) or set_value is None:
            return self._create_item(set_value, set_propname)
        elif isinstance(set_value, list):
            return self._create_items_of_list(set_value)
        elif isinstance(set_value, dict):
            return self._create_items_of_dict(set_value)
        else:
            msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(set_value), "etype":"'list[str|dict]', 'str', 'dict'"})
            raise

    def _create_item(self, set_value : Optional[str] , set_propname: Optional[str]=None) -> Optional["Item"]:
        return _await_async((self._localdb[self._of_item._oid])._async_create(self._relation,set_value,set_propname))

    def _create_items_of_list(self, set_values : 'typing.List[str | Dict[str, PropertyValue]]') -> Optional[list]:
        item_created = []
        for set_value in set_values:
            if isinstance(set_value, str):
                item_created.append(self._create_item(set_value))
            elif isinstance(set_value, dict):
                item_created.append(self._create_items_of_dict(set_value))
            else:
                msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":f"list[{str(type(set_value))}]", "etype":"'list[str|dict]'"})
        return item_created

    def _create_items_of_dict(self, set_value: Dict[str, "PropertyValue"]) -> Optional["Item"]:
        # list_1 = set(set_value.keys())
        # list_2 = set([field.name for field in self.type.fields])
        # print(next(iter(list_1.difference(list_2))))
        if "name" in set_value:
            if not isinstance(set_value.get("name"), str):
                msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(set_value.get("name")), "etype":"'str'"})
                raise
            else:
                item = self._create_item(str(set_value.get("name")))
                if item:
                    for key,val in set_value.items():
                        if key != "name":
                            item.set(key,val)
                return item
        else:
            msg._tell_dev(msg.M524_missing_property_value__listname_propname,{"listname":self._prop_obj.name, "propname":"name"})
            raise

    def first(self) -> "Optional[Item]":
        iter = self.__iter__()
        try:
            return iter.__next__()
        except StopIteration:
            # FIXME: if warn on none feature flag is set, generate warning that first() is none
            return None

    def before(self,item: "Item") -> "Item":
        raise Exception("before is not yet implemented")

    def after(self,item: "Item") -> "Optional[Item]":
        raise Exception("after of item is unimplemented")

    def last(self) -> "Optional[Item]":
        this_r_n = self._items_in_list
        if this_r_n is None:
            raise Exception("list not here yet")
        elif len(this_r_n) == 0:
            # FIXME: if warn on none feature flag is set, generate warning that first() is none
            return None
        last_oid = this_r_n[len(this_r_n)-1]
        alocaldb = self._localdb
        if last_oid not in alocaldb:
                from .Item import Item
                alocaldb[last_oid] = Item(alocaldb, last_oid, self._of_item._datastore, True)
        return alocaldb[last_oid]

    def _use_paging_error(self) -> None:
        raise Exception('for long r-n lists you must use paging. See http://DATANET/function-relation-length.')

    def find(self,search_for: "Union[str,Item]", search_in_field: Optional[str]=None) -> "Optional[Item]":
        # print("FIND")
        #print(repr(searchstring))
        #print(repr(self._relation))
        #print(repr(self._localdb[self._of_item]))
        name_of_relation = self._prop_obj.get("name")
        return (_await_async( (self._localdb[self._of_item._oid])._find_in_list_by_propstr(
            name_of_relation, search_for, search_in_field)))

    def __getitem__(self, search_term : str) -> Optional["Item"]:
        item = self.find(search_term)
        if item is None :
            msg._tell_dev(msg.M520_item_not_found_in_list__key_item_list,{"key": search_term, "item":self._of_item, "list":self._prop_obj.get("name")} )
        return item

    class __rnIterator(object):
        def __init__(self, r_n_o: "List") -> None:
            self.index: int = 0
            self._of_List : "List" = r_n_o

        def __next__(self) -> "Item":
            self.index = self.index + 1
            if (self.index > self._of_List._MAX_ITEM_WITHOUT_PAGING):
                self._of_List._use_paging_error()

            if self._of_List._items_in_list is None:
                raise StopIteration
            this_r_n : typing.List[str] = self._of_List._items_in_list
            if self.index > len(this_r_n):
                raise StopIteration
            next_oid = str(this_r_n[self.index - 1])
            alocaldb = self._of_List._localdb
            if next_oid not in alocaldb:
                from .Item import Item
                alocaldb[next_oid] = Item(alocaldb, next_oid, self._of_List._of_item._datastore, True)

            next_Item = alocaldb[next_oid]
            return next_Item

    def recall(self) -> "List":
        return self

    def __iter__(self) -> '__rnIterator':
        tor = self.__rnIterator(self)
        return tor

    def slice(self, start_at: Optional["Item"] = None , size: int = 16,
                search_term: Optional[Any] =None, search_field: Optional[str] = None) -> "Optional[Slice]":
        localDb = self._localdb
        return Slice(self,localDb, start_at, size, search_term, search_field, True) # Yes, first arg is this list

    def define_property(self, name : str, proptype: Union[str,PythonClass,None] = None) -> "Item":
        return self._prop_obj.define_property(name, proptype)

    def define_calculated_property(self, name:str, datatype: str, formula:str) -> "Item":
        return self._prop_obj.define_calculated_property(name,datatype,formula)

    def define_subitem(self,link_name:str,
                inverse_name:Optional[str]=None) -> "Item":
        return self._prop_obj.define_subitem(link_name,inverse_name)

    def define_link(self, name:str,range:Optional[str]=None, inverse_name:Optional[str]=None,
                    inverse_cardinal:Optional[str]=None,inverse_range:Optional[str]=None) -> "Item":
        return self._prop_obj.define_link(name,range,inverse_name,inverse_cardinal,inverse_range)

    def define_calculated_link(self,name:str,range:str,formula:str,
                            inverse_name:Optional[str]=None) -> "Item":
        return self._prop_obj.define_calculated_link(name,range,formula,inverse_name)

    def define_list_of_items(self, name:str, inverse_name:Optional[str]=None) -> "Item":
        return self._prop_obj.define_list_of_items(name, inverse_name)

    def define_list_of_links(self,list_name:str,range:Optional[str]=None,
                             inverse_name:Optional[str]=None,inverse_cardinal:Optional[str]=None,inverse_range:Optional[str]=None) -> "Item":
        return self._prop_obj.define_list_of_links(list_name,range,inverse_name,inverse_cardinal,inverse_range)

    def define_list(self,list_name:str,range:Optional[str]=None,
        inverse_name:Optional[str]=None,inverse_cardinal:Optional[str]=None,inverse_range:Optional[str]=None) -> "Item":
        return self._prop_obj.define_list(list_name,range,inverse_name,inverse_cardinal,inverse_range)

    def define_calculated_list(self,name:str,range:str,formula:str,
                            inverse_name:Optional[str]=None) -> "Item":
        return self._prop_obj.define_calculated_list(name,range,formula,inverse_name)

    def move_first(self, item: "Item") -> None:
        from .Item import Item
        if isinstance(item, Item):
            _await_async((self._localdb[self._of_item._oid])._async_move_first(self._relation,item))
        else:
            msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(item), "etype":"'Item'"})

    def move_last(self, item: "Item") -> None:
        from .Item import Item
        if isinstance(item, Item):
            _await_async((self._localdb[self._of_item._oid])._async_move_last(self._relation,item))
        else:
            msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(item), "etype":"'Item'"})

    def move_next(self, item: "Item") -> None:
        from .Item import Item
        if isinstance(item, Item):
            _await_async((self._localdb[self._of_item._oid])._async_move_next(self._relation,item))
        else:
            msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(item), "etype":"'Item'"})

    def move_prev(self, item: "Item") -> None:
        from .Item import Item
        if isinstance(item, Item):
            _await_async((self._localdb[self._of_item._oid])._async_move_prev(self._relation,item))
        else:
            msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(item), "etype":"'Item'"})

    def move_before(self, item1: "Item", item2: "Item") -> None:
        from .Item import Item
        if isinstance(item1, Item):
            if isinstance(item2, Item):
                _await_async((self._localdb[self._of_item._oid])._async_move_before(self._relation, item1, item2))
            else:
                msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(item2), "etype":"'Item'"})
        else:
            msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(item1), "etype":"'Item'"})

    def move_after(self, item1: "Item", item2: "Item") -> None:
        from .Item import Item
        if isinstance(item1, Item):
            if isinstance(item2, Item):
                _await_async((self._localdb[self._of_item._oid])._async_move_after(self._relation, item1, item2))
            else:
                msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(item2), "etype":"'Item'"})
        else:
            msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(item1), "etype":"'Item'"})

    def move(self, item: "Item", position: "str", relative_to_item: "Optional[Item]"=None) -> None:
        from .Item import Item
        if isinstance(item, Item):
            if relative_to_item is None or isinstance(relative_to_item, Item):
                _await_async((self._localdb[self._of_item._oid])._async_move(self._relation, item, position, relative_to_item))
            else:
                msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(relative_to_item), "etype":"'Item'"})
        else:
            msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(item), "etype":"'Item'"})


    def append_before(self, item:  "typing.List[Item] | Item | List", relative_to_item:Optional["Item"]=None) -> None:
        from .Item import Item # putting this at the beginning creates a circular import
        before:bool=True
        if type(item) == Item:
            self.__append_item(item,before,relative_to_item)
        elif type(item) == typing.List[Item] or type(item) == List:
            self.__append_items(item,before,relative_to_item)
        else:
            msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(item), "etype":"'list[Item]', 'Item', 'List'"})

    def append_after(self, item:  "typing.List[Item] | Item | List", relative_to_item:Optional["Item"]=None) -> None:
        from .Item import Item # putting this at the beginning creates a circular import
        before:bool=False
        if type(item) == Item:
            self.__append_item(item,before,relative_to_item)
        elif type(item) == typing.List[Item] or type(item) == List:
            self.__append_items(item,before,relative_to_item)
        else:
            msg._tell_dev(msg.M523_argtype_mismatch__rtype_etype,{"rtype":type(item), "etype":"'list[Item]', 'Item', 'List'"})
