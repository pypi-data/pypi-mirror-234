r"""This module contains some helper functions to manipulate objects."""

from __future__ import annotations

__all__ = [
    "all_child_classes",
    "full_object_name",
    "import_object",
    "instantiate_object",
    "is_lambda_function",
]

import inspect
import logging
from typing import Any, Callable

from tornado.util import import_object as tornado_import_object

from objectory.errors import AbstractClassFactoryError, IncorrectObjectFactoryError

logger = logging.getLogger(__name__)


def all_child_classes(cls: type) -> set[type]:
    r"""Gets all the child classes (or subclasses) of a given class.

    SOURCE: https://stackoverflow.com/a/3862957

    Args:
    ----
        cls: Specifies the class whose child classes you want to get.

    Returns:
    -------
        set: The set of all the child classes of the given class.

    Example usage:

    .. code-block:: pycon

        >>> from objectory.utils import all_child_classes
        >>> class Foo:
        ...     pass
        ...
        >>> all_child_classes(Foo)
        set()
        >>> class Bar(Foo):
        ...     pass
        ...
        >>> all_child_classes(Foo)
        {<class '....Bar'>}
    """
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_child_classes(c)]
    )


def full_object_name(obj: Any) -> str:
    r"""Computes the full name of an object.

    This function works for class and function objects.

    Args:
    ----
        obj: Specifies the class/function that you want to compute
            the full name.

    Returns:
    -------
        str: The full name of the object.

    Raises:
    ------
        ``TypeError`` if the object is not a class or a function.

    Example usage:

    .. code-block:: pycon

        >>> from objectory.utils import full_object_name
        >>> class MyClass:
        ...     pass
        ...
        >>> full_object_name(MyClass)
        '....MyClass'
        >>> def my_function():
        ...     pass
        ...
        >>> full_object_name(my_function)
        '....my_function'
    """
    if inspect.isclass(obj) or inspect.isfunction(obj):
        return _full_object_name(obj)
    raise TypeError(f"Incorrect object type: {obj}")


def _full_object_name(obj: type) -> str:
    r"""Computes the full class name of a class/function.

    SOURCE: https://gist.github.com/clbarnes/edd28ea32010eb159b34b075687bb49e

    Args:
    ----
        obj: Specifies the class/function that you want to compute
            the full class name.

    Returns:
    -------
        str: The full class name.
    """
    name = obj.__qualname__
    if (module := obj.__module__) is not None and module != "__builtin__":
        name = module + "." + name
    return name


def import_object(object_path: str) -> Any:
    r"""Tries to import an object given its path.

    This function can be used to dynamically import a class or a
    function. The object path should have the following structure:
    ``module_path.object_name``. This function returns ``None`` if
    the object path does not respect this structure.

    Args:
    ----
        object_path (str): Specifies the path of the object to import.

    Returns:
    -------
        The object if the import was successful otherwise ``None``.

    Example usage:

    .. code-block:: pycon

        >>> from objectory.utils import import_object
        >>> obj = import_object("collections.Counter")
        >>> obj()
        Counter()
        >>> fn = import_object("math.isclose")
        >>> fn(1, 1)
        True
    """
    if not isinstance(object_path, str):
        raise TypeError(f"The object_path has to be a string (received: {object_path})")
    try:
        return tornado_import_object(object_path)
    except (ValueError, ImportError):
        return None


def instantiate_object(obj: Callable | type, *args, _init_: str = "__init__", **kwargs) -> Any:
    r"""Instantiates dynamically an object from its configuration.

    Args:
    ----
        obj (class or function): Specifies the class to instantiate
            or the function to call.
        *args: Variable length argument list.
        _init_ (str, optional): Specifies the function to use to
            create the object. This input is ignored if ``obj`` is a
            function. If ``"__init__"``, the object is created by
            calling the constructor. Default: ``"__init__"``.
        **kwargs: Arbitrary keyword arguments.

    Returns:
    -------
        The instantiated object if ``obj`` is a class name, otherwise
            the returned value of the function.

    Raises:
    ------
        TypeError if ``obj`` is not a class or a function.

    Example usage:

    .. code-block:: pycon

        >>> from collections import Counter
        >>> from objectory.utils import instantiate_object
        >>> instantiate_object(Counter, [1, 2, 1])
        Counter({1: 2, 2: 1})
        >>> instantiate_object(list, [1, 2, 1])
        [1, 2, 1]
    """
    if inspect.isfunction(obj):
        return obj(*args, **kwargs)
    if inspect.isclass(obj):
        return _instantiate_class_object(obj, *args, _init_=_init_, **kwargs)
    raise TypeError(f"Incorrect type: {obj}. The valid types are class and function")


def _instantiate_class_object(cls: type, *args, _init_: str = "__init__", **kwargs) -> Any:
    r"""Instantiates an object from its class and some arguments.

    The object can be instantiated by calling the constructor
    ``__init__`` (default) or ``__new__`` or a class method.

    Args:
    ----
        cls (class): Specifies the class of the object to instantiate.
        *args: Variable length argument list.
        _init_ (str, optional): Specifies the function to use to
            create the object. If ``"__init__"``, the object is
            created by calling the constructor.
            Default: ``"__init__"``.
        **kwargs: Arbitrary keyword arguments.

    Returns:
    -------
        The instantiated object.

    Raises:
    ------
        ``AbstractClassFactoryError`` if it is an abstract class.
        ``IncorrectObjectFactoryError`` if it is not possible to
            instantiate the object.
    """
    if inspect.isabstract(cls):
        raise AbstractClassFactoryError(
            f"Cannot instantiate the class {cls} because it is an abstract class."
        )

    if _init_ == "__init__":
        return cls(*args, **kwargs)

    if not hasattr(cls, _init_):
        raise IncorrectObjectFactoryError(f"{cls} does not have {_init_} attribute")
    init_fn = getattr(cls, _init_)
    if not callable(init_fn):
        raise IncorrectObjectFactoryError(f"The {_init_} attribute of {cls} is not callable")
    if _init_ == "__new__":
        return init_fn(cls, *args, **kwargs)
    return init_fn(*args, **kwargs)


def is_lambda_function(obj: Any) -> bool:
    r"""Indicates if the object is a lambda function or not.

    Adapted from https://stackoverflow.com/a/23852434

    Args:
    ----
        obj: Specifies the object to check.

    Returns:
    -------
        bool: ``True`` if the input is a lambda function,
            otherwise ``False``

    Example usage:

    .. code-block:: pycon

        >>> from objectory.utils import is_lambda_function
        >>> is_lambda_function(lambda value: value + 1)
        True
        >>> def my_function(value: int) -> int:
        ...     return value + 1
        ...
        >>> is_lambda_function(my_function)
        False
        >>> is_lambda_function(1)
        False
    """
    if not inspect.isfunction(obj):
        return False
    return obj.__name__ == "<lambda>"
