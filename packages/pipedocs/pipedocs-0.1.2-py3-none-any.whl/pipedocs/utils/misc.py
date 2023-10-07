from importlib import import_module
from pkgutil import iter_modules
from typing import Union, Callable, Any
import sys
from os import PathLike
from pathlib import Path
from types import ModuleType

def _import_file(filepath: Union[str, PathLike]) -> ModuleType:
    abspath = Path(filepath).resolve()
    if abspath.suffix not in (".py", ".pyw"):
        raise ValueError(f"Not a Python source file: {abspath}")
    dirname = str(abspath.parent)
    sys.path = [dirname] + sys.path
    try:
        module = import_module(abspath.stem)
    finally:
        sys.path.pop(0)
    return module


def load_object(path: Union[str, Callable]) -> Any:
    """Load an object given its absolute object path, and return it.

    The object can be the import path of a class, function, variable or an
    instance, e.g. 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'.

    If ``path`` is not a string, but is a callable object, such as a class or
    a function, then return it as is.
    """

    if not isinstance(path, str):
        if callable(path):
            return path
        raise TypeError(
            "Unexpected argument type, expected string " f"or object, got: {type(path)}"
        )

    try:
        dot = path.rindex(".")
    except ValueError:
        raise ValueError(f"Error loading object '{path}': not a full path")

    module, name = path[:dot], path[dot + 1 :]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError(f"Module '{module}' doesn't define any object named '{name}'")

    return obj

def walk_modules(path):
    """Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.

    For example: walk_modules('pipedocs.utils')
    """

    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, "__path__"):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + "." + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods