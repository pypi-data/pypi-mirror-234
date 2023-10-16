from copy import deepcopy
from typing import Union, Any
import re

def path_str(path: Union[str, int, slice]) -> str:
    """Convert path of int and slice types to str type to be used in json_path_data
    This is to handle data being a non-str.

    Args:
        path (Union[str, int, slice]): path to be converted

    Returns:
        str: string representation of `path`: "[path]" if int; "[start:stop:step]" if slice
    """
    _path = path
    if type(_path) == int:
        _path = f"$[{_path}]"
    elif type(_path) == slice:
        start = _path.start if _path.start != None else ""
        stop = _path.stop if _path.stop != None else ""
        step = _path.step if _path.step != None else ""
        _path = f"$[{start}:{stop}:{step}]"
    return _path


# JSONPath
#   Take a dict or list object and return the attribute identified in `key_path`.
#   If `value` is not None, set the attribute with `value`.
#   If `delete` is True, delete the attribute (and ignore `value`).
#
#   Recursive algorithm:
#   - Takes subscripts as individual attributes.
#     - e.g., "var[9]" -> "var.[9]", "var[9][8]" -> "var.[9].[8]"
#   - If leaf (path blank)
#     - return the root_dict as is
#   - Else (path non-blank)
#     - If not begins with [...]
#       - If begins with "$"
#         - If there are dots
#           - return json_path_data without "$."
#         - Else (leaf with key)
#           - Error if delete or update
#           - return the root_dict as is
#       - Elif (addressed element exists)
#         - If there are dots
#           - return json_path_data(addressed element)
#         - Else (check delete/update)
#           - get the parent (from arg list)
#           - delete and update if so
#           - return the addressed element (the old value)
#       - Else (addressed element not exists)
#         - If delete return None
#         - Elif update
#           - If there are dots
#             - create the element by assigning {} to it
#             - return json_path_data(element)
#           - Else
#             - create the element by assigning the value to it
#             - return the element
#         - Else
#           - return default
#     - If begins with [...]
#       - Handling slicing
#       - If list
#         - If there are dots
#           - return json_path_data(addressed element)
#         - Else (leaf on selfy)
#           - If delete, do so
#           - Elif update, do so
#           - return the old value
#       - Elif dict
#         - If there are dots
#           - If slice, error
#           - Else return json_path_data(addressed element)
#         - Else (no dots)
#           - If delete, do so
#           - Elif update, do so
#           - return the old value


def json_path_data(
        root_dict: Union[dict, list, tuple],
        key_path: str="",
        default: Any=None,
        delete: bool=False,
        value: Any=None,
        _parent_obj: Union[dict, list, tuple]=None,
        _parent_key: str=None
    ) -> Union[dict, list, tuple]:
    """JSONPath
    Take a dict or list object and return the attribute identified in `key_path`.
    If `value` is not None, set the attribute with `value`.
    If `delete` is True, delete the attribute (and ignore `value`).

    Args:
        root_dict (Union[dict, list, tuple]):
            The object the JSONPath is addressing.

        key_path (str, optional):
            The JSONPath.
            Defaults to "".

        default (Any, optional):
            If the addressed element does not exist, return `default`.
            Defaults to None.

        delete (bool, optional):
            Delete the addressed element if true.
            Defaults to False.

        value (Any, optional):
            Assign the `value` to the addressed element unless it is None.
            Defaults to None.

        _parent_obj (Union[dict, list, tuple], optional):
            The parent object of `root_dict` (for deleting from parent).
            Defaults to None (`root_dict` is at the top level).

        _parent_key (str, optional):
            The key of the parent object to address `root_dict` (for deleting from parent).
            Defaults to None.

    Raises:
        KeyError: Cannot delete {key}
        KeyError: Cannot set value for {key}
        KeyError: Invalid index syntax {indexes_str}
        KeyError: Invalid index range {indexes_str} for {key} - index_me={index_me}
        KeyError: Invalid index range {indexes_str} for branch node {key}
        KeyError: Cannot set value for {key}[{indexes_str}]

    Returns:
        Union[dict, list, tuple]:
            The element the JSONPath addresses
    """

    # root_dict is passed by reference
    # root_node is a twin of root_dict (a reference to the root node)
    # If delete is True, value will be ignored

    root_node = root_dict
    # Break down "var[9]" into "var.[9]", "var[9][8]" into "var.[9].[8]"
    path_keys = re.sub(r"(\[(-?[0-9:]+)\])", ".\\1", key_path).split(".")
    # Remove empty path key
    path_keys = [k for k in path_keys if k]

    # logger.debug(f"json_path_data({root_node}, key_path={key_path}->{'.'.join(path_keys[1:])}, default={default}, delete={delete}, value={value}, _parent_obj, _parent_key={_parent_key})")

    # In each case, ret should be set.
    if len(path_keys) == 0:
        # Blank key addresses the root
        # logger.debug(f"json_path_data - blank key")
        return root_node
    else:
        # Branch or leaf node the root_node is
        # The next level down is root_node[key]

        # _value = value
        # # Deepcopy value if dict
        # if type(_value) == dict or type(_value) == list:
        _value = deepcopy(value)

        key = path_keys[0]
        index_str = re.sub(r"^\[(.*)\]$", "\\1", key)

        if index_str == key:
            # It is a key
            if key == "$":
                # Path variable
                if len(path_keys) > 1:
                    # Branch node key exists - down one level
                    # logger.debug(f"json_path_data - branch node: {key}")
                    return json_path_data(root_node, '.'.join(path_keys[1:]), default, delete, _value, root_node, None)  # No parent
                else:
                    # Leaf node key exists - act on self
                    # logger.debug(f"json_path_data - leaf node: {key}")
                    old_value = root_node
                    if delete:
                        # logger.debug(f"Error: Cannot delete {key}")
                        # return None
                        raise KeyError(f"Cannot delete {key}")
                    elif _value != None:
                        # logger.debug(f"Error: Cannot set value for {key}")
                        # return old_value
                        raise KeyError(f"Cannot set value for {key}")
                    else:
                        return old_value
            elif key in root_node:
                # Key exists
                if len(path_keys) > 1:
                    # Branch node key exists - down one level
                    # logger.debug(f"json_path_data - branch key exists: {key}")
                    return json_path_data(root_node[key], '.'.join(path_keys[1:]), default, delete, _value, root_node, key)
                else:
                    # Leaf node key exists - act on self
                    # logger.debug(f"json_path_data - leaf key exists: {key}")
                    # logger.debug(f"json_path_data - root_node: {root_node}")
                    old_value = root_node[key]

                    parent_obj = _parent_obj if _parent_obj else root_node
                    if _parent_key != None:
                        parent_obj = parent_obj[_parent_key]

                    if delete:
                        # logger.debug(f"json_path_data - delete {key} from {root_node} (value={old_value})")
                        del parent_obj[key]
                    elif _value != None:
                        # logger.debug(f"json_path_data - set {key} to {value}")
                        # logger.debug(f"json_path_data - _parent_obj={_parent_obj}")
                        # logger.debug(f"json_path_data - _parent_key={_parent_key}")
                        parent_obj[key] = _value
                    return old_value
            else:
                # logger.debug(f"json_path_data - key not exists: {key}")
                # Key does not exists
                if delete:
                    # logger.debug(f"json_path_data - delete nothing")
                    # Nothing to delele
                    return None
                elif _value != None:
                    # Set value
                    if len(path_keys) > 1:
                        # Branch node - create the key (part of the path)
                        # logger.debug(f"json_path_data - set value {value} on new branch {key}")
                        root_node[key] = {}
                        return json_path_data(root_node[key], '.'.join(path_keys[1:]), default, delete, _value, root_node, key)
                    else:
                        # Leaf node
                        # logger.debug(f"json_path_data - set value {value} on new leave {key}")
                        root_node[key] = _value
                        return root_node[key]
                else:
                    return default
        else:
            # It is an index
            # Index string is in index_str

            # Determine the indexes regardless of root_node type
            indexes_str = index_str.split(":")
            # logger.debug(f"json_path_data - indexes_str: {indexes_str}")
            if len(indexes_str) == 0 or len(indexes_str) > 3:
                # [] or [9:9:9:9...]
                raise KeyError(f"Invalid index syntax {indexes_str}")
            # [9] or [9:9] or [9:9:9]
            # logger.debug(f"json_path_data - root_node len: {len(root_node)}")
            index_single = None
            index_slice = None
            if len(indexes_str) == 1:
                # indexes_str[0] must be not null,
                # or it would have been an error upon len(indexes_str) == 0
                # Special case of a single index
                index_single = int(indexes_str[0])
                # logger.debug(f"json_path_data - index_single: {index_single}")
            else:
                indexes = [None] * 3
                for ii in range(3):
                    if len(indexes_str) > ii and indexes_str[ii]:
                        indexes[ii] = int(indexes_str[ii])
                index_slice = slice(indexes[0], indexes[1], indexes[2])
                # logger.debug(f"json_path_data - index_slice: {index_slice}")
            index_me = index_single if index_single != None else index_slice
            if index_me == None:
                # Should not happen - just to be defensive
                raise KeyError(f"Invalid index range {indexes_str} for {key} - index_me={index_me}")

            # logger.debug(f"json_path_data - indexes: {indexes}")
            # logger.debug(f"json_path_data - root_node is {type(root_node)}")

            if type(root_node) in (list, tuple):
                if len(path_keys) > 1:
                    # Branch node
                    # logger.debug(f"json_path_data - list branch single - recur root_node={root_node}")
                    return json_path_data(root_node[index_me], '.'.join(path_keys[1:]), default, delete, _value, root_node, index_me)
                else:
                    # Leaf node - act on self
                    # logger.debug(f"json_path_data - list leaf - act on self root_node={root_node}")
                    old_value = root_node[index_me]
                    if delete:
                        del root_node[index_me]
                    elif _value != None:
                        root_node[index_me] = _value
                    return old_value
            elif type(root_node) == dict:
                if len(path_keys) > 1:
                    # Branch node
                    if index_slice:
                        # Range index
                        # logger.debug(f"Error: Invalid index range {indexes_str} for branch node {key}")
                        # return default
                        raise KeyError(f"Invalid index range {indexes_str} for branch node {key}")
                    else:
                        # Single index
                        # logger.debug(f"json_path_data - dict branch single - recur")
                        k = list(root_node.keys())[index_me]
                        return json_path_data(root_node[k], '.'.join(path_keys[1:]), default, delete, _value, root_node, k)
                else:
                    # Leaf node - act on self, element by element
                    # List of keys in root_node that is to be returned, deleted or set value

                    # logger.debug(f"json_path_data - root_node.keys(): {root_node.keys()}")
                    # logger.debug(f"json_path_data - indexes: {indexes}")

                    ndx_key_list = list(root_node.keys())[index_me]
                    if type(ndx_key_list) != list:
                        ndx_key_list = [ndx_key_list]

                    # logger.debug(f"json_path_data - dict leaf {ndx_key_list}")

                    old_value = {k: root_node[k] for k in ndx_key_list}

                    if delete:
                        for k in ndx_key_list:
                            del root_node[k]
                    elif _value != None:
                        # logger.debug(f"Error: Cannot set value for {key}[{indexes_str}]")
                        # return default
                        raise KeyError(f"Cannot set value for {key}[{indexes_str}]")

                    return old_value

    return default
