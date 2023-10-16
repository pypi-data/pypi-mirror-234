from typing import Any, Union, Callable, Iterator
from copy import deepcopy
import functools
from .json_path_data import *

# import logging
# logging.basicConfig()
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

magico_types_union = Union[dict, list, tuple]
magico_types = magico_types_union.__args__

excluded = [
    "__contains__",
    "__eq__",
    "__iter__",
    "__repr__",
    "__len__",
    "__getattr__",
    "__setattr__",
    "__delattr__",
    "__getitem__",
    "__setitem__",
    "__delitem_",
]

def get_callable_names(data_type: type, excluded: list=excluded) -> list:
    """Get a list of callable names of `data_type`

    Args:
        data_type (type):
            The data type to get the callable names from.
        excluded (list, optional):
            A list of names to ignore.
            Defaults to excluded (as defined prior).

    Returns:
        list: The list of callable names
    """
    callable_names = []
    for method_name in dir(data_type):
        method = getattr(data_type, method_name)
        if callable(method) and method_name not in excluded:
            callable_names.append(method_name)
    return callable_names


class MagicO():
    """Magic Object to enable attribute notation and
    JSONPath addressing of a Python dict, list, or tuple.
    """

    def __init__(self, data: magico_types_union) -> None:
        """MagicO constructor

        Args:
            data (magico_types_union):
                The Python dict, list, or tuple that
                the MagicO object is encapsulating.
        """
        # Use only __dict__ to avoid triggering magic functions
        self.__dict__["_data"] = data
        self.__dict__["_type_method_list"] = []
        data_type = type(data)
        if data_type in magico_types:
            self.__dict__["_type_method_list"] = get_callable_names(data_type)

        for type_method in self.__dict__["_type_method_list"]:
            self.__dict__[type_method] = self._type_method(data_type, type_method)


    def _type_method(self, type: type, method_name: str) -> Callable:
        """Internal method to return a callable from
        the encapsulted object, so that the MagicO object
        behaves like the object it encapsults.

        Args:
            type (type):
                The data type of the encapsulted object.

            method_name (str):
                The name of the callable method. For example,
                "keys" for dict, "append" for list, or "index" for tuple.

        Returns:
            Callable: The method of the `type` named `method_name`.
        """
        type_method = getattr(type, method_name)
        # logger.debug(f"type_method: {type_method}")
        @functools.wraps(type_method)
        def method_wrapper(*args, **kwargs):
            # logger.debug(f"method_wrapper: args={args}, kwargs={kwargs}")
            return type_method(self.__dict__["_data"], *args, **kwargs)
        return method_wrapper


    ############################################################
    #
    # Type behaviour methods
    #

    def __contains__(self, other: Any) -> bool:
        """Magic function to test if the
        encapsulated object contains `other`.

        Args:
            other (Any): The object to test.

        Returns:
            bool: True if the encapsulated object contains `other`.
        """
        # logger.debug(f"__contains__: {type(other)} {other}")
        try:
            if type(self._data) in (list, tuple) and other in self._data:
                # List element containment
                return True
            else:
                return self.__getitem__(other) != None
        except:
            return False


    def __eq__(self, other: magico_types_union) -> bool:
        """Magic function to test if the
        encapsulated objectequals to `other`.

        Args:
            other (Any): The object to test.

        Returns:
            bool: True if the encapsulated object equals to `other`.
        """
        # logger.debug(f"__eq__: {type(other)} {other}")
        return self._data == other


    def __iter__(self) -> Iterator:
        """Magic function to return an iterator
        of the encapsulated object.

        Returns:
            Iterator: The iterator of the encapsulated object.

        Yields:
            Iterator: The next element of the encapsulated object.
        """
        # logger.debug(f"__iter__: self={self}")
        if type(self._data) == list:
            # Make each "magico typed" element of the list itself a MagicO.
            return [MagicO(_) if type(_) in magico_types else _ for _ in self._data].__iter__()
        elif type(self._data) == tuple:
            # Make each "magico typed" element of the tuple itself a MagicO.
            return (MagicO(_) if type(_) in magico_types else _ for _ in self._data).__iter__()
        else:
            # Return the dict iterator as is.
            return self._data.__iter__()


    def __repr__(self) -> str:
        """Magic function to return the string
        representation of the encapsulated object.

        Returns:
            str: A string representation of the encapsulated object.
        """
        # logger.debug(f"__repr__")
        return str(self._data)


    def __len__(self) -> int:
        """Magic function to return the length
        of the encapsulated object.
        """
        # logger.debug(f"__len__")
        return len(self._data)


    ############################################################
    #
    # Attribute notation methods
    #

    def __getattr__(self, attr: str) -> Any:
        """Magic function to return the attribute named `attr`.

        Args:
            attr (str): The attribute name to address

        Raises:
            Exception:
                {type(self).__name__} object has no attribute '{attr}'

        Returns:
            Any: The attribute named `attr`.
        """
        # logger.debug(f"__getattr__: {type(attr)} {attr}")
        if attr in self.__dict__["_type_method_list"]:
            return self.__dict__["_type_method_list"][attr]
        elif attr in self._data:
            if type(self._data[attr]) in magico_types:
                return MagicO(self._data[attr])
            else:
                return self._data[attr]
        else:
            raise Exception(f"{type(self).__name__} object has no attribute '{attr}'")


    def __setattr__(self, attr: str, value: Any) -> None:
        """Magic function to set the attribute
        named `attr` with value `value`.

        Args:
            attr (str): The attribute name of the attribute to set.
            value (Any): The value to set the attribute with.
        """
        # logger.debug(f"__setattr__:  {type(attr)} {attr} <- {value}")
        # Use self.__dict__ to avoid recursion
        if "_data" not in self.__dict__:
            # Set the first _data attribute
            self._data = {attr: value}
        else:
            # self._data exists
            self._data[attr] = value


    def __delattr__(self, attr: str) -> None:
        """Magic function to delete the attribute named `attr`.

        Args:
            attr (str): The attribute name of the attribute to delete.
        """
        # logger.debug(f"__getattr__: {type(attr)} {attr}")
        if "_data" in self.__dict__ and attr in self._data:
            del self._data[attr]


    ############################################################
    #
    # JSONPath notation methods
    #

    def __getitem__(self, path: Union[dict, list, tuple]) -> Any:
        """Magic function to return the attribute
        addressed by JSONPath `path`.

        Args:
            path (Union[dict, list, tuple]): The JSONPath.

        Returns:
            Any: The object the JSONPath is addressing
            in the encapsulated object.
        """
        # logger.debug(f"__getitem__: {type(path)} {path}")
        if type(path) == str:
            return json_path_data(self._data, path_str(path))
        elif type(self._data[path]) not in magico_types:
            return self._data[path]
        else:
            val = MagicO(self._data[path])
            if val != None:
                return val
            else:
                return super().__getitem__(path)


    def __setitem__(self, path: Union[dict, list, tuple], value: Any) -> None:
        """Magic function to set the attribute
        addressed by JSONPath `path`.

        Args:
            path (Union[dict, list, tuple]): The JSONPath.
            value (Any): The value to set the attribute with.
        """
        # logger.debug(f"__setitem__: {type(path)} {path} <- {value}")
        json_path_data(self._data, path_str(path), value=value)


    def __delitem__(self, path: Union[dict, list, tuple]) -> None:
        """Magic function to delete the attribute
        addressed by JSONPath `path`.

        Args:
            path (Union[dict, list, tuple]): The JSONPath.
        """
        # logger.debug(f"__delitem__: {type(path)} {path}")
        json_path_data(self._data, path_str(path), delete=True)


    ############################################################
    #
    # Utility methods
    #

    def to_data(self) -> magico_types_union:
        """Get the encapsulated object.

        Returns:
            dict | list | tuple: The encapsulated object.
        """
        # logger.debug(f"to_data: {type(self._data)} {self._data}")
        return self._data


    def data_type(self) -> type:
        """Get the type of the encapsulated object.

        Returns:
            type: The type of the encapsulated object.
        """
        # logger.debug(f"data_type: {type(self._data)} {self._data}")
        return type(self._data)
