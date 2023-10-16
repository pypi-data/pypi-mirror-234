# MODULS
import dataclasses, traceback
import enum, inspect, operator, re, copy

from dataclasses import dataclass, field, _MISSING_TYPE, asdict
from collections import OrderedDict

# LOGGER
from ..logger import AlphaLogger

# LIBS
from ...libs import py_lib, json_lib, string_lib

# LOCALS
from ._enum import MappingMode
from ._exception import AlphaException

FORCE_AUTO_MAP = True


class AlphaMappingAttribute:
    def __init__(
        self,
        name: str,
        key: str | None = None,
        fct: object = None,
        required: bool = False,
        flat: bool = False,
    ):
        self.name = name
        self.key = key or name
        self.fct = fct
        self.required = required
        self.flat = flat


def get_score_dict_best_match(score_dict: dict[str, int]) -> str:
    max_keys = [
        x
        for x, y in score_dict.items()
        if y == max(score_dict.items(), key=lambda k: k[1])[1]
    ]
    min_size = min(max_keys, key=len)
    best_matchs = [x for x in max_keys if len(x) == len(min_size)]
    if len(best_matchs) > 1:
        print(f"ERROR: multiple match {best_matchs}")
    return best_matchs[0]


def is_auto_map(dataclass_type, mapping_mode: MappingMode | str | None = None) -> bool:
    if not hasattr(dataclass_type, "auto_map_from_dict"):
        return False
    if dataclass_type.get_mapping_mode() is not None and mapping_mode is None:
        mapping_mode = dataclass_type.get_mapping_mode()
    elif mapping_mode is None:
        mapping_mode = MappingMode.STRICT

    mapping_mode_str = str(mapping_mode)
    if type(mapping_mode) != str:
        mapping_mode_str: str = str(mapping_mode.value)
    mapping_mode_str = mapping_mode_str.lower()

    match mapping_mode_str:
        case MappingMode.AUTO.value:
            return True
    return False


class AlphaClass:
    _map: MappingMode | None = None
    _map_keys: dict[str, str] | None = None
    _no_map: list[str] | None = None

    def __init__(self, *args, log: AlphaLogger | None = None, **kwargs):
        self._init_args: dict = {"args": args, "kwargs": kwargs}
        self._children: list = []
        self._logger = log
        self._piles: dict[str, list[str]] = {}

    def make_child(self, child_cls, *args, **kwargs):
        if args is None:
            args = self._init_args["args"]
        if kwargs is None:
            kwargs = self._init_args["kwargs"]
        child = child_cls(self, *args, **kwargs)
        self._children.append(child)
        return child

    def get_children(self):
        return self._children

    @classmethod
    def get_mapping_mode(class_):
        return class_._map

    def get_attributes(self):
        return py_lib.get_attributes(self)

    def to_json(
        self,
        columns: list | None = None,
        rejected: list | None = None,
        not_none: bool = False,
        not_empty: bool = False,
    ):
        """d_rejected = [
            "_map",
            "_map_keys",
            "_no_map",
            "_piles",
            "_init_args",
            "_children",
            "_log",
        ]
        if rejected is not None:
            d_rejected.extend(rejected)"""
        dict_output = {}
        for x, y in self.get_attributes().items():
            if columns is not None and x not in columns:
                continue
            if x.startswith("_"):
                continue
            if not_none and y is None:
                continue
            is_iterable = py_lib.is_iterable(y)
            if not_empty and y is not None and is_iterable and len(y) == 0:
                continue
            dict_output[x] = json_lib.jsonify_data(
                y
            )  # if not hasattr(y, "to_json") or inspect.isclass(y) else y.to_json()
        return dict_output

    def __log(self, stack, message, ex=None, out: bool = False):
        if not stack in self._piles:
            self._piles[stack] = []
        pile = self._piles[stack]

        if self._logger is not None:
            method = getattr(self._logger, stack)
            if len(pile) != 0:
                for deb in pile:
                    method(deb, ex=ex)
                stack = []
            method(message, ex=ex)
        else:
            pile.append(message)
            if out:
                for stack, msg in self._piles.items():
                    print(f"{stack}: {msg}")
                if ex:
                    print(ex)

    def debug(self, message, ex=None):
        self.__log(inspect.stack()[0][3], message=message, ex=ex)

    def info(self, message, ex=None):
        self.__log(inspect.stack()[0][3], message=message, ex=ex)

    def warning(self, message, ex=None):
        self.__log(inspect.stack()[0][3], message=message, ex=ex)

    def error(self, message, out=False, ex=None):
        self.__log(inspect.stack()[0][3], message=message, ex=ex, out=out)
        if out:
            exit()

    def critical(self, message, out=False, ex=None):
        self.__log(inspect.stack()[0][3], message=message, ex=ex, out=out)
        if out:
            exit()

    def map_from_inputs(
        self, map_entries: list[AlphaMappingAttribute], inputs: dict[str, object]
    ):
        mapped = []
        for key in inputs:
            for mapping_attribute in map_entries:
                if mapping_attribute.name in mapped:
                    continue

                if key.endswith(mapping_attribute.key):
                    value = inputs[key]
                    if mapping_attribute.fct is not None and value is not None:
                        value = mapping_attribute.fct(value)

                    setattr(self, mapping_attribute.name, value)
                    mapped.append(mapping_attribute.name)

    def copy(self):
        return copy.copy(self)


DATACLASS_AUTO_MAP_MATCHS = {}


def convert_value(value: object, type_):
    if value is None:
        return None
    if type_ != bool:
        try:
            value = type_(value)
        except:
            pass
        if str(value).lower() in ["none", "null", "undefined"]:
            value = None
        return None if value is None else value
    else:
        str_val = str(value).upper()
        return (
            False
            if value is None
            else ("Y" in str_val or "T" in str_val or "1" in str_val)
        )


def identify(search_key: str, dict_keys: list[str], dataclass_type):
    identified_k = None
    for dict_key in dict_keys:
        if search_key in dict_key or dict_key in search_key:
            identified_k = dict_key
            dict_keys.remove(identified_k)
            break
    score = 100
    if identified_k is None:
        identified_k, score = string_lib.found_best_match(
            search_key, dict_keys, threshold=50
        )

        if identified_k is None:
            # print(f"{dataclass_type}: Cannot find a match for {search_key}")
            return None, score
    return identified_k, score


def get_association(key: str, associations: dict[str, str] = {}):
    associations = {
        x: y if type(associations[x]) != AlphaMappingAttribute else y.key
        for x, y in associations.items()
    }
    ass_matchs = [x for x, y in associations.items() if y == key]

    if len(ass_matchs) != 0:
        return ass_matchs[0]
    return None


def full_identify(
    dataclass_type,
    dict_key: str,
    fields_keys: list[str],
    associations: dict[str, str] = {},
    no_match: list[str] = [],
):
    patterns = {}
    required = False

    for x in fields_keys:
        if x in no_match:
            continue
        if x in associations:
            if type(associations[x]) == AlphaMappingAttribute:
                required = associations[x].required
                patterns[x] = associations[x].key
            else:
                patterns[x] = associations[x]
        else:
            patterns[x] = x

    patterns = OrderedDict(sorted(patterns.items(), key=lambda x: x[1], reverse=True))
    for field_name, k in patterns.items():
        if dict_key == field_name:
            return field_name, 100

    for field_name, k in patterns.items():
        matchs = re.findall(k, dict_key)
        if len(matchs) != 0:
            return field_name, 100

    identified_v, score = identify(dict_key, list(patterns.values()), dataclass_type)
    # print(f"    Idenfitied {dict_key} to {identified_v} with score {score}")

    if identified_v is None:
        if required:
            return None, 0
        return None, 0  # "CONTINUE"

    ass_matchs = [x for x, y in associations.items() if y == identified_v]
    if identified_v in associations.values() and dict_key not in ass_matchs:
        return None, 0

    set_1 = set(identified_v.split("_"))
    set_2 = set(dict_key.split("_"))
    is_common_part = len(list(set_1 & set_2)) != 0

    if not is_common_part:
        # print(f"{dataclass_type}: Weird match for {dict_key} with {identified_k}")
        return None, 0

    identified_k = [x for x, y in patterns.items() if y == identified_v][0]

    if identified_k in patterns:
        matchs = re.findall(patterns[identified_k], dict_key)
        if len(matchs) == 0:
            return None, 0

    return identified_k, score


@dataclass
class AutoMapping(AlphaClass):
    dataclass_type: object
    associations: dict[str, str] = field(default_factory=lambda: {})
    no_match: list[str] = field(default_factory=lambda: [])

    object_fields: dict[str, object] = field(default_factory=lambda: {})
    dict_fields: dict[str, object] = field(default_factory=lambda: {})
    list_fields: dict[str, object] = field(default_factory=lambda: {})
    flat_fields: dict[str, object] = field(default_factory=lambda: {})

    identified_object_fields: dict[str, object] = field(default_factory=lambda: {})
    identified_dict_fields: dict[str, object] = field(default_factory=lambda: {})
    identified_list_fields: dict[str, object] = field(default_factory=lambda: {})

    matchs_object_fields: dict[str, object] = field(default_factory=lambda: {})
    matchs_dict_fields: dict[str, object] = field(default_factory=lambda: {})
    matchs_list_fields: dict[str, object] = field(default_factory=lambda: {})

    already_assigned: list[str] = field(default_factory=lambda: [])

    is_identified: bool = False
    flat: bool = False

    def __post_init__(self):
        self.__set_fields_types()

    def __set_fields_types(self):
        for x, y in self.dataclass_type.__dataclass_fields__.items():
            if py_lib.is_subtype(y.type, list) or py_lib.is_subtype(y.type, list):
                self.list_fields[x] = y
            elif is_dataclass(y.type):
                self.dict_fields[x] = y
            else:
                self.object_fields[x] = y
        pass

    def identify(self, dict_values: dict[str, object]):
        dict_elements = {
            x: y for x, y in dict_values.items() if type(y) == dict or y is None
        }
        list_elements = {
            x: y for x, y in dict_values.items() if type(y) == list or y is None
        }
        other_elements = {
            x: y for x, y in dict_values.items() if type(y) != list or type(y) != dict
        }

        fields_groups = [
            (
                list_elements,
                self.list_fields,
                self.identified_list_fields,
                self.matchs_list_fields,
            ),
            (
                dict_elements,
                self.dict_fields,
                self.identified_dict_fields,
                self.matchs_dict_fields,
            ),
            (
                other_elements,
                self.object_fields,
                self.identified_object_fields,
                self.matchs_object_fields,
            ),
        ]

        identified = []
        for sub_dict_values, fields_dict, identified_dict, matchs in fields_groups:
            for dict_key in sub_dict_values.keys():
                identified_k = get_association(dict_key, self.associations)
                if identified_k is not None:
                    if not identified_k in matchs:
                        matchs[identified_k] = {}
                    matchs[identified_k][dict_key] = 100
                    identified.append(dict_key)

            for dict_key in sub_dict_values.keys():
                if dict_key in identified:
                    continue
                identified_k, score = full_identify(
                    self.dataclass_type,
                    dict_key,
                    list(fields_dict.keys()),
                    self.associations,
                    self.no_match,
                )
                if identified_k is None:
                    continue
                if not identified_k in matchs:
                    matchs[identified_k] = {}
                matchs[identified_k][dict_key] = score

            for field_key, score_dict in matchs.items():
                best_match = get_score_dict_best_match(score_dict)
                if field_key in fields_dict:
                    identified_dict[best_match] = fields_dict[field_key]
                    identified.append(best_match)

    def __identify_flat(self, dict_values: dict[str, object]):
        identified = []
        for dict_key in dict_values.keys():
            identified_k = get_association(dict_key, self.associations)
            if identified_k is not None:
                if not identified_k in self.matchs_object_fields:
                    self.matchs_object_fields[identified_k] = {}
                self.matchs_object_fields[identified_k][dict_key] = 100
                identified.append(dict_key)

        for dict_key in dict_values.keys():
            if dict_key in identified:
                continue
            identified_k, score = full_identify(
                self.dataclass_type,
                dict_key,
                list(self.object_fields.keys()),
                self.associations,
                self.no_match,
            )
            if identified_k is None:
                continue

            if not identified_k in self.matchs_object_fields:
                self.matchs_object_fields[identified_k] = {}
            self.matchs_object_fields[identified_k][dict_key] = score

        for field_key, score_dict in self.matchs_object_fields.items():
            best_match = get_score_dict_best_match(score_dict)
            if field_key in self.object_fields:
                self.identified_object_fields[best_match] = self.object_fields[
                    field_key
                ]

    def __map_flat(
        self,
        dict_values: dict[str, object],
        mapping_mode: MappingMode | str | None = None,
    ):
        if not self.is_identified:
            self.__identify_flat(dict_values)

        field_values = {}
        for (
            key,
            fd,
        ) in self.identified_object_fields.items():
            field_type = py_lib.get_first_non_none_type(fd.type)
            field_values[fd.name] = convert_value(dict_values[key], field_type)

        for fd in self.dict_fields.values():
            field_type = py_lib.get_first_non_none_type(fd.type)
            field_values[fd.name] = field_type.map_from_dict(
                dict_values={
                    x: y for x, y in dict_values.items() if not x in field_values
                },
                mapping_mode=mapping_mode,
            )

        return field_values

    def map(
        self,
        dict_values: dict[str, object],
        mapping_mode: MappingMode | str | None = None,
    ):
        if self.flat:
            return self.__map_flat(dict_values)

        if not self.is_identified:
            self.identify(dict_values)

        field_values = {}
        for (
            key,
            fd,
        ) in self.identified_object_fields.items():
            field_type = py_lib.get_first_non_none_type(fd.type)
            field_values[fd.name] = convert_value(dict_values[key], field_type)

        for (
            key,
            fd,
        ) in self.identified_dict_fields.items():
            field_type = py_lib.get_first_non_none_type(fd.type)
            field_values[fd.name] = (
                field_type.map_from_dict(
                    dict_values=dict_values[key], mapping_mode=mapping_mode
                )
                if dict_values[key] is not None
                else None
            )

        for (
            key,
            fd,
        ) in self.identified_list_fields.items():
            sub_type = fd.type.__args__[0]
            if hasattr(sub_type, "auto_map_from_dict"):
                field_values[fd.name] = (
                    [
                        (
                            sub_type.auto_map_from_dict(
                                dict_values=f, mapping_mode=mapping_mode
                            )
                            if f is not None
                            else None
                        )
                        for f in dict_values[key]
                    ]
                    if dict_values[key] is not None
                    else []
                )
            else:
                if type(dict_values[key]) == str:
                    field_values[fd.name] = string_lib.to_list(dict_values[key])
                else:
                    field_values[fd.name] = (
                        [
                            (sub_type(f) if f is not None else None)
                            for f in dict_values[key]
                        ]
                        if dict_values[key] is not None
                        else []
                    )
        return field_values


def convert_value_from_field(
    field_type, value, mapping_mode: MappingMode | str | None = None
):
    field_type = py_lib.get_first_non_none_type(field_type)
    if value is None:
        return None
    if is_dataclass(field_type):
        return field_type.map(
            asdict(value) if is_dataclass(value) else value, mapping_mode=mapping_mode
        )
    elif isinstance(value, list) and all(isinstance(item, dict) for item in value):
        return [convert_value_from_field(field_type, item) for item in value]
    else:
        try:
            return convert_value(value, field_type)
        except:
            return value


class AlphaDataclass(AlphaClass):
    def get_fields_dict(self, keys: list[str] | None = None) -> dict:
        dct = {}
        # dct['_tname'] = self.__class__.__name__

        for fd in dataclasses.fields(self):
            # field_type = py_lib.get_first_non_none_type(fd.type)
            value = getattr(self, fd.name)
            if hasattr(value, "get_fields_dict"):
                value = value.get_fields_dict()
            else:
                value = value
            if keys is not None and fd.name not in keys:
                continue
            dct[fd.name] = value

        return dct

    def compare(
        self, other, attrs_list: list[str], attrs_eq: dict[str, str] = None
    ) -> bool:
        if not isinstance(other, self.__class__) and not issubclass(
            self.__class__, other.__class__
        ):
            raise AlphaException(
                description=f"Cannot compare {self.__class__} object with {other.__class__} object"
            )

        [attrs_list.append(attr) for attr in (attrs_eq if attrs_eq is not None else [])]

        compared = []
        for attr in attrs_list:
            if hasattr(self, attr):
                self_attr, other_attr = getattr(self, attr), getattr(other, attr)

                custom_eq = (
                    attrs_eq[attr]
                    if attrs_eq is not None and attr in attrs_eq
                    else None
                )

                if (self_attr is None and other_attr is not None) or (
                    other_attr is None and self_attr is not None
                ):
                    compared.append(False)
                elif self_attr is None and other_attr is None:
                    compared.append(True)
                elif custom_eq is not None:
                    compared.append(getattr(self_attr, custom_eq)(other_attr))
                else:
                    compared.append(getattr(self_attr, "__eq__")(other_attr))
            else:
                raise AlphaException(
                    description=f"{self.__class__.__name__} object has no attribute {attr}"
                )

        return all(compared)

    def check_attrs_not_none(self, attrs_list: list[str]) -> bool | None:
        if attrs_list is None:
            return

        for attr in attrs_list:
            if hasattr(self, attr):
                self_attr = getattr(self, attr)
                if self_attr is None:
                    raise AlphaException(
                        description=f"{self.__class__.__name__} '{attr}' cannot be 'None'"
                    )
            else:
                raise AlphaException(
                    description=f"{self.__class__.__name__} object has no attribute {attr}"
                )

        return True

    def check_attrs_none(self, attrs_list: list[str]) -> bool | None:
        if attrs_list is None:
            return

        for attr in attrs_list:
            if hasattr(self, attr):
                self_attr = getattr(self, attr)
                if self_attr is not None:
                    raise AlphaException(
                        description=f"{self.__class__.__name__} '{attr}' must be 'None'"
                    )
            else:
                raise AlphaException(
                    description=f"{self.__class__.__name__} object has no attribute {attr}"
                )

        return True

    def replace_empty_with_none(self, attrs_list: list[str]) -> bool | None:
        if attrs_list is None:
            return

        for attr in attrs_list:
            if hasattr(self, attr):
                self_attr = getattr(self, attr)
                if self_attr == "":
                    self.__dict__[attr] = None
            else:
                raise AlphaException(
                    description=f"{self.__class__.__name__} object has no attribute {attr}"
                )

        return True

    def check_attributes_max_lenght(self, attrs_list: list[tuple[str, int]]):
        if attrs_list is None:
            return

        for attr, max_length in attrs_list:
            if hasattr(self, attr):
                self_attr = getattr(self, attr)
                if self_attr is not None and len(self_attr) > max_length:
                    raise AlphaException(
                        description=f"{self.__class__.__name__} {attr=} length={len(self_attr)} is > than {max_length=}"
                    )
            else:
                raise AlphaException(
                    description=f"{self.__class__.__name__} object has no {attr=}"
                )

        return True

    def update_from_auto_map_from_dict(
        self,
        dict_values: dict[str, object],
        associations: dict[str, str] = {},
        no_match: list[str] = [],
        flat: bool = False,
    ):
        instance = self.auto_map_from_dict(
            dict_values, associations, no_match, flat=flat
        )

        for key, fd in instance.__dict__.items():
            if fd is not None:
                setattr(self, key, fd)

    def flatten(self, parent: str | None = None):
        output = {}
        for key, field in self.__dataclass_fields__.items():
            if not key in self.__dict__:
                value = field.default
            else:
                value = self.__dict__[key]
            value_key = f"{parent}.{key}" if parent is not None else key

            if value is None:
                output[value_key] = None
            elif isinstance(value, AlphaDataclass):
                for k, v in value.flatten(parent=key).items():
                    output[k] = v
            elif type(value) == dict:
                for k, v in value.items():
                    output[f"{value_key}.{k}"] = v
            elif py_lib.is_list(value):
                output[value_key] = []
                for el in value:
                    if isinstance(el, AlphaDataclass):
                        output[value_key].append(el.flatten())
                    else:
                        output[value_key].append(el)
            else:
                output[value_key] = value
        return output

    @classmethod
    def get_fields_names(dataclass_type, init_only: bool = False):
        return [
            f.name
            for f in dataclasses.fields(dataclass_type)
            if (init_only and f.init) or not init_only
        ]

    @classmethod
    def get_fields(dataclass_type, init_only: bool = False):
        return [
            f
            for f in dataclasses.fields(dataclass_type)
            if (init_only and f.init) or not init_only
        ]

    @classmethod
    def auto_map_from_dict(
        dataclass_type,
        dict_values: dict[str, object],
        associations: dict[str, str] = {},
        no_match: list[str] = [],
        flat: bool = False,
    ):
        global DATACLASS_AUTO_MAP_MATCHS, FORCE_AUTO_MAP
        if dict_values is None or len(dict_values) == 0:
            return dataclass_type()

        dataclass_name = str(dataclass_type).split(".")[-1].replace("'>", "")
        uuid = f"{dataclass_name}({','.join(list(dict_values.keys()))})"

        # FIELDS
        if not uuid in DATACLASS_AUTO_MAP_MATCHS or FORCE_AUTO_MAP:
            DATACLASS_AUTO_MAP_MATCHS[uuid] = AutoMapping(
                dataclass_type, associations=associations, no_match=no_match, flat=flat
            )

        fields_values = DATACLASS_AUTO_MAP_MATCHS[uuid].map(dict_values)

        instance = None
        required_fields = [
            x
            for x, y in dataclass_type.__dataclass_fields__.items()
            if type(y.default) == _MISSING_TYPE
            and type(y.default_factory) == _MISSING_TYPE
        ]
        is_required_fields = set(required_fields).intersection(
            fields_values.keys()
        ) == set(required_fields)
        if not is_required_fields:
            return None
        try:
            if hasattr(dataclass_type, "map_from_dict"):
                instance = dataclass_type.map_from_dict(
                    fields_values, mapping_mode=MappingMode.STRICT
                )
            else:
                fields_values = {
                    x: y
                    for x, y in fields_values.items()
                    if x in dataclass_type.get_fields_names(True)
                }
                instance = dataclass_type(**fields_values)
        except Exception as ex:
            print(f"Error mapping {dataclass_type}")
            tb = traceback.format_exc()
            raise ex
        return instance

    @classmethod
    def map_from_json(
        dataclass_type, dict_values: str, mapping_mode: MappingMode | str | None = None
    ):
        dict_values = (
            json_lib.load_json(dict_values)
            if type(dict_values) != dict
            else dict_values
        )
        try:
            obj = dataclass_type.map_from_dict(dict_values, mapping_mode=mapping_mode)
        except Exception as ex:
            print(f"Failed to map {dataclass_type} with: {dict_values}")
            print(ex)
            obj = None
        return obj

    @classmethod
    def map_from_dict(
        dataclass_type,
        dict_values: dict[str, object] | dict[str, str],
        mapping_mode: MappingMode | str | None = None,
    ):
        if is_auto_map(dataclass_type, mapping_mode=mapping_mode):
            return dataclass_type.auto_map_from_dict(dict_values=dict_values)

        if not isinstance(dict_values, dict):
            return None

        if dict_values is None:
            return None

        field_values = {}
        for key, value in dict_values.items():
            no_match = False
            if dataclass_type._map_keys is not None:
                for ck, regex in dataclass_type._map_keys.items():
                    if regex.startswith("re:"):
                        matchs = re.findall(regex[3:], key)
                        if len(matchs) != 0:
                            key = ck
                            break
                    elif regex == key:
                        key = ck
                        break
            if dataclass_type._no_map is not None:
                for regex in dataclass_type._no_map:
                    if regex.startswith("re:"):
                        matchs = re.findall(regex[3:], key)
                        if len(matchs) != 0:
                            no_match = True
                            break
                    elif regex == key:
                        no_match = True
                        break
            if no_match:
                continue

            if key not in dataclass_type.__dataclass_fields__:
                continue

            field = dataclass_type.__dataclass_fields__[key]
            field_type = py_lib.get_first_non_none_type(field.type)

            if not field.init:
                continue

            if py_lib.is_subtype(field_type, list):
                field_values[key] = []
                if value is not None:
                    field_values[key] = [
                        convert_value_from_field(
                            py_lib.get_subtype(field_type), v, mapping_mode=mapping_mode
                        )
                        for v in value
                    ]
            else:
                field_values[key] = convert_value_from_field(
                    field_type, value, mapping_mode=mapping_mode
                )

        try:
            dc = dataclass_type(**field_values)
        except Exception as ex:
            dc = None
            if "missing" in str(ex) and "required" in str(ex):
                return None
            raise ex
        return dc

    @classmethod
    def map(
        dataclass_type, dict_values: dict, mapping_mode: MappingMode | str | None = None
    ):
        if dataclass_type.get_mapping_mode() is not None and mapping_mode is None:
            mapping_mode = dataclass_type.get_mapping_mode()
        elif mapping_mode is None:
            mapping_mode = MappingMode.STRICT

        mapping_mode_str = str(mapping_mode)
        if type(mapping_mode) != str:
            mapping_mode_str: str = str(mapping_mode.value)
        mapping_mode_str = mapping_mode_str.lower()

        match mapping_mode_str:
            case MappingMode.AUTO.value:
                return dataclass_type.auto_map_from_dict(dict_values)

        return dataclass_type.map_from_dict(dict_values, mapping_mode)


def is_dataclass(o):
    if dataclasses.is_dataclass(o):
        return True
    if isinstance(o, AlphaDataclass) or (
        isinstance(o, type) and issubclass(o, AlphaDataclass)
    ):
        return True
    return py_lib.is_subtype(o, AlphaDataclass)
