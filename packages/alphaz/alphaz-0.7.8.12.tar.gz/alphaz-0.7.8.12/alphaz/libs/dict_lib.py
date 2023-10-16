import dictdiffer
from typing import Iterable


def sort_dict(x, value=False, reverse=False):
    sorted_x = {
        x: y
        for x, y in sorted(
            x.items(), key=lambda kv: kv[1 if value else 0], reverse=reverse
        )
    }
    return sorted_x


def get_nested_dict_from_list(in_list) -> dict:
    """Convert list ['a','b','c'] to a nested dict {'a':{'b':{'c':{}}}}

    Args:
        in_list ([list]): list to convert

    Returns:
        [dict]: list converted to nested dict
    """
    out = {}
    for key in reversed(in_list):
        out = {key: out}
    return out


def get_nested(data: dict, keys: list[str], ignore_case: bool = True):
    if keys and data:
        element = keys[0].lower() if ignore_case else keys[0]
        if element:
            value = data.get(element)
            return value if len(keys) == 1 else get_nested(value, keys[1:])


def set_nested(data: dict, keys: list, value):
    if keys and data:
        key = keys[0]
        if key:
            if len(keys) == 1:
                data[key] = value
            else:
                set_nested(data[key], keys[1:], value)


def merge_dict(d1: dict, d2: dict) -> dict:
    """update first dict with second recursively

    Args:
        d1 (dict): [description]
        d2 (dict): [description]

    Returns:
        dict: [description]
    """
    if d1 is None or type(d1) != dict:
        return d1
    for k, v in d1.items():
        if k in d2 and type(d2) == dict:
            d2[k] = merge_dict(v, d2[k])
    d1.update(d2)
    return d1


def show_dict(diff: dict | tuple, level: int = 0, outputs=None, show_none: bool = True):
    if diff is None:
        return

    if isinstance(diff, dict):
        diff = dict(sorted(diff.items()))
    elif isinstance(diff, tuple):
        diff = {"old": diff[0], "new": diff[1]}
    else:
        diff = {"diff": diff}

    root = False
    if outputs is None:
        outputs, root = [], True

    for key, value in diff.items():
        if type(value) == list:
            is_diff = False
            for i, el in enumerate(value[::-1]):
                sub_outputs = []
                show_dict(el, level=level + 1, outputs=sub_outputs, show_none=show_none)
                if len(sub_outputs) != 0:
                    outputs.extend(sub_outputs)
                    outputs.append("    " * level + f"   {len(value) - i}")
                    is_diff = True
            if is_diff:
                outputs.append("    " * level + f"-{key}:")
        elif type(value) != dict:
            if not show_none and value is None:
                continue
            outputs.append("    " * level + f"-{key}: {value}")
        else:
            sub_outputs = []
            show_dict(value, level=level + 1, outputs=sub_outputs, show_none=show_none)
            if len(sub_outputs) != 0:
                outputs.extend(sub_outputs)
                outputs.append("    " * level + f"-{key}:")

    if root:
        print("\n".join(outputs[::-1]))


def compare_dicts(
    d1: dict, d2: dict, ignore: list | dict | None = None, show: bool = False
) -> dict | None:
    """Compare two dict, returns None if there is no difference

    Args:
        d1 (dict): _description_
        d2 (dict): _description_
        ignore (list | dict, optional): list or dict of keys to ignore. Defaults to None.
        show (bool, optional): _description_. Defaults to False.

    Returns:
        dict: _description_
    """
    if d1 == d2:
        return None

    res = None
    if type(d1) == dict and type(d2) == dict:
        output = {}
        keys1, keys2 = list(d1.keys()), list(d2.keys())

        for key in list(set(keys1).union(set(keys2))):
            if ignore is not None:
                if type(ignore) == list and key in ignore:
                    continue
                elif type(ignore) == dict and key in ignore and ignore[key] is None:
                    continue

            res = None
            if key in keys1 and key in keys2:
                res = compare_dicts(
                    d1[key],
                    d2[key],
                    ignore=ignore[key]
                    if isinstance(ignore, Iterable) and key in ignore
                    else None,
                )
            elif key in keys1:
                res = (d1[key], None)
            elif key in keys2:
                res = (None, d2[key])

            if res is not None and not (
                isinstance(res, Iterable) and all([x is None for x in res])
            ):
                output[key] = res
        return output if len(output) != 0 else None

    elif type(d1) != type(d2):
        res = (d1, d2)
    elif type(d1) == list and type(d2) == list:
        res = [
            compare_dicts(
                d1[i] if i < len(d1) else None,
                d2[i] if i < len(d2) else None,
                ignore=ignore,
            )
            for i in range(max(len(d1), len(d2)))
        ]
    elif d1 != d2:
        res = (d1, d2)

    if isinstance(res, Iterable) and (
        all([x is None for x in res])
        or all([isinstance(x, Iterable) and len(x) == 0 for x in res])
    ):
        return None
    if len(res) == 0:
        return None
    return res


def get_subdictionary(d: dict, keys: list[str] | None = None) -> dict:
    if keys is None:
        keys = d.keys()  # use all keys by default

    if isinstance(d, dict):
        return {
            k: get_subdictionary(v, keys) if isinstance(v, (dict, list)) else v
            for k, v in d.items()
            if k in keys
        }

    elif isinstance(d, list):
        return [get_subdictionary(item, keys) for item in d]

    return d


def get_nested_dictionary_keys(d: dict) -> list[str]:
    keys = []
    for k, v in d.items():
        keys.append(k)
        if isinstance(v, dict):
            keys.extend(get_nested_dictionary_keys(v))
    return set(keys)


def dict_diff(dict_1: dict, dict2: dict) -> list[any]:
    return [diff for diff in list(dictdiffer.diff(dict_1, dict2))]


def get_dicts_diff(dict_1: dict | list[dict], dict_2: dict | list[dict]):
    if isinstance(dict_1, dict):
        dict_1 = [dict_1]

    if isinstance(dict_2, dict):
        dict_2 = [dict_2]

    return [
        {
            "item": i,
            "diff": dict_diff(dict_1[i], dict_2[i]),
        }
        for i in range(len(dict_2))
    ]
