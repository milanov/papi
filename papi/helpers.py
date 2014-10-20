"""
Helpers is a collection of miscellaneous functions that were found
handy during the development of PAPI but didn't logically belong t
any class.

"""

import os
import re
import importlib
import inspect
from os.path import basename

IDENT_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_.]*$')


def ispackage_path(path):
    """
    Check if a given absolute path directory is
    a python package.

    """
    if os.path.isdir(path):
        end = os.path.basename(path)
        if IDENT_RE.match(end):
            for init in ('__init__.py', '__init__.pyc', '__init__.pyo'):
                if os.path.isfile(os.path.join(path, init)):
                    return True
    return False


def expand_paths(paths):
    """
    Expand a list of paths to their absolute ones.

    """
    return [os.path.abspath(path) for path in paths]


def safe_import(module):
    """
    Try to import a module by (dotted) name and return None if
    the import fails by any reason.

    """
    try:
        return importlib.import_module(module)
    except:
        return None


def isattribute(object):
    return not (inspect.ismodule(object) or inspect.isclass(object) or
                inspect.isroutine(object) or inspect.isframe(object) or
                inspect.istraceback(object) or inspect.iscode(object))


def visiblename(name):
    """
    Checks whether a given name should be documented/displayed by
    ignoring builtin ones.

    """
    return not (name.startswith('__') and name.endswith('__'))


def extract_attributes(module):
    """
    Returns the list of attributes defined in a given module.

    """
    attributes = []
    for name, obj in inspect.getmembers(module, isattribute):
        if visiblename(name):
            attributes.append((name, obj))
    return attributes


def extract_submodules(module, module_tree):
    """
    Returns the list of submodules for a given module in a module hierarchy.
    Example:
        module_tree = [test,
                       test.one,
                       test.one.two,
                       test.one.three,
                       test.four]

        extract_submodules('test.one', module_tree)
        >>> [two, three]

        extract_submodules('test', module_tree)
        >>> [one, four]
    """
    submodules = []
    module_prefix = module.__name__ + "."

    for submod in module_tree:
        submod_name = submod.__name__
        prefix_pred = submod_name.startswith(module_prefix)
        if prefix_pred and not "." in submod_name.split(module_prefix, 1)[1]:
            submodules.append(submod)

    return submodules
