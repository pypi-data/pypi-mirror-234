# MODULES
import traceback, inspect, trace, sys, os

from dataclasses import copy, dataclass
import pandas as pd

# CORE
from core import core

# LIBS
from alphaz.libs import dict_lib, database_lib

# MODELS
from alphaz.models.main import AlphaDataclass, AlphaClass

LOG = core.get_logger("tests")


@dataclass
class TestInput(AlphaDataclass):
    value: str
    number: int


class AlphaTest(AlphaClass):
    _test = True
    category = ""
    index = 0
    current_test_name = ""
    disable: bool = False

    outputs: dict[str, bool] = {}
    coverages: dict[str, object] = {}

    def __init__(self):
        self.begin_class()

    def begin_class(self):
        pass

    def begin(self):
        pass

    def end(self):
        pass

    def init_tables(
        self,
        tables: list[str],
        binds: list[str] | None = None,
        truncate: bool = False,
        drop: bool = False,
        create: bool = False,
        init: bool = True,
        init_views: bool = False,
        no_log: bool = True,
    ):
        database_lib.init_databases(
            core=core,
            binds=binds,
            tables=tables,
            truncate=truncate,
            drop=drop,
            create=create,
            init=init,
            init_views=init_views,
            no_log=no_log,
        )

    def test(self, name, coverage: bool = False) -> bool:
        self.output = None

        status = False
        self.current_test_name = name
        fct = getattr(self, name)
        if fct is None:
            LOG.info(
                f"Failed to get testing function <{name}> in category <{self.category}>"
            )
            return False

        ignore_dirs = [
            sys.prefix,
            sys.exec_prefix,
            os.sep.join(sys.prefix.split(os.sep)[:-1]),
        ]  # TODO: log ignored
        tracer = trace.Trace(ignoredirs=ignore_dirs)

        self.begin()
        status = fct()
        self.end()
        if coverage:
            tracer.runfunc(fct)
            self.coverages[name] = tracer.results()
        if self.output is not None:
            status = self.output

        return status

    def reverse(self) -> bool:
        return self.__reverse_output()

    def __reverse_output(self) -> bool:
        self.output = not self.output
        return self.output

    def _set_output(self, status) -> bool:
        if self.output is not None:
            self.output = status and self.output
        else:
            self.output = status
        return status

    def _assert(self, status, conditions: list[bool] = [], msg: str = "") -> bool:
        if len(conditions) != 0 and type(conditions) == list:
            status = status and all(conditions)
        return self._set_output(status)

    def assert_array_equal(
        self, a, b, conditions: list[bool] = [], msg: str = ""
    ) -> bool:
        status = len(a) == len(b)
        if status:
            for i in range(len(a)):
                if a[i] != b[i]:
                    status = False
        if not status:
            LOG.info(
                f"{self.current_test_name} {msg} - Assert: <{a}> and <{b}> are not equals"
            )
        return self._assert(status, conditions)

    def assert_is_not_none(self, a, conditions: list[bool] = [], msg: str = "") -> bool:
        status = a is not None
        if not status:
            LOG.info(f"{self.current_test_name} {msg} - Assert: value is None")
        return self._assert(status, conditions)

    def assert_is_none(self, a, conditions: list[bool] = [], msg: str = "") -> bool:
        status = a is None
        if not status:
            LOG.info(f"{self.current_test_name} {msg} - Assert: value is not None")
        return self._assert(status, conditions)

    def assert_is_empty(
        self, a, conditions: list[bool] = [], msg: str = "", attribute=None
    ) -> bool:
        status = self.assert_is_not_empty(
            a, conditions=conditions, attribute=attribute, msg=msg
        )
        if status:
            LOG.info(f"{self.current_test_name} {msg} - Assert: value is not empty")
        return self.__reverse_output()

    def assert_are_keys_in_model_attributes(
        self, a, model, attributes=[], conditions: list[bool] = [], msg: str = ""
    ) -> bool:
        status = self.assert_are_keys_in_models_attributes(
            a, [model], attributes=attributes, conditions=conditions
        )
        return status

    def assert_are_keys_in_models_attributes(
        self, a, models, attributes=[], conditions: list[bool] = [], msg: str = ""
    ) -> bool:
        self.assert_is_not_none(a, msg=msg)
        for model in models:
            attributes.extend(list(model.get_schema()._declared_fields.keys()))
        attributes = list(set(attributes))
        key_in = {x: x in attributes for x in a.keys()}
        status = all(key_in.values())
        if not status:
            LOG.info(
                f"{self.current_test_name} {msg} - Assert: missing keys in model: {','.join([x for x, y in key_in.items() if not y])}"
            )
        return self._assert(status, conditions)

    def assert_has_model_attributes(
        self, a, model, conditions: list[bool] = [], msg: str = ""
    ) -> bool:
        self.assert_is_not_none(a, msg=msg)
        fields = list(model.get_schema()._declared_fields.keys())
        if not hasattr(a, "keys"):
            return self._assert(False, conditions)
        key_in = {x: x in a.keys() for x in fields}
        status = all(key_in.values())
        if not status:
            LOG.info(
                f"{self.current_test_name} {msg} - Assert: missing model keys: {','.join([x for x, y in key_in.items() if not y])}"
            )
        return self._assert(status, conditions)

    def assert_is_true(
        self, a, conditions: list[bool] = [], msg: str = "", no_log: bool = False
    ) -> bool:
        status = a
        if not status and not no_log:
            LOG.info(f"{self.current_test_name} {msg} - Assert: value {a} is not True")
        return self._assert(status, conditions)

    def assert_is_false(self, a, conditions: list[bool] = [], msg: str = "") -> bool:
        status = a
        if status:
            LOG.info(f"{self.current_test_name} {msg} - Assert: value {a} is not False")
        return self._assert(not status, conditions)

    def assert_contains(
        self, container, element, conditions: list[bool] = [], msg: str = ""
    ) -> bool:
        status = element in container
        if not status:
            LOG.info(
                f"{self.current_test_name} {msg} - Assert: {container=} does not contain {element=}"
            )
        return self._assert(status, conditions)

    def assert_is_not_empty(
        self, a, conditions: list[bool] = [], msg: str = "", attribute=None
    ) -> bool:
        if attribute is not None:
            if not hasattr(a, attribute):
                LOG.info(
                    f"{self.current_test_name} {msg} - Object of type <{type(a)}> does not have an attribute named <{attribute}>"
                )
            status = a is not None and not len(getattr(a, attribute)) == 0
        elif isinstance(a, pd.DataFrame):
            status = a is not None and not a.empty
        else:
            status = a is not None and len(a) != 0
        if not status:
            LOG.info(f"{self.current_test_name} {msg} - Assert: value is None")
        return self._assert(status, conditions)

    def assert_is_dict(self, a, conditions: list[bool] = [], msg: str = "") -> bool:
        status = type(a) == dict
        if not type(a) == dict:
            LOG.info(f"{self.current_test_name} {msg} - Assert: value is not a dict")
        return self._assert(status, conditions)

    def assert_is_list(self, a, conditions: list[bool] = [], msg: str = "") -> bool:
        status = type(a) == list
        if not type(a) == list:
            LOG.info(f"{self.current_test_name} {msg} - Assert: value is not a list")
        return self._assert(status, conditions)

    def assert_is_dict_not_empty(self, a, conditions: list[bool] = [], msg: str = ""):
        self.assert_is_dict(a, msg=msg)
        status = self.assert_is_not_empty(a, msg=msg)
        if not status:
            LOG.info(f"{self.current_test_name} {msg} - Assert: dict {a} is empty")
        return self._assert(status, conditions)

    def assert_is_dict_with_key(
        self, a, key, conditions: list[bool] = [], msg: str = ""
    ) -> bool:
        self.assert_is_dict(a, msg=msg)
        status = key in a
        if not status:
            LOG.info(f"{self.current_test_name} {msg} - Assert: dict has not key {key}")
        return self._assert(status, conditions)

    def assert_is_dict_with_key_not_empty(
        self, a, key, conditions: list[bool] = [], msg: str = ""
    ) -> bool:
        self.assert_is_not_none(a, msg=msg)
        self.assert_is_dict_with_key(a, key, msg=msg)
        status = self.assert_is_not_empty(a, msg=msg)
        if not status:
            LOG.info(
                f"{self.current_test_name} {msg} - Assert: dict {a} has no empty key {key}"
            )
        return self._assert(status, conditions)

    def assert_is_dict_with_key_with_value(
        self, a, key, value, conditions: list[bool] = [], msg: str = ""
    ) -> bool:
        status = self.assert_is_dict_with_key_not_empty(a, key, msg=msg)
        if status:
            status = self.assert_equal(a[key], value, msg=msg)
        if not status:
            LOG.info(
                f"{self.current_test_name} {msg} - Assert: {a} does not contains a {key=} with {value=}"
            )
        return self._assert(status, conditions)

    def assert_is_list_no_empty(self, a, conditions: list[bool] = [], msg: str = ""):
        status = self.assert_is_list(a, msg=msg)
        if status:
            status = self.assert_is_not_empty(a)
        return self._assert(status, conditions)

    def assert_is_equal(
        self,
        a,
        b,
        ignore: list | dict | None = None,
        conditions: list[bool] = [],
        msg: str = "",
    ):
        return self.assert_equal(a, b, ignore=ignore, conditions=conditions, msg=msg)

    def assert_equal(
        self,
        a,
        b,
        ignore: list | dict | None = None,
        conditions: list[bool] = [],
        msg: str = "",
    ) -> bool:
        if isinstance(a, list) and isinstance(b, list) and len(a) == 0 and len(b) == 0:
            return True
        if (
            isinstance(a, list)
            and isinstance(b, list)
            and all(isinstance(item, dict) for item in a)
            and all(isinstance(item, dict) for item in b)
        ):
            return all(
                [
                    self.assert_equal(
                        a=item,
                        b=b[index],
                        ignore=ignore,
                        conditions=conditions,
                        msg=msg,
                    )
                    for index, item in enumerate(a)
                ]
            )

        elif type(a) == dict and type(b) == dict:
            diff = dict_lib.compare_dicts(a, b, ignore=ignore)

            status = diff is None
            if not status:
                LOG.info(
                    f"{self.current_test_name} {msg} - Assert: dict are not equals\n\n{dict_lib.show_dict(diff)}"
                )

        else:
            status = a == b
            if not status:
                LOG.info(
                    f"{self.current_test_name} {msg} - Assert: {a} and {b} are not equals"
                )
        return self._assert(status, conditions)

    def assert_in_str(
        self,
        a: str,
        b: str,
        conditions: list[bool] = [],
        msg: str = "",
    ) -> bool:
        for e in [a, b]:
            if type(e) != str:
                LOG.info(
                    f"{self.current_test_name} {msg} - Assert: {e} type is not str"
                )
                return self._assert(False, conditions)
        status = a in b
        if not status:
            LOG.info(
                f"{self.current_test_name} {msg} - Assert: {b} does not include {b}"
            )
        return self._assert(status, conditions)

    def assert_list_str_in_str(
        self,
        a: list[str],
        b: str,
        conditions: list[bool] = [],
        msg: str = "",
    ) -> bool:  # TODO add check on a type
        if type(b) != str:
            LOG.info(f"{self.current_test_name} {msg} - Assert: {b} type is not str")
            return self._assert(False, conditions)

        status = True
        for e in a:
            if e not in b:
                status = False
                LOG.info(
                    f"{self.current_test_name} {msg} - Assert: {e} does not include in {a}"
                )

                break

        return self._assert(status, conditions)

    def assert_not_equal(
        self,
        a,
        b,
        ignore: list | dict | None = None,
        conditions: list[bool] = [],
        msg: str = "",
    ) -> bool:
        status = a != b
        if not status:
            LOG.info(f"{self.current_test_name} {msg} - Assert: {a} and {b} are equals")
        return self._assert(status, conditions)

    def assert_length(
        self,
        a,
        length,
        conditions: list[bool] = [],
        msg: str = "",
        strict: bool = False,
    ) -> bool:
        status_not_none = self.assert_is_not_none(a, msg=msg)
        status = len(a) == length
        if strict:
            status = status and len(a) != 0
        if not status and status_not_none:
            LOG.info(
                f"{self.current_test_name} {msg} - Assert: length {len(a)} is not the {length} expected"
            )
        return self._assert(status, conditions)

    def assert_transaction(
        self, tr, conditions: list[bool] = [], msg: str = ""
    ) -> bool:
        status_not_none = self.assert_is_not_none(tr, msg=msg)
        status = tr is not None and tr != "timeout"
        if not status and status_not_none:
            LOG.info(
                f"{self.current_test_name} {msg} - Assert: object if not a transaction"
            )
        return self._assert(status, conditions)

    def assert_api_answer(
        self,
        url: str,
        method: str,
        expected_output: dict,
        default_values: dict,
        params: dict = {},
        msg: str = "",
        strict: bool = True,
    ) -> bool:
        raw_params = copy.copy(params)
        from ...libs import api_lib

        answer = api_lib.get_api_answer(
            url=url, method=method, params=params, no_log=False
        )

        expected_output_diff, real_output = {}, {}
        if not self.assert_equal(answer.error, 0):
            LOG.info("Answer is invalid")
            return self.output
        for x, y in answer.data.items():
            if x in expected_output:
                if not self.assert_equal(y, expected_output[x]):
                    real_output[x] = y
                    expected_output_diff[x] = expected_output[x]
            elif x in default_values:
                if not self.assert_equal(y, default_values[x]):
                    real_output[x] = y
                    expected_output_diff[x] = default_values[x]
            elif strict:
                if not self.assert_is_none(y):
                    real_output[x] = y
                    expected_output_diff[x] = None
        if not self.output:
            LOG.info(
                f"{self.current_test_name} {msg} - Assert: {raw_params=} > {params=} - discrepancy between:\n\nExpected output:\n\n{expected_output_diff}\n\nReal output:\n\n{real_output}\n"
            )
        return self.output

    def assert_api_answer_fail(
        self,
        url: str,
        method: str,
        params: dict,
        expected_output: str,
        default_values: dict | None = None,
        msg: str = "",
    ) -> bool:
        from ...libs import api_lib

        answer = api_lib.get_api_answer(
            url=url, method=method, params=params, no_log=True
        )

        self.assert_equal(answer.error, 1)
        self.assert_in_str(expected_output, answer.status_description)

        if not self.output:
            LOG.info(
                f"{self.current_test_name} {msg} - Assert: {params=} does not provide an {expected_output=} but {answer.status}"
            )
        return self.output
