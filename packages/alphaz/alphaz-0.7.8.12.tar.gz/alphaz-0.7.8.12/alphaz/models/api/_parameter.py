# MODULES
import ujson, datetime, re, sqlalchemy, xmltodict

from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import inspect as inspect_sqlalchemy

from flask import request
from collections.abc import Callable

# MAIN
from ..main import AlphaException
from ..main._base import is_dataclass
from ..main._enum import MappingMode, ParameterMode

# LIBS
from ...libs import date_lib, json_lib, py_lib, string_lib


# TODO: remove form
def convert_parameter_value(
    name: str,
    value,
    ptype,
    form,
    mode=None,
    map_none: bool = False,
    required: bool = False,
    mapping_mode: MappingMode | None = None,
):
    str_value = str(value).lower()
    if py_lib.is_subtype(ptype, bool):
        if str_value in ["y", "true", "t", "1"]:
            value = True
        elif str_value in ["n", "false", "f", "0"]:
            value = False
        elif not required and value is None:
            value = None
        else:
            raise AlphaException(
                f"Wrong value <{value}> for parameter <{name}> of type <bool>",
            )
        value = value
    elif py_lib.is_subtype(ptype, int):
        try:
            value = int(value) if value is not None else None
        except:
            raise AlphaException(
                f"Wrong value <{value}> for parameter <{name}> of type <int>"
            )
    elif py_lib.is_subtype(ptype, float):
        try:
            value = float(value)
        except:
            raise AlphaException(
                f"Wrong value <{value}> for parameter <{name}> of type <float>"
            )
    elif ptype == datetime.datetime:
        value = date_lib.str_to_datetime(value)
    elif py_lib.is_subtype(ptype, dict):
        value = json_lib.load_json(value)
    elif str_value in ["null()"]:
        value = sqlalchemy.null()
    elif str_value in [
        "null",
        "none",
        "undefined",
    ]:
        value = None
    elif is_dataclass(ptype):
        if hasattr(ptype, "map_from_json"):
            value = ptype.map_from_json(value, mapping_mode=mapping_mode)
        else:
            try:
                P = ujson.loads(value)
            except Exception as ex:
                raise ex
            value = ptype(**P)
    elif isinstance(ptype, DeclarativeMeta):  # DB MODEL
        if value is None:
            parameters = {x: y for x, y in form.items() if hasattr(ptype, x)}
        else:
            parameters = value if type(value) == dict else json_lib.load_json(value)
            parameters = {
                x: y
                for x, y in parameters.items()
                if hasattr(ptype, x) and (map_none or y is not None)
            }  # TODO: enhance
        value = dict_to_model(ptype, parameters)
    elif hasattr(ptype, "metadata") and not hasattr(
        value, "metadata"
    ):  # classic dataclass
        r = ujson.loads(value)
        value = ptype(**r)
    elif py_lib.is_subtype(ptype, str):
        if mode in [
            ParameterMode.LIKE,
            ParameterMode.IN_LIKE,
            ParameterMode.START_LIKE,
            ParameterMode.END_LIKE,
        ]:
            value = set_value_like_mode(value, mode)
    return value


def dict_to_model(model, parameters):
    from core import core

    inspected = inspect_sqlalchemy(model)

    """for key, col in dict(model.__dict__).items():
    if not hasattr(col, "prop"):
        continue

    binary_expression = type(col.expression) is BinaryExpression
    column_property = isinstance(col.prop, ColumnProperty)-

    if not relationship and (column_property and not binary_expression):
        attributes[key] = col"""

    #! TOTO: modify
    """if disabled_relationships:
        if (column_property or isinstance(col.prop, RelationshipProperty)) and not binary_expression and key not in disabled_relationships:
            attributes[key] = col"""
    for relationship, relationship_property in inspected.relationships.items():
        if relationship in parameters:
            relationship_table_name = relationship_property.target.key
            relationship_model = core.db.get_table_model(relationship_table_name)
            parameters[relationship] = dict_to_model(
                relationship_model, parameters[relationship]
            )
    M = (
        model(**{x: y for x, y in parameters.items() if x in model.__dict__})
        if type(parameters) != list
        else [
            model(**{x: y for x, y in p.items() if x in model.__dict__})
            for p in parameters
        ]
    )
    return M  # TODO: enhanced multi rel


def set_value_like_mode(value, mode):
    if value is None:
        return None
    value = str(value).replace("*", "%")

    if not value.startswith("%") and mode in [
        ParameterMode.IN_LIKE,
        ParameterMode.START_LIKE,
    ]:
        value = f"%{value}"

    if not value.endswith("%") and mode in [
        ParameterMode.IN_LIKE,
        ParameterMode.END_LIKE,
    ]:
        value = f"{value}%"
    return value


class Parameter:
    _value = None
    no_log: bool = False

    def __init__(
        self,
        name: str,
        default=None,
        empty_value=None,
        none_value=None,
        options=None,
        cacheable: bool = True,
        required: bool = False,
        ptype: type = str,
        private: bool = False,
        mode: ParameterMode = ParameterMode.NONE,
        override: bool = False,
        function: Callable | None = None,
        mapping_mode: MappingMode | str | None = None,
        map_none: bool = False,
        max_size: int | None = None,
        min_size: int | None = None,
        max_value: int | None = None,
        min_value: int | None = None,
        separators: list = [",", ";"],
    ):
        """[summary]

        Args:
            name (str): [description]
            default ([type], optional): [description]. Defaults to None.
            options ([type], optional): [description]. Defaults to None.
            cacheable (bool, optional): [description]. Defaults to True.
            required (bool, optional): [description]. Defaults to False.
            ptype (type, optional): [description]. Defaults to str.
            private (bool, optional): [description]. Defaults to False.
            mode (str, optional): [description]. Defaults to "none".
        """
        self.name = name
        self.default = default
        self.cacheable = cacheable
        self.empty_value = empty_value
        self.none_value = none_value
        self.options = options
        self.required = required
        self.ptype: type = ptype
        self.function: Callable = function
        self.type = str(ptype).replace("<class '", "").replace("'>", "")
        self.private = private
        self.mode = mode
        self.override = override
        self.is_value = False
        self.mapping_mode = mapping_mode
        self.max_size = max_size
        self.min_size = min_size
        self.map_none = map_none
        self.max_value = max_value
        self.min_value = min_value

    @property
    def value(self):
        return self._value if self._value is not None or self.is_value else self.default

    def __check_options(self, value):
        if (
            self.options is not None
            and value not in self.options
            and not (not self.required and value is None)
        ):
            raise AlphaException(
                "api_wrong_parameter_option",
                parameters={
                    "value": value,
                    "parameter": self.name,
                    "options": str(self.options),
                },
            )

    def _get_value_from_request(self, dataDict, api_json, form, args):
        if "<xml>" in str(request.data):
            try:
                data = xmltodict.parse(request.data)
                if self.name in data["xml"]:
                    self._value = data["xml"][self.name]
            except:
                pass

        if form is not None and self.name in form:
            self._value = form[self.name]
            self.is_value = True
        elif api_json is not None and self.name in api_json:
            self._value = api_json[self.name]
            self.is_value = True
        elif (
            self.name in args
            and self.name in dataDict
            and (self.ptype == list or py_lib.is_subtype(self.ptype, list))
            and (len(dataDict[self.name]) != 1)
        ):
            self._value = dataDict[self.name]
            self.is_value = True
        elif self.name in args:
            self._value = args.get(self.name)
            self.is_value = True
        elif self.name in dataDict:
            self._value = dataDict[self.name]
            self.is_value = True

    def _check_min_max_value(self):
        if (
            self.max_value is not None
            and self._value is not None
            and type(self._value) in [int, float]
            and self._value > self.max_value
        ):
            raise AlphaException(
                "api_parameter_value_above_max",
                parameters={
                    "parameter": self.name,
                    "value": self._value,
                    "max_value": self.max_value,
                },
            )
        if (
            self.min_value is not None
            and self._value is not None
            and type(self._value) in [int, float]
            and self._value < self.min_value
        ):
            raise AlphaException(
                "api_parameter_value_below_min",
                parameters={
                    "parameter": self.name,
                    "value": self._value,
                    "min_value": self.min_value,
                },
            )

    def _check_sizes(self):
        # check size
        if (
            self.max_size is not None
            and self._value is not None
            and len(self._value) > self.max_size
        ):
            raise AlphaException(
                "api_parameter_length_too_long",
                parameters={
                    "parameter": self.name,
                    "size": len(self.value),
                    "value": self._value,
                    "max": self.max_size,
                },
            )
        if (
            self.min_size is not None
            and self._value is not None
            and len(self._value) < self.min_size
        ):
            raise AlphaException(
                "api_parameter_length_too_short",
                parameters={
                    "parameter": self.name,
                    "size": len(self.value),
                    "value": self._value,
                    "min": self.min_size,
                },
            )

    def _check_none(self, form) -> bool:
        if self._value is None and form is not None and self.name in form:
            self._value = form[self.name]

        if self._value is not None and str(self._value).lower() in [
            "null",
            "none",
            "undefined",
        ]:
            self._value = self.none_value if self.is_value else None
            self.__check_options(self._value)
            return False
        if self._value is None:
            self.__check_options(self._value)
            self._value = self.default
        if self._value is None and self.required:
            raise AlphaException(f"Parameter {self.name} is required")
        return self._value is not None

    def _process_list_value(self, dataDict, form) -> bool:
        if not py_lib.is_subtype(self.ptype, list):
            return False
        is_empty = self._value is None or str(self._value).strip() == ""
        if is_empty:
            self._value = []
            return True

        is_not_list_format = all(not x in str(self._value) for x in [";", ",", "["])

        if is_not_list_format:
            dataDict = {x.strip(): y for x, y in dataDict.items()}
            self._value = (
                dataDict[self.name] if self.name in dataDict else [self._value]
            )

        if self._value is None:
            return True

        sub_type = py_lib.get_subtype(self.ptype)
        if is_dataclass(sub_type):
            values = re.findall(r"{[^{]*}", str(self._value))
            self._value = []
            for val in values:
                if hasattr(sub_type, "map_from_json"):
                    val = sub_type.map_from_json(val, mapping_mode=self.mapping_mode)
                else:
                    P = ujson.loads(val)
                    val = sub_type(**P)
                self._value.append(val)
        else:
            if not py_lib.is_subtype(self._value, list):
                self._value = string_lib.str_to_str_list(
                    str(self._value), separators=[",", ";"]
                )

            self._value = [
                convert_parameter_value(
                    self.name, x, py_lib.get_subtype(self.ptype), form
                )
                for x in self._value
            ]

            for val in self._value:
                self.__check_options(val)

            if self.mode in [
                ParameterMode.LIKE,
                ParameterMode.IN_LIKE,
                ParameterMode.START_LIKE,
                ParameterMode.END_LIKE,
            ]:
                self._value = [set_value_like_mode(x, self.mode) for x in self._value]
        return True

    def set_value(self, dataDict: dict, api_json, form, args):
        """Set parameter value

        Raises:
            AlphaException: [description]
        """
        dataDict = {x.strip(): y for x, y in dataDict.items()}

        self._value = self.default
        self.name = self.name.strip()

        self._get_value_from_request(dataDict, api_json, form, args)
        self._check_sizes()
        self._check_min_max_value()

        if not self._check_none(form):
            return

        # list
        if not self._process_list_value(dataDict, form):
            if self.empty_value is not None and str(self._value).lower() == "":
                self._value = self.empty_value

            self._value = convert_parameter_value(
                self.name,
                self._value,
                self.ptype,
                form,
                mode=self.mode,
                map_none=self.map_none,
                required=self.required,
                mapping_mode=self.mapping_mode,
            )

        self.__check_options(self._value)

        if self.function is not None:
            self._value = self.function(self._value)
