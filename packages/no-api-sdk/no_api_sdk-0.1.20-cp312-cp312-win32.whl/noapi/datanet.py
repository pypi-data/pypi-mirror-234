# emacs coding: utf-8
# mypy: disallow-untyped-defs
# mypy: check-untyped-defs
# mypy: disallow-incomplete-defs

# WARNING; this file is shared between noapi-src and noapi-apps/sdk/python
# If you update one, you need to update the other


import logging
from typing import Optional, Dict, Union, cast
import base64
import copy # FIXME: what to do with micropython
# do not import instruction as this file is also used in the python sdk

console = logging

class _datanet_args:
    def __init__(self, dicti) -> None: # type: ignore[no-untyped-def] # for micropython
        self.propid = "ERR-prop"
        self.oid = "ERR--oid"
        self.blob : Optional[str] = None
        self.text : Optional[str ]=  None
        self.length = 0
        self.target = "Err-trgt"
        self.operation = "?"
        self.datatype = "eRR"
        self.offset = 0
        for item in dicti:
            setattr(self,item,dicti[item])

def _encode_args2url(args: Dict[str,str]) -> bytes:
    return base64.urlsafe_b64encode(str(args).encode()) # FIXME: the args should be packed in a language independent way

def _datanet_encode(args_in: _datanet_args) -> str: # type: ignore[no-untyped-def]
    # Clone args_in to args
    args = copy.copy(args_in)
    # args.__dict__.update(args_in.__dict__)

    # do not use args: instruction, as this file is used by python sdk

    while len(args.propid) < 8:
        args.propid += " "

    padding = "\n"
    protocol_version = "0"
    flags = " "
    # This is called from python SDK as well, without using
    # class instruction, so we DO need to check the existence
    if ((not (hasattr(args,"offset"))) or (args.offset == None)):
        args.offset = 0

    reserved = ":"
    if (hasattr(args,"text") and (args.text != None)):
        args.blob = str(args.text) + "\0"

    if (hasattr(args,"blob") and (args.blob is not None)):
        args.length = len(args.blob)
        args_length_str : str = "%04d" % int(args.length)
        args_offset_str : str = "%04d" % int(args.offset)
        args.target = args_offset_str + args_length_str
        FLAG_BLOB_EXISTS=0x40
        flags = chr(FLAG_BLOB_EXISTS)

    try:
        cmd = (
            padding
            + protocol_version
            + args.operation
            + flags
            + args.datatype
            + reserved
            + args.oid
            + args.propid
            + args.target
        )
    except:
        raise

    if (hasattr(args,"blob") and (args.blob is not None)):
        cmd += str(args.blob)

    return cmd


def _datanet_decode(m: str):  # type: ignore[no-untyped-def] # for micropython. # FIXME: maybe this should be instruction? Or bytes instead of str
    instr : Dict[str,Union[str,int]]= {}
    instr["pad"] = m[0:1]
    instr["version"] = (m[1:2])
    instr["operation"] = (m[2:3])
    instr["flags"] = (m[3:4])
    instr["datatype"] = (m[4:7])
    instr["reserved"] = (m[7:8])
    instr["oid"] = (m[8:16])
    instr["propid"] = (m[16:24])
    # to use propid with names for now, remove extra spaces
    instr["propid"]

    try: # FIXME: instead of trying, we should not from the operation, whethere this is offset/length or not.
        instr["offset"] = int(m[24:28])
        instr["length"] = int(m[28:32])
    except ValueError:
        instr["offset"] = 0
        instr["length"] = 0

    instr["blob"] = m[32:]
    blobstr = cast(str,instr["blob"])
    if (len(blobstr)>0):
            endofstring = blobstr[len(blobstr) - 1]
            if endofstring == "\0":
                instr["text"] = (blobstr[0 : len(blobstr) - 1])
    if len(blobstr)==0:
        blob=None
    instr["target"] = (m[24:32])
    return instr

#
# def _datanet_args_encode(name: str, args: Dict[str,str]) -> str:
#         method_len = "{:08}".format(len(method_name))
#         strargs = method_len + method_name + chr(0)
#         for (arg_name, arg_val) in args.items():
#             strargs += arg_name + chr(0) + arg_val + chr(0)
#
#         offset = 8+8+len(args)*16 # argcount + length of method_name + (8 start+8len)=16 char each arg
#
#         method_offset_str =  "{:08}".format(offset)
#         countargs = "{:08}".format(1+len(args))
#
#         countargs += method_offset_str
#         offset += len(method_name) + 1
#
#         for (arg_name, arg_val) in args.items():
#             countargs += "{:08d}".format(len(arg_name))
#             countargs += "{:08d}".format(len(arg_val))
#
def _datanet_args_get_name(args: str) -> str:
    argcount = int(args[0:8])
    offset = int(args[8:16])
    method_name_len = int(args[offset:offset+8])
    method_name = args[offset+8:offset+8+method_name_len]
    return method_name

def _datanet_args_encode(name: str, args: Dict[str,Optional[str]]) -> str:
    method_len = "{:08}".format(len(name))
    strargs = method_len + name + chr(0)
    for (arg_name, arg_val) in args.items():
        if arg_val is None:
            strargs += arg_name + chr(0)
        else:
            strargs += arg_name + chr(0) + arg_val + chr(0)

    offset = 8+8+len(args)*16*2 # argcount + offset + (8 start+8len)=16 char each arg
    method_offset_str =  "{:08}".format(offset)
    countargs = "{:08}".format(1+len(args))
    countargs += method_offset_str
    offset += 8 + len(name) + 1 # method length + method_name + null

    for (arg_name, arg_val) in args.items():
        countargs += "{:08d}".format(offset)
        countargs += "{:08d}".format(len(arg_name))
        offset += len(arg_name)+1
        countargs += "{:08d}".format(offset)
        if arg_val is None:
            arg_val_len = 0
        else:
            arg_val_len = len(arg_val)+1
        countargs += "{:08d}".format(arg_val_len)
        offset += arg_val_len
    return countargs + strargs

def _datanet_args_decode(argstr: str) -> Dict[str,Optional[str]]:
    argcount = int(argstr[0:8])
    offset = int(argstr[8:16])
    method_name_len = int(argstr[offset:offset+8])
    method_name = argstr[offset+8:offset+8+method_name_len]
    args = {}
    for i in range(argcount-1):
        arg_name_offset_location =16 + i*32 # argcount+nameoffset
        arg_name_offset =  int(argstr[arg_name_offset_location:arg_name_offset_location+8])
        arg_name_len = int(argstr[arg_name_offset_location+8:arg_name_offset_location+16])
        arg_name = argstr[arg_name_offset:arg_name_offset+arg_name_len]

        arg_val_offset_location =  arg_name_offset_location + 16
        arg_val_offset = int(argstr[arg_val_offset_location:arg_val_offset_location+8])
        arg_val_len =  int(argstr[arg_val_offset_location+8:arg_val_offset_location+16])
        if arg_val_len == 0:
            arg_val = None
        else:
            arg_val = argstr[arg_val_offset:arg_val_offset+arg_val_len-1]

        args[arg_name] = arg_val
    return args

# x=datanet_args_encode("joex", { "aabbcc":"ddeeffhh", "ii": "jackal"})
# print(x)
# print(datanet_args_get_name(x))
# print(datanet_args_decode(x))
