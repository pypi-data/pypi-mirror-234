import sys, imp, inspect, os, glob, re, dataclasses
from types import UnionType
from typing import OrderedDict, Type, List, Dict, Any, get_origin, get_args, Union

# MODELS
from ..models.watcher import ModuleWatcher

myself = lambda: inspect.stack()[1][3]


def get_modules_infos(
    name: str | None = None, url: str | None = None, mode: str = None
):
    from importlib_metadata import version
    import pkgutil

    data = {}
    for item in pkgutil.iter_modules():
        if name is not None and name.lower() != item.name.lower():
            continue
        if item.module_finder.path.endswith("."):
            continue
        try:
            data[item.name] = version(item.name)
        except:
            continue

    if url:
        from . import api_lib

        params = {}
        if name:
            params["name"] = name
        answer = api_lib.get_api_answer(f"{url}/modules", params)
        data_url = answer.data

        K = [
            "local",
            "local_up",
            "local_down",
            "distant",
            "distant_up",
            "distant_down",
            "up",
            "down",
            "distant_align",
        ]
        updates, out = {x: [] for x in K}, {}
        keys = list(set(list(data_url.keys()) + list(data.keys())))
        for key in keys:
            if key in data_url and key in data and data_url[key] == data[key]:
                continue

            out[key] = [
                data[key] if key in data else None,
                data_url[key] if key in data_url else None,
            ]

            if key in data:
                updates["distant"].append(f"{key}=={data[key]}")
            if key in data and key in data_url:
                updates["distant_align"].append(f"{key}=={data[key]}")

            if key in data_url:
                updates["local"].append(f"{key}=={data_url[key]}")
            if key in data and key in data_url:
                updates["up"].append(
                    f"{key}=={data[key] if data[key] > data_url[key] else data_url[key]}"
                )
            if key in data and key in data_url:
                updates["down"].append(
                    f"{key}=={data[key] if data[key] < data_url[key] else data_url[key]}"
                )

            if key in data and key in data_url and data[key] < data_url[key]:
                updates["local_up"].append(f"{key}=={data_url[key]}")
                updates["distant_down"].append(f"{key}=={data[key]}")
            if key in data and key in data_url and data[key] > data_url[key]:
                updates["local_down"].append(f"{key}=={data_url[key]}")
                updates["distant_up"].append(f"{key}=={data[key]}")

        for key, items in updates.items():
            out[key] = " ".join(items)
        return out
    if mode == "requirements":
        return "\n".join([f"{x}=={y}" for x, y in data.items()])
    return data


def myself(fct=None):
    name = inspect.stack()[1][3]
    if fct:
        name = fct(name)
    return name


def get_project_name_from_stack(stack: inspect.FrameInfo):
    calling_module = inspect.getmodule(stack[0])
    module_path = calling_module.__name__.replace(".", os.sep) + ".py"
    root = calling_module.__file__.replace(module_path, "").split(os.sep)
    project_name = "Unknow"
    for name in root[::-1]:
        if name.strip() != "" and name.strip() != "backend":
            project_name = name
            break
    return project_name


def reload_modules(root, log=None):
    root = root.replace("\\", "\\\\")

    modules = [x for x in sys.modules.values()]

    for module in modules:
        if root in str(module) and not "core" in str(module).lower():
            if log:
                log.debug("   Reload %s" % module)
            try:
                imp.reload(module)
            except:
                pass


def watch_modules(roots: list = [], log=None):
    mw = ModuleWatcher()
    roots = [root.replace("\\", "\\\\") for root in roots]

    modules = [x for x in sys.modules.values()]
    for module in modules:
        for root in roots:
            if root in str(module) and not "core" in str(module).lower():
                if log:
                    log.debug(f"Add <{module}> to the watcher")
                mw.watch_module(str(module))
    mw.start_watching()


def execute_cmd(cmd="", root=None, log=None):
    current_folder = os.getcwd()
    if root is not None:
        os.chdir(root)
    if log:
        log.info("Execute: <%s>" % cmd)
    os.system(cmd)
    os.chdir(current_folder)


def get_directory_log_files(directory):
    return glob.glob(directory + os.sep + "*.log*")


def try_except(success, failure, *exceptions):
    try:
        return success()
    except exceptions or Exception:
        return failure() if callable(failure) else failure


def getsize(obj):
    """sum size of object & members."""
    if isinstance(obj, BLACKLIST):
        raise TypeError("getsize() does not take argument of type: " + str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size


def get_attributes(obj):
    attributes = inspect.getmembers(obj, lambda a: not (inspect.isroutine(a)))
    return {
        a[0]: a[1]
        for a in attributes
        if not (a[0].startswith("__") and a[0].endswith("__"))
    }


def filter_kwargs(fct, args: list = [], kwargs: dict = {}) -> dict:
    """Remove kwargs that are not in function kwargs

    Args:
        fct ([type]): [description]
        args (list): [description]
        kwargs (dict): [description]

    Returns:
        [type]: [description]
    """
    fargs = inspect.getfullargspec(fct)
    kwargs = {x: y for x, y in kwargs.items() if x in fargs.args}
    return kwargs


def get_subtype(parent_type):
    if hasattr(parent_type, "__args__"):
        if isinstance(parent_type.__args__[0], type):
            return parent_type.__args__[0]
    return None


def is_subtype_n(obj, parent_type):  # TODO: delete
    if not isinstance(obj, type):
        return is_subtype(type(obj), parent_type)
    if hasattr(obj, "__origin__"):
        return obj.__origin__ == parent_type
    return issubclass(obj, parent_type)


def is_union_type(o):
    sub_origin = get_origin(o)
    sub_args = get_args(o)
    return sub_args and sub_origin and (sub_origin is Union or sub_origin is UnionType)


def get_first_non_none_type(o):
    if not is_union_type(o):
        return o
    sub_args = get_args(o)
    sub_args = [t for t in sub_args if t != type(None)]
    return sub_args[0]


def is_subtype(sub_type, parent_type, debug: bool = False) -> bool:
    sub_origin = get_origin(sub_type)
    parent_origin = get_origin(parent_type)

    sub_args = get_args(sub_type)
    if sub_args:
        sub_args = [t for t in sub_args if t != type(None)]
    parent_args = get_args(parent_type)
    if parent_args:
        parent_args = [t for t in parent_args if t != type(None)]

    if not isinstance(sub_type, type) and sub_origin is None:
        return is_subtype(type(sub_type), parent_type)

    if is_union_type(sub_type):
        return all([is_subtype(s, parent_type) for s in sub_args])
    if is_union_type(sub_origin):
        return all([is_subtype(s, parent_type) for s in sub_args])

    infos = " / ".join(
        [
            str(x)
            for x in [
                sub_type,
                parent_type,
                sub_origin,
                parent_origin,
                sub_args,
                parent_args,
            ]
        ]
    )

    if sub_origin is not None and sub_origin == parent_type:
        return True

    if sub_type == parent_type:
        return True

    if sub_args and parent_args and all(a == b for a, b in zip(sub_args, parent_args)):
        return True

    try:
        if sub_args and any([issubclass(s, parent_type) for s in sub_args]):
            return True
    except:
        pass

    try:
        if issubclass(sub_type, parent_type):
            return True
    except:
        pass

    try:
        if isinstance(sub_type, parent_type):
            return True
    except:
        pass

    if sub_origin is None or parent_origin is None:
        if debug:
            print("   no origin: ", infos)
        return False

    if sub_origin != parent_origin:
        if debug:
            print("   diff origin: ", infos)
        return False

    if not parent_args and sub_origin == parent_origin:
        return True

    if not sub_args or not parent_args:
        if debug:
            print("   no args: ", infos)
        return False

    if not all(a == b for a, b in zip(sub_args, parent_args)):
        if debug:
            print("   diff args: ", infos)
        return False
    return True


def is_subtype_old(sub_type: type | Any, parent_type: type):
    if not isinstance(sub_type, type):
        return is_subtype(type(sub_type), parent_type)

    if sys.version_info >= (3, 7):
        if (
            isinstance(sub_type, type)
            and isinstance(parent_type, type)
            and sub_type == parent_type
        ):
            return True

        if hasattr(sub_type, "__origin__") and hasattr(parent_type, "__origin__"):
            return sub_type.__origin__ == parent_type.__origin__
        elif hasattr(sub_type, "__origin__") and isinstance(parent_type, type):
            return sub_type.__origin__ == parent_type
        elif hasattr(parent_type, "__args__") and hasattr(sub_type, "__args__"):
            if isinstance(parent_type.__args__[0], type):
                return sub_type.__args__ == parent_type.__args__
        elif hasattr(parent_type, "_name") and hasattr(sub_type, "_name"):
            return sub_type._name == parent_type._name

        return False

    else:
        if not hasattr(sub_type, "__extra__") or not hasattr(parent_type, "__extra__"):
            return False

        if sub_type.__extra__ != parent_type.__extra__:
            return False

        if not parent_type.__args__ or parent_type.__args__ == sub_type.__args__:
            return True

    return False


def sort_by_key(input_dict):
    return OrderedDict(sorted(input_dict.items(), key=lambda x: x[0]))


def compare_dicts(
    dict_obj_1,
    dict_obj_2,
    sub_elements: dict | None = None,
    ignore: list[str] | None = None,
):
    if not sub_elements:
        sub_elements = {}

    level_dict = {}

    if dict_obj_1 is None and dict_obj_2 is None:
        return None
    if dict_obj_1 is None or dict_obj_2 is None:
        list_keys = list(dict_obj_1.keys() if dict_obj_2 is None else dict_obj_2.keys())
    else:
        list_keys = list(set(dict_obj_1.keys()).union(set(dict_obj_2.keys())))
    list_keys.sort()

    diffs = []

    for key in list_keys:
        if ignore is not None and any([re.match(i, key) for i in ignore]):
            continue
        value_1, value_2 = (
            dict_obj_1.get(key, None) if dict_obj_1 is not None else None,
            dict_obj_2.get(key, None) if dict_obj_2 is not None else None,
        )
        ref_element = value_1 if value_1 is not None else value_2

        if key in sub_elements and value_1 is None and value_2 is None:
            level_dict[key] = None

        elif type(ref_element) == dict:
            level_dict[key] = compare_dicts(
                value_1,
                value_2,
                sub_elements.get(key, {}).get("sub_elements", None),
                sub_elements.get(key, {}).get("ignore", None),
            )
            diff = level_dict[key]["diff"]
            diffs.append(diff)
        elif type(ref_element) == list and key in sub_elements:
            sub_elements_1 = (
                {x[sub_elements[key]["key"]]: x for x in value_1}
                if value_1 is not None
                else None
            )
            sub_elements_2 = (
                {x[sub_elements[key]["key"]]: x for x in value_2}
                if value_2 is not None
                else None
            )
            sub_elements_1 = (
                sub_elements_1
                if sub_elements_1 is not None
                else {x: None for x in sub_elements_2.keys()}
            )
            sub_elements_2 = (
                sub_elements_2
                if sub_elements_2 is not None
                else {x: None for x in sub_elements_1.keys()}
            )
            list_keys = list(
                set(sub_elements_1.keys()).union(set(sub_elements_2.keys()))
            )

            dict_list = {}
            for list_key in list_keys:
                dict_list[list_key] = compare_dicts(
                    sub_elements_1.get(list_key, None),
                    sub_elements_2.get(list_key, None),
                    sub_elements[key]["sub_elements"],
                    ignore=sub_elements.get(key, {}).get("ignore", None),
                )

            if "key_type" in sub_elements[key]:
                dict_list = {
                    sub_elements[key]["key_type"](x): y for x, y in dict_list.items()
                }

            level_dict[key] = list(dict(sorted(dict_list.items())).values())
            diff = any(x["diff"] for x in dict_list.values())
            diffs.append(diff)
        else:
            diff = True
            if (value_1 is None and value_2 is None) or (value_1 == value_2):
                diff = False
            level_dict[key] = {"values": [value_1, value_2], "diff": diff}
            diffs.append(diff)

    level_dict = dict(sorted(level_dict.items()))

    level_dict["diff"] = any(diffs)
    return level_dict


def get_sub_lists(a_list: list, lenght: int):
    a_list = list(a_list)
    return [a_list[i : i + lenght] for i in range(0, len(a_list), lenght)]


def is_iterable(o):
    try:
        iter(o)
        return True
    except:
        return False


def is_list(o):
    return type(o) == list or is_subtype(type(o), list) or type(o) == tuple
