# emacs coding: utf-8
# mypy: disallow-untyped-defs
# mypy: disallow-untyped-defs
# mypy: check-untyped-defs
# mypy: disallow-incomplete-defs

# Levels
F = "F" # Fatal
C = "C" # Critical
E = "E" # Error
W = "W" # Warning
N = "N" # Notice
I = "I" # Info
D= "D" # Debug
T= "T" # Trace

all_levels = [F, C, E, W, N, I, D, T]

import logging
import warnings
from enum import Enum
from typing import Dict, Any, TYPE_CHECKING, Optional
from typing import List as TypingList

from typing_extensions import TypeAlias
import sys, types

if TYPE_CHECKING:
    MsgTuple : TypeAlias = "tuple[str,str,type[Exception], str,str]" # type: ignore

class msg(BaseException): # client generated messages. For server messages, see smsg.py

    # Fields: constant to refer to this messages, Level, Code,  Python Class,       Short description, Long description with variables
    # ------------------------------------------  -----  -----  -------------        ----------------- -----------------
    M311_nonetype_recall__fname_line              = ( W, "311", Warning,            "None was seen earlier", "None was seen earlier during a datastore operation in file '{fname}', line {lineno}")
    # warnings
    # ------------------------------------------  -----  -----  -------------        ----------------- -----------------
    M411_sdk_version_deprecated__version =          ( W, "411", DeprecationWarning, "SDK version deprecated, upgrade to newer version", "SDK version '{version}' has been deprecated, it will not be supported in the future" )
    M412_method_deprecated__method_replacement =    ( W, "412", DeprecationWarning, "Method deprecated", "Method '{method}' has been deprecated. Possible replacement: {replacement} " )
    M413_want_oftypelist_not_typelist__list =       ( W, "413", UserWarning,        "Did you mean to access list.type_of", "Did you want to find out which type list '{list}' belongs to. If so, you should be using '{list}.of_type' instead." )
    # errors
    # ------------------------------------------  -----  -----  -------------        ----------------- -----------------
    M511_field_not_found_on_get__key_type_item =    ( E, "511", AttributeError,     "Field not found on get", "Field '{key}' not found on type '{type}' while trying to get a field on item '{item}'" )
    M512_field_not_found_on_set__key_type_item =    ( E, "512", AttributeError,     "Field not found on set", "Field '{key}' not found on type '{type}' while trying to set a field on item '{item}'" )
    M513_method_removed__method_replacement =       ( E, "513", AttributeError,     "Method removed", "Method '{method}' has been removed. Possible replacement: {replacement} " )
    M514_create_called_on_relation__field =         ( E, "514", AttributeError,     "Create called without an Item", "Create has been called on the definition of field '{field}' without knowing which item it belongs to. Please use it as item.create('{field}') with the item on which you would like to create a new item" )
    M515_create_called_on_value__property =         ( E, "515", AttributeError,     "Create called on a property field", "Create has been called on the definition of property '{property}'. create() is used to create a new Item. Properties already exist when an item is created. Did you mean to call item.create('list_name')" )
    M516_create_called_without_a_list =             ( E, "516", AttributeError,     "Create called without a list/link name", "Create called without a list/link name. create(list_or_subitem_name) is used to create a new Item on that list, or a subitem. Did you forget list_name parameter to item.create('list_name')" )
    M517_create_called_on_type__type_container =    ( E, "517", AttributeError,     "Create called on a type", "Create has been called on type '{type}'. item.create(list_name) is used to create a new item on a list. Did you mean to call item.create('{container}') to create a new {type}" )
    M518_listnotfound_append__key_type_item_item2 = ( E, "518", AttributeError,      "Field not found during append", "List '{key}' not found on type '{type}' while trying to append item  '{item2}' to a list on item '{item}'" )
    M519_called_class_constructor =                 ( E, "519", AttributeError,     "Constructor call not allowed", "Calling no-api constructors directly is not allowed. Please follow links and lists from the start item to get to the Item/List/Property you want")
    M520_item_not_found_in_list__key_item_list =    ( E, "520", KeyError,           "Item not found", "An item with '{key}' as a search key was not found in the list '{item}.{list}'" )
    M521_item_not_iterable__item               =    ( E, "521", TypeError,          "Items are not iterable", "Items can not be iterated over (used as a list) while trying to do so with item '{item}'" )
    M522_set_invalid_type__field_key_rtype_etype =  ( E, "522", TypeError,          "Invalid field type on set", "Setting the {field} '{key}' with a value of type '{rtype}' is not valid. {field}s can only be set to values of type {etype}" )
    M523_argtype_mismatch__rtype_etype =            ( E, "523", TypeError,          "Invalid argument", "An inappropriate argument is passed to the function. Received '{rtype}' while expecting {etype}" )
    M524_missing_property_value__listname_propname= ( E, "524", AttributeError,     "Missing property value", "Create has been called on list '{listname}' without providing a value for the property '{propname}'" )
    M525_appending_existing_items__list_items     = ( E, "525", RuntimeError,       "Impossible to append", "One or more append operations failed due to item(s) already existing in list : '{listname}'. Items that caused the error : {items}" )
    M526_legacy_error                             = ( E, "526", RuntimeError,       "Legacy Error", "An error was received from the server without an explicit error code" )
    M527_unknown_datatype_from_server             = ( E, "527", RuntimeError,       "Unknown datatype from server", "An unknown datatype was received from the server, which usually indicates that there was an unexpected error in the server" )
    M528_method_removed__method_replacement       = ( E, "528", AttributeError,     "Method removed", "Method '{method}' has been removed from noapi. Possible replacement: {replacement} " )
    M529_fieldnotfound_find__key_type_list_item   = ( E, "529", AttributeError,     "Field not found during find", "Field '{key}' not found on type '{type}' while trying to find an item  in '{item}.{list}' whose '{key}' field is being searched" )
    M530_nonetype_attributeerror__orig_fname_line = ( E, "530", AttributeError,     "'NoneType' object has no attribute", "{orig}. Maybe caused by None result in file '{fname}', line {lineno}")
    M531_nonetype_typeerror__orig_fname_line      = ( E, "531", TypeError,          "'NoneType' object error", "{orig}. Maybe caused by a None result seen earlier during the execution in file '{fname}', line {lineno}")

    # critical
    # ------------------------------------------  -----  -----  -------------        ----------------- -----------------
    M711_unexpected_exception__exception =          ( C, "711", Exception,           "Unexpected exception", "Unexpected exception '{exception}'" )

    # fatal
    # ------------------------------------------  -----  -----  -------------        ----------------- -----------------
    M811_server_timeout__url =                      ( F, "811", ConnectionError,     "Server timeout", "Server timeout on url '{url}'" )
    M812_server_invalid_url__url =                  ( F, "812", ConnectionError,     "Server invalid url", "Server invalid url '{url}'" )
    M813_connection_error__url =                    ( F, "813", ConnectionError,     "Connection error", "Connection error on url '{url}'" )
    M814_invalid_handshake__url =                   ( F, "814", ConnectionError,     "Invalid handshake", "Invalid handshake on url '{url}'" )
    M815_oserr_connection_error__errno_url =        ( F, "815", ConnectionError,     "OSError connection error", "OS error '{errno}' on url '{url}'" )

    _REMOVE_FROM_STACK = [ r"nest_asyncio.py",
            r"asyncio/__main__.py",       r"asyncio\__main__.py",
            r"asyncio/base_events.py",    r"asyncio\base_events.py",
            r"asyncio/events.py",         r"asyncio\events.py",
            r"asyncio/futures.py",        r"asyncio\futures.py",
            r"asyncio/proactor_events.py",r"asyncio\proactor_events.py",
            r"asyncio/sslproto.py",       r"asyncio\sslproto.py",
            r"asyncio/tasks.py",          r"asyncio\tasks.py",
            r"asyncio/windows_events.py", r"asyncio\windows_events.py",
            r"futures/_base.py",          r"futures\_base.py",
            r"legacy/protocol.py",        r"legacy\protocol.py",
            r"noapi/__init__.py",         r"noapi\__init__.py",
            r"noapi/__main__.py",         r"noapi\__main__.py",
            r"noapi/await_async.py",      r"noapi\await_async.py",
            r"noapi/Item.py" ,            r"noapi\Item.py",
            r"noapi/Link.py",             r"noapi\Link.py",
            r"noapi/List.py",             r"noapi\List.py",
            r"noapi/msg.py",              r"noapi\msg.py",
            r"noapi/Slice.py",            r"noapi\Slice.py",
            r"noapi/Property.py",         r"noapi\Property.py",
            r"noapi/datanet.py",          r"noapi\datanet.py",
            r"<frozen runpy>", r"<frozen noapi.await_async>", r"<frozen noapi>",
            r"<frozen noapi.Item>" , r"<frozen noapi.Link>", r"<frozen noapi.List>",
            r"<frozen noapi.msg>", r"<frozen noapi.Property>", r"<frozen noapi.datanet>",
            r"<frozen noapi.Slice>", r"<frozen noapi.msg>"
    ]

    # class variables:
    unknown_encountered_filename : Optional[str] = None
    unknown_encountered_lineno : Optional[int] = None

    @staticmethod
    def _tell_dev(message: "MsgTuple", message_args: Dict[str,Any],prevent_raise:bool=False,from_e:Optional[Exception]=None) -> None:
        error_code="M???"
        short_desc_message="Error message missing, please inform"
        long_desc_message="Long error messsage missing, please inform"
        python_class : type
        level="W"
        try: # in case there is some problem with error descriptions
            (level, error_code, python_class,short_desc_template, long_desc_template) = message
            short_desc_message = level+error_code+"-"+short_desc_template+"."
            long_desc_message = short_desc_message + " "+long_desc_template.format(**message_args)+"."
            if level not in all_levels:
                if error_code is None:
                    error_code="526"
                msg._tell_dev_detail("E", error_code, Exception,"Legacy Error", str(message_args),from_e=from_e)
        except Exception as e:
            print("Exception in decoding error message")
            print(e)
            print(repr(e))
        msg._tell_dev_detail(level, error_code, python_class,short_desc_message,long_desc_message, prevent_raise,from_e=from_e)

    @staticmethod
    def _tell_dev_detail(level:str, error_code:str, python_class:"type|int",short_desc_message:str,long_desc_message:str,prevent_raise:bool=False,from_e:Optional[Exception]=None) -> None:
        # in order of likelihood: if we trace, then almost all messages will hit the first target. Fatal is unlikely to happen
        if level==T:
            logging.debug(long_desc_message) # no logging.trace() in python, so use debug instead.
        elif level==D:
            logging.debug(long_desc_message)
        elif level==I:
            logging.info(long_desc_message)
        elif level==N:
            logging.info(long_desc_message)
        elif level==E:
            logging.error(long_desc_message)
            if python_class is None:
                python_class = Exception
            error_exception = msg.create_exception_short_traceback(python_class,short_desc_message,[long_desc_message],from_e=from_e)
            if not prevent_raise:
                raise error_exception
            # raise python_class(short_desc_message,long_desc_message)
        elif level==W:
            logging.warning(long_desc_message)
            python_class_exception = Warning
            if python_class is None:
                python_class_exception = Warning
            elif type(python_class) is int:
                python_class_exception = Warning
            elif issubclass(type(python_class),Warning):
                python_class_exception = python_class  # type: ignore # already checked that it is of a warning type
            else:
                python_class_exception = Warning
            msg.__generate_warning(short_desc_message,python_class_exception,error_code=error_code)
        elif level==C:
            logging.critical(long_desc_message)
            if python_class is None:
                python_class = Exception
            critical_exception = msg.create_exception_short_traceback(python_class,short_desc_message,[long_desc_message],from_e=from_e)
            if not prevent_raise:
                raise critical_exception
        elif level==F:
            if python_class is None:
                python_class = RuntimeError
            if type(python_class) is int:
                python_class = RuntimeError
            fatal_exception = msg.create_exception_short_traceback(python_class,short_desc_message,[long_desc_message],from_e=from_e)
            logging.critical(long_desc_message) # no logging.fatal() in python, so use critical instead.
            if not prevent_raise:
                raise fatal_exception
        else:
            logging.error(long_desc_message)
            if python_class is None:
                python_class = Exception
            ee = msg.create_exception_short_traceback(python_class,short_desc_message,[long_desc_message],from_e=from_e)
            if not prevent_raise:
                raise ee

    @staticmethod
    def __generate_warning(short_desc_message:str,python_class:"type", error_code:str) -> None:
        import traceback
        stack = traceback.extract_stack()
        stackcount=0
        seen=0
        last_fname = None
        last_lineno = None
        for frame in stack:
            stackcount += 1
            remove = False
            for fname in msg._REMOVE_FROM_STACK:
                if frame.filename.endswith(fname):
                    remove=True
                    break
            if not remove:
                seen=stackcount
                last_fname = frame.filename
                last_lineno = frame.lineno

        stacklevel = stackcount-seen+1
        warnings.warn(short_desc_message,python_class,stacklevel=stacklevel) # type: ignore [arg-type] # for python_class
        if error_code == "496": # hardcoded from server for "unknown encountered"
            msg.unknown_encountered_filename = last_fname
            msg.unknown_encountered_lineno = last_lineno

    # TODO: look at jinja and copy what they do
    # https://github.com/pallets/jinja/blob/main/src/jinja2/debug.py
    @staticmethod
    def create_exception_short_traceback(python_class: "type|int", short_desc_message:str, long_desc_message:Optional[TypingList[str]], from_e: Optional[Exception]=None) -> BaseException:
        if from_e is None:
            import traceback
            try:
                raise Exception()
            except Exception as exc:
                from_e = exc
        e = from_e
        if True:
            # The above code is not doing anything. It is just a comment that says
            # "Python" and "back_frame".
            back_frame = None
            if e.__traceback__ is not None:
                back_frame =e.__traceback__.tb_frame
            bf = back_frame
            tb = e.__traceback__
            new_stack = []
            while tb is not None:
                f = tb.tb_frame
                fname = f.f_code.co_filename
                lineno = f.f_lineno
                remove=False
                for remove_f in msg._REMOVE_FROM_STACK:
                    if fname.endswith(remove_f):
                        remove=True
                        break
                if not remove:
                    new_stack.append(f)
                tb = tb.tb_next
            new_tb = None
            for f in reversed(new_stack):
                fname = f.f_code.co_filename
                lineno = f.f_lineno
                new_tb = types.TracebackType(new_tb,f,f.f_lasti,f.f_lineno)
            if type(python_class) is int:
                python_class_exception = BaseException
            else:
                python_class_exception = python_class  # type: ignore # already checked that it is of Exception type
            newe = python_class_exception(short_desc_message)
            show_notes = False
            if long_desc_message is not None:
                if hasattr(newe, "add_note"):
                    if long_desc_message is not None:
                        for note in long_desc_message:
                            newe.add_note(note)
                else:
                    try:
                        raise AttributeError("add_note")
                    except AttributeError:
                        show_notes = True
                        pass
            sys.excepthook(python_class_exception, newe, new_tb)
            if show_notes and long_desc_message is not None:
                for note in long_desc_message:
                    print(note,file=sys.stderr)

            return newe.with_traceback(new_tb)
            # raise newe.with_traceback(e.__traceback__) from None

    @staticmethod
    def _handle_native_exception(e:Exception) -> None:
        notes=None
        if hasattr(e,"__notes__"):
            notes=e.__notes__
        if "NoneType" in str(e) and msg.unknown_encountered_filename is not None:
            fname = msg.unknown_encountered_filename
            lineno = msg.unknown_encountered_lineno
            # reset saved values for next time around
            msg.unknown_encountered_filename = None
            msg.unknown_encountered_lineno = None

            if isinstance(e,AttributeError):
                msg._tell_dev(msg.M530_nonetype_attributeerror__orig_fname_line,{"orig":str(e),"fname":fname,"lineno":lineno},prevent_raise=True,from_e=e)
            elif isinstance(e,TypeError):
                msg._tell_dev(msg.M531_nonetype_typeerror__orig_fname_line,{"orig":str(e),"fname":fname,"lineno":lineno},prevent_raise=True,from_e=e)
            else:
                msg._tell_dev(msg.M311_nonetype_recall__fname_line,{"fname":fname,"lineno":lineno},from_e=e)
                #print("SHOW TRACEBACK")
                #f = Exception()
                #f.__traceback__ = e.__traceback__
                msg.create_exception_short_traceback(e.__class__,e.args[0],notes,from_e=e)
        else:
            msg.create_exception_short_traceback(e.__class__,e.args[0],notes,from_e=e)

    class TellDevException(BaseException):
        def __init__(self, msg: "MsgTuple", args: Dict[str,str]) -> None:
            self.e_msg  = msg
            self.e_args = args
