"""
Classes in this module are used to represent Python objects - modules,
classes, functions, methods and attributes.

"""

import inspect
import sys
import pkgutil
from os.path import dirname, basename, splitext
from papi.helpers import extract_attributes, safe_import, extract_submodules


class Resource():

    """
    Represents a resouce. Contains a list of ModuleObject modules
    from the module tree of that resource.
    """

    def __init__(self, path):
        sys.path.append(dirname(path))

        self._name, _ = splitext(basename(path))
        self._module_tree = self._get_module_tree(path)
        self._modules = self._get_modules()

    @property
    def name(self):
        return self._name

    @property
    def module_tree(self):
        return self._module_tree

    @property
    def modules(self):
        return self._modules

    @property
    def docsdir(self):
        return self._name + "_docs"

    def _get_module_tree(self, path):
        module_tree = [safe_import(self._name)]

        prefix = self._name + "."
        dummy = lambda x: x
        for _, modname, ispkg in pkgutil.walk_packages([path], prefix, dummy):
            module_tree.append(safe_import(modname))
        return list(filter(None, module_tree))

    def _get_modules(self):
        modules = []
        for mod in self._module_tree:
            submods = extract_submodules(mod, self.module_tree)
            simple_submods = [SimpleModuleObject(subm) for subm in submods]
            module_obj = ModuleObject(mod)
            module_obj.submodules = simple_submods
            modules.append(module_obj)
        return modules


class BaseObject():

    """
    A base class for objects -  modules/classes/functions. It stores the
    object and its name, docstring and source code.

    """

    def __init__(self, obj):
        self._obj = obj
        self._name = obj.__name__
        self._doc = inspect.getdoc(obj)
        try:
            self._code = inspect.getsource(obj)
        except IOError:
            self._code = ""

    @property
    def name(self):
        return self._name

    @property
    def doc(self):
        return self._doc

    @property
    def code(self):
        return self._code


class ModuleObject(BaseObject):

    """
    Represents a Python module with all of its submodules, classes,
    functions and attributes.

    """

    def __init__(self, module):
        sysmodule = sys.modules[module.__name__]
        super().__init__(sysmodule)

        self._short_name = super().name.split(".")[-1]
        self._submodules = []

        attributes = extract_attributes(sysmodule)
        self._attributes = [AttributeObject(attr) for attr in attributes]

        spr = super()
        isclass = lambda m: inspect.isclass(m) and m.__module__ == spr.name
        classes = inspect.getmembers(sysmodule, isclass)
        self._classes = [ClassObject(cls[1]) for cls in classes]

        isfunc = lambda m: inspect.isfunction(m) and m.__module__ == spr.name
        functions = inspect.getmembers(sysmodule, isfunc)
        self._functions = [FunctionObject(func[1]) for func in functions]

    @property
    def short_name(self):
        return self._short_name

    @property
    def submodules(self):
        return self._submodules

    @submodules.setter
    def submodules(self, value):
        self._submodules = value

    @property
    def classes(self):
        return self._classes

    @property
    def functions(self):
        return self._functions

    @property
    def attributes(self):
        return self._attributes


class SimpleModuleObject(BaseObject):

    """
    Represents a module object but with limited attributes. It
    doesn't recursively initialize its submodules to prevent
    the creating of giant composite objects.

    """

    def __init__(self, module):
        super().__init__(module)
        self._short_name = super().name.split(".")[-1]

    @property
    def short_name(self):
        return self._short_name


class ClassObject(BaseObject):

    """
    Represents a Python class and has its methods and attributes.

    """

    def __init__(self, cls):
        super().__init__(cls)
        methods = inspect.getmembers(cls, inspect.isfunction)
        self._methods = [FunctionObject(method[1]) for method in methods]
        attributes = extract_attributes(cls)
        self._attributes = [AttributeObject(attr) for attr in attributes]

    @property
    def methods(self):
        return self._methods

    @property
    def attributes(self):
        return self._attributes


class FunctionObject(BaseObject):

    """
    Represents a Python function/method and has its signature
    additional to the inherited name, docstring and source code.

    """

    def __init__(self, func):
        super().__init__(func)
        self._signature = str(inspect.signature(func))

    @property
    def signature(self):
        return self._signature


class AttributeObject():

    """
    Represents a Python data attribute and has its name and value.

    """

    def __init__(self, attr):
        self._name, self._value = attr

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value
