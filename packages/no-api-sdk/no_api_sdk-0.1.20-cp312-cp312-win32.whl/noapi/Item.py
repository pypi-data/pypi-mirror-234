# hey emacs mycoding: utf-8
# mypy: disallow-untyped-defs
# mypy: check-untyped-defs
# mypy: disallow-incomplete-defs

import logging
import sys
# import inspect
upython=False
if sys.implementation.name == "micropython":
    upython=True

if not upython:
    from decimal import Decimal

console = logging
# logging.basicConfig(filename='/tmp/noapipython.log',lxevel=logging.INFO)

from .Property import Property
from .Link import Link
from .List import List
from .Slice import Slice # type: ignore
from collections.abc import Iterator
from typing import Union, Any, Optional, Dict, TYPE_CHECKING, cast
import typing # to use typing.List
from typing_extensions import TypeAlias
from .msg import msg
from .datatypes import datatypes
import hashlib

if TYPE_CHECKING:
    from . import PropertyValue, Field, GetResult
    from . import noapi



PythonClass:TypeAlias = type # to distinguish python.type and Item.type

from .datanet import _encode_args2url # FIXME: this import should be removed, and formatting errors should be somewhere else

# import traceback

# TODO: add methods from https://docs.python.org/3/reference/datamodel.html

import asyncio
# from functools import partial

from .await_async import _await_async
import inspect

class Item(object):
    '''
    Item class
    '''

    def __init__(self, localdb: Dict[str,"Item"], oid: str, datastore: "noapi", internal : bool = False) -> None:
        if not internal:
            msg._tell_dev(msg.M519_called_class_constructor,{})
        self._oid = oid
        localdb[oid] = self
        self._localdb = localdb
        self._callbacks: Dict[str,Any] = {} # FIXME: instead of Any should be something like callable
        self._myfields: Dict[str,Field] = {}
        self._datastore = datastore

    def _get_item_by_id(self, oid: str) -> "Item":
        if oid in self._localdb:
            return self._localdb[oid]
        else:
            return Item(self._localdb, oid, self._datastore, True)

    __local_methods = [
        "_oid",
        "_localdb",
        "_datastore",
        "_myfields",
        "_updated",    "_callbacks",
        "find_in_list",
        "_find_in_list_by_propid",
        "_find_in_list_by_propstr",
        "_propstring_to_propid",
        "_propid_to_propstring",
        "_propstring_to_propid_of_list",
        "_get_by_propstr",
        "get","_forget"
        "__getattr__",
        "__getitem__",
        "__setitem__",
        "__setattr__",
        "set",
        "_async_set",
        "_async_get",
        "_async_get_impl",
        "keys",
        "_async_create",
        "define_range",
        "_refine_range",
        "_define_container",
        "define_property",
        "__define_property",
        "__define_subitem",
        "__define_link",
        "_define_property",
        "define_calculated_property",
        "__define_calculated_property",
        "define_calculated_link",
        "__define_calculated_link",
        "define_calculated_list",
        "__define_calculated_list",
        "_define_calculated_rel",
        "_define_relation",
        "new_link",
        "new_link_item",
        "new_subitem",
        "new_property",
        "new_property_value",
        "new_list",
        "new_list_item",
        "recall_field",
        "_recall_field",
        "call_method",
        "_call_method",
        "remove",
        "__repr__",
        "__str__",
        "destroy",
        "_deleted",
        "append",
        "_check_if_type",
        "on_update",
        "_call_callback",
        "_callbacks",
        "__iter__"  # Need to iterate through fields of this Item (used by vscode?)
    ]

    def __exception_on_future(future,result): # type: ignore # FIXME: add types
        if future is not None and (hasattr(future, "set_exception")):
            future.set_exception(result)
        else:
            future.exceptset(result) # FIXME: find what the real function is from micropython doc
        return result

    async def _await_future(future: Any) -> Any: # type : ignore # FIXME: add types
        tor = await future
        return tor

#        if (hasattr(future,"value") and callable(future.value)):
#            return future.value()
#        else:
#            return tor

    def __repr__(self) -> str:
        myhash = hashlib.shake_128(str(self._oid).encode()).hexdigest(3)
        if ("__name_f" in self._myfields):
            nameval = self._myfields["__name_f"]
            if nameval is None:
                namestr = "None"
                myhash = "-"+myhash
            else:
                namestr = f'{nameval.recall()}'
                myhash = "-"+myhash # show hash even with name, since different items may have same name

        else:
            # dont force recall of name, but use a hash
            namestr = "Name_not_retrieved-"
            myhash = myhash

        if ("__type__" in self._myfields):
            typeval= self.get("type")
            if type(typeval) is not Item:
                raise Exception("unexpected. type is not an Item")
            if ("__name_f" not in typeval._myfields):
            # case when name was not downloaded yet.
                typestr= "Type-"+hashlib.shake_128(str(typeval._oid).encode()).hexdigest(3)
            else:
                typestr = f'{typeval.get("name")}-' +hashlib.shake_128(str(typeval._oid).encode()).hexdigest(3)
        else:
            # force recall of type, but use a hash
            typestr = "Type_not_retrieved"

        tor = f"Item:{typestr}({namestr}{myhash})"
        return tor

    def __str__(self) -> str:
        name = str(self.get("name"))
        typea = self.get("type")
        if type(typea) is not Item:
            raise  Exception("unexpected. type is not an Item")
        typename = typea.get("name")
        if name is None or name=="None":
            name = "Name Unknown"
        tor = f"{typename}({name})"
        return tor

    async def async_get(self, key:str) -> "Field":
        tor = self.__getattr__(key)
        return tor

    async def _get_by_propstr (self, key: str) -> "Field":
        tor =  self.__getattr__(key)
        return tor

    def get(self, key:str) -> "Field":
        tor =  self.__getattr__(key)
        return tor

    async def _forget(self, key:str) -> None:
        console.debug("Forget property "+key)
        propid = await self._propstring_to_propid(key)
        if (propid in self._myfields):
            del self._myfields[propid]
            console.debug("DELETED property "+key)
        else:
            console.debug("Property not there to forget: "+key)


    def __getitem__(self, key:str) -> Any:
        return self.__getattr__(key)

    def __getattr__(self, key: str) -> Any:
        if key in Item.__local_methods:
            return object.__getattribute__(self,key)

        # ORIG GETATTR
        # loop = asyncio.get_event_loop()
        # resolve = Item._get_a_future()
        # loop.create_task(self._async_get(key, resolve))
        # return resolve

        # new GETATTR. Means this is a noapi property of item that needs to be looked up
        try:
            tor = _await_async(self._async_get_impl(key))
            return tor
        except KeyboardInterrupt as e:
            raise(e)
        except:
            raise

    async def _async_get(self, key:str, resolve:Any =None) -> "GetResult": # FIXME: resolve should have a type
        try:
            tor = await self._async_get_impl(key)
            if resolve:
                self._datastore._resolve_a_future(resolve,tor)

        except Exception as e:
            print(e)
            Item.__exception_on_future(resolve,e)
        return tor

    async def _async_get_impl(self, key:str) -> "GetResult":
        localref = await self._async_get_impl_no_recall(key)
        #if (
        #    (localref_class == Link)
        #    or (localref_class == List)
        #    or (localref_class == Property)
        #):
        if localref is None:
            return None
        else:
            return (cast("GetResult",localref.recall()))

    async def _async_get_impl_no_recall(self, key_in:str) -> "Field":
        oldkey = key_in
        key = await self._propstring_to_propid(key_in)

        if (key is None):
            # raise AttributeError('no property "'+oldkey+'" on '+str(self))
            msg._tell_dev(msg.M511_field_not_found_on_get__key_type_item,{"key":key_in, "item":str(self), "type":self.type})
            raise # to let type checker know that previous line generates an exception
        prevent_server_request = False
        # FIXME:  when we set self, all hell breaks loose
        # if (0 && (key in target) && ("requested" in target[key]))
        #   var prevent_server_request=true

        # oldkey = key
        # key = self.propstring_to_propid(key)

        # instead of self._localdb, use self to avoid infinite recurse
        #  localdb = object.__getattribute__(self,"_localdb")
        localdb = self._localdb
        if not (key in self._myfields or prevent_server_request):
            oid = self._oid
            console.debug("datastore")
            gotprop_fut = await self._datastore._request_fieldvalue_from_server(
                oid, key, prevent_server_request
            )
            try:
                gotprop = await gotprop_fut
                if issubclass(type(gotprop),msg.TellDevException    ):
                    msg._tell_dev(gotprop.e_msg,gotprop.e_args)
                    raise(gotprop)
                if issubclass(type(gotprop),Exception):
                    raise(gotprop)

            except msg.TellDevException as e:
                msg._tell_dev(e.e_msg,e.e_args)
            except Exception as e:
                raise e

            console.debug("GOT PROP FROM SERVER")
            console.debug(gotprop)

        localref = self._myfields[key]
        if localref == None:
            # TODO: self is probaby how to undefine a prop.
            # but for now, we just return.
            # later self should undefine the vale probably.
            return None

        console.debug(localref)
        # localref_class = type(localref)
        # if we get to a function its probably Item class function,
        # so return it.
        # TODO: carry self to sync verson of get. should be possible
        # if (typeof localref === 'function') {
        #    console.debug("returning function");
        #    return localref # was target???
        # }

        return localref

    async def _setProperty(self, propName:str, propType:str, propValue: "PropertyValue") -> None:
        #x print(f"_setPropertyX {self._oid}.{propName} ({propType})={propValue}")
        console.debug("_setPropertyX")
        console.debug(propName)
        console.debug(propType)
        console.debug(propValue)

        if propType == 'r-1' or propType == 'noi':
            if propName in self._myfields:
                r_1 : Field = self._myfields[propName]
                console.debug(r_1)
            else:
                dr_1 = Link(self._localdb, self, propName, True)
                r_1 = dr_1
                self._myfields[propName] = dr_1
                console.debug("r_1")
                # console.debug(r_1) - nodejs problem?

            # FIXME: this is a side effect of willy changes to types in define_relation
            if (type(r_1) == Link):
                cast(Link,r_1)._setRelation1(cast(str,propValue))
            else:
                raise Exception("IGNORING _setRelation1 as type mismatch")

            await self._updated(propName)


        elif propType == "r-n" or propType == "nol":
            if propName in self._myfields:
                r_n = self._myfields[propName]
            else:
                alocaldb = self._localdb
                toid = self._oid
                dr_n = List(alocaldb, self, propName, True)

                # python implementation works witout proxy class
                # r_n = new Proxy(dr_n,dr_n.proxy_handler())
                r_n = dr_n
            self._myfields[propName] = r_n
            # FIXME: this is a side effect of willy changes to types in define_relation
            if (type(r_n) == List):
                cast(List,r_n)._setRelationN(cast(str,propValue))
            else:
                raise Exception("IGNORING _setRelationN as type mismatch")
            await self._updated(propName)

            # self._myprops[propName] = new Proxy(new List(), list)
            # self._myprops[propName]._setRelationN(propValue)
            # callbacks should go here TODO
            # but we cannot send the whole list
            # so self needs some thought

        #elif propType == "mtd":
        #    console.debug("setproperty on a method was called")
        #    console.debug("SETPROP VAL-METHOD")
        #    console.debug(self)
        #    console.debug(propValue)
        #    # assume its a method kind of prop
        #    if propName in await self._myprops:
        #        dsmethodpropinstance = await self._myprops[propName]
        #    else:
        #        console.debug("METHOD NOT FOUND PROP IN OID")
        #        dsmethodpropinstance = dsmethodprop()
        #    console.debug("adding to oid")
        #    self._myprops[propName] = dsmethodpropinstance
        #    console.debug("added to oid")##
        #
        #    methodprop = dsmethodpropinstance
        #    # if method has changed
        #    # FIXME: how to compare functions? Assuming it has always changed!!
        #    # if (propertyinstance.valueOf() != propValue) {
        #    dsmethodpropinstance._setMethodName(propName)
        #    dsmethodpropinstance._setMethod(propValue)
        #    # updated(self,propName,propValue)

        elif (
            (propType == "str")
            or (propType == "num")
            or (propType == "bol")
            or (propType == "nos")
                or (propType == "non")
                or (propType == "nob")
                or (propType == "nod")
        ):
            console.debug("SETPROP VAL")
            console.debug(propName)
            console.debug(propValue)
            console.debug(self)

            # assume its a value kind of prop
            if propName in self._myfields:
                console.debug("FOUND PROP IN OID")
                field_instance = self._myfields[propName]
            else:
                console.debug("NOT FOUND PROP IN OID")
                field_instance = Property(True)
                console.debug("adding to oid")
                self._myfields[propName] = field_instance
                console.debug("added to oid")

            console.debug("Propertyinstance:")
            console.debug(field_instance)
            valprop = cast(Property,field_instance)
            if valprop._value_type != propType:
                valprop._setValueType(propType)

            if valprop.valueOf() != propValue:
                # if value has changed
                valprop._setValue(propValue)
                # valprop.updated(self._oid,propName,propValue)
                console.debug("UPDATED")
                await self._updated(propName)
            else:
                console.debug("NOTUPDATED")

        else:
            raise Exception("Unknown propType:" + propType)

        #x print(f"_setPropertyX {self._oid}.{propName} ({propType})={propValue} DONE")
    async def _deleted(self) -> None:
        alocaldb = self._localdb
        del alocaldb[self._oid]


    def on_update(self, prop:str, callback: Any) -> None: # FIXME: callback should be a function or async function
        prop = _await_async(self._propstring_to_propid(prop))
        if (not (prop in self._callbacks)):
            self._callbacks[prop] = []

        self._callbacks[prop].append(callback)

    async def _updated(self, key: str) -> None:
        # if there are no callbacks
        if not (key in (self._callbacks)):
            return

        # TODO: dont actually perform callbacks if the
        # updated value is the same as the existing value??
        #  I am guessing that self needs to be implemented
        # not here, but where self function is called from.
        ff = self._myfields[key]
        if ff is None:
            raise Exception("None encountered on _updated() callback")
        else:
            newvalue = ff.recall()
        for func in self._callbacks[key]:
            # loop = asyncio.get_event_loop()
            task = asyncio.create_task(self._call_callback(func,key,newvalue))

    async def _call_callback(self,func: Any, key: str, newvalue: "GetResult") -> None:
        # find the proxy to the item, so that
        # callbacks can use item.property to get at further properties
        proxytoObj = self._localdb[self._oid]
        propname = await self._propid_to_propstring(key)
        result = func(proxytoObj, propname, newvalue)
        # If the call back was defined async, then await it.
        if inspect.isawaitable(result):
            await result

    async def _propid_to_propstring(self, key: str) -> str:
        if (not (key in self._localdb)):
            propobj = Item(self._localdb, key, self._datastore, True)
        else:
            propobj = self._localdb[key]

        propstring = await propobj._async_get('name')
        if type(propstring) == Property or type(propstring) == str:
            return str(cast(Property,propstring))
        else:
            raise Exception(f"name of property {key} was not a string. {propstring=} with type = {type(propstring)}")
        return propstring

    async def _propstring_to_propid(self, key:str) -> Optional[str]:
        console.debug("propstrintoprpoid starting:")
        console.debug(key)
        # check harcoded keys.. type and fields, name
        if key in self._datastore.well_known_propids:
            tor = self._datastore.well_known_propids[key]
        else:
            console.debug("propstringtopropid lookuptype:")
            typeo: Item = cast(Item,await self._get_by_propstr("type"))
            console.debug("propstringtopropid lookup field:")
            console.debug(typeo)
            if typeo is None:
                raise Exception(f"?? type of Item is None while looking up {key=}.  Item is: "+self._oid)
            field = await typeo._find_in_list_by_propstr("fields", key, None)
            if field is None:
                return None
            console.debug("propstrintoprpoid finds:")
            console.debug(field)
            tor = field._oid
        return tor

    async def _propstring_to_propid_of_list(self, listid:str, key:str) -> str:
        console.debug("propstrintoprpoid starting:")
        console.debug(key)
        # check harcoded keys.. type and fields
        if key == "type":
            key = self._datastore.well_known_propids["type"]

        elif key == "fields":
            key = self._datastore.well_known_propids["fields"]
        else:
            console.debug("propstringtopropid lookuptype:")
            getf = self.get
            typeoa = getf("type")
            typeo = typeoa
            console.debug("propstringtopropid lookup field:")
            console.debug(typeo)
            if (listid not in self._localdb):
                self._localdb[listid] = Item(self._localdb, listid, self._datastore, True)

            listfield = self._localdb[listid]
            # is the listfield is also type, NO!
            type_from_listfield = (listfield.otherside).oftype
            field_item = await type_from_listfield._find_in_list_by_propstr("fields", key)
            console.debug("propstrintoprpoid finds:")
            console.debug(field_item)
            if field_item is None:
                raise KeyError(key)

            key = field_item._oid
        return key

    # deprecated
    # def find_in_list(self, listprop:str, search_for:Union[str,"Item"], in_field:Optional[str]=None) -> Optional["Item"]:
    # return _await_async(self._find_in_list_by_propstr(listprop, search_for, in_field))

    async def _find_in_list_by_propstr(self, listprop:str, search_for:Union[str,"Item"],
                                        in_field:Optional[str]=None
                                        ) -> Optional["Item"]:
        try:
            listpropid = await self._propstring_to_propid(listprop)
        except KeyError:

            raise # FIXME: use numbered exception similar to m529
        if (listpropid is None):
            raise Exception("Could not find property:"+listprop)
        if (in_field is not None):
            try:
                in_fieldid = await self._propstring_to_propid_of_list(listpropid,in_field) # FIXME: use numbered exception similar to m529
            except KeyError:
                raise # FIXME: use msg._tell_dev(msg.M529_field_not_found_on_find__key_type_list_item,{"key":in_field,"type":XXX})
        else:
            in_fieldid = None

        return self._find_in_list_by_propid(listpropid, search_for, in_fieldid)

    def _find_in_list_by_propid(self, listpropid: str, search_for: Union[str,"Item"], in_fieldid: Optional[str]=None) -> Optional["Item"]:
        if (in_fieldid is None):
            in_fieldid='00000000' # hardcoded.DICT_LOOKUP_DEFAULTID
        datastore = self._datastore
        cachekey = self._oid + "." + listpropid + "S" + in_fieldid+str(search_for)
        myoid = self._oid
        localdb = self._localdb
        if cachekey in localdb:  # has been searched before and is in the cache
            propobj = localdb[cachekey]
            # TODO: the following code was removed, did it break anythin?
            # if (not (propitem in localdb)): # if the item is not in the cache
            #     propobj = Item(localdb, propid, self._datastore)
            # else:
            #    propobj = localdb[propid]
            return propobj

        if (type(search_for) ==Item): # if item, send its oid instead.
            search_for = cast(Item,search_for)._oid

        console.debug("CALLING find from server")
        found_item_id = _await_async(datastore._request_find_from_server(
            myoid, listpropid, str(search_for), in_fieldid
        ))
        console.debug("RESOLVED find from server")
        console.debug(found_item_id)
        if found_item_id == None:
            return None

        try:
            # obj does not exists in localdb, so lets create it
            if not (found_item_id in localdb):
                console.debug("CREATED NEWOBJ")
                newobj = Item(localdb, found_item_id, self._datastore, True)
                localdb[found_item_id] = newobj
            else:
                newobj = localdb[found_item_id]
            #  FIXME: cache removal is not done!
            localdb[cachekey] = newobj
        except:
            return None

        return newobj

    def __setitem__(self, key:str, newvalue:"PropertyValue") -> None:
        self.__setattr__(key, newvalue)

    def __setattr__(self, key:str, newvalue:"PropertyValue") -> None:
        if key in Item.__local_methods:
            object.__setattr__(self, key, newvalue)
        else:
            _await_async(self._async_set(key,newvalue))

#        loop = asyncio.get_event_loop()
#        resolve = Item._get_a_future()

#        # loop.create_task(task2set(self,key,newvalue,resolve))
#        loop.create_task(self._async_set(key, newvalue, resolve))
#        return resolve
#         return se

    # WAS loop.create_task(self._async_set(key, newvalue, resolve))

    #async def async_set(self, key:str, newvalue:"PropertyValue") -> None:
    #    loop = asyncio.get_event_loop()
    #    resolve = Item.get_a_future()
    #   loop.create_task(self._async_set(key, newvalue, resolve))
    #    # tor = await resolve #
    #    tor = await Item._await_future(resolve)
    #    return tor

    def set_nowait(self, key:str, newvalue: "Item|PropertyValue") -> None:
        asyncio.ensure_future(self._async_set(key,newvalue))

    def set(self, key:str, newvalue: "Item|PropertyValue") -> None:
        _await_async(self._async_set(key,newvalue))

    async def _async_set(self, key:str, newvalue:"Item|PropertyValue", resolve: Any =None) -> None: # FIXME: what is type of resolve?
        datatype: Optional[str]
        try:
            propid = await self._propstring_to_propid(key)
            if propid is None:
                msg._tell_dev(msg.M512_field_not_found_on_set__key_type_item,{
                    "key":key, "item":str(self), "type":self.type
                })

            if (propid not in self._myfields):
                await  self._async_get_impl_no_recall(key)
            if (propid not in self._myfields):
                raise Exception("cannot set/get field:"+key)

            pyclasstype = type(self._myfields[propid])

            if pyclasstype==List:
                # FIXME: this is used by define_subitem/relation
                # so commented for now...
                raise Exception("cannot use set on a list")
                datatype="r-n"
                pass
            elif pyclasstype==Link:
                newvalue_type = type(newvalue)
                datatype = datatypes.LINK
                if newvalue_type == Item:
                    console.debug("setting new value as Item")
                    newvalue = cast(Item,newvalue)._oid
                elif newvalue is None:
                    datatype = datatypes.NO_LINK
                else:
                    msg._tell_dev(msg.M522_set_invalid_type__field_key_rtype_etype,
                                {"field": str(pyclasstype),"key": key,"rtype": str(newvalue_type), "etype":"Item | null"})
            elif pyclasstype==Property:
                thevalprop = cast(Property,self._myfields[propid])
                if thevalprop is None:
                    datatype = None
                else:
                    datatype = thevalprop._value_type
                if datatype=="num" or datatype=="non":
                    datatype="num"
                    if not upython:
                        if (not isinstance(newvalue, (int, float, complex, Decimal)) and not isinstance(newvalue, bool)):
                            raise Exception("must set a num value from a python int, float, complex or Decimal type, but the value used was:"+ str(type(newvalue)))
                    else: # micropython, which does not have Decimal
                        if (not isinstance(newvalue, (int, float, complex)) and not isinstance(newvalue, bool)):
                            raise Exception("must set a num value from a micopython int, float, or complex type, but the value used was:"+ str(type(newvalue)))

                elif datatype=="str" or datatype=="nos":
                    datatype="str"
                    if (not isinstance(newvalue,str)):
                        raise Exception("must set a str value from a python str type, but the value used was:"+ str(type(newvalue)))
                elif datatype=="bol" or datatype=="nob":
                    datatype="bol"
                    if (type(newvalue) != bool):
                        raise Exception("must set a bol value from a python bool, , but the value used was:"+ str(type(newvalue)))
                    newvalue = str(newvalue).lower()

                # elif datatype=="dat" or datatype=="nod":
                else:
                    raise Exception("Unknown value type of "+str(key))
            else:
                raise Exception("Unknown field type of "+str(key))

            alocaldb = self._localdb
            datastore = self._datastore

            set_result = await datastore._set_field_on_server(
                self._oid, propid, newvalue, datatype)

            console.debug("set_prop_on_server returns")
            console.debug(set_result)
            # TODO: was following code needed?
            #if pyclasstype==Link:
            #        if not (set_result in alocaldb):
            #            console.debug("Creating a new Item")
            #            console.debug(Item)
            #            newobj = Item(alocaldb, set_result, self._datastore)
            #        else:
            #            console.debug("Item already in localdb")

        except:
            console.error("APP-SET-ERROR")
            import traceback
            traceback.print_exc(file=sys.stdout)
            raise

    async def _async_append(self, propid:str, item:"Item",before:bool,relative_to_item:Optional["Item"]) -> "Item":
        try:
            newvalue_type = type(item)
            if (newvalue_type != Item):
                raise Exception("append can only append one item, but got:"+str(newvalue_type))
                console.debug("setting new value as Item")

            alocaldb = self._localdb
            datastore = self._datastore
            relative_to_item_str: Optional[str] = None
            if relative_to_item is not None:
                relative_to_item_str = relative_to_item._oid

            new_oid = await datastore._append_on_server(
                self._oid, propid, item._oid, before, relative_to_item_str
            )
            return self

        except Exception as e:
            raise e

    def create(self, key:Optional[str]=None) -> "Item":
        msg._tell_dev(msg.M528_method_removed__method_replacement,{'method':'create','replacement':'create_subitem or list.create'})
        raise # as previous line already raises an exception

    # FIXME: need to also allow python dict as argument to set many of its properties.
    def create_subitem(self, key:str, set_value: Optional["PropertyValue"]=None, on_property:Optional[str]=None) -> "Item":
        propid = _await_async(self._propstring_to_propid(key))
        if propid is None:
            raise Exception("did not find a property named:"+str(key))
        propid2 = cast(str,propid)
        return _await_async(self._async_create(propid2, set_value, on_property))

    def destroy_subitem(self, containername:str, item:"Item") -> None:
        boxid = _await_async(self._propstring_to_propid(containername))
        if boxid is None:
            raise Exception("did not find a property named:"+containername)
        if type(item) != Item:
            raise Exception("only an item can be destroyed")
        return _await_async(self._async_destroy(boxid, item._oid))

    async def _async_destroy(self, boxid:str, itemid:str) -> None:
        try:
            loop = asyncio.get_event_loop()

            alocaldb = self._localdb
            datastore = self._datastore
            result = await datastore._destroy_on_server(
                self._oid, boxid, itemid)

            print(type(result))
            raise Exception("fix next line based on type(result)")
            if (type(result) == Exception):
                raise result

            return result

        except:
            console.error("DESTROY-ERROR")
            import traceback
            traceback.print_exc(file=sys.stdout)
            raise

    async def _async_remove(self, listid:str, itemid:str) -> None:
        try:
            loop = asyncio.get_event_loop()

            alocaldb = self._localdb
            datastore = self._datastore
            result = await datastore._remove_on_server(
                self._oid, listid, itemid)

            if (type(result) == Exception):
                raise result

            return result

        except:
            console.error("REMOVE-ERROR")
            import traceback
            traceback.print_exc(file=sys.stdout)
            raise


    async def _async_create(self, propid:str, new_value: "Union[Item|PropertyValue]", set_prop_name:Optional[str]) -> "Item":
        try:
            datatype = "str"

            # to set r_1, we do target.prop=newvalue,
            # but value is the item that we want to set it to.
            # so, we should pass the oid of the item to server
            if type(new_value) is Item:
                console.debug("setting new value as Item")
                new_value = new_value._oid
                datatype = "r-1"

            alocaldb = self._localdb
            datastore = self._datastore
            loop = asyncio.get_event_loop()

            new_oid = await datastore._create_on_server(
                # FIXME: should pass data here, not different call
                # self._oid,propid, newvalue, newprop
                self._oid,propid, None, None
            )

            alocaldb[new_oid] = Item(alocaldb, new_oid, self._datastore, True)

            # FIXME:This should really happen on the server.
            if new_value:
                if set_prop_name is None:
                    set_prop_name = "name"

                # FIXME: should use a private function
                alocaldb[new_oid].set(set_prop_name,new_value)
            await Slice._updated(alocaldb[new_oid])
            return alocaldb[new_oid]

        except:
            console.error("APP-CREATE-ERROR")
            import traceback
            traceback.print_exc(file=sys.stdout)
            raise

    #def keys(self) -> typing.List[str]:
    def keys(self) -> None: # FIXME
        '''
        keys - returns keys of item
        '''

        raise Exception("Not Implemented Yet")

    def call_method(self,name:str, args: Dict[str,Optional[str]]={}) -> Dict[str,Optional[str]]:
        return _await_async(self._call_method(name, args))

    async def _call_method(self,name:str,args: Dict[str,Optional[str]]) -> Dict[str,Optional[str]]:
        method_result = await self._datastore._call_method_on_server(
            self._oid, name, args)
        return method_result

    async def __define_subitem(self,name:str,
                    inverse_name_in:Optional[str]) -> "Item":
        reply = await self._call_method("define_subitem", {"name":name, "inverse_name":inverse_name_in})
        if "Item" not in reply or reply["Item"] is None:
            msg._tell_dev(msg.M711_unexpected_exception__exception,{"exception":str(reply)})
            raise # to let type checker know that previous line will raise an exception
        return self._get_item_by_id(reply["Item"])

    async def __define_link(self,name:str,range:Optional[str],
                    inverse_name_in:Optional[str],inverse_cardinal:Optional[str],inverse_range:Optional[str]) -> "Item":
        reply = await self._call_method("define_link", {"name":name, "range":range,"inverse_name":inverse_name_in, "inverse_cardinal":inverse_cardinal, "inverse_range":inverse_range})
        if "Item" not in reply or reply["Item"] is None:
            msg._tell_dev(msg.M711_unexpected_exception__exception,{"exception":str(reply)})
            raise # to let type checker know that previous line will raise an exception
        return self._get_item_by_id(reply["Item"])

    async def __define_list(self,name:str,range:Optional[str],
                    inverse_name_in:Optional[str],inverse_cardinal:Optional[str],inverse_range:Optional[str]) -> "Item":
        reply = await self._call_method("define_list", {"name":name, "range":range,"inverse_name":inverse_name_in, "inverse_cardinal":inverse_cardinal, "inverse_range":inverse_range})
        if "Item" not in reply or reply["Item"] is None:
            msg._tell_dev(msg.M711_unexpected_exception__exception,{"exception":str(reply)})
            raise # to let type checker know that previous line will raise an exception
        return self._get_item_by_id(reply["Item"])

    async def __define_list_of_links(self,name:str,range:Optional[str],
                    inverse_name_in:Optional[str],inverse_cardinal:Optional[str],inverse_range:Optional[str]) -> "Item":
        reply = await self._call_method("define_list_of_links", {"name":name, "range":range,"inverse_name":inverse_name_in, "inverse_cardinal":inverse_cardinal, "inverse_range":inverse_range})
        if "Item" not in reply or reply["Item"] is None:
            msg._tell_dev(msg.M711_unexpected_exception__exception,{"exception":str(reply)})
            raise # to let type checker know that previous line will raise an exception
        return self._get_item_by_id(reply["Item"])


    async def __define_list_of_items(self,name:str,
                    inverse_name_in:Optional[str]) -> "Item":
        reply = await self._call_method("define_list_of_items", {"name":name, "inverse_name":inverse_name_in})
        if "Item" not in reply or reply["Item"] is None:
            msg._tell_dev(msg.M711_unexpected_exception__exception,{"exception":str(reply)})
            raise # to let type checker know that previous line will raise an exception
        return self._get_item_by_id(reply["Item"])

    async def __define_calculated_property(self,name:str, datatype: str,
                    formula:str) -> "Item":
        reply = await self._call_method("define_calculated_property", {"name":name, "formula":formula,"datatype":datatype})
        if "Item" not in reply or reply["Item"] is None:
            msg._tell_dev(msg.M711_unexpected_exception__exception,{"exception":str(reply)})
            raise # to let type checker know that previous line will raise an exception
        return self._get_item_by_id(reply["Item"])

    async def __define_calculated_link(self,name:str,range:Optional[str],
                    formula:str, inverse_name:Optional[str]) -> "Item":
        reply = await self._call_method("define_calculated_link", {"name":name, "range":range,"formula":formula,"inverse_name":inverse_name})
        if "Item" not in reply or reply["Item"] is None:
            msg._tell_dev(msg.M711_unexpected_exception__exception,{"exception":str(reply)})
            raise # to let type checker know that previous line will raise an exception
        return self._get_item_by_id(reply["Item"])

    async def __define_calculated_list(self,name:str,range:Optional[str],
                    formula:str, inverse_name:Optional[str]) -> "Item":
        reply = await self._call_method("define_calculated_list", {"name":name, "range":range,"formula":formula,"inverse_name":inverse_name})
        if "Item" not in reply or reply["Item"] is None:
            msg._tell_dev(msg.M711_unexpected_exception__exception,{"exception":str(reply)})
            raise # to let type checker know that previous line will raise an exception
        return self._get_item_by_id(reply["Item"])

    async def _check_if_type(self) -> "Item":
        # console.debug("Checking: "+self._oid)
        # console.debug(await self.name)
        iam = self
        mytype =  await iam._get_by_propstr("type")
        if type(mytype) is not Item:
            raise Exception("Unexcepted type for mytye")
        mytypename = await mytype._get_by_propstr("name")
        # Check if I am a type; if not try to walk to the type by
        # using oftype of the otherside, so that we can chain
        # define link/list/box/container calls.
        if (mytypename != "type"):
            if ((mytype._oid == "__link__") or (mytype._oid == "__list__")):
                console.debug("Link Or LIST!")
                otherside = self.otherside
                console.debug("otherside is:"+str(otherside))
                oftype = otherside.oftype
                console.debug("otherside oftype is:"+str(oftype))
                iam = oftype
                console.debug("walked to:"+iam._oid)
                mytypename = ((iam.type).name)
                console.debug(mytypename)
            else:
                newiam  =  await iam._get_by_propstr("type")
                if type(newiam) is not Item:
                    raise Exception("Unexcepted python type for newiam")
                iam = newiam
                newiamtype = cast(Item,newiam).type
                mytypename = await newiamtype._get_by_propstr("name")

        if (mytypename != "type"):
            print(mytypename)
            raise Exception("Could not find type")

        return iam

    def define_property(self,name:str,proptype:Union[str,PythonClass,None]=None) -> "Item":
        return _await_async(self.__define_property(name,proptype))

    async def __define_property(self,name:str,proptype:Union[str,PythonClass,None]) -> "Item":
        python_class: Optional[str] = None
        if type(proptype) == PythonClass and isinstance(proptype,type):
            python_class = str(proptype)
            proptype = None
        elif proptype is None:
            pass
        else:
            proptype = str(proptype)
        reply = await self._call_method("define_property", {"name":name, "datatype":proptype, "python_class":python_class })
        if "Item" not in reply or reply["Item"] is None:
            msg._tell_dev(msg.M711_unexpected_exception__exception,{"exception":str(reply)})
            raise # to let type checker know that previous line will raise an exception
        return self._get_item_by_id(reply["Item"])

    async def _define_calculated_property(self,name:str,proptype:str,
                                    formula:str) -> "Item":
        reply = await self._call_method("define_calculated_property", {"name":name, "datatype":proptype, "formula":formula})
        if "Item" not in reply or reply["Item"] is None:
            msg._tell_dev(msg.M711_unexpected_exception__exception,{"exception":str(reply)})
            raise # to let type checker know that previous line will raise an exception
        return self._get_item_by_id(reply["Item"])

    def define_calculated_property(self,name:str,proptype:str,
                                    formula:str) -> "Item":
        return _await_async(
                    self.__define_calculated_property(name,proptype,formula))

    def define_calculated_list(self,name:str,range:str,formula:str,
                            inverse_name:Optional[str]=None) -> "Item":
        return _await_async(self.__define_calculated_list(name,range,formula,inverse_name))

    def define_calculated_link(self,name:str,range:str,formula:str,
                            inverse_name:Optional[str]=None) -> "Item":
        return _await_async(self.__define_calculated_link(name,range,formula,inverse_name))

    def recall_field(self,name:str )-> Optional["Item"]:
        return _await_async(self._recall_field(name))

    async def _recall_field(self,name:str) -> Optional["Item"]:
        mytype = await self._check_if_type()
        field = await mytype._find_in_list_by_propstr("fields",name)
        return field

    def new_subitem(self,link_name:str,inverse_name:Optional[str]=None) -> None:
        """
        new_subitem - defines and creates a new subitem
        .. deprecated:: use :py:meth:`noapi_ref.Item.define_subitem` instead
        """
        msg._tell_dev(msg.M412_method_deprecated__method_replacement,{"method":"new_subitem","replacement":"define_subitem then create_subitem"})

    def destroy(**args) -> None:
        """
        deprecated - use destroy_subitem
        .. deprecated:: use :py:meth:`noapi_ref.Item.destroy_subitem` instead
        """
        msg._tell_dev(msg.M412_method_deprecated__method_replacement,{"method":"destroy","replacement":"destroy_subitem"})


    async def _destroy_locally(self,**args: Dict[str, Any]) -> None: # called from __init__
        raise NotImplementedError()

    def define_subitem(self,link_name:str,
                inverse_name:Optional[str]=None) -> "Item":
        """ implements: :py:meth:`noapi_ref.Item.define_subitem` """
        new_link = _await_async (self.__define_subitem(link_name,inverse_name))
        return new_link

    def define_link(self,link_name:str,range:Optional[str]=None,
                inverse_name:Optional[str]=None,inverse_cardinal:Optional[str]=None,inverse_range:Optional[str]=None) -> "Item":
        """ implements: :py:meth:`noapi_ref.Item.define_link` """
        new_link = _await_async (self.__define_link(link_name,range,inverse_name,inverse_cardinal,inverse_range))
        return new_link

    def define_list(self,list_name:str,range:Optional[str]=None,
        inverse_name:Optional[str]=None,inverse_cardinal:Optional[str]=None,inverse_range:Optional[str]=None) -> "Item":
        """ implements: :py:meth:`noapi_ref.Item.define_list` """
        new_list = _await_async (self.__define_list(list_name,range,inverse_name,inverse_cardinal,inverse_range))
        return new_list

    def define_list_of_links(self,list_name:str,range:Optional[str]=None,
                            inverse_name:Optional[str]=None,inverse_cardinal:Optional[str]=None,inverse_range:Optional[str]=None) -> "Item":
        new_list = _await_async (self.__define_list_of_links(list_name,range,inverse_name,inverse_cardinal,inverse_range))
        return new_list

    def define_list_of_items(self,name:str,
            inverse_name:Optional[str]=None) -> "Item":
        """ implements: :py:meth:`noapi_ref.Item.new_list` """
        return _await_async(self.__define_list_of_items(name,inverse_name))

    def __iter__(self) -> None:
        # FIXME: return an iterator that can be used to iterate through fields of this item
        msg._tell_dev(msg.M521_item_not_iterable__item,{"item":str(self)})

    async def _async_move_first(self, propid:str, item:"Item") -> "Item":
        try:
            reply = await self._call_method(
                "move_first", {"oid": self._oid, "listid":propid, "target":item._oid})
            return self
        except Exception as e:
            raise e

    async def _async_move_last(self, propid:str, item:"Item") -> "Item":
        try:
            reply = await self._call_method(
                "move_last", {"oid": self._oid, "listid":propid, "target":item._oid})
            return self
        except Exception as e:
            raise e

    async def _async_move_prev(self, propid:str, item:"Item") -> "Item":
        try:
            reply = await self._call_method(
                "move_prev", {"oid": self._oid, "listid":propid, "target":item._oid})
            return self
        except Exception as e:
            raise e

    async def _async_move_next(self, propid:str, item:"Item") -> "Item":
        try:
            reply = await self._call_method(
                "move_next", {"oid": self._oid, "listid":propid, "target":item._oid})
            return self
        except Exception as e:
            raise e

    async def _async_move_before(self, propid:str, item1: "Item", item2: "Item") -> "Item":
        try:
            reply = await self._call_method(
                "move_before", {"oid": self._oid, "listid":propid, "target":item1._oid, "relative_to_item":item2._oid})
            return self
        except Exception as e:
            raise e

    async def _async_move_after(self, propid:str, item1: "Item", item2: "Item") -> "Item":
        try:
            reply = await self._call_method(
                "move_after", {"oid": self._oid, "listid":propid, "target":item1._oid, "relative_to_item":item2._oid})
            return self
        except Exception as e:
            raise e

    async def _async_move(self, propid:str, item1: "Item", position: str, item2: "Optional[Item]") -> "Item":
        try:
            if item2 is None:
                item2_oid = None
            else:
                item2_oid = item2._oid
            reply = await self._call_method(
                "move", {"oid": self._oid, "listid":propid, "target":item1._oid, "position":position, "relative_to_item":item2_oid})
            return self
        except Exception as e:
            raise e
