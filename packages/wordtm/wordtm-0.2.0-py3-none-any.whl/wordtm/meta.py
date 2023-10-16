# meta.py
#    
# WordTM: Add meta features to functions of a module
#
# Copyright (C) 2022-2023 WordTM Project
# Author: Johnny Cheng <johnnywfc@gmail.com>
# Updated: 4 October 2023
#
# URL:  nil
# For license information, see LICENSE.TXT

import inspect
from functools import wraps
import pkgutil
from importlib import import_module
import time


def get_module_info(modname='wordtm'):
    """Get the function info of each sub-module of the root module"""
    # modname = __name__.split('.')[0]
    module = import_module(modname)

    i = 0
    mod_info = "The list of sub-modules and their functions of Module '" + modname + "'\n"
    for _, submodname, ispkg in pkgutil.iter_modules(module.__path__):
        if not ispkg:
            i += 1
            mod_info += "%d. %s:" %(i, submodname) + "\n"
            submod = import_module(".."+submodname, modname+"."+submodname)
            for name, member in inspect.getmembers(submod):
                if inspect.isfunction(member) and name != 'files':
                    #mod_info += "\t", name, str(inspect.signature(member)) + "\n"
                    mod_info += "\t{} {}\n".format(name, inspect.signature(member))

    return mod_info


def addin(func):
    """Add additional features to a function at runtime"""
    if "code" in inspect.signature(func).parameters:
        raise TypeError('"code" argument already defined in "' + \
                        func.__name__ + '" function')

    @wraps(func)
    def wrapper(*args, code=False, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")

        if code:
            print("\n" + inspect.getsource(func))

        return value

    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    params.append(inspect.Parameter("code",
                                    inspect.Parameter.KEYWORD_ONLY,
                                    default=False))
    wrapper.__signature__ = sig.replace(parameters=params)
    return wrapper


def addin_all_functions(submod):
    """Apply "addin" function to all functions of a module at runtime"""
    for name, member in inspect.getmembers(submod):
        if callable(member) and \
           member.__name__ != 'files' and \
           name[0].islower():
            # print("\t", name)
            setattr(submod, name, addin(member))


def addin_all(modname='wordtm'):
    """Apply "addin" function to all functions of all sub-modules of a module at runtime"""

    module = import_module(modname)

    if hasattr(module, "__path__"):
        for _, submodname, ispkg in pkgutil.iter_modules(module.__path__):
            if not ispkg and submodname != 'meta':
                # print("@", submodname)
                submod = import_module(".." + submodname, \
                                       modname + "." + submodname)
                addin_all_functions(submod)
    else:
        addin_all_functions(module)
