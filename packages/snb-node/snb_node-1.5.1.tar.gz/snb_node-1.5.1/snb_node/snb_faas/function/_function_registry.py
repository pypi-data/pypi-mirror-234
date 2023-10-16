#  wangixnyi
# 2022-10-28
import importlib.util
import os
import sys
import types

from snb_node.snb_faas.function.exceptions import (
    InvalidTargetTypeException,
    MissingTargetException,
)
# REGISTRY_MAP stores the registered functions.
# Keys are user function names, values are user function signature types.

def get_user_function(source, source_module):
    function = {}
    tempes=dir(source_module)
    for temp in tempes:
        temp_obj=getattr(source_module, temp)
        if isinstance(temp_obj,types.FunctionType):
            if temp_obj.__annotations__ and temp_obj.__annotations__.get('return')=='HTTP':
                function['HTTP'] = temp_obj
            '''if temp_obj.__annotations__ and temp_obj.__annotations__.get('return') == 'HELP':
                function['HELP'] = temp_obj'''
    # Check that it is a function
    if function==None:
        raise InvalidTargetTypeException(
            "The function defined in file {source}  needs to be of "
            "type function. Got: invalid type {target_type}".format(
                source=source,  target_type=type(function)
            )
        )
    return function


def load_function_module(source):
    """Load user function source file."""
    # 1. Extract the module name from the source path
    realpath = os.path.realpath(source)
    directory, filename = os.path.split(realpath)
    name, extension = os.path.splitext(filename)
    # 2. Create a new module

    spec = importlib.util.spec_from_file_location(
        name, realpath, submodule_search_locations=[directory]
    )
    source_module = importlib.util.module_from_spec(spec)
    # 3. Add the directory of the source to sys.path to allow the function to
    # load modules relative to its location
    sys.path.append(directory)
    # 4. Add the module to sys.modules
    sys.modules[name] = source_module
    return source_module, spec

